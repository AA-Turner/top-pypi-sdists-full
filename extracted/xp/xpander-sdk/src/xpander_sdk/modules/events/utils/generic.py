from urllib.parse import urlparse

from xpander_sdk.models.configuration import Configuration
from xpander_sdk.utils.env import url_host

# Exact cloud inbound-gateway hostnames (matched by parsed hostname, never
# substring); only these reroute event streaming to the cloud agent-controller.
XPANDER_CLOUD_INBOUND_HOSTS = frozenset(
    {"inbound.xpander.ai", "inbound.stg.xpander.ai"}
)

# Hosts eligible for the local-dev 8085 -> 9016 controller rewrite.
_LOOPBACK_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})


def backoff_delay(attempt: int) -> int:
    """1 s after first failure, 2 s after second, 3 s for attempts >= 3."""
    return 1 if attempt == 1 else 2 if attempt == 2 else 3


def get_events_root(configuration: Configuration) -> str:
    """
    Construct the organization-scoped root URL for event-streaming endpoints.

    Returns:
        str: "{base}/{organization_id}" with the base resolved from configuration.
    """
    # Fail loudly on a missing base URL instead of streaming to a cloud default.
    if not configuration.base_url:
        raise ValueError(
            "Event streaming requires a base URL - set Configuration.base_url "
            "or the XPANDER_BASE_URL environment variable."
        )

    parsed = urlparse(configuration.base_url)
    host = (parsed.hostname or "").lower()

    if host in XPANDER_CLOUD_INBOUND_HOSTS:
        is_stg = host == "inbound.stg.xpander.ai"
        base = f"https://agent-controller{'.stg' if is_stg else ''}.xpander.ai"
    elif parsed.port == 8085 and host in _LOOPBACK_HOSTS:
        # local dev only: API served on 8085, agent-controller on 9016
        base = "http://localhost:9016"
    else:
        base = configuration.base_url

    return f"{base}/{configuration.organization_id}"


def get_events_base(configuration: Configuration) -> str:
    """
    Construct the base URL used for event streaming endpoints.

    Returns:
        str: The base URL for event streaming based on configuration and environment.
    """
    return f"{get_events_root(configuration)}/events"


def is_stg_environment(configuration: Configuration) -> bool:
    """True when event streaming targets the staging cloud or local dev."""
    host = url_host(get_events_base(configuration))
    return host == "localhost" or "stg" in host.split(".")


def get_events_headers(configuration: Configuration) -> dict[str, str]:
    """
    Construct the headers required for requests, including authentication.

    Returns:
        dict[str, str]: HTTP headers including the API key for authorization.
    """
    return {"x-api-key": configuration.api_key}
