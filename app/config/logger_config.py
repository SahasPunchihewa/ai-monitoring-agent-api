import logging

from app.config.variable import HOST_ENV

log = logging

log_excluded_endpoints = ['/health']

uvicorn_logger = logging.getLogger('uvicorn.access')

if HOST_ENV == 'gcp':
    from google.cloud.logging import Client

    client = Client()
    client.setup_logging()
    log.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
else:
    log = logging.getLogger('Monitoring Agent')
    log.setLevel(logging.DEBUG)

    logger_channel = logging.StreamHandler()
    logger_channel.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger_channel.setFormatter(formatter)

    log.addHandler(logger_channel)


class LogFilter(logging.Filter):
    def filter(self, record):
        if record.args and len(record.args) >= 3:
            if record.args[2] in log_excluded_endpoints:
                return False
        return True
