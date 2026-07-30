import os

import requests

# LOGS
DEFAULT_LOGLEVEL = "WARNING"
LOGLEVEL = lambda: os.getenv("ABSTRA_LOGLEVEL", DEFAULT_LOGLEVEL)  # noqa: E731
NOISY_LOGLEVEL = lambda: os.getenv("ABSTRA_NOISY_LOGLEVEL", DEFAULT_LOGLEVEL)  # noqa: E731

PROCESS_LOGFORMAT = "[%(asctime)s][%(levelname)s][%(name)s][%(process)d]%(message)s"
DEFAULT_LOGFORMAT = "[%(asctime)s][%(levelname)s][%(name)s] %(message)s"
LOGFORMAT = lambda: os.getenv("ABSTRA_LOGFORMAT", DEFAULT_LOGFORMAT)  # noqa: E731
CLOUD_SAMPLE_RATE = float(os.getenv("ABSTRA_CLOUD_SAMPLE_RATE", 0.2))
LOCAL_SAMPLE_RATE = float(os.getenv("ABSTRA_LOCAL_SAMPLE_RATE", 0.0))

# SERVER
HOST = os.getenv("ABSTRA_HOST", "localhost")
DEFAULT_PORT = os.getenv("PORT") or os.getenv("ABSTRA_SERVER_PORT")

# PRODUCTION ENVIRONMENT
BUILD_ID = os.getenv("ABSTRA_BUILD_ID") or "dev"
PROJECT_ID = os.getenv("ABSTRA_PROJECT_ID") or "dev-project-id"
PROJECT_URL = os.getenv("ABSTRA_PROJECT_URL")

# Web editor with cloud-api-served player: when set, the editor pod does not
# register the player blueprint — player routes are served by cloud-api at
# this URL (see /_editor/player-url for the authenticated hand-off).
EXTERNAL_PLAYER_URL = os.getenv("ABSTRA_EXTERNAL_PLAYER_URL")

# PASSWORDLESS AUTHENTICATION
EMAIL_JWT_AUDIENCE = f"abstra:email:{PROJECT_ID}"
PUBLIC_KEY = os.getenv("ABSTRA_JWT_PUBLIC_KEY_PEM")

# OIDC AUTHENTICATION
OIDC_CLIENT_ID = lambda: os.getenv("ABSTRA_OIDC_CLIENT_ID")  # noqa: E731
OIDC_AUTHORITY = lambda: os.getenv("ABSTRA_OIDC_AUTHORITY")  # noqa: E731


# CLOUD API
CLOUD_API_DEFAULT_ENDPOINT = "https://cloud-api.abstra.cloud"
CLOUDFRONT_CLOUD_API_ENDPOINT = "https://cloud.abstra.io/api/cloud-api"


def select_cloud_api_endpoint() -> str:
    try:
        response = requests.get(f"{CLOUD_API_DEFAULT_ENDPOINT}/healthcheck", timeout=10)
        if response.status_code == 200:
            return CLOUD_API_DEFAULT_ENDPOINT
    except Exception as e:
        print(f"Healthcheck failed for {CLOUD_API_DEFAULT_ENDPOINT}: {e}")

    return CLOUDFRONT_CLOUD_API_ENDPOINT


CLOUD_API_ENDPOINT = os.getenv("CLOUD_API_ENDPOINT") or select_cloud_api_endpoint()


CLOUD_API_CLI_URL = f"{CLOUD_API_ENDPOINT}/cli"

_DEFAULT_DEV_SHARED_TOKEN = "shared-token-for-development-only"
CLOUD_API_PROD_SHARED_TOKEN = os.getenv(
    "ABSTRA_CLOUD_API_SHARED_TOKEN", _DEFAULT_DEV_SHARED_TOKEN
)
CLOUD_API_PROD_HEADERS = {"shared-token": CLOUD_API_PROD_SHARED_TOKEN}
CLOUD_API_PROD_URL = f"{CLOUD_API_ENDPOINT}/apps"

CLOUD_CONSOLE_URL = os.getenv("ABSTRA_CONSOLE_URL", "https://cloud.abstra.io")


# DOCS

DOCS_URL = os.getenv("ABSTRA_DOCS_URL", "https://www.abstra.io/docs")

# DEBUG
DISABLE_STDIO_PATCH = os.getenv("ABSTRA_DISABLE_STDIO_PATCH", "false") == "true"
REQUEST_TIMEOUT = int(os.getenv("ABSTRA_REQUEST_TIMEOUT", 300))
MAX_HTTP_CLIENT_THREADS = int(os.getenv("ABSTRA_MAX_HTTP_CLIENT_THREADS", 10))

# FILES
FILES_FOLDER = os.getenv("ABSTRA_FILES_FOLDER")
WORKER_FILES_FOLDER = os.getenv("ABSTRA_WORKER_FILES_FOLDER", "/files")
DISABLED_STAGES_FOLDER = os.getenv("ABSTRA_DISABLED_STAGES_FOLDER")

SMARTCHAT_PACKAGES_FOLDER = os.getenv("ABSTRA_SMARTCHAT_PACKAGES_FOLDER")

# CLAMAV DOWNLOAD SCANNING
CLAMAV_SCAN_ENABLED = (
    os.getenv("ABSTRA_CLAMAV_SCAN_ENABLED", "false").strip().lower() == "true"
)
CLAMD_HOST = os.getenv("ABSTRA_CLAMD_HOST", "clamd.security.svc.cluster.local")
CLAMD_PORT = int(os.getenv("ABSTRA_CLAMD_PORT", "3310"))

# WEBEDITOR
WAITING_ROOM_URL = os.getenv("ABSTRA_WAITING_ROOM_URL") or ""

# ENVIRONMENT
IS_PRODUCTION = os.getenv("ABSTRA_ENVIRONMENT") == "production"
IS_DEVELOPMENT = not IS_PRODUCTION
EDITOR_MODE = os.getenv("ABSTRA_EDITOR_MODE") or "local"

# WEB EDITOR HEARTBEAT (used to decide if the shared EFS storage of a
# web-editor pod can be safely cleaned on startup — see
# services/web_editor_heartbeat.py)
# Defaults: write every 15 min (900 s); consider stale after 3 days (259200 s).
WEB_EDITOR_HEARTBEAT_INTERVAL_SECONDS = int(
    os.getenv("ABSTRA_WEB_EDITOR_HEARTBEAT_INTERVAL_SECONDS", 900)
)
WEB_EDITOR_HEARTBEAT_STALENESS_SECONDS = int(
    os.getenv("ABSTRA_WEB_EDITOR_HEARTBEAT_STALENESS_SECONDS", 259200)
)

# EDITOR STALL WATCHDOG (measures whole-process scheduling stalls on the
# web editor — see services/editor_stall_watchdog.py)
# Defaults: probe every 0.5 s; record stalls of 2 s or more. Consecutive
# stalls are batched into one event, flushed when the process recovers or
# every 60 s while the burst lasts (bounds log volume, drops no data).


def _float_env(name: str, default: float, minimum: float) -> float:
    """Defensive parse for tuning knobs: this module is imported by every
    abstra entrypoint, so a malformed value must fall back to the default
    instead of crashing the boot. Values below `minimum` are clamped — an
    interval of 0 would busy-loop the watchdog thread at 100% CPU.
    """
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        value = float(raw)
    except ValueError:
        return default
    if not (value >= minimum):  # also catches NaN
        return minimum
    return value


EDITOR_STALL_WATCHDOG_INTERVAL_SECONDS = _float_env(
    "ABSTRA_EDITOR_STALL_WATCHDOG_INTERVAL_SECONDS", default=0.5, minimum=0.25
)
EDITOR_STALL_WATCHDOG_THRESHOLD_SECONDS = _float_env(
    "ABSTRA_EDITOR_STALL_WATCHDOG_THRESHOLD_SECONDS", default=2.0, minimum=0.5
)
EDITOR_STALL_WATCHDOG_BATCH_WINDOW_SECONDS = _float_env(
    "ABSTRA_EDITOR_STALL_WATCHDOG_BATCH_WINDOW_SECONDS", default=60, minimum=1.0
)

# FORMS CONFIG
SHOW_WATERMARK = os.getenv("ABSTRA_SHOW_WATERMARK", "false") == "true"

# AMQP
WORKER_LOG_TO_QUEUE = os.getenv("ABSTRA_WORKER_LOG_TO_QUEUE", "false") == "true"
RABBITMQ_EXECUTION_QUEUE = os.getenv("ABSTRA_RABBITMQ_EXECUTION_QUEUE", "executions")
RABBITMQ_DEFAUT_EXCHANGE = os.getenv("ABSTRA_RABBITMQ_DEFAUT_EXCHANGE", "")
RABBITMQ_CONNECTION_URI = os.getenv("ABSTRA_RABBITMQ_CONNECTION_URI")

# WEB EDITOR POSTGRES STORAGE
# Single switch between the file-based (EFS) backend and the PostgreSQL backend
# for the web-editor pods. Captured ONCE at import; presence is decided once at
# boot in the repository factory and never re-evaluated at runtime. Absence ⇒
# behavior identical to the current file-based path. No default by design.
WEB_EDITOR_DATABASE_URI = os.getenv("ABSTRA_WEB_EDITOR_DATABASE_URI")


def web_editor_uses_db() -> bool:
    """Single source of truth for the web-editor backend switch (§6/§12): the
    PostgreSQL backend is used iff the DB URI was injected. Every site that needs
    to know the backend (factory, editor/worker boot, stdio gating) calls this so
    the predicate can never drift between modules."""
    return WEB_EDITOR_DATABASE_URI is not None


def linter_sidecar_enabled() -> bool:
    """Kill-switch for running the editor's linter in a dedicated child
    process (default ON). "0"/"false" falls back to the untouched in-process
    LocalLinterRepository — temporary rollback path, slated for removal after
    a couple of stable releases. Read at call time (factory build) so tests
    and operators can flip it without re-importing."""
    return os.getenv("ABSTRA_LINTER_SIDECAR", "true").strip().lower() not in (
        "0",
        "false",
    )


def linter_sidecar_serial() -> bool:
    """Whether the linter sidecar child runs its rules serially (one at a time)
    instead of the thread-per-rule fan-out.

    Only the web editor (pod) runs serial: there, thread-per-rule would inflate
    the cgroup's CFS throttle and steal CPU from the editor's HTTP serving
    threads. A local install has no cgroup budget to protect, so it keeps the
    parallel fan-out — a full lint pass (boot, deploy gate) then finishes in
    roughly the time of its slowest rule instead of the sum of all rules. Read
    at call time (the spawned child inherits ABSTRA_EDITOR_MODE) so operators
    and tests can flip it without re-importing."""
    return (os.getenv("ABSTRA_EDITOR_MODE") or "local").strip().lower() == "web"


# NOTE on ABSTRA_WORKER_LOG_TO_QUEUE: it only ever made sense for queue-based
# log streaming. On the DB backend the editor poller streams logs/events straight
# from Postgres, so the queue path is bypassed and the env var is IGNORED. Sites
# that gate on it spell out `WORKER_LOG_TO_QUEUE and not web_editor_uses_db()`
# inline (rather than a helper) so existing tests can still patch the module-level
# WORKER_LOG_TO_QUEUE constant.


# NATS
NATS_URL = os.getenv("ABSTRA_NATS_URL")
NATS_CREDS = os.getenv("ABSTRA_NATS_CREDS")

# AMQP Connection Resilience
RABBITMQ_CONNECTION_TIMEOUT_SECONDS = float(
    os.getenv("ABSTRA_RABBITMQ_CONNECTION_TIMEOUT_SECONDS", 60)
)
RABBITMQ_RETRY_MAX_ATTEMPTS = int(os.getenv("ABSTRA_RABBITMQ_RETRY_MAX_ATTEMPTS", 5))
RABBITMQ_RETRY_INITIAL_DELAY_SECONDS = float(
    os.getenv("ABSTRA_RABBITMQ_RETRY_INITIAL_DELAY_SECONDS", 2)
)

# EXECUTION DRAIN (HTTP server waiting for RabbitMQ response)
DRAIN_START_TIMEOUT_SECONDS = float(
    os.getenv("ABSTRA_DRAIN_START_TIMEOUT_SECONDS", 120.0)
)
DRAIN_RESPONSE_TIMEOUT_SECONDS = float(
    os.getenv("ABSTRA_DRAIN_RESPONSE_TIMEOUT_SECONDS", 120.0)
)

# WORKER PROCESSING
PROCESS_TIMEOUT_SECONDS = int(os.getenv("ABSTRA_PROCESS_TIMEOUT_SECONDS", 60 * 60 * 2))

ABSTRA_EXECUTOR_POOL_SIZE = int(os.getenv("ABSTRA_EXECUTOR_POOL_SIZE", 2))
ABSTRA_MIN_FORMS_EXECUTORS = int(os.getenv("ABSTRA_MIN_FORMS_EXECUTORS", 0))
ABSTRA_EXECUTOR_MAX_EXECUTIONS = int(os.getenv("ABSTRA_EXECUTOR_MAX_EXECUTIONS", 8))
ABSTRA_EXECUTOR_WARMUP_TIMEOUT = float(
    os.getenv("ABSTRA_EXECUTOR_WARMUP_TIMEOUT", 60.0)
)
ABSTRA_EXECUTOR_WARMUP_PARALLELISM = int(
    os.getenv("ABSTRA_EXECUTOR_WARMUP_PARALLELISM", 1)
)
ABSTRA_EXECUTOR_ACQUIRE_TIMEOUT = float(
    os.getenv("ABSTRA_EXECUTOR_ACQUIRE_TIMEOUT", 600.0)  # 10 minutes default
)

# DEBUG MODE
ABSTRA_DEBUG_MODE_INTERVAL = int(os.getenv("ABSTRA_DEBUG_MODE_INTERVAL", 30))

# GUNICORN SERVER
WORKERS = os.getenv("ABSTRA_WORKERS", 2)
THREADS = os.getenv("ABSTRA_THREADS", 20)
WORKER_CLASS = os.getenv("ABSTRA_WORKER_CLASS", "gthread")
WORKER_CONNECTIONS = int(os.getenv("ABSTRA_WORKER_CONNECTIONS", 1000))
WORKER_TEMP_DIR = os.getenv("ABSTRA_WORKER_TEMP_DIR")

# GIT
FORCE_GIT_CLIENT = os.getenv("ABSTRA_FORCE_GIT_CLIENT")
REMOTE_GIT_URL = f"{CLOUD_API_CLI_URL}/git/repo.git"
REMOTE_NAME = "abstra"
