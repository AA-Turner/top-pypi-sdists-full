"""Edited assistant answers — what the model sees on the next turn.

A person can edit an assistant answer in place (``cx_message_edit`` archives the
model's own output into ``content_history`` and stamps ``status='edited'``).
Whether the NEXT turn's history carries the edited text or the model's original
output is an organization decision (rich-content PLAN decision 13, ruled by
Arman): the ``agents.messages / edited_answer_visible_to_model`` knob, default
``true`` — the edit is the record.

The package cannot read the knob register (no DB reads of the host's registry
inside a package), so the HOST injects a per-organization resolver through
``matrx_ai.configure(edited_answer_visibility_resolver=...)`` (aidream:
``package_integration._edited_answer_visible_to_model``) — a per-call resolver,
never a boot-time scalar, because the answer differs per organization.

With no resolver installed (a standalone matrx-ai install), the platform default
applies: the edited text is what the model sees. A resolver that raises is
announced loudly and the default applies for that turn — never a silent guess.

This module carries NO ORM imports, so it is importable (and testable) without a
configured host.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any

from matrx_utils import vcprint

#: Mirrors the seeded knob default (aidream migration ai_093). The edit is the record.
DEFAULT_EDITED_ANSWER_VISIBLE_TO_MODEL = True

#: The knob address — the host resolves this row per organization.
EDITED_ANSWER_KNOB = ("agents.messages", "edited_answer_visible_to_model")

EditedAnswerVisibilityResolver = Callable[[str | None], Awaitable[bool]]


def set_edited_answer_visibility_resolver(
    resolver: EditedAnswerVisibilityResolver | None,
) -> None:
    """Install (or, with ``None``, remove) the resolver outside ``configure()``."""
    from matrx_ai import _ext

    if resolver is None:
        _ext._registry.pop(_ext._EDITED_ANSWER_VISIBILITY_RESOLVER_KEY, None)
    else:
        _ext.configure_ext(**{_ext._EDITED_ANSWER_VISIBILITY_RESOLVER_KEY: resolver})


async def edited_answer_visible_to_model(organization_id: str | None) -> bool:
    """Whether an edited assistant answer replays as edited for this organization."""
    from matrx_ai._ext import get_edited_answer_visibility_resolver

    resolver = get_edited_answer_visibility_resolver()
    if resolver is None:
        return DEFAULT_EDITED_ANSWER_VISIBLE_TO_MODEL
    try:
        return bool(await resolver(organization_id))
    except Exception as exc:  # noqa: BLE001 — announced; the ruled default applies
        vcprint(
            "[edited answers] agents.messages/edited_answer_visible_to_model could not be "
            f"resolved for organization {organization_id!r} ({exc!r}); replaying the EDITED "
            "text (the platform default). Fix the knob row or the resolver.",
            color="red",
        )
        return DEFAULT_EDITED_ANSWER_VISIBLE_TO_MODEL


def original_model_content(message: Any) -> Any | None:
    """The model's own output for an edited assistant row, or ``None``.

    ``cx_message_edit`` appends ``{content, saved_at}`` to ``content_history``
    on every save, so entry 0 is what the model originally produced. Returns
    ``None`` for any row that is not an edited assistant answer with a usable
    archive — the caller then replays the row as stored.
    """
    if getattr(message, "role", None) != "assistant":
        return None
    if getattr(message, "status", None) != "edited":
        return None
    history = getattr(message, "content_history", None)
    if not isinstance(history, list) or not history:
        return None
    first = history[0]
    if not isinstance(first, dict) or "content" not in first:
        return None
    return first["content"]
