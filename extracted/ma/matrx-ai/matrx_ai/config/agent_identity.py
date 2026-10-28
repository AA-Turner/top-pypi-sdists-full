"""WHO MADE THIS AGENT — every agent names AI Matrx and the lab of the model it runs on.

Arman, 2026-10-26 (``common-docs/systems/agents/agent-design/VISION.md``): "All agents
should identify as being a 'collaboration between AI Matrx and whatever lab they're
from". The trigger: the General Voice Assistant (Grok Voice) answered "who built you?"
with its lab alone.

The words are a knob, never code
--------------------------------
``platform.feature_knob`` feature ``agents.identity`` (organization-overridable):

* ``statement`` — the sentence, with ``{lab}`` filled from the CATALOG maker of the
  model actually running (``ai.model_definition.provider_id`` -> ``ai.provider.name``,
  what ``ai.model_public.maker`` reads; ``AiCatalogManager.model_maker``);
* ``statement_own_model`` — when that maker is AI Matrx itself;
* ``statement_unknown_lab`` — when the catalog names no maker: AI Matrx is still named,
  no lab is invented, and the gap is announced.

The host installs ONE async resolver at boot (``set_identity_statement_resolver``) that
answers the three strings for an organization. No resolver -> no part, announced once
(this package holds no fallback wording).

Placement: the per-turn context channel, NOT the cached system prefix
---------------------------------------------------------------------
The part rides ``MessageList.attach_turn_context`` (slot ``agent_identity``), staged by
the send boundary at EVERY loop send (``send_boundary._stage_agent_identity``). Why not
the system prefix, where the date sits:

1. A FROZEN conversation sends exactly the prompt its row stores
   (``_enforce_frozen_prompt``) and a mandate-held one sends its frozen record
   (``_settle_held_prompt``). A new system part would make every existing
   conversation's render differ from its row — a false cache-line alarm on every
   old thread — or never reach it at all.
2. A model switch mid-conversation changes the lab. The frozen prefix is turn one's
   bytes forever, so it would keep naming the first lab. The turn context is rebuilt
   from ``config.model`` on every send, so it always names the lab that is answering.
3. The turn-context block renders after the newest message (or as an uncached second
   system block), so the cached prefix stays byte-stable. Cost: ~40 uncached tokens a
   send.

Non-chat models (TTS / image / video) never carry it: ``strip_chat_decorations`` turns
``SystemInstruction.include_identity`` off and the capability gate clears the slot
(``unified_client._strip_chat_decorations_if_non_fc``). Realtime voice sessions append
the SAME rendered block to the session instructions on the server
(``aidream/services/ai_execution/realtime_session.py``); the browser never holds the
words.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from matrx_utils import vcprint

#: The turn-context slot the part rides in.
IDENTITY_SLOT = "agent_identity"

#: The organization knobs the host resolves (``platform.feature_knob``).
IDENTITY_KNOB_FEATURE = "agents.identity"
STATEMENT_KEY = "statement"
OWN_MODEL_KEY = "statement_own_model"
UNKNOWN_LAB_KEY = "statement_unknown_lab"
IDENTITY_KNOB_KEYS = (STATEMENT_KEY, OWN_MODEL_KEY, UNKNOWN_LAB_KEY)

#: The catalog's own provider name for the models we build (``ai.provider.name``).
OWN_MAKER = "AI Matrx"

IDENTITY_OPEN = '<agent_identity source="platform">'
IDENTITY_CLOSE = "</agent_identity>"

IdentityResolver = Callable[[str | None], Awaitable[dict[str, str]]]

_RESOLVER: IdentityResolver | None = None
_announced_unbound = False


def set_identity_statement_resolver(resolver: IdentityResolver | None) -> None:
    """Install the host's ``organization_id -> {key: text}`` reader (``None`` = standalone)."""
    global _RESOLVER, _announced_unbound
    _RESOLVER = resolver
    _announced_unbound = False


def model_lab(model_ref: str | None) -> str | None:
    """The catalog maker of ``model_ref``, or ``None`` when the catalog cannot say."""
    if not model_ref:
        return None
    from matrx_ai.catalog.manager import ai_catalog_manager

    return ai_catalog_manager.model_maker(str(model_ref))


def compose_identity(knobs: dict[str, str], lab: str | None, *, model_ref: str | None = None) -> str:
    """The framed part for ``lab`` from the knob texts (pure; raises on a missing knob)."""
    if lab and lab.strip().casefold() == OWN_MAKER.casefold():
        text = knobs[OWN_MODEL_KEY]
    elif lab and lab.strip():
        text = knobs[STATEMENT_KEY].replace("{lab}", lab.strip())
    else:
        vcprint(
            f"[agent_identity] the catalog names no maker for model {model_ref!r}; the agent "
            "names AI Matrx and no lab (fix the model's ai.model_definition.provider_id)",
            color="yellow",
        )
        text = knobs[UNKNOWN_LAB_KEY]
    text = (text or "").strip()
    if not text:
        raise ValueError("the agents.identity statement knob is empty")
    return f"{IDENTITY_OPEN}{text}{IDENTITY_CLOSE}"


async def render_identity(model_ref: str | None, organization_id: str | None) -> str | None:
    """THE ONE RENDERER — the framed identity part for the model about to answer.

    ``None`` when no host resolver is bound (announced once). A resolver failure raises
    to the caller, which announces it and sends without the part."""
    global _announced_unbound
    if _RESOLVER is None:
        if not _announced_unbound:
            _announced_unbound = True
            vcprint(
                "[agent_identity] no host resolver bound for 'agents.identity'; agents are "
                "not told who made them (bind one with set_identity_statement_resolver())",
                color="yellow",
            )
        return None
    knobs = await _RESOLVER(str(organization_id) if organization_id else None)
    return compose_identity(knobs, model_lab(model_ref), model_ref=model_ref)


__all__ = [
    "IDENTITY_CLOSE",
    "IDENTITY_KNOB_FEATURE",
    "IDENTITY_KNOB_KEYS",
    "IDENTITY_OPEN",
    "IDENTITY_SLOT",
    "OWN_MAKER",
    "compose_identity",
    "model_lab",
    "render_identity",
    "set_identity_statement_resolver",
]
