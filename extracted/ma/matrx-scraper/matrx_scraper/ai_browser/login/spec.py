"""The ONE-CALL Attempt specification — the agent states the whole login in one call.

D-11: *"The agent needs to really tell us exactly what to do so we can do it with
ease… making sure we have all the fields that we need."* A partial specification is
a schema defect, not a caller mistake — a page left with a username typed and no
password is a WORSE state than an untouched page, because the site may count the
partial attempt. So the spec is validated in full and the whole attempt is REFUSED
before a single field is touched when it cannot be completed.

Everything here is pure Pydantic + validation logic — no I/O, no DB, no worker — so
the refusal-before-touch guarantee is exhaustively testable against synthetic pages.

🚨 A field names EITHER a ``field_key`` (a vault secret, resolved server-side and
never seen by the agent) OR a ``literal`` (a value the agent legitimately knows,
e.g. an AWS region). Never both, and a ``literal`` may never be a secret — the tool
cannot check that, so the contract states it and the audit records that a literal
was used.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

# The submit kinds a single step may declare. ``none`` is legal and is how a
# deliberately-paused fill is expressed (e.g. hand over for MFA immediately); it is
# never the default.
SubmitKind = Literal["click", "press_enter", "none"]


class FieldSpec(BaseModel):
    """One field of the attempt: a selector that receives either a named vault
    secret (``field_key``) or an agent-supplied literal (``literal``)."""

    model_config = ConfigDict(extra="forbid")

    selector: str = Field(min_length=1)
    field_key: str | None = None
    literal: str | None = None
    clear_first: bool = True

    @model_validator(mode="after")
    def _exactly_one_source(self) -> "FieldSpec":
        has_key = self.field_key is not None and self.field_key != ""
        has_literal = self.literal is not None
        if has_key and has_literal:
            raise ValueError(
                f"field {self.selector!r} names both a field_key and a literal — "
                "a field is either a vault secret OR an agent-known literal, never both"
            )
        if not has_key and not has_literal:
            raise ValueError(f"field {self.selector!r} names neither a field_key nor a literal")
        return self

    @property
    def is_secret(self) -> bool:
        return self.field_key is not None and self.field_key != ""


class SubmitSpec(BaseModel):
    """The submit action for a step. Exactly one kind."""

    model_config = ConfigDict(extra="forbid")

    kind: SubmitKind = "click"
    selector: str | None = None

    @model_validator(mode="after")
    def _selector_required_for_targeted(self) -> "SubmitSpec":
        if self.kind in ("click", "press_enter") and not self.selector:
            raise ValueError(f"submit kind {self.kind!r} requires a selector")
        return self


class WaitForSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    selector: str = Field(min_length=1)
    timeout_ms: int = Field(default=15_000, ge=100, le=120_000)


class StepSpec(BaseModel):
    """One step of a multi-step flow. Its ``fields`` are selector references into
    the top-level ``fields`` list — a two-step flow is ONE call, not two."""

    model_config = ConfigDict(extra="forbid")

    fields: list[str] = Field(min_length=1)  # selectors, referencing AttemptSpec.fields
    submit: SubmitSpec = Field(default_factory=SubmitSpec)
    wait_for: WaitForSpec | None = None


class ExpectSpec(BaseModel):
    """What the agent expects after submit. A HINT that feeds verification as
    agent-supplied signals — never proof, never a short-circuit (D-12)."""

    model_config = ConfigDict(extra="forbid")

    success_url_prefix: str | None = None
    success_selector: str | None = None
    failure_selector: str | None = None
    challenge_selector: str | None = None
    timeout_ms: int = Field(default=30_000, ge=100, le=120_000)


class AttemptSpec(BaseModel):
    """The complete login specification — the ``Attempt`` arm of the credential_login
    discriminated union."""

    model_config = ConfigDict(extra="forbid")

    credential_item_id: str | None = None
    run_id: str | None = None
    fields: list[FieldSpec] = Field(default_factory=list)
    submit: SubmitSpec | None = None
    steps: list[StepSpec] | None = None
    expect: ExpectSpec = Field(default_factory=ExpectSpec)
    reason: str | None = None

    @model_validator(mode="after")
    def _fields_xor_steps(self) -> "AttemptSpec":
        if self.steps is not None and self.steps:
            if self.submit is not None:
                raise ValueError(
                    "a multi-step attempt uses `steps`; the top-level `submit` is "
                    "declared per-step and must be omitted"
                )
        else:
            if not self.fields:
                raise ValueError("an attempt must declare at least one field")
            if self.submit is None:
                raise ValueError("a single-step attempt requires a `submit` action")
        return self

    @property
    def field_keys(self) -> list[str]:
        """The distinct vault secret keys this attempt needs, sorted. Literals are
        excluded — they are agent-known, never resolved from the vault."""
        keys = {f.field_key for f in self.fields if f.is_secret and f.field_key}
        return sorted(keys)

    def field_by_selector(self, selector: str) -> FieldSpec | None:
        for f in self.fields:
            if f.selector == selector:
                return f
        return None

    def ordered_fill_plan(self) -> list[tuple[FieldSpec, SubmitSpec | None, WaitForSpec | None]]:
        """Flatten the attempt into an ordered list of (field, submit_after, wait).

        Single-step: every field, then the one submit on the last field.
        Multi-step: each step's referenced fields, then that step's submit + wait.
        The submit rides the LAST field of its group so the executor performs it
        exactly once, in order, and never fires a submit against an empty step.
        """
        plan: list[tuple[FieldSpec, SubmitSpec | None, WaitForSpec | None]] = []
        if self.steps:
            for step in self.steps:
                step_fields = [self.field_by_selector(sel) for sel in step.fields]
                missing = [sel for sel, fld in zip(step.fields, step_fields) if fld is None]
                if missing:
                    raise SpecIncompleteError(
                        missing_fields=missing,
                        detail=(
                            "step references selector(s) not declared in `fields`: "
                            + ", ".join(missing)
                        ),
                    )
                for idx, fld in enumerate(step_fields):
                    assert fld is not None  # guarded above
                    last = idx == len(step_fields) - 1
                    plan.append(
                        (fld, step.submit if last else None, step.wait_for if last else None)
                    )
        else:
            assert self.submit is not None  # guarded by _fields_xor_steps
            for idx, fld in enumerate(self.fields):
                last = idx == len(self.fields) - 1
                plan.append((fld, self.submit if last else None, None))
        return plan


class SpecIncompleteError(ValueError):
    """The attempt cannot be completed as written — a named field is unknown to the
    vault, sealed, or inactive, or a step references an undeclared selector. Raised
    BEFORE the page is touched; the caller returns a ``spec_incomplete`` refusal and
    NOTHING is typed."""

    def __init__(self, *, missing_fields: list[str], detail: str) -> None:
        self.missing_fields = missing_fields
        self.detail = detail
        super().__init__(detail)


__all__ = [
    "AttemptSpec",
    "ExpectSpec",
    "FieldSpec",
    "SpecIncompleteError",
    "StepSpec",
    "SubmitKind",
    "SubmitSpec",
    "WaitForSpec",
]
