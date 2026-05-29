# Import Config Class
import sys
import base64
from pathlib import Path
from typing import Any

from navconfig import config, BASE_DIR, DEBUG
from navconfig.logging import logging, logger
from querysource.conf import CACHE_HOST, CACHE_PORT
from .utils.functions import get_worker_list
from .exceptions import FlowTaskError
from .storages import FileTaskStorage
from .storages.files import FileStore


# Disable Debug Logging of external tools
logging.getLogger('faker.factory').setLevel(logging.INFO)
logging.getLogger('numba.core').setLevel(logging.INFO)
logging.getLogger('h5py').setLevel(logging.INFO)


# Environment
ENVIRONMENT = config.get("ENVIRONMENT", fallback="development")

## environment name:
ENV = config.get("ENV", fallback="dev")

DEFAULT_ENCODING = config.get("DEFAULT_ENCODING", fallback="ascii")

PRODUCTION = config.getboolean("PRODUCTION", fallback=(not DEBUG))
LOCAL_DEVELOPMENT = DEBUG is True and sys.argv[0] == "run.py"

APP_DIR = BASE_DIR.joinpath("flowtask")

# DB Default (database used for interaction (rw))
DBHOST = config.get("DBHOST", fallback="localhost")
DBUSER = config.get("DBUSER")
DBPWD = config.get("DBPWD")
DBNAME = config.get("DBNAME", fallback="navigator")
DBPORT = config.get("DBPORT", fallback=5432)
if not DBUSER:
    raise RuntimeError("Missing PostgreSQL Default Settings.")
# database for changes (admin)
default_dsn = f"postgres://{DBUSER}:{DBPWD}@{DBHOST}:{DBPORT}/{DBNAME}"
default_pg = f"postgres://{DBUSER}:{DBPWD}@{DBHOST}:{DBPORT}/{DBNAME}"
# sqlalchemy+asyncpg connector:
default_sqlalchemy_pg = f"postgresql+asyncpg://{DBUSER}:{DBPWD}@{DBHOST}:{DBPORT}/{DBNAME}"


### InfluxDB configuration:
## INFLUXDB
USE_INFLUX = config.getboolean("USE_INFLUX", fallback=True)
INFLUX_DRIVER = config.get("INFLUX_DRIVER", fallback="influx")
INFLUX_HOST = config.get("INFLUX_HOST", fallback="127.0.0.1")
INFLUX_PORT = config.get("INFLUX_PORT", fallback="8086")
INFLUX_USER = config.get("INFLUX_USER")
INFLUX_PWD = config.get("INFLUX_PWD")
INFLUX_DATABASE = config.get("INFLUX_DATABASE", fallback="navigator")
INFLUX_TASKS_STARTED = config.get("INFLUX_TASKS_STARTED", fallback="started_tasks")
INFLUX_ORG = config.get("INFLUX_ORG", fallback="navigator")
INFLUX_TOKEN = config.get("INFLUX_TOKEN")
if USE_INFLUX is True and not INFLUX_TOKEN:
    raise FlowTaskError("Missing InfluxDB Settings and Influx DB is enabled.")

# Database Connections:
# RETHINKDB
RT_DRIVER = config.get('RT_DRIVER', fallback='rethink')
RT_HOST = config.get('RT_HOST', fallback='localhost')
RT_PORT = config.get('RT_PORT', fallback=28015)
RT_DATABASE = config.get('RT_DATABASE', fallback='navigator')
RT_USER = config.get('RT_USER')
RT_PASSWORD = config.get('RT_PWD')


### Plugins Folder:
PLUGINS_DIR = config.get('PLUGINS_DIR', fallback=BASE_DIR.joinpath('plugins'))
if isinstance(PLUGINS_DIR, str):
    PLUGINS_DIR = Path(PLUGINS_DIR).resolve()
if not PLUGINS_DIR.exists():
    PLUGINS_DIR.mkdir(parents=True, exist_ok=True)

# Add PLUGINS_DIR to sys.path so Python can import modules from it
if str(PLUGINS_DIR) not in sys.path:
    sys.path.insert(0, str(PLUGINS_DIR))

# TEMPLATE SYSTEM
TEMPLATE_DIR = config.get("TEMPLATE_DIR", fallback=BASE_DIR.joinpath("templates"))

## Scheduler Configuration
# Schedule System
SCHEDULER = config.getboolean("SCHEDULER", fallback=True)
# Jobs Activation
ENABLE_JOBS = config.getboolean("ENABLE_JOBS", fallback=True)
USE_WEBHOOKS = config.getboolean("USE_WEBHOOKS", fallback=True)
SCHEDULER_MAX_INSTANCES = config.get("MAX_INSTANCES", fallback=2)
SCHEDULER_GRACE_TIME = config.get("GRACE_TIME", fallback=900)

SCHEDULER_SERVICE_GROUPS = config.getlist(
    "SCHEDULER_SERVICE_GROUPS", fallback=["admin", "superuser"]
)

SCHEDULER_ADMIN_GROUPS = config.getlist(
    "SCHEDULER_ADMIN_GROUPS", fallback=["admin", "superuser"]
)

# Timezone (For parsedate)
TIMEZONE = config.get("timezone", section="l18n", fallback="UTC")
USE_TIMEZONE = config.getboolean("USE_TIMEZONE", fallback=True)

DEFAULT_TIMEZONE = config.get(
    "default_timezone", section="l18n", fallback="America/New_York"
)
SYSTEM_LOCALE = config.get("locale", section="l18n", fallback="en_US.UTF-8")

"""
Worker Configuration
"""
WORKER_DEFAULT_HOST = config.get("WORKER_DEFAULT_HOST", fallback="0.0.0.0")
WORKER_DEFAULT_PORT = config.get("WORKER_DEFAULT_PORT", fallback=8888)
WORKER_DEFAULT_QTY = config.get("WORKER_DEFAULT_QTY", fallback=4)
WORKER_QUEUE_SIZE = config.get("WORKER_QUEUE_SIZE", fallback=4)
WORKER_REDIS_DB = config.get("WORKER_REDIS_DB", fallback=2)
WORKER_REDIS = f"redis://{CACHE_HOST}:{CACHE_PORT}/{WORKER_REDIS_DB}"
REDIS_CACHE_DB = config.get("REDIS_CACHE_DB", fallback=1)
REDIS_URL = f"redis://{CACHE_HOST}:{CACHE_PORT}/{REDIS_CACHE_DB}"

workers = config.get("WORKER_LIST")
if workers:
    WORKER_LIST = get_worker_list([e.strip() for e in list(workers.split(","))])
else:
    WORKER_LIST = None

workers_high = config.get("WORKER_HIGH_LIST", fallback="127.0.0.1:8899")
if workers_high:
    WORKER_HIGH_LIST = get_worker_list(
        [e.strip() for e in list(workers_high.split(","))]
    )
else:
    WORKER_HIGH_LIST = None

# Make sure that the worker list is not empty
WORKERS_LIST = {
    "low": WORKER_LIST,
    "high": WORKER_HIGH_LIST,
    "default": WORKER_LIST,
}

SCHEDULER_WORKER_TIMEOUT = config.getint("SCHEDULER_WORKER_TIMEOUT", fallback=60)
SCHEDULER_RETRY_ENQUEUE = config.getint("SCHEDULER_RETRY_ENQUEUE", fallback=10)
SCHEDULER_MAX_RETRY_ENQUEUE = config.getint("SCHEDULER_MAX_RETRY_ENQUEUE", fallback=60)

## HTTPClioent
HTTPCLIENT_MAX_SEMAPHORE = config.getint("HTTPCLIENT_MAX_SEMAPHORE", fallback=5)
HTTPCLIENT_MAX_WORKERS = config.getint("HTTPCLIENT_MAX_WORKERS", fallback=1)

### Memcache
MEMCACHE_HOST = config.get("MEMCACHE_HOST", "localhost")
MEMCACHE_PORT = config.get("MEMCACHE_PORT", fallback=11211)

### Redash System
REDASH_HOST = config.get("REDASH_HOST")
REDASH_API_KEY = config.get("REDASH_API_KEY")

"""
Notification System
"""
### Notification System
SHOW_VERSION = config.getboolean("SHOW_VERSION", fallback=True)
NOTIFY_ON_SUCCESS = config.get("DI_EVENT_ON_SUCCESS", fallback="dummy")
NOTIFY_ON_ERROR = config.get("DI_EVENT_ON_ERROR", fallback="dummy")
NOTIFY_ON_FAILURE = config.get("DI_EVENT_ON_FAILURE", fallback="dummy")
NOTIFY_ON_WARNING = config.get("DI_EVENT_ON_WARNING", fallback="dummy")

SEND_NOTIFICATIONS = bool(config.get("SEND_NOTIFICATIONS", fallback=True))
DEFAULT_RECIPIENT = {
    "name": "Jesus Lara",
    "account": {"address": "jesuslarag@gmail.com", "number": "+00000000"},
}
SCHEDULER_DEFAULT_NOTIFY = config.get("SCHEDULER_DEFAULT_NOTIFY", fallback="telegram")
TELEGRAM_BOT_TOKEN = config.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = config.get("TELEGRAM_CHAT_ID")
TELEGRAM_JIRA_BOT_TOKEN = config.get("TELEGRAM_JIRA_BOT_TOKEN")

EVENT_CHAT_BOT = config.get("EVENT_CHAT_BOT", fallback=TELEGRAM_BOT_TOKEN)
EVENT_CHAT_ID = config.get("EVENT_CHAT_ID", fallback=TELEGRAM_CHAT_ID)

# Notify on Slack
SLACK_DEFAULT_CHANNEL = config.get("SLACK_DEFAULT_CHANNEL")
SLACK_DEFAULT_CHANNEL_NAME = config.get("SLACK_DEFAULT_CHANNEL_NAME")

# Notify on MS Teams
MS_TEAMS_TENANT_ID = config.get("MS_TEAMS_TENANT_ID", fallback="common")
MS_TEAMS_CLIENT_ID = config.get("MS_TEAMS_CLIENT_ID")
MS_TEAMS_CLIENT_SECRET = config.get("MS_TEAMS_CLIENT_SECRET")
MS_TEAMS_DEFAULT_TEAMS_ID = config.get("MS_TEAMS_DEFAULT_TEAMS_ID")
MS_TEAMS_DEFAULT_CHANNEL_ID = config.get("MS_TEAMS_DEFAULT_CHANNEL_ID")
MS_TEAMS_DEFAULT_CHANNEL_NAME = config.get("MS_TEAMS_DEFAULT_CHANNEL_NAME", fallback="Navigator")
MS_TEAMS_DEFAULT_WEBHOOK = config.get("MS_TEAMS_DEFAULT_WEBHOOK")
DEFAULT_TEAMS_USER = config.get("DEFAULT_TEAMS_USER")
TEAMS_USER = config.get("TEAMS_USER")
TEAMS_PASSWORD = config.get("TEAMS_PASSWORD")

"""
Task Execution System
"""


# this is the backend for saving task executions
USE_TASK_EVENT = config.getboolean("USE_TASK_EVENT", fallback=True)
# this is the backend for saving task executions
TASK_EXEC_BACKEND = config.get("TASK_EXEC_BACKEND", fallback="influx")
TASK_EVENT_TABLE = config.get("TASK_EVENT_TABLE", fallback="task_execution")
TASK_EXEC_TABLE = config.get("TASK_EXEC_TABLE", fallback="task_activity")

TASK_EXEC_CREDENTIALS = {
    "host": INFLUX_HOST,
    "port": INFLUX_PORT,
    "bucket": INFLUX_DATABASE,
    "org": INFLUX_ORG,
    "token": INFLUX_TOKEN,
}

# Pub/Sub Channel:
PUBSUB_REDIS_DB = config.get("PUBSUB_REDIS_DB", fallback=5)
PUBSUB_REDIS = f"redis://{CACHE_HOST}:{CACHE_PORT}/{PUBSUB_REDIS_DB}"
ERROR_CHANNEL = config.get("ERROR_CHANNEL", fallback="FLOWTASK:FAILED:TASKS")

# Executor configuration:
DEFAULT_EXECUTOR = config.get("DEFAULT_EXECUTOR", fallback="local")
DOCKER_IMAGE = config.get("DOCKER_IMAGE", fallback="flowtask:latest")
K8S_NAMESPACE = config.get("K8S_NAMESPACE", fallback="default")
ALLOW_RESCHEDULE = config.getboolean("ALLOW_RESCHEDULE", fallback=False)
SCHEDULER_STARTUP_JOB = config.getboolean("SCHEDULER_STARTUP_JOBS", fallback=False)

"""
Email Configuration
"""
# email:
EMAIL_USERNAME = config.get("EMAIL_USERNAME")
EMAIL_PASSWORD = config.get("EMAIL_PASSWORD")
EMAIL_PORT = config.get("EMAIL_PORT", fallback=587)
EMAIL_HOST = config.get("EMAIL_HOST")
IMAP_RETRY_SELECT = config.getint("IMAP_RETRY_SELECT", fallback=3)
try:
    IMAP_RETRY_AUTH = config.getint("IMAP_RETRY_AUTH", fallback=3)
except Exception:
    IMAP_RETRY_AUTH = 3
try:
    IMAP_RETRY_AUTH_BACKOFF = config.getfloat("IMAP_RETRY_AUTH_BACKOFF", fallback=2.0)
except Exception:
    IMAP_RETRY_AUTH_BACKOFF = 2.0

"""
Sendgrid Config
"""
SENDGRID_USERNAME = config.get("sendgrid_user")
SENDGRID_PASSWORD = config.get("sendgrid_password")
SENDGRID_PORT = config.get("sendgrid_port", fallback=587)
SENDGRID_HOST = config.get("sendgrid_host")


"""
MS Teams
"""
MS_TEAMS_NAVIGATOR_CHANNEL = config.get(
    "MS_TEAMS_NAVIGATOR_CHANNEL", fallback="Navigator"
)
MS_TEAMS_NAVIGATOR_CHANNEL_ID = config.get("MS_TEAMS_NAVIGATOR_CHANNEL_ID")

"""
Resource Usage
"""
QUERY_API = config.getboolean("QUERY_API", fallback=True)
WEBSOCKETS = config.getboolean("WEBSOCKETS", fallback=True)
VARIABLES = config.getboolean("VARIABLES", fallback=True)
API_TIMEOUT = 36000  # 10 minutes
SEMAPHORE_LIMIT = config.get("SEMAPHORE_LIMIT", fallback=4096)
# upgrade no-files
NOFILES = config.get("ULIMIT_NOFILES", fallback=16384)


#################################################
### MarketPlace infraestructure:

MARKETPLACE_DIR = config.get("MARKETPLACE_DIR")
USE_SSL = config.getboolean("SSL", section="ssl", fallback=False)
if not MARKETPLACE_DIR:
    MARKETPLACE_DIR = BASE_DIR.joinpath("docs", "plugins", "components")

## Sign-in infraestructure
MARKETPLACE_PUBLIC_KEY = BASE_DIR.joinpath("docs", "ssl", "public_key.pem")
MARKETPLACE_CERTIFICATE = BASE_DIR.joinpath("docs", "ssl", "certificate.pem")
MARKETPLACE_PRIVATE_KEY = BASE_DIR.joinpath("docs", "ssl", "private_key.pem")


murl = "http://nav-api.dev.local:5000/api/v1/marketplace/"
MARKETPLACE_URL = config.get("MARKETPLACE_URL", fallback=murl)

## PGP component:
# PGP Credentials
PGP_KEY_PATH = config.get("PGP_KEY_PATH")
PGP_PASSPHRASE = config.get("PGP_PASSPHRASE")

# JIRA:
JIRA_SECRET_TOKEN = config.get('JIRA_SECRET_TOKEN')
JIRA_API_TOKEN = config.get("JIRA_API_TOKEN")
JIRA_USERNAME = config.get("JIRA_USERNAME")
JIRA_INSTANCE = config.get("JIRA_INSTANCE")
JIRA_PROJECT = config.get("JIRA_PROJECT")

# Zammad:
ZAMMAD_INSTANCE = config.get("ZAMMAD_INSTANCE")
ZAMMAD_TOKEN = config.get("ZAMMAD_TOKEN")
ZAMMAD_USER = config.get("ZAMMAD_USER")
ZAMMAD_PASSWORD = config.get("ZAMMAD_PASSWORD")
ZAMMAD_DEFAULT_GROUP = config.get("ZAMMAD_DEFAULT_GROUP")
ZAMMAD_DEFAULT_CUSTOMER = config.get("ZAMMAD_DEFAULT_CUSTOMER")

## Google API:
GOOGLE_API_KEY = config.get('GOOGLE_API_KEY')
GOOGLE_SEARCH_API_KEY = config.get('GOOGLE_SEARCH_API_KEY')
GOOGLE_SEARCH_ENGINE_ID = config.get('GOOGLE_SEARCH_ENGINE_ID')
GOOGLE_PLACES_API_KEY = config.get('GOOGLE_PLACES_API_KEY')
CENSUS_BUREAU_API_KEY = config.get('CENSUS_BUREAU_API_KEY')
GOOGLE_CREDENTIALS_FILE = Path(
    config.get(
        'GOOGLE_CREDENTIALS_FILE',
        fallback=BASE_DIR.joinpath('env', 'google', 'key.json')
    )
)

# Workplace:
WORKPLACE_ACCESS_TOKEN = config.get("WORKPLACE_ACCESS_TOKEN")

### Azure Authentication
# Microsoft Azure
AZURE_ADFS_CLIENT_ID = config.get("AZURE_ADFS_CLIENT_ID")
AZURE_ADFS_CLIENT_SECRET = config.get("AZURE_ADFS_CLIENT_SECRET")
AZURE_ADFS_TENANT_ID = config.get("AZURE_ADFS_TENANT_ID", fallback="common")
AZURE_ADFS_SECRET = config.get("AZURE_ADFS_SECRET")
AZURE_ADFS_DOMAIN = config.get("AZURE_ADFS_DOMAIN", fallback="contoso.onmicrosoft.com")
default_scopes = "User.Read,User.Read.All,User.ReadBasic.All,openid"
AZURE_ADFS_SCOPES = [
    e.strip()
    for e in list(config.get("AZURE_ADFS_SCOPES", fallback="").split(","))
]

# Azure Auth:
AZURE_TENANT_ID = config.get('AZURE_TENANT_ID')
AZURE_CLIENT_ID = config.get('AZURE_CLIENT_ID')
AZURE_SECRET_ID = config.get('AZURE_SECRET_ID')

### barcodelookup api
BARCODELOOKUP_API_KEY = config.get("BARCODELOOKUP_API_KEY")

## Bigquery Credentials
BIGQUERY_DEFAULT_CREDENTIALS = BASE_DIR.joinpath('env', 'google', 'bigquery.json')
BIGQUERY_MARKETING_CREDENTIALS = BASE_DIR.joinpath('env', 'google', 'marketing.json')
BIGQUERY_DEFAULT_PROJECT = config.get('BIGQUERY_PROJECT_ID')

### Oxylabs Proxy Support for Selenium
OXYLABS_USERNAME = config.get('OXYLABS_USERNAME')
OXYLABS_PASSWORD = config.get('OXYLABS_PASSWORD')
OXYLABS_ENDPOINT = config.get('OXYLABS_ENDPOINT')

## Office 365:
O365_CLIENT_ID = config.get('O365_CLIENT_ID')
O365_CLIENT_SECRET = config.get('O365_CLIENT_SECRET')
O365_TENANT_ID = config.get('O365_TENANT_ID')

# Sharepoint:
SHAREPOINT_APP_ID = config.get('SHAREPOINT_APP_ID')
SHAREPOINT_APP_SECRET = config.get('SHAREPOINT_APP_SECRET')
SHAREPOINT_TENANT_ID = config.get('SHAREPOINT_TENANT_ID')
SHAREPOINT_TENANT_NAME = config.get('SHAREPOINT_TENANT_NAME')
SHAREPOINT_SITE_ID = config.get('SHAREPOINT_SITE_ID')
SHAREPOINT_DEFAULT_HOST = config.get('SHAREPOINT_DEFAULT_HOST')

# AWS S3:
aws_region = config.get('AWS_REGION')
aws_bucket = config.get('AWS_BUCKET')
aws_key = config.get('AWS_KEY')
aws_secret = config.get('AWS_SECRET')

# AWS S3 Vision:
vision_aws_region = config.get('vision_aws_region')
vision_aws_bucket = config.get('vision_aws_bucket')

# Thumbnail Configuration:
THUMBNAIL_LOCAL_BASE_URL = config.get('THUMBNAIL_LOCAL_BASE_URL', fallback='')

### AI Models Settings #
EMBEDDING_DEVICE = config.get('EMBEDDING_DEVICE', fallback='cpu')
EMBEDDING_DEFAULT_MODEL = config.get(
    'EMBEDDING_DEFAULT_MODEL',
    fallback='thenlper/gte-base'
)

# AI Models Cache Configuration
HUGGINGFACE_EMBEDDING_CACHE_DIR = config.get(
    'HUGGINGFACE_EMBEDDING_CACHE_DIR',
    fallback=Path.home().joinpath('.cache', 'huggingface', 'embeddings')
)

## MILVUS DB ##:
MAX_BATCH_SIZE = config.get('MAX_BATCH_SIZE', fallback=768)
MILVUS_HOST = config.get('MILVUS_HOST', fallback='localhost')
MILVUS_PROTOCOL = config.get('MILVUS_PROTOCOL', fallback='http')
MILVUS_PORT = config.get('MILVUS_PORT', fallback=19530)
MILVUS_DATABASE = config.get('MILVUS_DATABASE')
MILVUS_URL = config.get('MILVUS_URL')
MILVUS_TOKEN = config.get('MILVUS_TOKEN')
MILVUS_USER = config.get('MILVUS_USER')
MILVUS_PASSWORD = config.get('MILVUS_PASSWORD')
MILVUS_SECURE = config.getboolean('MILVUS_SECURE', fallback=False)
MILVUS_SERVER_NAME = config.get(
    'MILVUS_SERVER_NAME'
)
MILVUS_CA_CERT = config.get('MILVUS_CA_CERT', fallback=None)
MILVUS_SERVER_CERT = config.get('MILVUS_SERVER_CERT', fallback=None)
MILVUS_SERVER_KEY = config.get('MILVUS_SERVER_KEY', fallback=None)
MILVUS_USE_TLSv2 = config.getboolean('MILVUS_USE_TLSv2', fallback=False)

## Bot Configuration:
ENABLE_BOT_REVIEWER = config.getboolean('ENABLE_BOT_REVIEWER', fallback=False)
DEFAULT_BOT_NAME = config.get('BOT_NAME', fallback='TaskReviewer')
DEFAULT_LLM_MODEL = config.get('LLM_MODEL', fallback='gemini-2.5-flash')
DEFAULT_LLM_TEMPERATURE = config.get('LLM_TEMPERATURE', fallback=0.1)

## Dask Configuration:
DASK_SCHEDULER = config.get("DASK_SCHEDULER", fallback="tcp://127.0.0.1:8786")
DASK_SCHEDULER_PORT = config.get("DASK_SCHEDULER_PORT", fallback=8786)

## LeadIQ Configuration:
LEADIQ_API_KEY = config.get('LEADIQ_API_KEY')

## Paradox Configuration:
PARADOX_ACCOUNT_ID = config.get('PARADOX_ACCOUNT_ID')
PARADOX_API_SECRET = config.get('PARADOX_API_SECRET')

## Network Ninja Configuration:
NETWORKNINJA_API_KEY = config.get('NETWORKNINJA_API_KEY')
NETWORKNINJA_BASE_URL = config.get('NETWORKNINJA_BASE_URL')
NETWORKNINJA_ENV = config.get('NETWORKNINJA_ENV', fallback='production')

"""
Tasks and ETLs
"""
## Default Task Path
program = config.get("TASK_PATH")
if not program:
    TASK_PATH = BASE_DIR.joinpath("tasks", "programs")
else:
    TASK_PATH = Path(program).resolve()

logger.notice(f"FlowTask Default Path: {TASK_PATH}")

TASK_STORAGES: dict[str, Any] = {"default": FileTaskStorage(path=TASK_PATH)}

ETL_PATH = config.get("ETL_PATH")
FILES_PATH = Path(ETL_PATH).resolve()

FILE_STORAGES: dict[str, Any] = {
    "default": FileStore(path=FILES_PATH, prefix="files")
}

# AWS:
AWS_CREDENTIALS = {
    "default": {
        "use_credentials": True,
        "aws_key": aws_key,
        "aws_secret": aws_secret,
        "region_name": aws_region,
        "bucket_name": aws_bucket
    },
    "navigator": {
        "use_credentials": False,
        "aws_key": aws_key,
        "aws_secret": aws_secret,
        "region_name": aws_region,
        "bucket_name": aws_bucket
    },
    "vision": {
        "use_credentials": False,
        "aws_key": None,
        "aws_secret": None,
        "region_name": vision_aws_region,
        "bucket_name": vision_aws_bucket
    },
}

# Workday SOAP settings
WORKDAY_CLIENT_ID = config.get("WORKDAY_CLIENT_ID")
WORKDAY_CLIENT_SECRET = config.get("WORKDAY_CLIENT_SECRET")
WORKDAY_TOKEN_URL = config.get("WORKDAY_TOKEN_URL")
WORKDAY_WSDL_PATH = config.get("WORKDAY_WSDL_PATH", fallback=BASE_DIR.joinpath("env", "workday", "staffing_custom_44_2.wsdl"))
WORKDAY_WSDL_TIME = config.get("WORKDAY_WSDL_TIME", fallback=BASE_DIR.joinpath("env", "workday", "timetracking_custom_44_2.wsdl"))
WORKDAY_WSDL_HUMAN_RESOURCES = config.get("WORKDAY_WSDL_HUMAN_RESOURCES", fallback=BASE_DIR.joinpath("env", "workday", "humanresources_troc_44_2.wsdl"))
WORKDAY_WSDL_FINANCIAL_MANAGEMENT = config.get("WORKDAY_WSDL_FINANCIAL_MANAGEMENT", fallback=BASE_DIR.joinpath("env", "workday", "financial_management_45.wsdl"))
WORKDAY_WSDL_RECRUITING = config.get("WORKDAY_WSDL_RECRUITING", fallback=BASE_DIR.joinpath("env", "workday", "recruiting_44_2.wsdl"))
WORKDAY_WSDL_ABSENCE_MANAGEMENT = config.get("WORKDAY_WSDL_ABSENCE_MANAGEMENT", fallback=BASE_DIR.joinpath("env", "workday", "absense_management_45_custom.wsdl"))
WORKDAY_WSDL_TIME_BLOCK_REPORT = config.get("WORKDAY_WSDL_TIME_BLOCK_REPORT", fallback=BASE_DIR.joinpath("env", "workday", "extract_time_blocks_navigator.wsdl"))
WORKDAY_WSDL_CUSTOM_PUNCH_FIELD_REPORT = config.get("WORKDAY_WSDL_CUSTOM_PUNCH_FIELD_REPORT", fallback=BASE_DIR.joinpath("env", "workday", "custom_punch_field_report_nav.wsdl"))
WORKDAY_WSDL_INTEGRATIONS = config.get("WORKDAY_WSDL_INTEGRATIONS", fallback=BASE_DIR.joinpath("env", "workday", "integrations_45.wsdl"))
WORKDAY_REFRESH_TOKEN = config.get("WORKDAY_REFRESH_TOKEN", fallback=None)
# Custom Report Credentials (for basic auth)
WORKDAY_REPORT_USERNAME = config.get("WORKDAY_REPORT_USERNAME", fallback=None)
WORKDAY_REPORT_PASSWORD = config.get("WORKDAY_REPORT_PASSWORD", fallback=None)
# Alternative: base64-encoded password (to avoid special character issues)
WORKDAY_REPORT_PASSWORD_BASE64 = config.get("WORKDAY_REPORT_PASSWORD_BASE64", fallback=None)
if WORKDAY_REPORT_PASSWORD_BASE64 and not WORKDAY_REPORT_PASSWORD:
    WORKDAY_REPORT_PASSWORD = base64.b64decode(WORKDAY_REPORT_PASSWORD_BASE64).decode('utf-8')

## Zoom Configuration:
ZOOM_ACCOUNT_ID = config.get('ZOOM_ACCOUNT_ID')
ZOOM_CLIENT_ID = config.get('ZOOM_CLIENT_ID')
ZOOM_CLIENT_SECRET = config.get('ZOOM_CLIENT_SECRET')

## Zoom SMS Configuration:
ZOOM_SMS_ACCOUNT_ID = config.get('ZOOM_SMS_ACCOUNT_ID')
ZOOM_SMS_CLIENT_ID = config.get('ZOOM_SMS_CLIENT_ID')
ZOOM_SMS_CLIENT_SECRET = config.get('ZOOM_SMS_CLIENT_SECRET')
ZOOM_SMS_DEFAULT_FROM = config.get('ZOOM_SMS_DEFAULT_FROM')
ZOOM_WEBHOOK_SECRET_TOKEN = config.get('ZOOM_WEBHOOK_SECRET_TOKEN')
ZOOM_WEBHOOK_REPLAY_WINDOW_SECONDS = config.getint(
    'ZOOM_WEBHOOK_REPLAY_WINDOW_SECONDS', fallback=300
)
ZOOM_ALLOWED_CIDRS = config.get('ZOOM_ALLOWED_CIDRS', fallback='')

try:
    from navconfig.conf import *  # pylint: disable=W0401,W0614 # noqa
except ImportError as e:
    print(e)
try:
    from settings.settings import *  # pylint: disable=W0401,W0614 # noqa
except ImportError as e:
    print(e)
    logging.warning(
        "Wrong *Settings* Module, Settings is required for fine-tune configuration."
    )
except Exception as e:
    print(e)
    logging.warning(
        "Missing *Settings* Module, Settings is required for fine-tune configuration."
    )
