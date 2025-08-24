import re
import time
from typing import List

from httpx import Client

from app.config.logger_config import log
from app.config.variable import GRAFANA_BASE_URL, FREQUENCY
from app.model.exception import LokiException, InvalidLogException
from app.model.request import LogRequest


class LokiService:
    client: Client = Client()

    def query_logs(self, request: LogRequest):
        try:
            log.info(f'Querying logs for services: {request.services} and level: {request.level}')
            url = f'{GRAFANA_BASE_URL}/loki/api/v1/query_range'

            end = int(time.time() * 1e9)
            start = end - (int(FREQUENCY) * 60 * 1_000_000_000)

            if len(request.services) == 0:
                query = f'"{request.level}"'
            elif len(request.services) == 1:
                query = f'{{service_name="{request.services[0]}"}} |~ "{request.level}"'
            else:
                query = f'{{service_name=~"{"|".join(s for s in request.services)}"}} |~ "{request.level}"'

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

            logs = {}

            for item in response:
                if item['stream']['service_name'] in logs:
                    logs[item['stream']['service_name']].extend(item['values'])
                else:
                    logs[item['stream']['service_name']] = item['values']

            final_logs = []
            for service, log_list in logs.items():
                final_logs.append({'service': service, 'logs': self.aggregate_logs(log_list, request.level, request.exclusions)})

            return final_logs
        except Exception as ex:
            log.error(f'Error querying logs from Loki: {ex}')
            raise LokiException(f'Error querying logs from Loki: {ex}')

    def aggregate_logs(self, logs: list, level: str, exclusions: List[str]) -> list:
        log_details = {}

        for err_log in logs:
            raw_log = err_log[1]
            try:
                cleaned_log = self.sanitize_log(raw_log, level, exclusions)
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

    @staticmethod
    def sanitize_log(raw_log: str, level: str, exclusions: List[str]) -> str:
        if any(word in raw_log for word in exclusions):
            raise InvalidLogException(f'Exclusion word found in log.')

        cleaned_log = re.sub(r"\[\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+ #\d+\]", "", raw_log).strip()
        url_free_log = cleaned_log

        urls = re.findall(r'https?://[^\s\)\]\[\<\>,"\']+', url_free_log)
        endpoints = re.findall(r'/\?[^\s]+', url_free_log)

        urls.extend(endpoints)

        for url in urls:
            url_free_log = url_free_log.replace(url, '')

        if level not in url_free_log:
            raise InvalidLogException(f'Log does not contain "{level}" keyword.')
        else:
            return cleaned_log
