import os
from typing import Any, Mapping, Optional

from novita_sandbox.core.connection_config import DEFAULT_NOVITA_DOMAIN, is_legacy_domain


def resolve_domain(domain: Optional[str] = None) -> str:
    resolved = domain or os.getenv("NOVITA_DOMAIN") or DEFAULT_NOVITA_DOMAIN
    if not resolved:
        raise ValueError("domain cannot be empty")
    return resolved


def should_use_legacy(opts: Optional[Mapping[str, Any]] = None) -> bool:
    domain = opts.get("domain") if opts is not None else None
    return is_legacy_domain(resolve_domain(domain))


def raise_if_legacy(opts: Optional[Mapping[str, Any]], feature: str) -> None:
    if should_use_legacy(opts):
        raise NotImplementedError(f"{feature} is not supported on legacy domains")
