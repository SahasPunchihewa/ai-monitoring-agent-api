# 🚀 Monitoring & Alerting Service

## 🔧 Configuration

All configuration values are provided via environment variables.

### Mandatory

- `GRAFANA_BASE_URL` : Base URL of Grafana instance (e.g. http://grafana:3000)
- `SERVICES` : Comma-separated list of service names (e.g. auth,orders,payments)
- `EMAIL_USER_NAME` : SMTP email username
- `EMAIL_PASSWORD` : SMTP email password
- `EMAIL_RECIPIENT` : Comma-separated list of recipient emails

### Optional

- `HOST_ENV` : `local` (default) – Environment identifier
- `LOG_LEVEL` : `ERROR` (default) – Log level [`DEBUG`, `INFO`, `WARNING`, `ERROR`]
- `QUERY` : `""` (default) – Comma-separated list of queries
- `FREQUENCY` : `5` (default) – Frequency (minutes) for checks
- `EMAIL_SERVER` : `smtp.gmail.com` (default) – SMTP server
- `EMAIL_PORT` : `465` (default) – SMTP port
- `LOGO_URL` : `""` (default) – Company logo URL
- `COMPANY_NAME` : `""` (default) – Company name
- `COPYRIGHT_NOTICE` : `Copyright© {{year}}{{platformName}}. All rights reserved.` (default)
- `ALERT_OPTIONS` : `EMAIL,SLACK` (default) – Notification channels
- `SLACK_TOKEN` : `""` (default) – Slack API token
- `SLACK_CHANNEL` : `alerts` (default) – Slack channel

---

## ⚙️ Installation & Running

### Create & Activate Virtual Environment

```shell
python3 -m venv venv
```

```shell
source venv/bin/activate
```

### Install Dependencies

```shell
pip install -r requirements.txt
```

### Run FastAPI App (Local Dev)

```shell
uvicorn main:app --host 0.0.0.0 --port 8080
```

## 🐳 Docker

### Build the Image

```shell
docker build -t monitoring-alert-service .
```

### Run the Container

```shell
docker run -d \
  -p 8080:8080 \
  --name monitoring-alert-service \
  -e HOST_ENV=local \
  -e GRAFANA_BASE_URL=http://grafana.local \
  -e SERVICES=service1,service2 \
  -e EMAIL_USER_NAME=alerts@company.com \
  -e EMAIL_PASSWORD=supersecret \
  -e EMAIL_RECIPIENT=devops@company.com,ops@company.com \
  monitoring-alert-service
```

## 🧪 Testing

```shell
curl -X POST "http://localhost:8080/logs" \
  -H "Content-Type: application/json" \
  -d '{
    "services": ["service1", "service2"],
    "level": "ERROR",
    "queries": ["exception", "timeout"],
    "limit": 100
  }'
```


