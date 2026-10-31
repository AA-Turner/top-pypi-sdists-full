"""The framing Observational Memory wraps around a person's memory — an ORG KNOB.

Before a person's agent answers, OM prepends a system message: a preamble, the
``<observations>`` block, then instructions for using it. That framing is not an
Observer/Reflector call and not a Holder's text — it is an OPINION about how an
agent should read its memory, so it is an organization's choice (law 6: opinions
become knobs; BYPASS-CENSUS aidream round-3 residue, 2026-09-25).

The host installs ONE resolver at boot (aidream: the ``agents.memory`` feature
knobs ``context_preamble`` / ``context_instructions``, org-overridable). With no
host — the package installed on its own — there is NO default text: asking for the framing raises
:class:`ContextFramingNotConfigured` (the package keeps no copy of the platform's text). A resolver
that FAILS never silently changes what the model sees:

1. the failure is captured through the platform's error capture (``memory_framing_unreadable``);
2. the organization's last text read from the knob rows is used; else the PLATFORM value
   (``resolver(None)``, the knob row itself); else the platform's last text read;
3. only when no knob text has ever been readable in this process does the turn carry the
   observations with no framing, and that is captured too (``memory_framing_missing``), so a knob
   outage never takes a person's memory away and never hides.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable

logger = logging.getLogger(__name__)

#: ``async (organization_id) -> (preamble, instructions)``.
ContextFramingResolver = Callable[[str | None], Awaitable[tuple[str, str]]]

_RESOLVER: ContextFramingResolver | None = None
#: The last framing each organization (``None`` = platform) read from the knob rows in this process.
_LAST_READ: dict[str | None, tuple[str, str]] = {}

UNREADABLE_KIND = "memory_framing_unreadable"
MISSING_KIND = "memory_framing_missing"


class ContextFramingNotConfigured(RuntimeError):
    """No host installed the memory-framing resolver, so there is no framing text to wrap memory in."""

    def __init__(self) -> None:
        super().__init__(
            "Observational Memory has no framing text: call set_context_framing_resolver(<async org -> "
            "(preamble, instructions)>) at startup. The package keeps no default copy of the text."
        )


def set_context_framing_resolver(resolver: ContextFramingResolver | None) -> None:
    """Install the host's org-knob reader (``None`` removes it)."""
    global _RESOLVER
    _RESOLVER = resolver
    _LAST_READ.clear()


async def _capture(exc: BaseException, kind: str, organization_id: str | None, used: str) -> None:
    from matrx_connect.streaming.error_capture import capture_error

    logger.error(
        "[OM] memory context framing (%s) for org %s: %s: %s; this turn uses %s; check the "
        "agents.memory feature knobs (context_preamble / context_instructions)",
        kind, organization_id, type(exc).__name__, exc, used,
    )
    await capture_error(
        exc,
        kind=kind,
        route="memory.context_framing",
        error_type=type(exc).__name__,
        context={"organization_id": organization_id, "framing_used": used},
    )


async def _read(organization_id: str | None) -> tuple[str, str]:
    assert _RESOLVER is not None
    preamble, instructions = await _RESOLVER(organization_id)
    got = (str(preamble or ""), str(instructions or ""))
    _LAST_READ[organization_id] = got
    return got


async def resolve_context_framing(organization_id: str | None) -> tuple[str, str]:
    """The (preamble, instructions) this organization's agents wrap memory in."""
    if _RESOLVER is None:
        raise ContextFramingNotConfigured()
    try:
        return await _read(organization_id)
    except Exception as exc:  # noqa: BLE001 — captured, then the knob rows' own text is used
        failure: BaseException = exc
    if organization_id in _LAST_READ:
        await _capture(failure, UNREADABLE_KIND, organization_id, "the organization's last read text")
        return _LAST_READ[organization_id]
    if organization_id is not None:
        try:
            got = await _read(None)
        except Exception:  # noqa: BLE001 — the org failure below is the one captured
            pass
        else:
            await _capture(failure, UNREADABLE_KIND, organization_id, "the platform value")
            return got
    if None in _LAST_READ:
        await _capture(failure, UNREADABLE_KIND, organization_id, "the platform's last read text")
        return _LAST_READ[None]
    await _capture(failure, MISSING_KIND, organization_id, "no framing text")
    return "", ""


__all__ = [
    "MISSING_KIND",
    "UNREADABLE_KIND",
    "ContextFramingNotConfigured",
    "ContextFramingResolver",
    "resolve_context_framing",
    "set_context_framing_resolver",
]
