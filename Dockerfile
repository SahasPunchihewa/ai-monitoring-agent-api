FROM python:3.12-slim

WORKDIR /monitoring-alert-service

COPY requirements.txt /

RUN pip install --upgrade -r /requirements.txt
RUN rm -rf requirements.txt

COPY . /monitoring-alert-service

ENV PYTHONPATH="${PYTHONPATH}:/monitoring-alert-service"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]