"""``data.assert`` — fail a run when a predicate is false.

A validation gate. Put this between two stages of a workflow to halt
execution when the upstream output violates an expected invariant. The
sandboxed predicate has access to `inputs` bound at the top level; raise
``ValueError`` on mismatch, which the scheduler surfaces as a normal
node failure.
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.nodes._sandbox import safe_eval
from matrx_graph.nodes._template import render_template_string
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras


class AssertInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class AssertConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    predicate: str = Field(
        min_length=1,
        description=(
            "Predicate expression over `inputs`. Must be truthy for the node "
            "to succeed. Example: ``inputs['count'] > 0``."
        ),
        json_schema_extra=field_extras(
            widget="code",
            code_language="python",
            placeholder="inputs['count'] > 0",
        ),
    )
    message: str = Field(
        default="Assertion failed",
        description=(
            "The sentence the person reads when the check fails. Values from this "
            "step's inputs fill ``{path}`` placeholders (the shared template language, "
            "e.g. ``{material.total_chars} characters read, {min_chars:n} needed``); "
            "``:n`` shows a number with thousands separators (1,000)."
        ),
    )


class AssertOutput(KindModel, kind="assertion_result"):
    passed: bool = Field(
        default=True,
        description="Always true when the node succeeds — a falsy predicate fails "
        "the run instead of returning false.",
    )
    inputs: dict[str, JsonValue] = Field(
        description="The inputs passed through unchanged, so downstream steps still receive them."
    )


class AssertExecutor:
    """Evaluate a predicate; raise ValueError on falsy result."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.assert",
        category=NodeCategory.DATA,
        display_name="Safety Check",
        description="Stop the run when a required condition is not met.",
        input_schema=AssertInput,
        output_schema=AssertOutput,
        config_schema=AssertConfig,
        output_kind="assertion_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="shield-check",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: AssertInput,
        config: AssertConfig,
    ) -> NodeResult[AssertOutput]:
        _ = ctx
        payload = inputs.model_dump(mode="json")
        if not safe_eval(config.predicate, payload):
            # Node Result System: a falsy predicate is a genuine node Failure
            # with a stable code (retry_on / ERROR edges can match it).
            # The person reads the author's sentence, filled from the inputs; the
            # predicate (code) is technical detail, never the sentence.
            message, _ = render_template_string(config.message, payload, whole_key="inputs")
            return failure(
                "assertion_failed",
                message,
                details={"predicate": config.predicate},
                technical=f"{message}: predicate={config.predicate!r}",
            )
        return success(AssertOutput(passed=True, inputs=payload))

