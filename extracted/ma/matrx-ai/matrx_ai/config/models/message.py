"""The pydantic UnifiedMessage — modelled on production data, not on the hints.

Corpus: 57,213 message objects inside ``chat.request_snapshot`` (Phase 1a).
Five of the nine declared fields ever appear on the wire; ``name``, ``status``,
``is_visible_to_model`` and ``position`` never serialize into ``config.messages``
(they are runtime/persistence concerns). They are kept — absence in the corpus is
not proof a field is dead (`unfinished-work-alarm.md`) — but they are marked.

🚨 THE ONE TYPE CORRECTION — ``timestamp``
------------------------------------------
The dataclass declares ``timestamp: int | None``. Production has NEVER stored an
int there: **11,259 of 11,259 observed values are ISO-8601 strings**
(``2026-05-18T07:18:52.600691+00:00``, all exactly 32 chars, zero pure-digit
values). The writer is explicit about it —
``message_config.py::from_cx_message`` does
``timestamp=message.created_at.isoformat()``.

So the hint has been wrong for the life of the field, and a dataclass never
noticed. A literal port to ``int | None`` would raise ``ValidationError`` on
every message carrying a timestamp — a hard production failure on the first turn
after the flip, on 11,259 corpus cases. This model types it as the data actually
is and accepts the int form too, because nothing forbids a caller from setting
one and silently rejecting it would be the same class of mistake in reverse.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class UnifiedMessageModel(BaseModel):
    """Shadow twin of ``matrx_ai.config.message_config.UnifiedMessage``.

    Config choices are deliberately the LEAST surprising ones for step one —
    they reproduce dataclass behaviour exactly (CUTOVER.md §4):

    * ``extra="allow"`` — the dataclass filters unknown keys via
      ``_filter_kwargs`` rather than raising. Forbidding here would change
      behaviour before the shadow has proven anything. Tightening is its own
      later flip.
    * ``validate_assignment=False`` — dataclasses allow free mutation and the
      orchestrator mutates messages mid-loop.
    * ``arbitrary_types_allowed=True`` — ``content`` holds the existing
      ``UnifiedContent`` dataclasses; they are NOT converted here. Converting
      content is its own step, after this one is green.
    """

    model_config = ConfigDict(
        extra="allow",
        validate_assignment=False,
        arbitrary_types_allowed=True,
    )

    role: str
    content: list[Any] = Field(default_factory=list)

    # cx_message.id (UUID) ONLY — never a provider response id (those live on
    # TokenUsage.response_id; one stamped here became a cx_message PK and 500'd
    # the turn, 2026-07-02). Corpus: 19,273 occurrences, always a string.
    id: str | None = None

    # Corpus: never serialized. Kept, not deleted.
    name: str | None = None

    # 🚨 CORRECTED FROM `int | None` — see the module docstring. Corpus says
    # ISO-8601 string, 11,259/11,259. int stays accepted for any in-memory
    # caller that sets one.
    timestamp: str | int | None = None

    # Corpus: never serialized (runtime/persistence concern).
    status: str = "active"

    # False = persisted and shown to the user but NEVER replayed to the
    # provider. Corpus: never serialized; carried in-memory from
    # cx_message.is_visible_to_model.
    is_visible_to_model: bool = True

    metadata: dict[str, Any] = Field(default_factory=dict)

    # cx_message.position. Corpus: never serialized.
    position: int | None = None
