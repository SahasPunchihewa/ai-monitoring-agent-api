import re
import time

from httpx import Client

from app.config.logger_config import log
from app.config.variable import GRAFANA_BASE_URL
from app.model.exception import LokiException, InvalidLogException
from app.model.request import LogRequest


class LokiService:
    client: Client = Client()

    def query_logs(self, request: LogRequest):
        try:
            log.info(f'Querying logs for service: {request.service} and level: {request.level}')
            url = f'{GRAFANA_BASE_URL}/loki/api/v1/query_range'

            end = int(time.time() * 1e9)
            start = end - 300_000_000_000  # 5 minutes ago in nanoseconds
            query = f'{{service_name="{request.service}"}} |~ "(?i){request.level}"'

            for query_item in request.queries:
                query += f' |~ "(?i){query_item}"'

            params = {
                'query': query,
                'start': start,
                'end': end,
            }

            if request.limit:
                params['limit'] = request.limit

            response = self.client.get(url, params=params).json()['data']['result']

            logs = []
            log_details = {}

            for item in response:
                logs.extend(item['values'])

            for err_log in logs:
                raw_log = err_log[1]
                try:
                    cleaned_log = self.sanitize_log(raw_log)
                    log_details[err_log[0]] = cleaned_log
                except InvalidLogException:
                    log.info(f'Skipping invalid log: {raw_log}')
                    continue

            aggregated_logs = {}

            for timestamp, err_log in log_details.items():
                if err_log not in aggregated_logs:
                    aggregated_logs[err_log] = {'log': err_log, 'timestamps': [timestamp], 'count': 1}
                else:
                    aggregated_logs[err_log]['count'] += 1
                    aggregated_logs[err_log]['timestamps'].append(timestamp)

            result_list = list(aggregated_logs.values())

            return result_list
        except Exception as ex:
            log.error(f'Error querying logs from Loki: {ex}')
            raise LokiException(f'Error querying logs from Loki: {ex}')

    @staticmethod
    def sanitize_log(raw_log: str) -> str:
        cleaned_log = re.sub(r"\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+ #\d+\]", "", raw_log).strip()
        url_free_log = cleaned_log

        urls = re.findall(r'https?://[^\s\)\]\[\<\>,"\']+', url_free_log)
        endpoints = re.findall(r'/\?[^\s]+', url_free_log)

        urls.extend(endpoints)

        for url in urls:
            url_free_log = url_free_log.replace(url, '')

        if "error" not in url_free_log.lower():
            raise InvalidLogException('Log does not contain "error" keyword.')
        else:
            return cleaned_log
