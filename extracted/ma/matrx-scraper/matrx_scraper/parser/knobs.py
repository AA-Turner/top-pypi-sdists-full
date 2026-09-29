"""Parser thresholds — host-bound `platform.feature_knob` values (feature ``knowledge.scraper``).

Authority: ``common-docs/policies/limits-are-knobs-agents-set-them.md`` (Arman,
2026-08-20) and USD-5 (2026-09-10): a behavioural value is a registry row an
admin turns, never a constant nobody can see. This package must not import
aidream, so the host injects a ONE-ARGUMENT reader (``key -> value``) here —
aidream binds ``knob_*_sync("knowledge.scraper", key)`` in ``package_integration`` —
and every read below goes through it, live, so turning the row takes effect
within the host's knob cache TTL and no deploy.

Standalone posture: with no host bound, each read answers with the package's
own default, which the call site declares beside a ``KNOB MIRROR`` comment
naming the registry row. That mirror is the standalone contract, not a silent
fallback: it is the value the row was seeded with, and it is announced once
per process so a host that forgot to bind is never mistaken for one that did.
"""

from __future__ import annotations

import sys
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

FEATURE = "knowledge.scraper"

@dataclass(frozen=True)
class KnobScope:
    """WHO a read is for — the rungs the platform resolver walks.

    Every knob has a platform default an organization (and, where the knob
    allows it, a person or a site) may override (Arman's standing rule). A read
    that knows its organization passes it, so that organization's override
    applies to it and to nobody else.
    """

    organization_id: str
    user_id: str | None = None
    site_id: str | None = None


#: ``async (keys, scope) -> {key: value}`` — the host's scoped resolver for
#: feature ``knowledge.scraper`` (platform → organization → site → user). A key
#: the host cannot resolve is simply absent from the answer.
ScopedReader = Callable[[list[str], KnobScope], Awaitable[dict[str, Any]]]

_reader: Callable[[str], Any] | None = None
_scoped_reader: ScopedReader | None = None
_announced = False
_scoped_announced = False
_failed: set[str] = set()


def configure_parser_knobs(
    reader: Callable[[str], Any] | None, *, scoped_reader: ScopedReader | None = None
) -> None:
    """Bind the host's readers for feature ``knowledge.scraper``.

    ``reader`` answers the PLATFORM value (``key -> value``, sync — the parser
    runs in sync code). ``scoped_reader`` answers the value for one
    organization / person / site, async and in bulk, so a crawl resolves all
    its keys once per run. ``None`` unbinds, restoring the standalone posture."""
    global _reader, _scoped_reader, _announced, _scoped_announced
    _reader = reader
    _scoped_reader = scoped_reader
    _announced = False
    _scoped_announced = False
    _failed.clear()


def parser_knob(key: str, mirror: Any) -> Any:
    """The live value of ``knowledge.scraper.<key>`` through the host, or the declared
    mirror when no host is bound (announced once)."""
    global _announced
    if _reader is None:
        if not _announced:
            _announced = True
            print(
                "[matrx_scraper] no host knob reader bound for 'knowledge.scraper'; using the "
                "package's mirrored defaults (bind one with configure_parser_knobs())",
                file=sys.stderr,
            )
        return mirror
    try:
        return _reader(key)
    except Exception as exc:  # noqa: BLE001 — announced, never a crashed parse
        # The host is bound but cannot answer (typically a process that never
        # primed its knob snapshot). Say so once per key, with the remedy, and
        # keep the declared mirror rather than failing the caller's work.
        if key not in _failed:
            _failed.add(key)
            print(
                f"[matrx_scraper] host knob reader failed for {FEATURE!r}.{key!r}: {exc!r}; "
                f"using the mirrored default {mirror!r} until the host primes the "
                f"feature (aidream: prime_knob_features(*SYNC_READ_FEATURES))",
                file=sys.stderr,
            )
        return mirror


async def scoped_parser_knobs(
    mirrors: dict[str, Any], scope: KnobScope | None
) -> dict[str, Any]:
    """Every key in ``mirrors`` resolved FOR ``scope``, in one host call.

    With no scope (a caller that does not know whose work this is) the answer is
    the platform value (:func:`parser_knob`). With a scope but no scoped reader
    bound, or a reader that fails, the platform value is used and that is said
    once — an organization's override that silently did nothing is the defect
    this exists to prevent.
    """
    global _scoped_announced
    platform = {key: parser_knob(key, mirror) for key, mirror in mirrors.items()}
    if scope is None:
        return platform
    if _scoped_reader is None:
        if not _scoped_announced:
            _scoped_announced = True
            print(
                f"[matrx_scraper] no scoped knob reader bound for {FEATURE!r}; organization "
                "and user overrides are NOT applied — platform values are used (bind one with "
                "configure_parser_knobs(..., scoped_reader=...))",
                file=sys.stderr,
            )
        return platform
    try:
        resolved = await _scoped_reader(list(mirrors), scope)
    except Exception as exc:  # noqa: BLE001 — announced, never a failed crawl
        print(
            f"[matrx_scraper] scoped knob read for {FEATURE!r} failed for organization "
            f"{scope.organization_id}: {exc!r}; its overrides are NOT applied to this run — "
            "platform values are used",
            file=sys.stderr,
        )
        return platform
    return {key: resolved.get(key, platform[key]) for key in mirrors}


__all__ = [
    "FEATURE",
    "KnobScope",
    "ScopedReader",
    "configure_parser_knobs",
    "parser_knob",
    "scoped_parser_knobs",
]
