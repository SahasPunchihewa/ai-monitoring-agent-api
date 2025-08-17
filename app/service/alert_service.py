import json
from typing import List

from markdown_it import MarkdownIt

from app.config.logger_config import log
from app.config.variable import AI_ENABLED, ALERT_OPTIONS
from app.model.exception import LokiException, AiException, EmailException, SlackException
from app.model.request import LogRequest
from app.service.ai_service import AIService
from app.service.email_service import EmailService
from app.service.loki_service import LokiService
from app.service.slack_service import SlackService


class AlertService:
    loki_service = LokiService()
    email_service = EmailService()
    slack_service = SlackService()
    ai_service = AIService()
    markdown_service = MarkdownIt()

    def send_alert(self, subject: str, level: str, services: List[str], queries=None, limit: int = None):
        try:
            if queries is None:
                queries = []
            request = LogRequest(
                services=services,
                level=level,
                queries=queries,
                limit=limit
            )

            logs = self.loki_service.query_logs(request)

            if len(logs) > 0:
                ai_summary = self.ai_service.generate_log_insights(json.dumps(logs)) if AI_ENABLED == 'True' else ''
                html_ai_summary = self.markdown_service.render(ai_summary)

                if 'EMAIL' in ALERT_OPTIONS:
                    self.email_service.send_email(subject, logList=logs, logoEnabled='False', aiSummary=html_ai_summary, aiEnabled=AI_ENABLED)
                if 'SLACK' in ALERT_OPTIONS:
                    self.slack_service.send_message(logs=logs)
        except (LokiException | AiException | EmailException | SlackException):
            pass
        except Exception as ex:
            log.error(f'Error sending alert: {ex}')
