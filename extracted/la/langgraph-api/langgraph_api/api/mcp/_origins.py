from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING
from urllib.parse import urlsplit

from langgraph_api.config import ANY_ORIGIN

if TYPE_CHECKING:
    from langgraph_api.config.schemas import CorsConfig

LOOPBACK_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})
WEB_SCHEMES = frozenset({"http", "https"})


@dataclass(frozen=True, slots=True)
class OriginPolicy:
    listed: frozenset[str]
    pattern: re.Pattern[str] | None

    @classmethod
    def of(cls, settings: CorsConfig) -> OriginPolicy:
        regex = settings.get("allow_origin_regex")
        return cls(
            frozenset(settings.get("allow_origins", ())) - {ANY_ORIGIN},
            re.compile(regex) if regex is not None else None,
        )

    def allows(self, origin: str | None) -> bool:
        return (
            origin is None
            or origin in self.listed
            or (self.pattern is not None and self.pattern.fullmatch(origin) is not None)
            or _bare_origin_host(origin) in LOOPBACK_HOSTS
        )


def _bare_origin_host(origin: str) -> str | None:
    try:
        parsed = urlsplit(origin)
    except ValueError:
        return None
    if (
        parsed.scheme not in WEB_SCHEMES
        or "@" in parsed.netloc
        or parsed.path
        or parsed.query
        or parsed.fragment
    ):
        return None
    return parsed.hostname or None
