from fastapi import FastAPI, Request
from fastapi_crons import Crons
from starlette.responses import JSONResponse

from app.config.logger_config import uvicorn_logger, LogFilter, log
from app.config.variable import SERVICES, LOG_LEVEL, QUERY, FREQUENCY
from app.model.exception import LokiException
from app.model.request import LogRequest
from app.service.alert_service import AlertService
from app.service.loki_service import LokiService

log.info(f'----Starting AI Monitoring Agent----')
app = FastAPI()
scheduler = Crons(app=app)

uvicorn_logger.addFilter(LogFilter())

loki_service = LokiService()
alert_service = AlertService()

log.info('----App started successfully----')


@app.on_event("startup")
async def startup_event():
    await every_five_minutes()


@app.exception_handler(LokiException)
async def generic_exception_handler(request: Request, ex: LokiException):
    return JSONResponse(status_code=500, content='An Internal Server Error occurred fetching logs.')


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, ex: Exception):
    log.error(f'An Internal Server Error occurred: {ex}')
    return JSONResponse(status_code=500, content='An Internal Server Error occurred')


@app.get("/health")
async def health():
    return {"message": "Health good"}


@app.post("/logs", status_code=200)
async def get_logs(request: LogRequest):
    return loki_service.query_logs(request)


@scheduler.cron(f'*/{FREQUENCY} * * * *', name="error_log_service")
async def every_five_minutes():
    log.info('Checking for error logs...')

    alert_service.send_alert(
        subject='Application Error Alert',
        level=LOG_LEVEL,
        services=SERVICES,
        queries=QUERY,
        limit=None
    )
