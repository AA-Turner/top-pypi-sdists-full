from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, Field, RootModel, field_validator

from matrx_ai.tools.arg_models._coercion import (
    coerce_object as _coerce_object_field,
)
from matrx_ai.tools.arg_models._coercion import (
    coerce_rows as _coerce_rows_field,
)
from matrx_ai.tools.declared import ToolArgs

# Fuzzy JSON-string → container coercion lives in the shared `_coercion` module
# so every tool's arg models share one implementation. See its docstring for the
# rationale (the 2026-05-25 SQL-tool stringify-loop incident).


class DbQueryArgs(BaseModel):
    table: str
    match: dict[str, Any] = Field(default_factory=dict)
    fields: list[str] = Field(default_factory=lambda: ["*"])
    order_by: list[str] = Field(default_factory=list)
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)


# Response verbosity for write actions. "full" (default) echoes the affected
# row(s); "minimal" returns only the generated id(s) — used to keep large rows
# (e.g. ai_model with big jsonb columns) out of the model context.
Returning = Literal["minimal", "full"]


class DbInsertArgs(BaseModel):
    table: str
    data: dict[str, Any] | list[dict[str, Any]]
    returning: Returning = "full"

    @field_validator("data", mode="before")
    @classmethod
    def _coerce_data(cls, v: Any) -> Any:
        return _coerce_rows_field(v, field="data")


class DbUpdateArgs(BaseModel):
    table: str
    data: dict[str, Any]
    match: dict[str, Any]
    returning: Returning = "full"

    @field_validator("data", mode="before")
    @classmethod
    def _coerce_data(cls, v: Any) -> Any:
        return _coerce_object_field(v, field="data", purpose="columns to set")

    @field_validator("match", mode="before")
    @classmethod
    def _coerce_match(cls, v: Any) -> Any:
        return _coerce_object_field(v, field="match", purpose="column=value WHERE filters")


class DbSchemaArgs(BaseModel):
    table: str = ""


# ── Per-action wire contract for the `sql` dispatcher ───────────────────────
# The models the executor validates each incoming `sql` call against, assembled
# into the discriminated-union RootModel `SqlArgs` registered with @tool. Field
# sets == tool_def.parameters "$variants". The plain Db*Args models above stay as
# inner worker-arg models. Descriptions live only in the DB (Rule 4). The same
# JSON-string coercion is applied here so the fuzzy acceptance happens at the
# executor's pre-dispatch validation boundary (the first gate a call hits).


class SqlQueryWire(ToolArgs):
    action: Literal["query"]
    table: str
    match: dict[str, Any] = Field(default_factory=dict)
    fields: list[str] = Field(default_factory=lambda: ["*"])
    order_by: list[str] = Field(default_factory=list)
    limit: int = Field(default=100, ge=1, le=1000)
    offset: int = Field(default=0, ge=0)


class SqlInsertWire(ToolArgs):
    action: Literal["insert"]
    table: str
    data: dict[str, Any] | list[dict[str, Any]]
    returning: Returning = "full"

    @field_validator("data", mode="before")
    @classmethod
    def _coerce_data(cls, v: Any) -> Any:
        return _coerce_rows_field(v, field="data")


class SqlUpdateWire(ToolArgs):
    action: Literal["update"]
    table: str
    data: dict[str, Any]
    match: dict[str, Any]
    returning: Returning = "full"

    @field_validator("data", mode="before")
    @classmethod
    def _coerce_data(cls, v: Any) -> Any:
        return _coerce_object_field(v, field="data", purpose="columns to set")

    @field_validator("match", mode="before")
    @classmethod
    def _coerce_match(cls, v: Any) -> Any:
        return _coerce_object_field(v, field="match", purpose="column=value WHERE filters")


class SqlDeleteWire(ToolArgs):
    action: Literal["delete"]
    table: str
    match: dict[str, Any]

    @field_validator("match", mode="before")
    @classmethod
    def _coerce_match(cls, v: Any) -> Any:
        return _coerce_object_field(v, field="match", purpose="column=value WHERE filters")


class SqlUpsertWire(ToolArgs):
    action: Literal["upsert"]
    table: str
    # object OR array-of-objects (same shape as insert) — canonicalises to
    # "object", matching tool_def.parameters.$variants.upsert.data.type. Was `Any`,
    # which canonicalises to "any" and drifted against the DB's type=object.
    data: dict[str, Any] | list[dict[str, Any]]
    on_conflict: str | None = None
    returning: Returning = "full"

    @field_validator("data", mode="before")
    @classmethod
    def _coerce_data(cls, v: Any) -> Any:
        return _coerce_rows_field(v, field="data")


class SqlSchemaWire(ToolArgs):
    action: Literal["schema"]
    table: str = ""


class SqlArgs(
    RootModel[
        Annotated[
            SqlQueryWire
            | SqlInsertWire
            | SqlUpdateWire
            | SqlDeleteWire
            | SqlUpsertWire
            | SqlSchemaWire,
            Field(discriminator="action"),
        ]
    ]
):
    pass
