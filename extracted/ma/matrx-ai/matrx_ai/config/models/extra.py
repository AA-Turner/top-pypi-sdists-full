"""Pydantic twins for the remaining pure-data contract types (Phase 1b.2).

Shadowed, not swapped. Retirement Ledger row 7.

Four types that are genuinely data bags: the three `extra_config` content blocks
and `ProviderCharge`. Their methods are pure serializers (`to_google`,
`to_openai`, `to_storage_dict`) or a single combinator, so nothing behavioural
has to move with the fields.

The other three siblings are NOT here, deliberately — `MessageList`,
`SystemInstruction` and `TokenUsage` each carry behaviour or state that makes a
mechanical field-for-field port the wrong move. The analysis and the
recommendation for each is in PLAN.md; converting them without deciding what
they ARE would be the kind of "looks like progress" step this campaign keeps
catching.

CORPUS NOTES. `code_exec` and `code_result` have ZERO stored blocks — their
round-trip was repaired earlier today (metadata was dropped on persist) while it
was still latent. `web_search` has 18, all storing `{id, status, type,
metadata:{action}}`. `ProviderCharge` is not persisted as a block at all; it
hangs off `TokenUsage.provider_charge` and reaches storage inside the usage
record.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

_BLOCK = ConfigDict(extra="forbid", validate_assignment=False, arbitrary_types_allowed=True)


class CodeExecutionContentModel(BaseModel):
    model_config = _BLOCK

    type: Literal["code_execution"] = "code_execution"
    code: str = ""
    language: str = "python"
    metadata: dict[str, Any] = Field(default_factory=dict)


class CodeExecutionResultContentModel(BaseModel):
    model_config = _BLOCK

    type: Literal["code_execution_result"] = "code_execution_result"
    outcome: str = "success"
    output: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)


class WebSearchCallContentModel(BaseModel):
    model_config = _BLOCK

    type: Literal["web_search_call"] = "web_search_call"
    id: str = ""
    status: str = ""
    action: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ProviderChargeModel(BaseModel):
    """Independent reconciliation evidence for a provider's own stated charge.

    The first contract type met so far with REQUIRED fields — four of them. Every
    other twin in this migration is all-defaults, which is why every previous
    schema test asserted `"required" not in schema`; here it is present and that
    is correct.
    """

    model_config = _BLOCK

    amount_usd: float
    # int | float | str, in that order, because the provider's own raw value is
    # whatever the provider sent — xAI's integer USD ticks, a float, or a
    # decimal string. Pydantic's smart mode preserves the input type here rather
    # than coercing to the first member.
    raw_amount: int | float | str
    raw_unit: str
    field_path: str
    source: str = "response"
    currency: str = "USD"
    is_final: bool = True
