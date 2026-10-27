import os

WIN_OS = "windows"
ARM_64 = "arm64"
X64 = "x64"

OS_MAP = {
    "darwin": "mac",
    "linux": "linux",
    WIN_OS: WIN_OS
}

ARCH_MAP = {
    "x86_64": X64,
    "amd64": X64,
    ARM_64: ARM_64,
    "aarch64": ARM_64
}

# Cache for operations.py
TABLES_COLUMNS_TYPES = {}

# Global constants - use constants.<Global_variable> to access them as they can be overridden in the
DEBUGGING = False
EXECUTED_VIA_CLI = False
TABLES = {}
SCHEMA_QUALIFIED = False

UPLOAD_FILENAME = "code.zip"
CONFIGURATION_FORM_FILENAME = "configuration_form.pb"
LAST_VERSION_CHECK_FILE = "_last_version_check"
ROOT_LOCATION = os.path.join(".fivetran", "connector_sdk")
CONFIG_FILE = "_config.json"
CONFIG_ENCRYPTION_KEY_FILE = "config_encryption_key"
ENCRYPTED_VALUE_PREFIX = "fivetran_encrypted:"

# `fivetran configuration`
REQUIRED_INPUT_MESSAGE = "This field is required and cannot be skipped. Please provide a valid input."
DROPDOWN_LABEL = "DROPDOWN_FIELD"
TOGGLE_LABEL = "TOGGLE_FIELD"
OUTPUT_FILES_DIR = "files"
CRASH_REPORTS_DIR = "crash-reports"
CRASH_REPORT_FILENAME_FORMAT = "crash_%Y%m%d-%H%M%S.log"
REQUIREMENTS_TXT = "requirements.txt"
PYPROJECT_TOML = "pyproject.toml"
PYPROJECT_SKIP_VALIDATION_MESSAGE = "using pyproject.toml; skipping dependency validation"
RECOMMEND_STABLE_VERSION_MESSAGE = "We recommend using the current stable version for the following libraries:"
CONFIGURATION_JSON = "configuration.json"
DESTINATION_JSON = "destination.json"
FIVETRAN_API_KEY_ENV = "FIVETRAN_API_KEY"
API_KEY_FIELD = "api_key"  # Must never be written to the local options file
FIELD_DESTINATION = "destination"
FIELD_CONNECTION = "connection"
FIELD_PYTHON_VERSION = "python_version"
FIELD_NAMING = "naming"
FIELD_HYBRID_DEPLOYMENT_AGENT_ID = "hybrid_deployment_agent_id"
FIELD_PROXY_ID = "proxy_id"
FIELD_PROXY_HOST_CONFIG_KEY = "proxy_host_config_key"
FIELD_PACKAGE_ID = "package_id"
MANAGED_OPTIONS_FIELDS = frozenset({
    FIELD_DESTINATION, FIELD_CONNECTION, FIELD_PYTHON_VERSION, FIELD_NAMING,
    FIELD_HYBRID_DEPLOYMENT_AGENT_ID, FIELD_PROXY_ID, FIELD_PROXY_HOST_CONFIG_KEY, FIELD_PACKAGE_ID,
})
FIVETRAN_DESTINATION_NAME_ENV = "FIVETRAN_DESTINATION_NAME"
FIVETRAN_CONNECTION_NAME_ENV = "FIVETRAN_CONNECTION_NAME"
PYPI_PACKAGE_DETAILS_URL = "https://pypi.org/pypi/fivetran_connector_sdk/json"
SIX_HOUR_IN_SEC = 6 * 60 * 60
REQUEST_TIMEOUT_SECONDS = 60  # for a call to the Fivetran API: how long a connection or a reply may stay silent
MEMORY_LIMIT_BYTES = 4 * 1024 ** 3  # 4 GB memory limit to simulate memory constraints during local debug
CHECKPOINT_OP_TIMEOUT_IN_SEC = 120 # seconds
FIFO_READ_TIMEOUT_SECONDS = 30 # seconds - timeout for reading from FIFOs (named pipes)
MAX_RETRIES = 3
SDK_LOGGING_PREFIX = "⚡ sdk "
DEBUGGER_LOGGING_PREFIX = "⚡ debugger"
CONNECTOR_LOGGING_PREFIX = "⚡ connector"
VIRTUAL_ENV_CONFIG = "pyvenv.cfg"
GITIGNORE_FILENAME = ".gitignore"
ROOT_FILENAME = "connector.py"
MAX_RECORDS_IN_BATCH = 100
MAX_BATCH_SIZE_IN_BYTES = 100000 # Default 100 KB
QUEUE_SIZE = 100
FILE_UPLOAD_CHUNK_SIZE_BYTES = int(2 * 1024 * 1024) # 2 MB
FILE_UPLOAD_READ_TIMEOUT_SEC = int(300) # 5 minutes
FIVETRAN_FILE_PATH_COLUMN = "_fivetran_file_path"

ALWAYS_INCLUDED_FILES = [GITIGNORE_FILENAME]
EXCLUDED_DIRS = ["__pycache__", "lib", "include", OUTPUT_FILES_DIR, CRASH_REPORTS_DIR]
EXCLUDED_PIPREQS_DIRS = ["bin", "etc", "include", "lib", "Lib", "lib64", "Scripts", "share"]
VALID_COMMANDS = ["version", "init", "debug", "run", "deploy", "reset", "package", "configuration", "help"]
PACKAGE_SUBCOMMANDS = ["create", "update", "list"]
PACKAGE_LIST_MAX_PAGE_SIZE = 1000
PACKAGE_LIST_PAGE_PROGRESS_WIDTH = 40
INVALID_API_KEY_MESSAGE = "ensure you're using a valid base64-encoded API key"
DEPRECATED_FORCE_FLAG_WARNING = (
    "--force and -f are deprecated and will be removed in a future release. "
    "Use --non-interactive or --yes instead. See help for more details."
)
MAX_ALLOWED_EDIT_DISTANCE_FROM_VALID_COMMAND = 3
COMMANDS_AND_SYNONYMS = {
    "debug": {"test", "verify", "diagnose", "check"},
    "deploy": {"upload", "ship", "launch", "release"},
    "reset": {"reinitialize", "reinitialise", "re-initialize", "re-initialise", "restart", "restore"},
}

CONNECTION_SCHEMA_NAME_PATTERN = r'^[_a-z][_a-z0-9]*$'
PRODUCTION_BASE_URL = "https://api.fivetran.com"
INSTALLATION_SCRIPT_MISSING_MESSAGE = "installation.sh not found in the drivers directory; this file is required to configure custom drivers"
INSTALLATION_SCRIPT = "installation.sh"
DRIVERS = "drivers"
JAVA_LONG_MAX_VALUE = 9223372036854775807
JAVA_LONG_MIN_VALUE = -9223372036854775808
JAVA_INT_MAX_VALUE = 2147483647
JAVA_INT_MIN_VALUE = -2147483648
MAX_CONFIG_FIELDS = 100
SUPPORTED_PYTHON_VERSIONS = ["3.14", "3.13", "3.12", "3.11", "3.10"]
DEFAULT_PYTHON_VERSION = "3.14"
FIVETRAN_HD_AGENT_ID = "FIVETRAN_HD_AGENT_ID"
FIVETRAN_PYTHON_VERSION_ENV = "FIVETRAN_PYTHON_VERSION"
FIVETRAN_NAMING_ENV = "FIVETRAN_NAMING"  # Environment variable name for setting naming strategy
FIVETRAN_NAMING_VALUE = "FIVETRAN"  # Fivetran naming strategy value
SOURCE_NAMING_VALUE = "SOURCE"  # Source naming strategy value
UNDERSCORE_NAMING = "_NAMING"  # Suffix for sending naming to Fivetran API
OPTIONS_FILENAME = "options.toml"
FIVETRAN_OPTIONS_FILE_ENV = "FIVETRAN_OPTIONS_FILE"
DEFAULT_PROFILE_NAME = "default"
OPTIONS_FILE_MIGRATION_DOCS_URL = (
    "https://fivetran.com/docs/connector-sdk/technical-reference/options-file#automaticmigration")
FIELD_RESOLUTION_ORDER_DOCS_URL = (
    "https://fivetran.com/docs/connector-sdk/getting-started/connector-sdk-commands#fieldresolutionorder")
OPTIONS_FILE_SKIP_MIN_PYTHON_MESSAGE = "local options file requires Python 3.11 or later; skipping"
OPTIONS_FILE_HEADER_COMMENT = (
    "# This file is managed by you. The Fivetran Connector SDK CLI only adds or updates the profile of the connection being deployed.\n"
    "# It stores `fivetran deploy` fields grouped into profiles. Edit, move, or delete it freely.\n"
)
UTF_8 = "utf-8"
REDACTED_VALUE = "****"
EXAMPLES_GITHUB_REPO = "fivetran/connector_sdk"
GITHUB_BRANCH = "main"
CONNECTORS_GITHUB_REPO = "fivetran/community_connectors"
CONNECTORS_TEMPLATE_PREFIX = "connectors/"
TOOLS_GITHUB_REPO = "fivetran/connector_sdk_tools"
TOOLS_GITHUB_REPO_URL = f"https://github.com/{TOOLS_GITHUB_REPO}"
AI_TOOLS_INSTALLATION_DOCS_URL = (
    "https://fivetran.com/docs/connector-sdk/building-connectors/ai-tools#installingtheplugin"
)
TOOLS_PLUGIN_ID = "fivetran-connector-sdk-ai"
TOOLS_PLUGIN_NAME = f"fivetran-connector-sdk@{TOOLS_PLUGIN_ID}"
AGENT_PLUGINS = {
    "claude": {
        "display_name": "Claude Code",
        "cli_command": "claude",
        "install_commands": [
            ["claude", "plugin", "marketplace", "add", TOOLS_GITHUB_REPO],
            ["claude", "plugin", "install", TOOLS_PLUGIN_NAME],
        ],
        "update_commands": [
            ["claude", "plugin", "update", TOOLS_PLUGIN_NAME],
        ],
    },
    "codex": {
        "display_name": "Codex CLI",
        "cli_command": "codex",
        "min_supported_version": (0, 131, 0),
        "install_commands": [
            ["codex", "plugin", "marketplace", "add", TOOLS_GITHUB_REPO],
            ["codex", "plugin", "add", TOOLS_PLUGIN_NAME],
        ],
        "update_commands": [
            ["codex", "plugin", "marketplace", "upgrade", TOOLS_PLUGIN_ID],
        ],
    },
    "gemini": {
        "display_name": "Gemini CLI",
        "cli_command": "gemini",
        "install_commands": [
            ["gemini", "extensions", "install", TOOLS_GITHUB_REPO_URL, "--consent", "--skip-settings", "--auto-update"],
        ],
    },
    "copilot": {
        "display_name": "GitHub Copilot CLI",
        "cli_command": "copilot",
        "install_commands": [
            ["copilot", "plugin", "marketplace", "add", TOOLS_GITHUB_REPO],
            ["copilot", "plugin", "install", TOOLS_PLUGIN_NAME],
        ],
        "update_commands": [
            ["copilot", "plugin", "update", TOOLS_PLUGIN_NAME],
        ],
    },
}
SUPPORTED_AGENT_DISPLAY_NAMES = ", ".join(config["display_name"] for config in AGENT_PLUGINS.values())
TEMPLATE_CONNECTOR_PATH = "_template_connector"

# Messages of the setup form and its tests (`fivetran configuration`)
CONFIGURATION_FORM_MISSING = (
    "Your connector does not implement the configuration_form() method. Please implement it and re-run."
    "\nFor more information, see https://fivetran.com/docs/connector-sdk/technical-reference/connector-sdk-setup-form")
CONFIGURATION_TESTS_MISSING = "Your connector does not provide any configuration tests to run."

# --- Telemetry ---
# Anonymous CLI usage telemetry — see the shared fivetran_cli_telemetry package. Sent to a Fivetran webhook
# connector dedicated to Connector SDK CLI usage; the fivetran CLI uses a different webhook URL.
CONNECTOR_SDK_CLI_TELEMETRY_WEBHOOK_URL = "https://webhooks.fivetran.com/webhooks/e02e86c4-5a36-4ac5-833a-d9062f25ecf0"
TELEMETRY_SOURCE_NAME = "fivetran-connector-sdk"
