from __future__ import annotations

import logging
from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.paths import resolve_path
from matrx_graph.nodes._sandbox import safe_eval
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras

logger = logging.getLogger(__name__)

# The surface workflow render components are authored/resolved against. A CAPS
# constant, not an env var — it is part of the product, not per-environment.
WORKFLOW_RENDER_SURFACE = "matrx-user/workflow"

EmitMode = Literal["confirmation", "summary", "full", "restructured"]

# HOW the emission is shown, orthogonal to ``mode`` (WHAT is sent):
#   panel    — the step's normal window panel (the default; nothing changes).
#   showcase — a dedicated, large, page-centered presentation that renders
#              ONLY this payload — as its kind component when the value is a
#              ``__kind`` instance. The author's "present this to the user"
#              choice: a workflow's final deliverable, a mid-run reveal.
EmitPresentation = Literal["panel", "showcase"]


class ToFrontendInput(BaseModel):
    model_config = ConfigDict(extra="allow")


class ToFrontendOutput(BaseModel):
    # Pass-through: whatever came in flows out unchanged, so an emit node placed
    # mid-chain (or inserted on an edge) never alters routing.
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": "authored passthrough — the incoming payload flows out unchanged"
        },
    )


class ToFrontendConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mode: EmitMode = Field(
        default="full",
        description=(
            "What to send: 'confirmation' (a short line), 'summary' or "
            "'restructured' (a custom shape via transform_expression), or "
            "'full' (the whole incoming payload)."
        ),
        json_schema_extra=field_extras(widget="select", help="How much to send back"),
    )
    message: str = Field(
        default="",
        description="The line shown for mode='confirmation'.",
        json_schema_extra=field_extras(widget="text", placeholder="Your notes are ready"),
    )
    transform_expression: str | None = Field(
        default=None,
        description=(
            "For 'summary'/'restructured': a sandboxed Python expression over "
            "the incoming payload (`inputs`). Result is what gets sent."
        ),
        json_schema_extra=field_extras(
            widget="code",
            code_language="python",
            placeholder="{'title': inputs['title'], 'first': inputs['items'][0]}",
            help="Safe expression (literals, subscripts, math — no function calls) returning the shape to send",
        ),
    )
    component_ref: str | None = Field(
        default=None,
        description=(
            "Name (tool_ui.tool_name) of a custom render component for this "
            "output. Leave empty to use the generic viewer."
        ),
    )
    surface: str = Field(
        default=WORKFLOW_RENDER_SURFACE,
        description="The ui_surface the component is resolved against.",
        json_schema_extra=field_extras(hidden=True),
    )
    title: str | None = Field(
        default=None, description="Human label for this output on the screen."
    )
    presentation: EmitPresentation = Field(
        default="panel",
        description=(
            "How to show it: 'panel' (the step's normal window panel) or "
            "'showcase' (a large, centered presentation of just this result — "
            "rendered as its kind component when the value is a kind instance)."
        ),
        json_schema_extra=field_extras(
            widget="select",
            help="Pick 'showcase' for the result you want the user to SEE — the finale, a reveal",
        ),
    )
    payload_key: str | None = Field(
        default=None,
        description=(
            "Which incoming key holds the data to send; empty = the whole "
            "payload. A dotted path reaches inside ('report.structured_output')."
        ),
        json_schema_extra=field_extras(placeholder="result.structured_output"),
    )


class ToFrontendExecutor:
    """Send data back to the screen mid-run, without stopping the workflow.

    The emit is a non-blocking side-channel: it fires a ``node_emitted`` event
    (recorded in wf_node_events so a re-opened run re-renders it) and the run
    continues immediately. Emission failures are swallowed with a log — they
    are NEVER load-bearing, exactly like ``ctx.progress``. The node passes its
    input through unchanged so it can sit on any edge without altering routing.

    ``config.presentation`` picks the surface: ``panel`` (the step's normal
    window panel) or ``showcase`` (a dedicated large, centered presentation
    that renders only this payload — its kind component when ``__kind``-marked).
    """

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="output.to_frontend",
        category=NodeCategory.IO,
        display_name="Show on Screen",
        description="Show data on the screen mid-run, then keep going.",
        input_schema=ToFrontendInput,
        output_schema=ToFrontendOutput,
        config_schema=ToFrontendConfig,
        # Round-1 F7: 'json' is a FORMAT word, not an identity — declaring
        # it masked the payload's real kind and settlement would stamp
        # __kind:'json' into business data. Undeclared, this pass-through
        # settles with the kind of what actually flowed (runtime
        # propagation), which is the honest answer.
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        # PASS-THROUGH BY DESIGN — an emit step never alters routing; what
        # came in flows out. Declared dynamic (GAP 2, §10g) so runtime
        # __kind propagation is the honest answer instead of a NULL that
        # reads as "undeclared".
        dynamic_output=True,
        determinism=ActionTier.SIDE_EFFECT,
        emits_stream=True,
        icon="monitor-up",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: ToFrontendInput,
        config: ToFrontendConfig,
    ) -> NodeResult[ToFrontendOutput]:
        payload = inputs.model_dump(mode="json")
        data = _pick(payload, config.payload_key) if config.payload_key else payload
        emitted = self._shape(config, payload, data)

        # Fire-and-forget. NEVER load-bearing — a lost emit must not affect the
        # run. (Same contract as ctx.progress.)
        try:
            from matrx_graph.types.events import NodeEmittedEvent

            kind, kind_ok, ir_metadata = await _verify_emitted_kind(emitted)
            empty_values, empty_notice = _empty_verdict(emitted, config.title)
            await ctx.emitter.send_data(
                NodeEmittedEvent(
                    run_id=ctx.run_id,
                    step=ctx.step,
                    node_id=ctx.node_id,
                    dispatch_id=ctx.dispatch_id,
                    item_index=ctx.item_index,
                    attempt=ctx.attempt,
                    mode=config.mode,
                    payload=emitted,
                    component_ref=config.component_ref or None,
                    surface=config.surface,
                    title=config.title,
                    presentation=config.presentation,
                    kind=kind,
                    kind_ok=kind_ok,
                    metadata=ir_metadata,
                    empty_values=list(empty_values),
                    empty_notice=empty_notice,
                )
            )
            if empty_notice:
                logger.warning(
                    "to_frontend is presenting an EMPTY value (run=%s node=%s): %s",
                    ctx.run_id[:8],
                    ctx.node_id,
                    empty_notice,
                )
        except Exception:  # noqa: BLE001 — emit is best-effort
            logger.warning(
                "to_frontend emit failed (run=%s node=%s) — UI update lost",
                ctx.run_id[:8],
                ctx.node_id,
                exc_info=True,
            )

        # Pass the original payload through unchanged so routing is unaffected.
        return success(ToFrontendOutput(**payload))

    @staticmethod
    def _shape(config: ToFrontendConfig, payload: dict[str, Any], data: Any) -> Any:
        if config.mode == "confirmation":
            return {"message": config.message or "Done"}
        if config.mode in ("summary", "restructured") and config.transform_expression:
            result = safe_eval(config.transform_expression, payload)
            return result if isinstance(result, dict) else {"value": result}
        # 'full' (and summary/restructured with no expression) → the data as-is.
        if isinstance(data, dict):
            return data
        return {"value": data}


def _empty_verdict(
    emitted: dict[str, Any], title: str | None
) -> tuple[tuple[str, ...], str | None]:
    """What in this emission is a hollow shell, and the sentence that says so.

    THE DEFECT THIS CLOSES (Expert Book Challenge wall W59, 2026-09-12): run
    ``9347de24…`` presented ``the_regimen`` as
    ``{"instructions": [], "headline_finding": "", …}`` — schema-valid, wholly
    empty — beside a full letter, as the finished answer to a parent. The
    emission is never blocked (an emit is not load-bearing and a partial
    answer is still worth showing), but it must arrive NAMED: a presenter that
    knows which values are empty can say "this part came back with nothing"
    instead of rendering a blank panel as a completed result.

    Never raises: a verdict is a view, and a workflow must not lose its
    emission over one.
    """
    try:
        from matrx_graph.emptiness import empty_structured_output, zero_valued_keys

        keys = zero_valued_keys(emitted)
        if keys:
            label = f"'{title}' " if title else ""
            listed = ", ".join(keys)
            return keys, (
                f"This result {label}came back with nothing in it: "
                f"{listed} {'is' if len(keys) == 1 else 'are'} empty. "
                "It is shown as it arrived, not as a completed answer."
            )
        if empty_structured_output(emitted) is not None:
            label = f"'{title}' " if title else ""
            return (), (
                f"This result {label}came back completely empty. "
                "It is shown as it arrived, not as a completed answer."
            )
    except Exception:  # noqa: BLE001 — a verdict is never load-bearing
        logger.warning("to_frontend empty verdict failed — emission ships unmarked", exc_info=True)
    return (), None


async def _verify_emitted_kind(
    emitted: dict[str, Any],
) -> tuple[str | None, bool | None, dict[str, Any] | None]:
    """The emission's kind verdict — the SAME hand-off ``node_completed`` makes.

    A payload SAYS what it is (``__kind``); the registry decides whether that
    is true. A verified pass ships the canonical Content IR envelope at
    ``metadata.__ir`` (wire-elided: the payload already rides ``payload``) so
    the screen renders the real kind component without re-parsing — the
    difference between a showcase and a JSON dump. Drift, an unregistered
    slug, or a degraded check → neutral (``kind_ok`` False/None, no envelope);
    the consumer classifies on its own. Never load-bearing: any failure here
    returns neutral and the emission still ships.
    """
    try:
        from matrx_graph.content_ir.model import kind_of

        kind = kind_of(emitted)
        if kind is None or kind == "json":
            return None, None, None
        from matrx_graph.kinds import check_against_kind

        check = await check_against_kind(emitted, kind)
        if not check.checked:
            return kind, None, None
        if check.errors:
            return kind, False, None
        from matrx_graph.content_ir.envelope import ir_metadata_for_verified_output

        return kind, True, ir_metadata_for_verified_output(emitted, kind)
    except Exception:  # noqa: BLE001 — a verdict is never load-bearing
        logger.warning("to_frontend kind verdict failed — emission ships neutral", exc_info=True)
        return None, None, None


def _pick(payload: dict[str, Any], key: str) -> Any:
    """Resolve ``payload_key``: an exact top-level key first (keys may contain
    dots), else the path walked by THE ONE resolver (``matrx_graph.paths`` —
    the same one edge mappings use, so a path that works here works there);
    missing → None."""
    if key in payload:
        return payload[key]
    found, value = resolve_path(payload, key)
    return value if found else None
