import logging
import logging_loki
import os
import sys
import uuid

# Resolvendo as variáveis de ambiente
DB_HOST = os.getenv("DB_HOST") or os.getenv("DATABASE_HOST")
DB_PORT = int(os.getenv("DB_PORT") or os.getenv("DATABASE_PORT"))
DB_BASE = os.getenv("DB_BASE") or os.getenv("DATABASE_NAME")
DB_USER = os.getenv("DB_USER") or os.getenv("DATABASE_USER")
DB_PASS = os.getenv("DB_PASS") or os.getenv("DATABASE_PASS")
DB_DRIVER = os.getenv("DB_DRIVER") or os.getenv("DATABASE_DRIVER")

if DB_HOST is None:
    raise Exception("Faltando variável de ambiente DB_HOST")
if DB_PORT is None:
    raise Exception("Faltando variável de ambiente DB_PORT")
if DB_BASE is None:
    raise Exception("Faltando variável de ambiente DB_BASE")
if DB_USER is None:
    raise Exception("Faltando variável de ambiente DB_USER")
if DB_PASS is None:
    raise Exception("Faltando variável de ambiente DB_PASS")

QUEUE_NAME = os.environ["QUEUE_NAME"]
QUEUE_TABLE = os.environ["QUEUE_TABLE"]
QUEUE_SUBSCRIBER_TABLE = os.getenv("QUEUE_SUBSCRIBER_TABLE")

QUEUE_MAX_RETRY = int(os.getenv("QUEUE_MAX_RETRY", "100"))
QUEUE_BASE_INTERVAL_RETRY = int(os.getenv("QUEUE_BASE_INTERVAL_RETRY", "5"))

QUEUE_MINUTE_RETRY_THREAD = os.getenv(
    "QUEUE_MINUTE_RETRY_THREAD", "0,5,10,15,20,25,30,35,40,45,50,55"
)
QUEUE_MINUTE_PURGE_THREAD = os.getenv("QUEUE_MINUTE_PURGE_THREAD", "0")
QUEUE_MINUTE_NOTIFY_THREAD = os.getenv(
    "QUEUE_MINUTE_NOTIFY_THREAD", "0,5,10,15,20,25,30,35,40,45,50,55"
)

QUEUE_PURGE_MAX_AGE = int(os.getenv("QUEUE_PURGE_MAX_AGE", "60"))
QUEUE_PURGE_LIMIT = int(os.getenv("QUEUE_PURGE_LIMIT", "1000"))
QUEUE_PURGE_ROUND_LIMIT = int(os.getenv("QUEUE_PURGE_ROUND_LIMIT", "100"))

QUEUE_WAIT_NOTIFY_INTERVAL = int(os.getenv("QUEUE_PURGE_LIMIT", "30"))

DEFAULT_WEBHOOK_TIMEOUT = int(os.getenv("DEFAULT_WEBHOOK_TIMEOUT", "20"))

ENV = os.getenv("ENV", "DEV").upper()
GRAFANA_URL = os.getenv("GRAFANA_URL")
LOG_DEBUG = os.getenv("LOG_DEBUG", "False").upper() == "TRUE"

CLIENT_SERVER_MODE = os.getenv("CLIENT_SERVER_MODE", "False").upper() == "TRUE"
SERVER_HOST = os.getenv("SERVER_HOST", "127.0.0.1")
NOTIFY_SERVICE_PORT = int(os.getenv("NOTIFY_SERVICE_PORT", "8770"))
LOCK_SERVICE_PORT = int(os.getenv("LOCK_SERVICE_PORT", "8970"))
TIMEOUT_SOCKET_MESSAGE = int(os.getenv("TIMEOUT_SOCKET_MESSAGE", "5"))

MULTI_DATABASE = os.getenv("MULTI_DATABASE", "False").upper() == "TRUE"
MULTI_DATABASE_USER = os.getenv("MULTI_DATABASE_USER")
MULTI_DATABASE_PASSWORD = os.getenv("MULTI_DATABASE_PASSWORD")
MULTI_DATABASE_CLIENT_ID = os.getenv("MULTI_DATABASE_CLIENT_ID")
MULTI_DATABASE_API_CREDETIALS_URL = os.getenv(
    "MULTI_DATABASE_API_CREDETIALS_URL",
    "https://api.sre.nasajon.com.br/erp/credentials",
)

OAUTH_TOKEN_URL = os.getenv(
    "OAUTH_TOKEN_URL",
    "https://auth.nasajon.com.br/auth/realms/master/protocol/openid-connect/token",
)

# Resolvendo as constantes e variáveis globais
WORKER_NAME = f"{QUEUE_NAME}_WORKER_{uuid.uuid4()}"
GLOBAL_RUN = True

END_MARK = "###END###"
SOCKET_BUFFER_SIZE = 1024

# Configurando o logger
logger = logging.getLogger(WORKER_NAME)
if LOG_DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)

if GRAFANA_URL is not None and GRAFANA_URL.strip() != "":
    loki_handler = logging_loki.LokiHandler(
        url=GRAFANA_URL,
        tags={ENV.upper() + "_flask_api_skeleton": ENV.lower() + "_log"},
        version="1",
    )
    loki_handler.setFormatter(log_format)
    logger.addHandler(loki_handler)
