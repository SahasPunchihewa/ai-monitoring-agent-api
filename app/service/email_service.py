import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.config.logger_config import log
from app.config.variable import EMAIL_SERVER, EMAIL_PORT, EMAIL_USER_NAME, EMAIL_PASSWORD, EMAIL_RECIPIENTS
from app.model.exception import EmailException
from app.service.template_service import TemplateService


class EmailService:
    template_service = TemplateService()

    def send_email(self, subject: str, **kwargs):
        try:
            log.info(f'Sending email for subject: {subject}')
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = EMAIL_USER_NAME
            msg['To'] = ", ".join(EMAIL_RECIPIENTS)
            body = self.template_service.render_template('alert-html', **kwargs)

            part = MIMEText(body, 'html')
            msg.attach(part)

            smtp_server = smtplib.SMTP_SSL(EMAIL_SERVER, EMAIL_PORT)
            smtp_server.ehlo()
            smtp_server.login(EMAIL_USER_NAME, EMAIL_PASSWORD)
            smtp_server.sendmail(EMAIL_USER_NAME, EMAIL_RECIPIENTS, msg.as_string())
            smtp_server.close()
        except Exception as ex:
            log.error(f'Error sending email: {ex}')
            raise EmailException(f'Error sending email: {ex}')
