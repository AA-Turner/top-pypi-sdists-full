"""Pydantic twin of ``UnifiedResponse`` (agent-engine-extraction, Phase 1b.2).

Shadowed, not swapped. ``config/unified_config.py::UnifiedResponse`` is still the
live dataclass; this model is built beside it and compared by
``config/_parity.py``. Retirement Ledger row 3 retires this beside-file the day
the dataclass is deleted.

WHAT THE CORPUS SAID (5,473 production rows in ``chat.request_snapshot``, the
persisted output of ``UnifiedResponse.to_dict()``):

  * FIVE structural cases, total. Every one is a subset of the six fields.
  * ``finish_reason`` is a JSON string whenever present — stop 3,383,
    tool_calls 1,831, max_tokens 14; absent 245. ZERO explicit JSON nulls.
  * ``stop_reason`` present in only 705/5,473 (12.9%) — stop 257,
    tool_calls 448. ZERO explicit JSON nulls.
  * ``metadata`` is ``{}`` in 5,473 of 5,473 rows. Declared, never populated.
  * ``messages`` is non-empty in 5,473 of 5,473 rows.
  * ``usage`` absent in 2 rows — the two times the red missing-usage warning
    actually fired in production.

Both "zero explicit nulls" facts are consequences of ``to_dict()`` DROPPING
None rather than emitting it. That is load-bearing, not incidental: absence IS
the encoding of None on this shape. ``to_dict`` below reproduces it exactly.

TWO FIELDS ARE DELIBERATELY UNTYPED, AND NOT OUT OF LAZINESS:

  * ``raw_response`` is DECLARED ``dict[str, Any] | None`` and that declaration
    is FALSE. ``from_openai`` takes an ``OpenAIResponse``; groq, cerebras and
    together take ``Any``; every one of them passes that SDK object straight
    through as ``raw_response``. Porting the declaration literally would make
    pydantic reject virtually every real provider response. (This is the same
    class of trap as ``UnifiedMessage.timestamp: int | None``, which the corpus
    showed to be an ISO-8601 string 11,259 times out of 11,259.)
  * ``usage`` holds a ``TokenUsage`` dataclass that has not been migrated yet —
    14 fields, a ``__post_init__``, and cost calculation that reads the pricing
    catalog. Narrowing it here would hard-fail every test that passes a stand-in.
    It gets its own phase and its own corpus pass.

``messages`` is ``list[Any]`` for the same staged reason: it carries
``UnifiedMessage`` dataclasses today and ``UnifiedMessageModel`` after that type
reaches S4. Narrowing any of the three is a separate, deliberate, corpus-backed
step — never a side effect of this file.
"""

from __future__ import annotations

from typing import Any

from matrx_utils import vcprint
from pydantic import BaseModel, ConfigDict, Field, model_validator


class UnifiedResponseModel(BaseModel):
    # extra="forbid" MATCHES the dataclass here, which is the opposite of the
    # call made for UnifiedMessage. A dataclass raises TypeError on an unknown
    # keyword, so the old shape already refuses extras; all 40 construction
    # sites pass literal keywords and nothing rebuilds this type from stored
    # data (there is no from_dict anywhere — it is forward-only, translator to
    # orchestrator). Forbidding is the faithful port, not a tightening.
    #
    # validate_assignment stays OFF because providers/anthropic/anthropic_api.py
    # assigns ``converted_response.usage`` after construction (lines 253, 311).
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=False,
        arbitrary_types_allowed=True,
    )

    # Field ORDER is part of the contract: to_dict() walks __dict__, so this
    # order is the key order of every persisted snapshot. Keep it aligned with
    # the dataclass.
    messages: list[Any]
    usage: Any = None
    stop_reason: str | None = None
    finish_reason: str | None = None
    raw_response: Any = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _warn_when_usage_is_missing(self) -> UnifiedResponseModel:
        # The dataclass's __post_init__, moved verbatim. It fired twice in the
        # production corpus; losing it would silence the only signal that a
        # paid call recorded no cost.
        if self.usage is None:
            vcprint(
                "⚠️  WARNING: UnifiedResponse missing usage data. This means costs cannot be calculated.",
                color="red",
                log_level="warning",
            )
        return self

    def to_dict(self) -> dict[str, Any]:
        # Byte-for-byte the dataclass's implementation, INCLUDING the quirk that
        # the list branch tests only value[0]: a list whose first element has no
        # to_dict passes through raw even if later elements have one. Faithful
        # first; fixing it is a separate decision with its own evidence.
        result: dict[str, Any] = {}

        for key, value in self.__dict__.items():
            if value is None:
                continue

            if isinstance(value, list) and value and hasattr(value[0], "to_dict"):
                result[key] = [item.to_dict() for item in value]
            elif hasattr(value, "to_dict"):
                result[key] = value.to_dict()
            else:
                result[key] = value

        return result
