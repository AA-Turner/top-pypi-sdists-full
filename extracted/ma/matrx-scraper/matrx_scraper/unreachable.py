"""A host we could not reach is said in words — which host, what failed, what to do.

A fetch that never got an answer (the name does not resolve, the connection is refused, the
network has no route) has no HTTP status. It used to be recorded as ``status_code=500`` with the
bare reason ``request_error``, so a person typing a misspelled address read "the site answered
500" — a server error from a server that does not exist (web-app walk, 2026-09-26). This module
is the ONE place that recognises those failures (the crawler's escalation gate reads the same
signatures) and writes the sentence every result surface shows.
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any
from urllib.parse import urlsplit

#: Resolver failures: the name does not exist (or the resolver could not answer).
DNS_SIGNATURES: tuple[str, ...] = (
    "name or service not known",
    "nodename nor servname",
    "temporary failure in name resolution",
    "could not resolve host",
    "getaddrinfo",
    "no address associated with hostname",
    "err_name_not_resolved",
)

#: The name resolved, but nothing answered.
CONNECT_SIGNATURES: tuple[str, ...] = (
    "connection refused",
    "no route to host",
    "network is unreachable",
    "err_connection_refused",
    "err_address_unreachable",
)

#: Every signature that means "we never reached the host".
UNREACHABLE_ERROR_SIGNATURES: tuple[str, ...] = DNS_SIGNATURES + CONNECT_SIGNATURES


def _texts(failure_details: Iterable[dict[str, Any]] | None) -> list[str]:
    return [str(v).lower() for d in (failure_details or []) for v in (d or {}).values()]


def unreachable_kind(failure_details: Iterable[dict[str, Any]] | None) -> str | None:
    """``"dns"``, ``"connect"`` or ``None`` for a result's recorded failure details."""
    texts = _texts(failure_details)
    if any(sig in t for t in texts for sig in DNS_SIGNATURES):
        return "dns"
    if any(sig in t for t in texts for sig in CONNECT_SIGNATURES):
        return "connect"
    return None


def host_of(url: str) -> str:
    raw = (url or "").strip()
    host = urlsplit(raw if "//" in raw else f"//{raw}").hostname or ""
    return host or raw or "this address"


def unreachable_sentence(url: str, failure_details: Iterable[dict[str, Any]] | None) -> str | None:
    """The sentence for a host we never reached, or ``None`` when the failure is something else."""
    kind = unreachable_kind(failure_details)
    if kind is None:
        return None
    host = host_of(url)
    if kind == "dns":
        return (
            f"We could not reach {host}: that address does not exist (its name did not resolve), "
            "so nothing was read and nothing was saved. Check the web address for a typo; if it "
            "is right, the site may be offline — try again later."
        )
    return (
        f"We could not reach {host}: it did not accept a connection, so nothing was read and "
        "nothing was saved. The site may be down or blocking connections — check the address "
        "and try again later."
    )


def announce_unreachable(result: Any) -> bool:
    """On an unusable result whose host we never reached: no fabricated HTTP status, and the
    sentence on ``failure_message``. Returns True when it applied. In place."""
    details = getattr(result, "failure_details", None)
    sentence = unreachable_sentence(str(getattr(result, "url", "") or ""), details)
    if sentence is None:
        return False
    result.failure_message = sentence
    result.status_code = 0
    return True


__all__ = [
    "CONNECT_SIGNATURES",
    "DNS_SIGNATURES",
    "UNREACHABLE_ERROR_SIGNATURES",
    "announce_unreachable",
    "host_of",
    "unreachable_kind",
    "unreachable_sentence",
]
