"""THE ONE UNSAVED RUN — every AI run is recorded like a chat, except the conversation labeler.

Owner ruling (Arman, 2026-10-23): "There is only ONE approved call that SHOULD NOT get saved
and that is the one which labels the conversations. That's it. All else must be treated like
any other run." A person may still choose an unsaved chat for themselves (the request's own
``store: false`` through the conversation gate, or a confidential/sealed turn) — that choice
arrives on the request context, never as a code argument.

So a MACHINE caller can no longer ask for ``store=False``: the code doors that accept it
(``execute_ai_request(store=False)``, ``run_agent(store=False)``) call
:func:`refuse_machine_unsaved_run`, which raises unless

* the call is held by :data:`UNSAVED_RUN_EXEMPTION` (the labeler's mandates), or
* nothing is sent at all — a provider-request capture (the model-view / dry-run preview),
  which stops at the transport and is not a run.

Static guard over every other spelling (``with_overrides(store=False)``,
``system_app_context(store=False)``, ``config.store = False``, ``"store": False``):
``scripts/check_no_machine_unsaved_runs.py`` (allowlist with a reason per lawful site).
"""

from __future__ import annotations

from typing import Any

from matrx_ai.code_call_mandate_keys import (
    CONVERSATION_LABEL_AGENT_RUN_MANDATE,
    CONVERSATION_LABEL_CHAT_MANDATE,
)

#: The ONE named exemption: the mandates that label conversations.
UNSAVED_RUN_EXEMPTION: frozenset[str] = frozenset(
    {CONVERSATION_LABEL_CHAT_MANDATE, CONVERSATION_LABEL_AGENT_RUN_MANDATE}
)


class MachineUnsavedRunRefused(ValueError):
    """A machine caller asked for an unsaved (``store=False``) run."""


def _key_of(mandate_key: Any, metadata: Any) -> str:
    if isinstance(mandate_key, str) and mandate_key:
        return mandate_key
    if isinstance(metadata, dict):
        return str(metadata.get("mandate_key") or "")
    return ""


def refuse_machine_unsaved_run(*, door: str, mandate_key: Any = None, metadata: Any = None) -> None:
    """Raise :class:`MachineUnsavedRunRefused` for a code-level ``store=False`` request."""
    from matrx_ai.providers.request_capture import is_capturing

    if is_capturing():
        return
    key = _key_of(mandate_key, metadata)
    if key in UNSAVED_RUN_EXEMPTION:
        return
    raise MachineUnsavedRunRefused(
        f"{door}(store=False) refused for {key or 'an unnamed caller'}: every run is recorded like "
        "a chat (owner ruling 2026-10-23). Run it as a saved system run (system_run=True); only the "
        f"conversation labeler ({', '.join(sorted(UNSAVED_RUN_EXEMPTION))}) and a person's own "
        "unsaved-chat choice stay unsaved."
    )
