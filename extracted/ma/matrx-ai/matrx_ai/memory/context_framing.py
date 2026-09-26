"""The framing Observational Memory wraps around a person's memory — an ORG KNOB.

Before a person's agent answers, OM prepends a system message: a preamble, the
``<observations>`` block, then instructions for using it. That framing is not an
Observer/Reflector call and not a Holder's text — it is an OPINION about how an
agent should read its memory, so it is an organization's choice (law 6: opinions
become knobs; BYPASS-CENSUS aidream round-3 residue, 2026-09-25).

The host installs ONE resolver at boot (aidream: the ``agents.memory`` feature
knobs ``context_preamble`` / ``context_instructions``, org-overridable). With no
host — the package installed on its own — the constants below are the default.
A resolver that FAILS is said out loud and the default is used for that turn, so
a knob outage never takes a person's memory away.
"""

from __future__ import annotations

import logging
from collections.abc import Awaitable, Callable

from .constants import OBSERVATION_CONTEXT_INSTRUCTIONS, OBSERVATION_CONTEXT_PROMPT

logger = logging.getLogger(__name__)

#: ``async (organization_id) -> (preamble, instructions)``.
ContextFramingResolver = Callable[[str | None], Awaitable[tuple[str, str]]]

_RESOLVER: ContextFramingResolver | None = None


def set_context_framing_resolver(resolver: ContextFramingResolver | None) -> None:
    """Install the host's org-knob reader (``None`` restores the standalone default)."""
    global _RESOLVER
    _RESOLVER = resolver


async def resolve_context_framing(organization_id: str | None) -> tuple[str, str]:
    """The (preamble, instructions) this organization's agents wrap memory in."""
    if _RESOLVER is None:
        return OBSERVATION_CONTEXT_PROMPT, OBSERVATION_CONTEXT_INSTRUCTIONS
    try:
        preamble, instructions = await _RESOLVER(organization_id)
    except Exception as exc:  # noqa: BLE001 — one failure shape, said out loud
        logger.error(
            "[OM] memory context framing knob could not be read for org %s (%s: %s) — "
            "using the platform default text for this turn; check the agents.memory "
            "feature knobs (context_preamble / context_instructions)",
            organization_id,
            type(exc).__name__,
            exc,
        )
        return OBSERVATION_CONTEXT_PROMPT, OBSERVATION_CONTEXT_INSTRUCTIONS
    return str(preamble or ""), str(instructions or "")


__all__ = [
    "ContextFramingResolver",
    "resolve_context_framing",
    "set_context_framing_resolver",
]
