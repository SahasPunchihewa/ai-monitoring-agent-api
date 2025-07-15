from slack_sdk import WebClient

from app.config.logger_config import log
from app.config.variable import SLACK_TOKEN
from app.model.exception import SlackException
from app.service.template_service import TemplateService


class SlackService:
    client = WebClient(token=SLACK_TOKEN)
    template_service = TemplateService()

    def send_message(self, **kwargs):
        try:
            log.info('Sending Slack message...')
            markdown = self.template_service.render_template('alert-md', **kwargs)

            self.client.chat_postMessage(
                channel="alerts",
                text=markdown,
                username="Bot User"
            )
        except Exception as ex:
            log.error(f'Error sending Slack message: {ex}')
            raise SlackException(f'Error sending Slack message: {ex}')
