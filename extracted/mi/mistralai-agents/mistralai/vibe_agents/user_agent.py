"""The `User-Agent` product token that identifies Agents SDK callers to the control plane."""

from packaging.version import InvalidVersion, Version

from mistralai.vibe_agents import __version__

_PRODUCT_PREFIX = "mistralai-agents/"
# The caller controls this header, so cap what it can write into events. PEP 440 does not bound local versions.
_MAX_VERSION_LENGTH = 64

USER_AGENT = f"{_PRODUCT_PREFIX}{__version__}"


def sdk_version_from_user_agent(user_agent: str | None) -> str | None:
    """Return the Agents SDK version a request was sent with, or `None` when another client sent it."""
    if user_agent is None:
        return None
    for token in user_agent.split():
        if not token.startswith(_PRODUCT_PREFIX):
            continue
        raw_version = token.removeprefix(_PRODUCT_PREFIX)
        if len(raw_version) > _MAX_VERSION_LENGTH:
            return None
        try:
            return str(Version(raw_version))
        except InvalidVersion:
            return None
    return None


__all__ = ["USER_AGENT", "sdk_version_from_user_agent"]
