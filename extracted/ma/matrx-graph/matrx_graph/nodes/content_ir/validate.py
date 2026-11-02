"""``content_ir.validate`` — does this value actually match the Shape it claims?

ARMAN, 2026-08-23, on the Agent Foundry failure this closes:

    "if we're building things correctly, it would be impossible for that to
     happen. Because after all, we're talking about schemas and code. So,
     surely, if you had someone create a schema, you then have a validation
     node where whoever is creating the example puts the example through the
     validation, and we confirm that it works."

There was no such node. A workflow could DECLARE a kind on a step and the
scheduler would check the step's own output against it — but a workflow could
not ASK the question about an arbitrary value, mid-run, and act on the answer.
So the Foundry handed two Component Artisans a kind whose canonical example
contradicted its own schema, and the only thing that noticed was the agents.

WHAT THIS IS, DELIBERATELY
--------------------------
A general question — *"is this value a valid instance of kind X?"* — not a
Foundry step. Anything can ask it: before feeding an agent, after parsing a
file, at the top of a branch, when accepting a webhook. The Foundry is its
first caller, not its purpose.

IT IS NOT A SECOND VALIDATOR. Every verdict comes from
``matrx_graph.kinds.check_against_kind`` — the same funnel the scheduler's own
input gate and output drift-check use. A workflow asking the question must get
the same answer the engine would, or the two become independently wrong.

A SKIPPED CHECK IS NEVER A PASS
-------------------------------
``check_against_kind`` distinguishes "validated and clean" from "could not
validate" (unregistered slug, missing schema, unreachable catalog). That
distinction survives into the result as ``checked`` beside ``valid``, because
collapsing them is precisely how 555 of 555 canonical examples came to read as
passing while 506 of them had never been judged against the schema they were
being cited for.

FAILING IS NOT AN ERROR — BY DEFAULT
------------------------------------
The node answers the question and lets the workflow decide: branch on
``valid``, record the reasons with ``log.record``, repair, retry. That is the
whole point of asking. ``fail_run_when_invalid`` is there for the author who
means "this must never happen" — an explicit choice, never the default,
because a validation step that kills the run cannot be used to RECOVER from
the thing it found.
"""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras

#: Reported verbatim rather than summarized — a validator that says "3 errors"
#: sends a human back to the raw payload, which is where they were already
#: stuck. Capped so one deeply wrong value cannot fill a checkpoint.
MAX_REPORTED_ERRORS = 25


class ValidateKindInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: str = Field(
        default="",
        min_length=0,
        description=(
            "The registered Shape to check against. Leave empty to use the "
            "value's own `__kind` — the honest default, since a payload that "
            "declares its identity is asking to be judged by it."
        ),
        json_schema_extra=field_extras(widget="text", placeholder="blog_post_outline"),
    )
    value: JsonValue = Field(
        default=None,
        description="The value to check.",
        json_schema_extra=field_extras(widget="json"),
    )


class ValidateKindConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: str = Field(
        default="",
        description="Author-time Shape, used when the step is not given one at run time.",
        json_schema_extra=field_extras(widget="text"),
    )
    fail_run_when_invalid: bool = Field(
        default=False,
        description=(
            "Stop the workflow when the value does not match. OFF by default: "
            "the reason to ask is usually to handle the answer — branch, record "
            "it, repair, retry. Turn this on only for 'this must never happen'."
        ),
        json_schema_extra=field_extras(widget="toggle"),
    )


class KindValidationResult(BaseModel):
    """Mirrored by the registered ``kind_validation_result`` kind."""

    model_config = ConfigDict(extra="forbid")

    valid: bool = Field(
        description=(
            "True only when the value WAS checked and matched. Never true for "
            "a check that could not run — read `checked` for that."
        )
    )
    checked: bool = Field(
        description=(
            "Did validation actually happen? False means the Shape is "
            "unregistered, has no schema, or the catalog was unreachable — a "
            "platform gap, not a verdict about the value."
        )
    )
    kind: str = ""
    error_count: int = 0
    errors: list[str] = []
    #: Named reason the check was skipped (`kind_not_registered`,
    #: `schema_unavailable`, `catalog_unreachable`), never invented.
    degraded_reason: str | None = None
    kind_version: int | None = None
    kind_active: bool | None = None
    #: Plain-language line, safe to put straight into a `log.record` message.
    summary: str = ""


def _summarise(kind: str, checked: bool, errors: list[str], degraded: str | None) -> str:
    if not checked:
        return (
            f"Could not check against '{kind}': {degraded or 'unknown reason'}. "
            "That is a gap in the Shape registry, not a verdict about the value."
        )
    if not errors:
        return f"Valid instance of '{kind}'."
    head = "; ".join(errors[:3])
    more = f" (+{len(errors) - 3} more)" if len(errors) > 3 else ""
    return f"Not a valid '{kind}': {head}{more}"


class ValidateKindExecutor:
    """Ask the platform whether a value matches a Shape, and hand back the answer."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="content_ir.validate",
        category=NodeCategory.DATA,
        display_name="Check Shape",
        description=(
            "Check whether a value really matches a Shape, and carry on with "
            "the answer — so a workflow can fix or report a bad value instead "
            "of passing it along."
        ),
        input_schema=ValidateKindInput,
        output_schema=KindValidationResult,
        config_schema=ValidateKindConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.PURE,
        icon="shield-check",
        output_kind="kind_validation_result",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: ValidateKindInput,
        config: ValidateKindConfig,
    ) -> NodeResult[KindValidationResult]:
        from matrx_graph.content_ir.model import kind_of
        from matrx_graph.kinds import check_against_kind

        slug = (inputs.kind or config.kind or "").strip()
        if not slug:
            # A payload that declares its own identity is asking to be judged
            # by it; `kind_of` is the one reader of that marker.
            declared = kind_of(inputs.value) if isinstance(inputs.value, dict) else None
            slug = (declared or "").strip()
        if not slug or slug == "json":
            # 'json' is a format word, never an identity (the same refusal the
            # scheduler makes) — there is nothing to check against.
            return failure(
                code="validation",
                message=(
                    "No Shape to check against: name one on the step, or give a "
                    "value that declares its own `__kind`."
                ),
            )

        check = await check_against_kind(inputs.value, slug)
        errors = list(check.errors or [])[:MAX_REPORTED_ERRORS]
        degraded = check.degraded_reason.value if check.degraded_reason else None
        valid = bool(check.checked) and not check.errors
        summary = _summarise(slug, bool(check.checked), errors, degraded)

        result = KindValidationResult(
            valid=valid,
            checked=bool(check.checked),
            kind=slug,
            error_count=len(check.errors or []),
            errors=errors,
            degraded_reason=degraded,
            kind_version=check.kind_version,
            kind_active=getattr(check, "kind_active", None),
            summary=summary,
        )

        if config.fail_run_when_invalid and not valid:
            # The author asked for a hard stop. The failure carries the same
            # sentence the result would have, so the run's error is readable
            # without opening the step.
            return failure(
                code="kind_invalid",
                message=summary,
                details=result.model_dump(mode="json"),
            )
        return success(result)
