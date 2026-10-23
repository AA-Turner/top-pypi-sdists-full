"""Typed shapes of the agent-test check language (Agent Evaluation CONTRACT v2 §2, §3.1).

Pure data: stdlib + pydantic only. Nothing here imports the fill or execution code —
the independence guard (aidream/services/agent_tests/tests/test_check_independence.py)
fails the build if it ever does.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue

Sink = Literal[
    "reply",
    "output",
    "request",
    "preview",
    "stored",
    "conversation",
    "tool_calls",
    "rows",
    "usage",
    "outcome",
    "door",
]
Op = Literal[
    "eq",
    "ne",
    "contains",
    "not_contains",
    "matches",
    "not_matches",
    "in",
    "routes_in",
    "not_leaks",
    "exists",
    "empty",
    "matches_schema",
    "conforms",
    "gte",
    "lte",
    "count",
    "same_across_doors",
]
OpKind = Literal["positive", "negative", "presence", "bound", "parity"]
OP_KIND: dict[str, OpKind] = {
    "eq": "positive",
    "contains": "positive",
    "matches": "positive",
    "in": "positive",
    "routes_in": "positive",
    "ne": "negative",
    "not_contains": "negative",
    "not_matches": "negative",
    "not_leaks": "negative",
    "exists": "presence",
    "empty": "presence",
    "matches_schema": "presence",
    "conforms": "presence",
    "gte": "bound",
    "lte": "bound",
    "count": "bound",
    "same_across_doors": "parity",
}
CheckOutcome = Literal["pass", "fail", "undecided", "not_applicable"]
Verdict = Literal["pass", "pass_judged", "fail", "fail_format", "inconclusive", "blocked", "error"]
OutcomeStatus = Literal[
    "completed", "refused_by_agent", "refused_by_platform", "refused_by_validation", "error"
]
At = Literal["seeded", "edited"]


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class Split(_Strict):
    sep: str
    index: int


class Modifiers(_Strict):
    """Applied in this order: split → match → trim → lower."""

    split: Split | None = None
    match: str | None = None
    trim: bool = False
    lower: bool = False


class Expected(Modifiers):
    from_: Literal["literal", "input", "marker", "pick_list", "prompt_block", "default", "observed", "run"] = Field(
        alias="from"
    )
    value: JsonValue = None
    path: str | None = None
    name: str | None = None
    var: str | None = None
    part: str | None = None
    at: At = "seeded"
    field: str | None = None
    # from = observed
    sink: Sink | None = None
    turn: int | None = None
    read: ReadSpec | None = None


class ReadSpec(Modifiers):
    path: str = ""
    field: str | None = None
    line: int | None = None
    final: int | None = None
    tool: str | None = None
    table: str | None = None
    where: dict[str, Expected | JsonValue] | None = None
    limit: int = Field(default=50, ge=1, le=200)


class Check(_Strict):
    id: str = Field(min_length=1)
    title: str = ""
    proves: str = ""
    turn: int | Literal["each"] | None = None
    sink: Sink
    read: ReadSpec = Field(default_factory=ReadSpec)
    op: Op
    expected: Expected | None = None
    count_op: Literal["eq", "gte", "lte"] | None = None
    ignore: list[str] = Field(default_factory=list)
    required: bool = True


class JudgeFact(_Strict):
    id: str
    statement: str
    expected: Expected | None = None
    turn: int | None = None


class FixtureTarget(_Strict):
    kind: Literal["pick_list_item", "agent_default", "prompt_block", "context_value"]
    list_id: str | None = None
    item_id: str | None = None
    var: str | None = None
    name: str | None = None


class FixtureEdit(_Strict):
    id: str
    target: FixtureTarget
    field: Literal["label", "description", "default", "content", "value"]
    value: JsonValue


class FixtureSpec(_Strict):
    target: FixtureTarget
    values: dict[str, JsonValue] = Field(default_factory=dict)


class TurnSpec(_Strict):
    user_text: str = ""
    context: dict[str, JsonValue] | None = None
    variable_edits: dict[str, JsonValue] = Field(default_factory=dict)
    fixture_edits: list[FixtureEdit] = Field(default_factory=list)


# ── Evidence: what the readers observed ──────────────────────────────────────


class RequestView(_Strict):
    system: str = ""
    user: list[str] = Field(default_factory=list)
    messages: list[dict[str, str]] = Field(default_factory=list)
    tools: list[str] = Field(default_factory=list)
    model: str | None = None


class ToolCall(_Strict):
    name: str
    args: dict[str, JsonValue] = Field(default_factory=dict)


class Outcome(_Strict):
    status: OutcomeStatus = "completed"
    error_code: str | None = None
    http_status: int | None = None
    message: str | None = None


class Usage(_Strict):
    cost_cents: Decimal | None = None
    tokens: int | None = None
    turns: int | None = None
    ttft_ms: int | None = None
    duration_ms: int | None = None


class TurnEvidence(_Strict):
    reply: str | None = None
    output: JsonValue = None
    request: RequestView | None = None
    preview: RequestView | None = None
    stored_user_message: str | None = None
    stored_messages: list[dict[str, str]] | None = None
    tool_calls: list[ToolCall] | None = None


class Evidence(_Strict):
    door: str | None = None
    turns: list[TurnEvidence] = Field(default_factory=list)
    conversation_variables: dict[str, JsonValue] | None = None
    usage: Usage | None = None
    outcome: Outcome | None = None
    #: key = engine.rows_key(table, resolved where)
    rows: dict[str, list[dict[str, JsonValue]]] = Field(default_factory=dict)


# ── Bindings: where expected values come from ────────────────────────────────


class PickListValue(_Strict):
    label: str = ""
    hidden_text: str = ""


class TurnBinding(_Strict):
    user_text: str = ""
    context: dict[str, JsonValue] = Field(default_factory=dict)
    variable_edits: dict[str, JsonValue] = Field(default_factory=dict)
    fixture_edits: dict[str, JsonValue] = Field(default_factory=dict)


class Bindings(_Strict):
    variables: dict[str, JsonValue] = Field(default_factory=dict)
    #: turns[0] is turn 1
    turns: list[TurnBinding] = Field(default_factory=list)
    markers: dict[str, str] = Field(default_factory=dict)
    run: dict[str, JsonValue] = Field(default_factory=dict)
    pick_lists: dict[str, dict[At, list[PickListValue]]] = Field(default_factory=dict)
    prompt_blocks: dict[str, dict[At, str]] = Field(default_factory=dict)
    defaults: dict[str, dict[At, JsonValue]] = Field(default_factory=dict)
    #: None = unknown (every variable treated as declared)
    declared_variables: list[str] | None = None


# ── Results ──────────────────────────────────────────────────────────────────


class CheckResult(_Strict):
    id: str
    title: str = ""
    proves: str = ""
    required: bool = True
    sink: str = ""
    outcome: CheckOutcome
    side: Literal["reply", "request", "other"] = "other"
    observed: JsonValue = None
    expected: JsonValue = None
    expected_source: str = ""
    reason: str = ""
    can_fail: bool | None = None
    mutation: str | None = None
    #: the value came from hidden text, a prompt block or a request sink
    sensitive: bool = False
    truncated: bool = False
    redacted: bool = False
    locator: dict[str, JsonValue] | None = None
    #: a structural failure (the answer is not the declared output): the verdict is ``fail_format``
    #: decided by code, and the judge is never paid for it
    format_failure: bool = False


class JudgeDecision(_Strict):
    verdict: Literal["holds", "violated", "format_only", "unanswerable", "judge_unfed"]
    advisory: bool = False
    fed_ok: bool = True
    verdict_id: str | None = None


class VerdictResult(_Strict):
    verdict: Verdict
    reason: str = ""
    counted: bool = False


class FailProof(_Strict):
    can_fail: bool
    mutation: str
    outcome_after: CheckOutcome


Expected.model_rebuild()
ReadSpec.model_rebuild()
Check.model_rebuild()
