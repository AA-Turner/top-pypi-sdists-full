"""Keep SDK OSS discovery within the requested metadata environment."""

from __future__ import annotations

import inspect
from typing import Any

STORAGE_SIDES = {
    "dev": "pre",
    "internal-dev": "pre",
    "external-dev": "pre",
    "prod": "online",
}


def oss_fallback_kwargs(repo: Any, client: Any, method: str, environment: str) -> dict:
    """Allow API reads across environments; disable unsafe storage fallback.

    Missing/unknown storage provenance is insufficient for explicit online/pre
    discovery. auto follows the bound store. Bind missing SDK discovery provenance.
    """
    profile = getattr(repo, "profile", None)
    # instance-repo 1.3.5.dev2+ reads _p in Dataset discovery without binding it
    # during construction. Supply the actual Repo profile before that check.
    if callable(getattr(client, "_discovery_env_match", None)) and not hasattr(client, "_p"):
        client._p = profile
    if environment == "auto":
        return {}
    storage = getattr(profile, "storage_env", "")
    storage = storage.strip().lower() if isinstance(storage, str) else ""
    side = STORAGE_SIDES.get(storage, "")
    if side and side == environment:
        return {}

    try:
        parameters = inspect.signature(getattr(client, method)).parameters
    except (AttributeError, TypeError, ValueError):
        parameters = {}
    if "fallback_to_oss" in parameters:
        return {"fallback_to_oss": False}
    # Older metadata-only clients have no storage fallback to disable.
    if getattr(client, "_content", None) is None:
        return {}
    if any(p.kind is inspect.Parameter.VAR_KEYWORD for p in parameters.values()):
        return {"fallback_to_oss": False}
    raise RuntimeError(
        "The installed instance-repo cannot disable OSS discovery for this query. "
        "Upgrade the SDK or use a cluster with storage matching --environment."
    )
