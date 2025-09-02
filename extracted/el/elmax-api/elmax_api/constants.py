"""Constants for the Elmax Cloud service client."""

from . import __version__


# URL Constants
BASE_URL = "https://cloud.elmaxsrl.it/api/ext/"
ENDPOINT_DEVICES = "devices"
ENDPOINT_LOGIN = "login"
ENDPOINT_STATUS_ENTITY_ID = "status"
ENDPOINT_DISCOVERY = "discovery"
ENDPOINT_LOCAL_CMD = "cmd"
ENDPOINT_REFRESH = "refresh"

# User agent
USER_AGENT = f"elmax-api/{__version__}"

# DEFAULT HTTP TIMEOUT
DEFAULT_HTTP_TIMEOUT = 20.0
BUSY_WAIT_INTERVAL = 2.0

# OTHER DEFAULTS
DEFAULT_PANEL_PIN = "000000"

# Version constants
VERSION_REFRESH_SUPPORT = "4.13.2"
