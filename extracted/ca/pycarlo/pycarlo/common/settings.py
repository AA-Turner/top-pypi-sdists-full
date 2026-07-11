import os
import re
from enum import Enum
from pathlib import Path
from urllib.parse import urlparse

"""Environmental configuration"""

# Enable error logging.
MCD_VERBOSE_ERRORS = os.getenv("MCD_VERBOSE_ERRORS", False) in (True, "true", "True")

# MCD API endpoint.
MCD_API_ENDPOINT = os.getenv("MCD_API_ENDPOINT")

# Override MCD Default Profile when reading from the config-file in a session.
MCD_DEFAULT_PROFILE = os.getenv("MCD_DEFAULT_PROFILE")

# Override MCD API ID when creating a session.
MCD_DEFAULT_API_ID = os.getenv("MCD_DEFAULT_API_ID")

# Override MCD API Token when creating a session.
MCD_DEFAULT_API_TOKEN = os.getenv("MCD_DEFAULT_API_TOKEN")

# MCD ID header (for use in local development and testing)
MCD_USER_ID_HEADER = os.getenv("MCD_USER_ID_HEADER")

# Override MCD OAuth client credentials when creating a session.
MCD_DEFAULT_OAUTH_CLIENT_ID = os.getenv("MCD_DEFAULT_OAUTH_CLIENT_ID")
MCD_DEFAULT_OAUTH_CLIENT_SECRET = os.getenv("MCD_DEFAULT_OAUTH_CLIENT_SECRET")

# Override the OAuth token / API endpoints (otherwise derived from the API endpoint).
MCD_TOKEN_ENDPOINT = os.getenv("MCD_TOKEN_ENDPOINT")
MCD_OAUTH_API_ENDPOINT = os.getenv("MCD_OAUTH_API_ENDPOINT")

# Deployment instance id (e.g. us1, eu1) used to build the OAuth instance-routing scope so the
# global gateway can route to the right instance.
MCD_DEFAULT_INSTANCE_ID = os.getenv("MCD_DEFAULT_INSTANCE_ID")

# dbt cloud API token
DBT_CLOUD_API_TOKEN = os.getenv("DBT_CLOUD_API_TOKEN")

# dbt cloud account ID
DBT_CLOUD_ACCOUNT_ID = os.getenv("DBT_CLOUD_ACCOUNT_ID")

"""Internal Use"""

# Default API endpoint when not provided through env variable nor profile
DEFAULT_MCD_API_ENDPOINT = "https://api.getmontecarlo.com/graphql"

# Default Gateway endpoint used when no endpoint is provided through env var or profile
DEFAULT_MCD_IGW_ENDPOINT = "https://integrations.getmontecarlo.com"

# Name of the current package.
DEFAULT_PACKAGE_NAME = "pycarlo"

# Default config keys for the MC config file. Created via the CLI.
DEFAULT_MCD_API_ID_CONFIG_KEY = "mcd_id"
DEFAULT_MCD_API_TOKEN_CONFIG_KEY = "mcd_token"
DEFAULT_MCD_API_ENDPOINT_CONFIG_KEY = "mcd_api_endpoint"
DEFAULT_MCD_OAUTH_CLIENT_ID_CONFIG_KEY = "mcd_oauth_client_id"
DEFAULT_MCD_OAUTH_CLIENT_SECRET_CONFIG_KEY = "mcd_oauth_client_secret"
DEFAULT_MCD_TOKEN_ENDPOINT_CONFIG_KEY = "mcd_token_endpoint"
DEFAULT_MCD_OAUTH_API_ENDPOINT_CONFIG_KEY = "mcd_oauth_api_endpoint"
DEFAULT_MCD_INSTANCE_ID_CONFIG_KEY = "mcd_instance_id"

# The Cognito custom scope requested for API access via OAuth.
API_OAUTH_SCOPE = "https://api.getmontecarlo.com/access"

# Prefix of the per-instance routing scope; the deployment instance id is appended.
INSTANCE_OAUTH_SCOPE_PREFIX = "https://instance.getmontecarlo.com/"

# Instance ids are short DNS-safe identifiers (e.g. "us1", "eu1"): alphanumerics + hyphens,
# 1-63 chars. Matches the global-api-gateway's validator so the SDK never accepts an id the
# gateway would reject.
INSTANCE_ID_PATTERN = re.compile(r"^[A-Za-z0-9-]{1,63}$")


def validate_instance_id(instance_id: str) -> str:
    """Validate and normalize a deployment instance id (e.g. ``us1``, ``eu1``).

    Returns the trimmed id, or raises ``ValueError`` if it isn't a valid identifier — a malformed
    value would otherwise produce a broken instance-routing scope.
    """
    normalized = (instance_id or "").strip()
    if not INSTANCE_ID_PATTERN.fullmatch(normalized):
        raise ValueError(
            f"Invalid instance id {instance_id!r}; expected an identifier matching "
            f"{INSTANCE_ID_PATTERN.pattern!r} (e.g. us1, eu1)."
        )
    return normalized


# Authorization header for OAuth bearer tokens.
DEFAULT_AUTHORIZATION_HEADER = "Authorization"


def derive_token_endpoint(api_endpoint: str) -> str:
    """OAuth token endpoint derived from the API endpoint: same host, path ``/oauth2/token``.

    The token request goes to the global gateway (same host as the API), which routes it to the
    right instance by the requested instance scope.

    e.g. ``https://api.getmontecarlo.com/graphql`` -> ``https://api.getmontecarlo.com/oauth2/token``.

    Raises ``ValueError`` if ``api_endpoint`` isn't the expected ``/graphql`` endpoint (e.g. the
    IGW root or a custom endpoint) so a misconfiguration fails loudly at session construction
    rather than posting credentials to the wrong URL; set ``mcd_token_endpoint`` explicitly for
    a custom endpoint.
    """
    parsed = urlparse(api_endpoint)
    if parsed.path.rstrip("/") != "/graphql":
        raise ValueError(
            f"Cannot derive the OAuth token endpoint from {api_endpoint!r}: expected an API "
            "endpoint ending in /graphql. Set mcd_token_endpoint explicitly."
        )
    return f"{parsed.scheme}://{parsed.netloc}/oauth2/token"


def derive_instance_scope(instance_id: str) -> str:
    """OAuth instance-routing scope for a deployment instance id (e.g. ``us1``), requested at
    token time so the global gateway can route to that instance.

    e.g. ``us1`` -> ``https://instance.getmontecarlo.com/us1``.
    """
    return f"{INSTANCE_OAUTH_SCOPE_PREFIX}{instance_id}"


# Default headers for the MC API.
DEFAULT_MCD_API_ID_HEADER = f"x-{DEFAULT_MCD_API_ID_CONFIG_KEY.replace('_', '-')}"
DEFAULT_MCD_API_TOKEN_HEADER = f"x-{DEFAULT_MCD_API_TOKEN_CONFIG_KEY.replace('_', '-')}"
DEFAULT_MCD_USER_ID_HEADER = "user-id"

# Default headers to trace and help identify requests. For debugging.
DEFAULT_MCD_SESSION_ID = "x-mcd-session-id"  # Generally the session name.
DEFAULT_MCD_TRACE_ID = "x-mcd-trace-id"

# File name for profile configuration.
PROFILE_FILE_NAME = "profiles.ini"

# Default profile to be used.
DEFAULT_PROFILE_NAME = "default"

# Default path where any configuration files are written.
DEFAULT_CONFIG_PATH = os.path.join(str(Path.home()), ".mcd")

# Default initial wait time for retries in seconds.
DEFAULT_RETRY_INITIAL_WAIT_TIME = 0.25

# Default maximum wait time for retries in seconds.
DEFAULT_RETRY_MAX_WAIT_TIME = 10.0

# Default initial wait time for idempotent request retries in seconds.
DEFAULT_IDEMPOTENT_RETRY_INITIAL_WAIT_TIME = 4.0

# Default maximum wait time for idempotent request retries in seconds.
DEFAULT_IDEMPOTENT_RETRY_MAX_WAIT_TIME = 4 * pow(
    2, 4
)  # retry 4 times, max wait 64 seconds, total wait 124

# Default timeout for requests sent to Integration Gateway
DEFAULT_IGW_TIMEOUT_SECS = 10

# Additional request headers
HEADER_MCD_TELEMETRY_REASON = "x-mcd-telemetry-reason"  # why the request was made
HEADER_MCD_TELEMETRY_SERVICE = "x-mcd-telemetry-service"  # what service made the request


class RequestReason(Enum):
    USER = "user"  # request made directly by a user
    SERVICE = "service"  # request made by a service, on behalf of a user or automation
