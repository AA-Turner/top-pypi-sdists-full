"""Installer constants shared by CLI, per-user, and system installation.

Keep the two deployment profiles distinct: their service names and port defaults
are intentional. Importing this module does not provision services or read config.
"""
from pathlib import Path

from hugpy_core.imports.constants import ENV_CALLLOG_DSN, ENV_CORE_DB, ENV_CORE_SCHEMA

# Per-user installer defaults (the 7300 port block).
SERVICE = "hugpy-core"
TS_SERVICE = "hugpy-toolserver"
PG_SERVICE = "hugpy-postgres"     # the orbit's own cluster, OWNED by `abstract-toolserver db install` (own mode)
PACKAGE = SERVICE
TS_EXE = "abstract-toolserver"    # the DB CLI core shells out to — core provisions no Postgres itself
DEFAULT_DB = "hugpy"              # the database name (own mode: the cluster's db; create-db: the new db)
DEFAULT_SCHEMA = "hugpy_core"     # existing-DSN mode: core's own schema inside the account's database
DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORTS = {"core": 7301, "wrapper": 7302, "router": 7303, "toolserver": 7304}
CLUSTER_PORT = 7305               # the orbit's own Postgres cluster (own mode; the hugpy 7300 block)
PEER_HOST = "/var/run/postgresql" # the system cluster's socket dir (--create-db path)
TS_HOST = "127.0.0.1"
HEALTH_WAIT_S = 120               # core binds first, then ensures its schema and seeds before serving
TS_HEALTH_WAIT_S = 60
MARK = "written by `hugpy-core install`"
ENV_CORE_URL = "HUGPY_CORE_URL"
ENV_CORE_HOST = "HUGPY_CORE_HOST"            # bookkeeping: what the unit was rendered with
ENV_CORE_PORT = "HUGPY_CORE_PORT"
ENV_CORE_TS_URL = "HUGPY_CORE_TOOLSERVER_URL"
ENV_CORE_TS_TOKEN = "HUGPY_CORE_TOOLSERVER_TOKEN"
ENV_CENTRAL_MODELS_HOME = "HUGPY_CENTRAL_MODELS_HOME"
ROUTER_KEY_ENV = "HUGPY_ROUTER_KEY"          # the router's admin key, in router.env
ROUTER_PORT_ENV = "HUGPY_ROUTER_PORT"
WRAPPER_PORT_ENV = "FITEVICT_PORT"
TS_TOKEN_ENV = "TOOLSERVER_OPERATOR_TOKEN"
TS_DB_KEYS = ("SOLCATCHER_POSTGRESQL_HOST", "SOLCATCHER_POSTGRESQL_PORT", "SOLCATCHER_POSTGRESQL_USER",
              "SOLCATCHER_POSTGRESQL_NAME", "SOLCATCHER_POSTGRESQL_PASS")

# System installer paths and defaults (a distinct deployment profile).
ACCOUNT = SERVICE
STATE = Path("/var/lib") / SERVICE
CONFIG_DIR = Path("/etc/hugpy")
CONFIG = CONFIG_DIR / "core.env"
FLASK_CONFIG = CONFIG_DIR / "core.service-flask-db.env"
TOOLSERVER_CONFIG = CONFIG_DIR / "toolserver.env"
ENDPOINT = CONFIG_DIR / "core.endpoint.json"
UNIT_DIR = Path("/etc/systemd/system")
CORE_UNIT = f"{SERVICE}.service"
DOWNLOAD_UNIT = f"{SERVICE}-downloader.service"
CATALOG_UNIT = f"{SERVICE}-catalog.service"
INTAKE_UNIT = f"{SERVICE}-intake.service"
PG_UNIT = f"{SERVICE}-postgres.service"
TS_UNIT = f"{SERVICE}-toolserver.service"
TS_HOME = STATE / "toolserver"
DEFAULT_PORT = 7020
PG_PORT = 7306

# Shared CLI dispatch vocabulary.
INSTALLER_VERBS = ("install", "uninstall", "status")

# Defaults also used inside system installer operations.
WRAPPER_ENDPOINT = CONFIG.with_name("wrapper.endpoint.json")
WRAPPER_CONFIG = CONFIG.with_name("wrapper.env")
WRAPPER_TOKEN_ENV = "FITEVICT_TOKEN"
