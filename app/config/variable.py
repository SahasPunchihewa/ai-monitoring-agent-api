import os

HOST_ENV = os.getenv('HOST_ENV', 'local')

GRAFANA_BASE_URL = os.getenv('GRAFANA_BASE_URL')
SERVICES = os.getenv('SERVICES', '').split(',')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'ERROR')
QUERY = os.getenv('QUERY', '').split(',')
FREQUENCY = os.getenv('FREQUENCY', '5')

EMAIL_SERVER = os.getenv('EMAIL_SERVER', 'smtp.gmail.com')
EMAIL_PORT = os.getenv('EMAIL_PORT', 465)
EMAIL_USER_NAME = os.getenv('EMAIL_USER_NAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENT').split(',')

LOGO_URL = os.getenv('LOGO_URL')
COMPANY_MANE = os.getenv('COMPANY_MANE', '')
COPYRIGHT_NOTICE = os.getenv('COPYRIGHT_NOTICE', 'Copyright© {{year}}{{platformName}}. All rights reserved.')

ALERT_OPTIONS = os.getenv('ALERT_OPTIONS', 'EMAIL,SLACK').split(',')

SLACK_TOKEN = os.getenv('SLACK_TOKEN')

AI_ENABLED = os.getenv('AI_ENABLED', 'True')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
