import os

from langchain.chat_models import init_chat_model

from app.config.logger_config import log
from app.config.variable import OPENAI_API_KEY
from app.model.exception import AiException

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


class AIService:
    llm = init_chat_model("gpt-4o-mini", model_provider="openai")

    def generate_log_insights(self, data: str) -> str:
        try:
            log.info('Generating AI insights...')

            system_template = f'''
            You are a AI assistant that generates help from error logs.
             
            - generate short and concise supportive summary based on JSON input.
            - Include troubleshooting tips and suggestions.
            
            JSON Input:
            {data}
            '''

            response = self.llm.invoke(system_template)

            return response.content
        except Exception as ex:
            log.error(f'Error generating AI insights: {ex}')
            raise AiException(f'Error generating AI insights: {ex}')
