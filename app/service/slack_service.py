from slack_sdk import WebClient

from app.config.logger_config import log
from app.config.variable import SLACK_TOKEN, SLACK_CHANNEL
from app.model.exception import SlackException
from app.service.template_service import TemplateService


class SlackService:
    client = WebClient(token=SLACK_TOKEN)
    template_service = TemplateService()

    def send_message(self, logs: list, **kwargs):
        try:
            log.info('Sending Slack message...')

            self.send_error_alert(
                channel=SLACK_CHANNEL,
                log_list=logs
            )
        except Exception as ex:
            log.error(f'Error sending Slack message: {ex}')
            raise SlackException(f'Error sending Slack message: {ex}')

    def send_error_alert(self, channel: str, log_list: list):

        def trunc(s, n=255):
            s = (s or "").replace("\n", " ")
            return s if len(s) <= n else s[: n - 3] + "..."

        blocks = [
            {"type": "header", "text": {"type": "plain_text", "text": "Application ERROR Alert"}}
        ]

        for svc in log_list:

            blocks.append({
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Service:* {svc.get('service', '-')}"}
            })

            blocks.append({
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": "*Log*"},
                    {"type": "mrkdwn", "text": "*Count*"}
                ]
            })

            for entry in svc.get("logs", []):
                log_text = trunc(entry.get("log", ""))
                count = entry.get("count", 0)
                blocks.append({
                    "type": "section",
                    "fields": [
                        {"type": "mrkdwn", "text": f"`{log_text}`"},
                        {"type": "mrkdwn", "text": str(count)}
                    ]
                })
                blocks.append({"type": "divider"})

        def chunk(lst, size):
            for i in range(0, len(lst), size):
                yield lst[i:i + size]

        MAX_BLOCKS = 48
        header = blocks[:1]
        body = blocks[1:]

        for i, body_chunk in enumerate(chunk(body, MAX_BLOCKS)):
            self.client.chat_postMessage(
                channel=channel,
                text="Application ERROR Alert",
                blocks=(header + body_chunk),
                username="Bot User"
            )
