import os


def parse_list(env: str) -> list:
    if env == '':
        return []
    else:
        return env.split(',')


HOST_ENV = os.getenv('HOST_ENV', 'local')

GRAFANA_BASE_URL = os.getenv('GRAFANA_BASE_URL', 'http://159.138.171.113:3100')
SERVICES = parse_list(os.getenv('SERVICES', 'jam-bp-jam-lk-api,troika-bp-smile-th-api'))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'ERROR')
QUERY = parse_list(os.getenv('QUERY', ''))
EXCLUSIONS = parse_list(os.getenv('EXCLUSIONS', ''))
FREQUENCY = os.getenv('FREQUENCY', '30')

EMAIL_SERVER = os.getenv('EMAIL_SERVER', 'smtp.gmail.com')
EMAIL_PORT = os.getenv('EMAIL_PORT', 465)
EMAIL_USER_NAME = os.getenv('EMAIL_USER_NAME', 'shamikakosgolle@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'iwey ppky zugh fyvc')
EMAIL_RECIPIENTS = parse_list(os.getenv('EMAIL_RECIPIENT'))

LOGO_URL = os.getenv('LOGO_URL')
COMPANY_MANE = os.getenv('COMPANY_MANE', '')
COPYRIGHT_NOTICE = os.getenv('COPYRIGHT_NOTICE', 'Copyright© {{year}}{{platformName}}. All rights reserved.')

ALERT_OPTIONS = parse_list(os.getenv('ALERT_OPTIONS', 'EMAIL,SLACK'))

SLACK_TOKEN = os.getenv('SLACK_TOKEN')
SLACK_CHANNEL = os.getenv('SLACK_CHANNEL', 'alerts')
