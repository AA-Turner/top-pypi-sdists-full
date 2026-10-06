"""Canonical agent executor.

Single entry point for running an already-loaded ``Agent``. Wraps the call
in ``child_agent_context(label)`` so every caller gets the same lifecycle
guarantees (context fork, sub_agent init/completion events, reservation
tracker isolation, parent restoration on exit) without ever touching
``set_app_context`` / ``clear_app_context`` directly.

Replaces every hand-rolled ``_execute_agent`` / ``_run_agent`` helper
scattered across ``research/``, ``agent_runners/``, etc.

Usage::

    from matrx_ai.agents import Agent, run_agent

    agent = await Agent.from_agent("7e021d98-…", is_version=False)
    agent.set_variables(topic="AI Safety", page_content=text)

    result = await run_agent(
        agent,
        label="page_summary",
        source_app="matrx-ai",
        source_feature="page_summary",
    )
    if not result.success:
        ...  # result.error / result.error_kind
    text = result.output
    cost = result.usage["total"]["total_cost"]

    # With JSON extraction:
    class SuggestOutput(BaseModel):
        title: str
        suggested_keywords: list[str] = Field(default_factory=list)

    result = await run_agent(
        agent,
        label="suggest",
        source_app="matrx-ai",
        source_feature="suggest",
        json_schema=SuggestOutput,
    )
    if result.parsed is not None:
        title = result.parsed.title
    elif result.parse_error:
        # Raw output is still on result.output; the full unaltered model
        # response was already vcprint-ed in red by the executor.
        ...
"""

from __future__ import annotations

import asyncio
import json
import re
import uuid
from typing import Any, Generic, Literal, TypeVar

from matrx_connect.context.app_context import child_agent_context
from matrx_utils import vcprint
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from matrx_ai.agents.definition import Agent, AgentExecuteResult
from matrx_ai.agents.source_tracking import resolve_child_source
from matrx_ai.config.media_config import collect_media_refs
from matrx_ai.config.usage_config import AggregatedUsage, TokenUsage

ParsedT = TypeVar("ParsedT", bound=BaseModel)


# A cancellation can arrive after Agent.execute() returned but while the
# terminal runtime-spine write is being awaited. Keep that write alive outside
# the caller task: otherwise the already-open utility remains RUNNING until its
# lease expires and the reaper falsely reports it abandoned.
_SPINE_SETTLE_TASKS: set[asyncio.Task[Any]] = set()


def _is_uuid_text(value: object) -> bool:
    try:
        uuid.UUID(str(value))
    except (ValueError, TypeError, AttributeError):
        return False
    return bool(value)


def _discard_spine_settle(task: asyncio.Task[Any]) -> None:
    _SPINE_SETTLE_TASKS.discard(task)
    if task.cancelled():
        return
    try:
        task.exception()
    except Exception:
        pass


async def _settle_spine(
    settle: Any,
    status: str,
    *,
    error: str | None = None,
    meters: dict[str, Any] | None = None,
) -> None:
    """Await a terminal settle without letting caller cancellation cancel it."""
    task = asyncio.create_task(
        settle(status, error=error, meters=meters),
        name="internal_agent_run_spine_settle",
    )
    _SPINE_SETTLE_TASKS.add(task)
    task.add_done_callback(_discard_spine_settle)
    await asyncio.shield(task)


# What an early-ended run spent rides the exception out of ``run_agent`` so the
# caller that owns a spine record for it (agent-as-tool's child execution, a
# time-limited caller's own tally) can settle the real amount. The innermost
# ``run_agent`` the exception passes through is the caller's own run, so each
# one overwrites the stamp on the way out.
_RUN_USAGE_ATTR = "_matrx_agent_run_usage_history"


def run_usage_from_exception(exc: BaseException | None) -> list[TokenUsage]:
    """The usage an early-ended ``run_agent`` accumulated, read off the
    exception it raised — or off the cause/context chain, so a ``TimeoutError``
    that ``asyncio.wait_for`` / ``asyncio.timeout`` raised from the run's
    cancellation still yields it. Empty when nothing was billed."""
    seen: set[int] = set()
    while exc is not None and id(exc) not in seen:
        seen.add(id(exc))
        found = getattr(exc, _RUN_USAGE_ATTR, None)
        if found is not None:
            return list(found)
        exc = exc.__cause__ or exc.__context__
    return []


def _stamp_run_usage(exc: BaseException, history: list[TokenUsage]) -> None:
    try:
        setattr(exc, _RUN_USAGE_ATTR, list(history))
    except Exception:  # noqa: BLE001 — cost capture must never mask the real error
        pass


def _early_exit_meters(history: list[TokenUsage], *, label: str) -> dict[str, Any] | None:
    """Settle meters for a run that ended before ``Agent.execute`` returned —
    the same builder the success path uses, so an unpriced call still records
    the known subtotal plus ``unpriced_calls``, never a silent 0."""
    if not history:
        return None
    from matrx_ai.config.usage_config import cost_meters_from_totals

    return cost_meters_from_totals(TokenUsage.aggregate_by_model(history).total, label=label) or None

# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------


# "candidate_stopped": a mandate-candidate run ended at a contained call
# (matrx_ai.tools.candidate_containment) — not a crash, and never a success.
ErrorKind = Literal["execution", "parse", "candidate_stopped", None]


class AgentRunResult(BaseModel, Generic[ParsedT]):
    """Typed result of a single agent execution.

    ``success`` reflects whether the agent itself produced a response.
    JSON parse failures do NOT flip ``success`` — they populate
    ``parse_error`` / ``error_kind="parse"`` while still returning the raw
    text on ``output``. Callers that only care about the text never need
    to look at ``parsed``.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    success: bool
    output: str = ""
    usage: dict[str, Any] = Field(default_factory=dict)
    usage_aggregated: AggregatedUsage | None = None
    usage_history: list[TokenUsage] = Field(default_factory=list)
    model_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
    error_kind: ErrorKind = None
    # The exception that failed the run, traceback intact — so a caller that
    # turns this into a tool failure (agent_call) hands the operator the real
    # type, message and stack instead of a sentence. In memory only.
    exception: BaseException | None = Field(default=None, exclude=True, repr=False)

    parsed: ParsedT | None = None
    parse_error: str | None = None

    # Durable references to any media the agent PRODUCED (images, audio, video,
    # documents), newest message only. Each item is
    # ``{"file_id": str, "mime_type": str | None, "kind": "image"|"audio"|...}``.
    #
    # WHY THIS EXISTS: ``output`` is TEXT. A picture cannot travel through a text
    # channel — flattening one used to yield a signed URL, which meant the calling
    # agent received a link it could only parrot, never an image it could SEE, and
    # that link then got persisted and died. Media travels as an identity here, and
    # the consumer (``agent_call``) turns it back into a real content block that the
    # provider resolves to bytes at send time.
    media: list[dict[str, Any]] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# JSON extraction
# ---------------------------------------------------------------------------


_FENCED_JSON_RE = re.compile(r"```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```", re.DOTALL)


def extract_json_block(text: str) -> str:
    """Pull the first JSON object/array out of a model response.

    Handles three shapes commonly seen in the wild:
      1. ```json ... ``` fenced block
      2. raw object/array with prose around it
      3. exactly one JSON object spanning the whole response

    Returns the original text if nothing JSON-shaped is found; the parser
    will then raise and the executor will report a parse error.

    Public helper — reused by ``run_agent``'s schema validator and by any
    downstream step that needs to recover
    JSON from a noisy LLM response.
    """
    if not text:
        return text

    # 🚨 THE WHOLE MESSAGE WINS WHEN IT IS ITSELF VALID JSON — checked BEFORE
    # any fence. A model answering in raw JSON can legitimately CONTAIN a
    # ```json fence inside one of its string values, and the fence branch below
    # would then return that inner fragment and throw the real answer away.
    #
    # Measured, 2026-08-16: a Hindsight reviewer returned a perfectly valid
    # 7,947-character JSON object whose `section_content` proposed the sentence
    # *"Do NOT wrap your answer like this: ```json {...} ```"*. Extraction
    # returned the literal string `{...}`, the schema parse failed with
    # "Expecting property name enclosed in double quotes (line 1, col 2)", and a
    # $0.18 review of ten real conversations was discarded — while the
    # structured-output event upstream reported success, so nothing looked
    # broken. Any agent whose output discusses JSON formatting can hit this.
    #
    # This branch is a pure widening: it changes the result ONLY for text that
    # is entirely valid JSON, where returning the whole thing is definitionally
    # right. Everything below is untouched.
    stripped = text.strip()
    if stripped[:1] in ("{", "["):
        try:
            json.loads(stripped)
        except ValueError:
            pass
        else:
            return stripped

    fence_match = _FENCED_JSON_RE.search(text)
    if fence_match:
        return fence_match.group(1).strip()

    obj_start = text.find("{")
    arr_start = text.find("[")
    candidates = [pos for pos in (obj_start, arr_start) if pos >= 0]
    if not candidates:
        return text.strip()
    start = min(candidates)
    open_ch = text[start]
    close_ch = "}" if open_ch == "{" else "]"

    depth = 0
    in_string = False
    escape_next = False
    for i in range(start, len(text)):
        ch = text[i]
        if escape_next:
            escape_next = False
            continue
        if ch == "\\" and in_string:
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return text[start : i + 1]

    return text[start:].strip()


def _parse_with_schema(
    raw_output: str,
    json_schema: type[BaseModel],
    label: str,
) -> tuple[BaseModel | None, str | None]:
    """Try to parse + validate ``raw_output`` against ``json_schema``.

    On any failure, dump the FULL unaltered model response in red via
    vcprint (so debugging never has to play "what did the model actually
    return?") and return a structured error message. The raw output is
    preserved on ``AgentRunResult.output`` regardless.
    """
    from matrx_ai.agents.response_parser import decode_residual_escapes

    try:
        candidate = extract_json_block(raw_output)
        # THE SECOND PARSE FUNNEL. `extract_json` is the other one; both decode
        # residual double-escaped `\uXXXX` sequences so no consumer of a parsed
        # agent answer ever receives the literal text a model escaped twice.
        data = decode_residual_escapes(json.loads(candidate))
    except json.JSONDecodeError as exc:
        vcprint(
            raw_output,
            f"[AgentExecutor:{label}] Error Parsing Agent Response",
            color="red",
        )
        return None, f"JSONDecodeError: {exc.msg} (line {exc.lineno}, col {exc.colno})"

    try:
        parsed = json_schema.model_validate(data)
    except ValidationError as exc:
        vcprint(
            raw_output,
            f"[AgentExecutor:{label}] Error Parsing Agent Response",
            color="red",
        )
        return None, f"ValidationError: {exc.errors()}"

    # Schema-valid is not enough: Anthropic constrained decoding can give up
    # mid-generation and fill required fields with the literal string
    # "placeholder" while still satisfying the schema (feedback 0788c8a5).
    # Accepting that silently persists corrupt content into live surfaces —
    # fail the parse LOUDLY instead so the caller retries or surfaces an error.
    from matrx_ai.agents.response_parser import find_degenerate_strings

    degenerate_paths = find_degenerate_strings(data)
    if degenerate_paths:
        vcprint(
            raw_output,
            f"[AgentExecutor:{label}] DEGENERATE structured output — the model "
            f"filled {len(degenerate_paths)} field(s) with literal placeholder "
            "filler and gave up mid-generation. Result REJECTED, never persisted.",
            color="red",
        )
        shown = ", ".join(degenerate_paths[:8])
        return None, (
            f"DegenerateOutputError: {len(degenerate_paths)} field(s) contain "
            f"literal placeholder filler ({shown}) — the model abandoned the "
            "generation; the run must be retried, not persisted"
        )

    return parsed, None


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def bind_structured_output(agent: Agent, json_schema: type[BaseModel] | dict[str, Any]) -> None:
    """Bind a provider-native structured-output contract onto ``agent``.

    THE ONE binding step: ``run_agent`` calls it before a live run, and the
    Batch lane (aidream ``mandates.batch_lane``) calls it before
    ``render_agent_provider_request``, so a batched request carries the exact
    ``response_format`` a live run would send. Raises when the schema cannot
    be enforced (the caller decides whether that refuses the run)."""
    from matrx_ai.config.response_format import (
        response_format_for_model,
        response_format_for_schema,
    )

    bound_format = (
        response_format_for_schema(json_schema)
        if isinstance(json_schema, dict)
        else response_format_for_model(json_schema)
    )
    bound_wire = bound_format.model_dump(mode="json", by_alias=True, exclude_none=True)
    agent.config.response_format = bound_wire
    agent.output_schema = bound_wire["json_schema"]


async def run_agent(
    agent: Agent,
    *,
    label: str,
    source_app: str | None = None,
    source_feature: str,
    user_input: str | list[dict[str, Any]] | None = None,
    json_schema: type[ParsedT] | dict[str, Any] | None = None,
    extra_client_tools: list[str] | None = None,
    conversation_id: str | None = None,
    independent_request: bool = False,
    suppress_stream: bool = False,
    allow_client_delegation: bool = True,
    emit_lifecycle: bool = True,
    system_run: bool = False,
    stream_system_run: bool = False,
    store: bool | None = None,
    require_complete_output: bool = False,
    max_iterations: int | None = None,
    metadata: dict[str, Any] | None = None,
    stream_data_types: frozenset[str] | None = None,
) -> AgentRunResult[ParsedT]:
    """Execute an already-prepared ``Agent`` inside ``child_agent_context``.

    ``metadata`` (optional) is merged OVER the metadata the child inherits from
    the parent context, so a caller can name what this child run IS — e.g. a
    mandate run stamps its own ``mandate_key`` and resolution instead of
    inheriting a parent chat's.

    The caller is responsible for:
      * loading the agent (``Agent.from_agent``, ``Agent.from_dict``, etc.)
      * applying variables (``agent.with_variables(...)``)
      * applying any config overrides (``agent.apply_config_overrides(...)``)
      * setting any custom tools on ``agent.config.custom_tools``
      * ``source_feature`` (required) — the spawning surface for CX /
        usage attribution (``agent_call``, ``page_summary``, …). Never
        inherit the parent request's feature.
      * ``source_app`` (optional) — defaults to the host's
        ``default_child_source_app`` ext (``matrx-ai`` standalone).

    The executor is responsible for:
      * stamping ``source_app`` / ``source_feature`` on the forked child
        context (overriding whatever the parent carried)
      * forking AppContext via ``child_agent_context(label)``
      * emitting sub_agent init/completion lifecycle events
      * isolating the reservation tracker
      * (optional) extending the forked ``ctx.client_tools`` with
        ``extra_client_tools`` so client-delegated tool dispatch works
      * (optional) stamping a fresh ``request_id`` on the forked context
        when ``independent_request=True`` so the call is rooted as its
        own user-level unit instead of a sub-step of the parent request
      * translating ``AgentExecuteResult`` -> ``AgentRunResult``
      * optional JSON parsing + Pydantic validation, with a loud red dump
        of the full unaltered response on failure
      * never raising; success/failure is communicated via the result

    Args:
        agent: A loaded ``Agent`` ready to execute.
        label: Short identifier used as the sub_agent label and in vcprint
               diagnostics. Surfaces in stream events to the frontend.
        source_app: Product/app tag for the child conversation. Omit to
                    use ``default_child_source_app`` from ``configure()``.
        source_feature: Required feature tag naming this spawn surface.
        user_input: Optional user message (string or content blocks)
                    appended before execution. Equivalent to passing
                    ``user_input=`` to ``agent.execute``.
        json_schema: Optional Pydantic model or persisted JSON-schema dictionary
                     used to enforce provider-native structured output before
                     the call. Pydantic models also parse and validate the
                     returned text afterward. Always optional.
        extra_client_tools: Optional list of tool names to merge into the
                            forked ``AppContext.client_tools`` for the
                            duration of this agent run. Mirrors what
                            ``prepare_agent_run`` does for the /agents/
                            HTTP endpoint when ``custom_tools`` /
                            ``client_tools`` are passed.
        conversation_id: Optional EXISTING conversation the child runs inside,
                            replacing the fresh uuid ``child_agent_context``
                            mints. Threaded into the context fork itself so the
                            sub_agent INIT event and every child-fork hook see
                            the real id (never a phantom). The conversation gate
                            is idempotent, so an existing row (e.g. a fork
                            created for this run) is reused and the child's new
                            turns append to it. The caller owns the access
                            check — this executor never widens access.
        independent_request: When True, the forked child context gets a
                            FRESH ``request_id`` (uuid4) so this call is
                            persisted as its own ``cx_user_request`` row
                            rather than a sub-step of the caller. Use for
                            fan-out workloads where each call is a
                            standalone user-level unit (e.g. concurrent
                            per-page summaries in the research pipeline)
                            that must not race on the parent's
                            ``cx_user_request`` id. Defaults to False —
                            the normal sub-agent rooting.
        system_run: When True, this is an INTERNAL machine call (fan-out
                            derivations, pipelines, mandates). The forked
                            context gets ``system_run=True``. A stored system
                            run keeps its FULL history exactly like a chat —
                            conversation backfill, messages, cost rows, request
                            snapshot — so it opens and reads like any chat;
                            nothing turns that off (Arman, 2026-10-05). It
                            skips only non-history ceremony: the title LLM
                            call, the cache_state refresh and the context-state
                            event. Output is muted by default; set
                            ``stream_system_run=True`` only when the containing
                            user-facing pipeline promises the AI output in its
                            real-time stream. Client delegation is blocked and
                            citations default off.
        stream_system_run: Preserve the parent emitter for a system run
                            instead of replacing it with ``SilentEmitter``.
                            Client-delegation blocking remains unchanged.
        store:            None = inherit the parent's persistence intent. True
                            persists this run even inside a non-persisting
                            parent (a machine context minted ``store=False``
                            by default); a non-UUID inherited request id is
                            replaced with a fresh one so the stored rows have
                            a valid parent. False makes the run ephemeral.
        allow_client_delegation: Whether this child may suspend for a client-
                            executed tool. Silenced/reference/system children
                            force this off because their emitter cannot deliver
                            the delegation event needed to claim the work.
        require_complete_output: Mark a contained failed, paused, suspended,
                            truncated, or empty child result as a failed
                            lifecycle completion. Use when partial child text
                            must be rewound rather than retained.
        max_iterations: This ONE run's iteration ceiling — the subtree half of a
                            per-child execution budget (the time half rides the
                            forked context; see
                            ``matrx_ai.orchestrator.subtree_budget``). The loop
                            stops AT the ceiling through its graceful
                            ``max_iterations_exceeded`` exit and keeps
                            everything it produced. None = the funnel default.

    Returns:
        ``AgentRunResult`` — ``success`` indicates execution status;
        ``parsed`` / ``parse_error`` cover JSON validation when requested.
    """
    if json_schema is not None:
        try:
            bind_structured_output(agent, json_schema)
        except Exception as exc:
            vcprint(
                f"[AgentExecutor:{label}] Refusing structured-output call: {exc}",
                color="red",
            )
            return AgentRunResult(
                success=False,
                error=str(exc),
                error_kind="execution",
            )

    resolved_app, resolved_feature = resolve_child_source(
        source_app=source_app,
        source_feature=source_feature,
        caller=f"run_agent({label!r})",
    )

    # Host spine tracking for internal agent runs (mandatory when injected —
    # see _ext.get_internal_run_tracker). Opened inside the child context so
    # the host sees the run's own request_id / agent identity; settled exactly
    # once below (success path) or in the except branch (crash path).
    _spine_settle = None
    _child_conversation_id: str | None = None
    _child_request_id: str | None = None
    _contained_incomplete_reason: str | None = None
    # Whatever this run's loop spends is readable here even if it never returns
    # (cancel / time limit / crash) — see execution_state.RunUsageSink.
    from matrx_ai.orchestrator.execution_state import (
        close_run_usage_sink,
        open_run_usage_sink,
    )

    _usage_sink, _usage_sink_token = open_run_usage_sink()
    try:
        async with child_agent_context(
            label, emit_lifecycle=emit_lifecycle, conversation_id=conversation_id
        ):
            from matrx_connect.context.app_context import get_app_context, set_app_context

            from matrx_ai.db.conversation_gate import (
                CONVERSATION_STEP_LABEL_KEY,
                PARENT_REQUEST_ID_KEY,
                resolve_step_label_for_title,
            )

            child_ctx = get_app_context()
            child_metadata = {
                k: v
                for k, v in child_ctx.metadata.items()
                if k not in ("agent_name", CONVERSATION_STEP_LABEL_KEY)
            }
            child_metadata[CONVERSATION_STEP_LABEL_KEY] = resolve_step_label_for_title(
                label,
                getattr(agent, "name", None),
            )
            if metadata:
                child_metadata.update(metadata)
                # What PERSISTS on the run's request row is the agent's own
                # request metadata (Agent.execute → AIMatrixRequest.metadata),
                # not the context's — so the caller's naming rides both.
                agent.request_metadata = {**agent.request_metadata, **metadata}
            from matrx_ai.tools.merge import (
                ACTIVE_TOOL_EXECUTORS_KEY,
                CLIENT_DELEGATION_DISABLED_KEY,
            )

            delegation_disabled = (
                not allow_client_delegation
                or suppress_stream
                or system_run
                or child_metadata.get(CLIENT_DELEGATION_DISABLED_KEY) is True
            )
            if delegation_disabled:
                child_metadata[CLIENT_DELEGATION_DISABLED_KEY] = True
                child_metadata[ACTIVE_TOOL_EXECUTORS_KEY] = []
            # Agent attribution + title/model seed — mirror what the HTTP route's
            # prepare_agent_run does, so programmatic NamedAgent / run_agent calls
            # write cx_user_request.agent_id / cx_conversation.initial_agent_id
            # instead of NULL (the research/podcast/NER attribution gap). The
            # agent name and resolved model also feed the conversation title and
            # the cx_conversation.config model self-rescue.
            agent_name = getattr(agent, "name", None)
            if agent_name:
                child_metadata["agent_name"] = agent_name
            initial_model = getattr(agent.config, "model", None)
            if initial_model:
                child_metadata.setdefault("initial_model", initial_model)

            overrides: dict[str, Any] = {
                "metadata": child_metadata,
                "source_app": resolved_app,
                "source_feature": resolved_feature,
            }
            # Stamp the agx_agent identity onto the forked context so the
            # conversation gate's _stamp_agent_refs writes real attribution.
            # is_version=True → a pinned version snapshot (agent_version_id);
            # is_version=False → a floating master row (agent_id).
            source_id = getattr(agent, "source_id", None)
            # The OTHER half is cleared: a forked context inherits the parent's
            # agent refs, and a child left holding its parent's agent_id would
            # attribute its rows (chat.message.agent_id included) to the parent.
            if source_id:
                if getattr(agent, "source_is_version", False):
                    overrides["agent_version_id"] = source_id
                    overrides["agent_id"] = None
                else:
                    overrides["agent_id"] = source_id
                    overrides["agent_version_id"] = None
            if delegation_disabled:
                overrides["client_tools"] = []
            elif extra_client_tools:
                overrides["client_tools"] = list(
                    dict.fromkeys(list(child_ctx.client_tools or []) + list(extra_client_tools))
                )
            if independent_request:
                # Its own request record, LINKED to the request it ran under: the
                # fresh user_request row carries ``metadata.parent_request_id``, so
                # per-run joins work and lineage is never lost (Agent Factory review
                # 4 N4-7: sequential mandate runs shared the first run's id and only
                # the first got a user_request row).
                parent_request_id = child_ctx.request_id
                overrides["request_id"] = str(uuid.uuid4())
                # R38: its own record, the TREE's cap — spend keys on the root request.
                from matrx_ai.orchestrator.cost_budget import link_tree_request

                link_tree_request(overrides["request_id"], parent_request_id)
                from matrx_ai.db.conversation_gate import canonical_request_id, request_has_record

                if parent_request_id and _is_uuid_text(parent_request_id) and not request_has_record(parent_request_id):
                    # N4-7: a link names a REAL row or nothing — an ambient synthetic
                    # request (a machine context, an MCP call) has no record to point at.
                    # The tree cap link above still holds (in memory, not a row).
                    vcprint(
                        f"[run_agent] independent run {overrides['request_id']} under request "
                        f"{parent_request_id}, which has no record here — no lineage link written "
                        "(the tree cap still applies)",
                        color="yellow",
                    )
                    parent_request_id = None
                if parent_request_id and _is_uuid_text(parent_request_id):
                    parent_request_id = canonical_request_id(parent_request_id)
                    child_metadata[PARENT_REQUEST_ID_KEY] = str(parent_request_id)
                    # The completion write REPLACES the row's metadata with the
                    # agent's request metadata (requests.py to_user_request), so
                    # the link rides there too or it is lost at completion.
                    if isinstance(getattr(agent, "request_metadata", None), dict):
                        agent.request_metadata = {
                            **agent.request_metadata,
                            PARENT_REQUEST_ID_KEY: str(parent_request_id),
                        }
                else:
                    child_metadata.pop(PARENT_REQUEST_ID_KEY, None)
            if store is not None and bool(getattr(child_ctx, "store", True)) != store:
                overrides["store"] = store
                if store and not _is_uuid_text(overrides.get("request_id", child_ctx.request_id)):
                    # A stored run needs a UUID request id (the executor refuses
                    # otherwise); a synthetic machine context may carry none.
                    overrides["request_id"] = str(uuid.uuid4())
                    from matrx_ai.orchestrator.cost_budget import link_tree_request

                    link_tree_request(overrides["request_id"], child_ctx.request_id)
            if system_run:
                # A system run keeps its full history like any chat; the flag
                # only skips non-history ceremony (title LLM call, cache_state
                # refresh, context-state event) — the 2026-07-07 fan-out
                # starvation came from that ceremony, not from the history
                # writes, which ride the one coordinator flush.
                #
                # A MANDATE CANDIDATE is not marked system_run at all: its run
                # is the evidence a person reads beside the live run (PLAN
                # §2.7). Every other system_run behaviour below — muted stream,
                # no client delegation, no citations — still applies, so what
                # the model is offered and sees is exactly the live run's.
                from matrx_graph.candidate import candidate_marker

                if candidate_marker(child_metadata) is None:
                    overrides["system_run"] = True
                    # The child already owns its conversation — name it so the
                    # system-run transition does not mint another one.
                    overrides.setdefault("conversation_id", child_ctx.conversation_id)
                if not stream_system_run:
                    suppress_stream = True
                # Ratified citations exclusion: a system_run is by definition a
                # machine-consumed internal call — its documents must not carry
                # citability (citation-split blocks corrupt machine parsing).
                # setdefault: an explicit citations_enabled=True force-enable
                # (or a NamedAgent's declared policy) still wins. The provider
                # translator gate announces every actual strip loudly.
                agent.config.metadata.setdefault("citations_enabled", False)
            if suppress_stream:
                # Side-quest agent: mute its token/event stream so its (often
                # JSON, stream:true) output can't leak into the parent's
                # user-facing content stream. The structured result still
                # returns via AgentRunResult; persistence is unaffected.
                from matrx_connect.emitters import SilentEmitter

                # ``stream_data_types``: the few typed data events a muted child
                # still delivers live to the parent (a TTS stage's audio chunks).
                overrides["emitter"] = SilentEmitter(
                    forward_to=child_ctx.emitter if stream_data_types else None,
                    forward_data_types=stream_data_types,
                )
            set_app_context(child_ctx.with_overrides(**overrides))
            # Surface the child's conversation identity on the result — the
            # completion metadata does not reliably carry it for programmatic
            # runs, which left consumers (agent_call collab provenance) with
            # None. Captured here; setdefault'd onto result.metadata below.
            _child_conversation_id = getattr(child_ctx, "conversation_id", None)
            _child_request_id = getattr(get_app_context(), "request_id", None) or None
            if independent_request:
                # Fresh request_id ⇒ fresh cx_user_request. execute_ai_request
                # also ensures this, but tools can run before that gate; mint
                # the parent here so tool_call FKs never orphan.
                from matrx_ai.db.conversation_gate import ensure_user_request_exists

                _fresh = get_app_context()
                if _fresh.request_id and _fresh.user_id and _fresh.store:
                    await ensure_user_request_exists(
                        request_id=_fresh.request_id,
                        user_id=_fresh.user_id,
                    )

            # Spine tracking (host-injected, mandatory when configured): every internal agent
            # run — MCP agent-service, NamedAgent research fan-out, podcast
            # metadata — funnels through HERE, so this one call is what puts
            # them all on the host's runtime spine. The tracker reads the
            # ambient (child) context; None means the host declined (e.g. the
            # run is already inside a tracked execution tree).
            try:
                from matrx_ai._ext import get_internal_run_tracker

                _tracker = get_internal_run_tracker()
                if _tracker is not None:
                    _spine_settle = await _tracker(label=label, source_feature=resolved_feature)
            except Exception as _track_exc:  # noqa: BLE001 — refuse paid work without its ledger
                vcprint(
                    f"[AgentExecutor:{label}] internal-run tracker open failed "
                    f"(PAID RUN REFUSED): {_track_exc}",
                    color="red",
                )
                raise

            execute_result: AgentExecuteResult = await agent.execute(
                user_input=user_input, max_iterations=max_iterations
            )
            if require_complete_output:
                child_status = str((execute_result.metadata or {}).get("status") or "")
                incomplete = (
                    child_status == "failed"
                    or child_status == "paused"
                    or child_status == "truncated"
                    or child_status.startswith("suspended")
                    or not (execute_result.output or "").strip()
                )
                if incomplete:
                    from matrx_connect.context.app_context import mark_child_agent_failed

                    _contained_incomplete_reason = child_status or "empty_response"
                    mark_child_agent_failed(f"status={_contained_incomplete_reason}")
    except asyncio.CancelledError as _cancel_exc:
        # A cancelled run (fan-out sibling cancellation via gather(), parent task
        # teardown, shutdown) must still settle its spine execution — the except
        # Exception branch below can't see BaseException, and an unsettled row
        # sits RUNNING until the reaper false-fails it as `matrx_execution_abandoned`
        # a full lease later (live incident: internal_agent_run rows reaped at
        # exactly the 30-min utility lease for runs that ended in seconds).
        # The settle itself detaches its DB write, so this await is instant.
        #
        # It settles what the run REALLY spent: the model calls made before the
        # cancel were billed. Settling with no meters recorded $0 (news run
        # 70601b15: a per-call time limit cut a judge off mid-loop and ~$0.70
        # vanished from the run total, the cost tree and the monthly ceiling).
        _spent = _usage_sink.usage_history()
        _stamp_run_usage(_cancel_exc, _spent)
        if _spine_settle is not None:
            try:
                await _settle_spine(
                    _spine_settle,
                    "cancelled",
                    meters=_early_exit_meters(_spent, label=label),
                )
            except Exception:  # noqa: BLE001 — the host's reaper is the backstop
                pass
        raise
    except Exception as exc:
        vcprint(
            f"[AgentExecutor:{label}] Agent execution failed: {exc}",
            color="red",
        )
        # A crash out of the loop (a commit barrier, a host hook) still owes
        # every call it made before the crash — same rule as the cancel above.
        _spent = _usage_sink.usage_history()
        _stamp_run_usage(exc, _spent)
        if _spine_settle is not None:
            try:
                await _settle_spine(
                    _spine_settle,
                    "failed",
                    error=str(exc) or type(exc).__name__,
                    meters=_early_exit_meters(_spent, label=label),
                )
            except Exception:  # noqa: BLE001 — the host's reaper is the backstop
                pass
        _spent_total = TokenUsage.aggregate_by_model(_spent) if _spent else None
        _spent_dict: dict[str, Any] = {}
        if _spent_total is not None:
            try:
                _spent_dict = _spent_total.to_dict()
            except Exception:  # noqa: BLE001
                _spent_dict = {}
        return AgentRunResult(
            success=False,
            error=str(exc),
            error_kind="execution",
            exception=exc,
            usage=_spent_dict,
            usage_aggregated=_spent_total,
            usage_history=_spent,
        )
    finally:
        close_run_usage_sink(_usage_sink_token)

    usage_dict: dict[str, Any] = {}
    if execute_result.usage is not None:
        try:
            usage_dict = execute_result.usage.to_dict()
        except Exception:
            usage_dict = {}

    model_id: str | None = None
    if execute_result.metadata:
        model_id = execute_result.metadata.get("model")
    if not model_id:
        # The execution metadata doesn't reliably carry the resolved model slug
        # for programmatic NamedAgent runs, which left consumers like
        # rs_analysis.model_id NULL even though cx_request recorded the model.
        # agent.config holds the resolved config after execute() — read the slug
        # from there so the model is always surfaced on the result.
        model_id = getattr(agent.config, "model", None)

    from matrx_ai.tools.candidate_containment import CANDIDATE_STOPPED_STATUS

    candidate_stopped = execute_result.metadata.get("status") == CANDIDATE_STOPPED_STATUS
    execution_failed = (
        execute_result.metadata.get("status") == "failed"
        or _contained_incomplete_reason is not None
        or candidate_stopped
    )
    execution_error: str | None = None
    if candidate_stopped:
        stop = execute_result.metadata.get(CANDIDATE_STOPPED_STATUS) or {}
        execution_error = (
            f"candidate run stopped at step {stop.get('step')}: {stop.get('tool')} "
            f"({stop.get('class')}) was not executed"
        )
    elif execution_failed:
        raw_error = execute_result.metadata.get("error")
        if isinstance(raw_error, dict):
            execution_error = str(
                raw_error.get("user_message") or raw_error.get("message") or raw_error
            )
        elif raw_error is not None:
            execution_error = str(raw_error)
        elif _contained_incomplete_reason == "truncated":
            execution_error = "agent response was truncated before completion"
        elif _contained_incomplete_reason == "paused":
            execution_error = "agent paused before producing a complete response"
        elif (_contained_incomplete_reason or "").startswith("suspended"):
            execution_error = "agent suspended before producing a complete response"
        elif _contained_incomplete_reason == "empty_response":
            execution_error = "agent returned an empty response"
        else:
            execution_error = "agent execution failed"

    if _spine_settle is not None:
        # Settle the spine execution with the run's real outcome + final meters
        # ({usd, input_tokens, output_tokens} — the utility-flavor contract).
        # The host owns durability semantics. Aidream runs the DB work in an
        # isolated task and awaits its terminal attempt so a short-lived host
        # cannot exit after metering but before completion.
        try:
            # `total_cost or 0` here used to turn an honestly-unknown bill into
            # a silent $0 on the spend ledger (139 zero-cost internal_agent_run
            # rows in 30 days, 2026-09-12). The shared builder records the
            # catalog-known subtotal plus an explicit `unpriced_calls` meter.
            from matrx_ai.config.usage_config import cost_meters_from_totals

            meters: dict[str, Any] = cost_meters_from_totals(
                getattr(execute_result.usage, "total", None), label=label
            )
            # A run the loop STOPPED (tree budget, deadline, subtree time
            # budget, a person's cancel between calls) returns normally with
            # status "cancelled" — it is not "completed", and the spine must
            # say so. Its real spend still settles with it.
            _stopped = (execute_result.metadata or {}).get("status") == "cancelled"
            _settle_status = (
                "failed" if execution_failed else "cancelled" if _stopped else "completed"
            )
            _settle_error = execution_error
            if _stopped and not execution_failed:
                _raw_stop = (execute_result.metadata or {}).get("error")
                if isinstance(_raw_stop, dict):
                    _raw_stop = (
                        _raw_stop.get("user_message") or _raw_stop.get("message") or _raw_stop
                    )
                _settle_error = str(_raw_stop) if _raw_stop else "run stopped by execution control"
            await _settle_spine(
                _spine_settle,
                _settle_status,
                error=_settle_error,
                meters=meters or None,
            )
        except Exception as _settle_exc:  # noqa: BLE001 — the host's reaper is the backstop
            vcprint(
                f"[AgentExecutor:{label}] internal-run tracker settle failed "
                f"(run unaffected): {_settle_exc}",
                color="yellow",
            )

    result: AgentRunResult[ParsedT] = AgentRunResult(
        success=not execution_failed,
        output=execute_result.output or "",
        usage=usage_dict,
        usage_aggregated=execute_result.usage,
        usage_history=list(execute_result.usage_history or []),
        model_id=model_id,
        metadata=dict(execute_result.metadata or {}),
        error=execution_error,
        exception=getattr(execute_result, "exception", None) if execution_failed else None,
        error_kind=(
            "candidate_stopped"
            if candidate_stopped
            else ("execution" if execution_failed else None)
        ),
        media=collect_media_refs(getattr(execute_result, "assistant_response", None)),
    )
    if _child_conversation_id:
        result.metadata.setdefault("conversation_id", _child_conversation_id)
    # The run's own request id and spine execution, so a caller can link the run
    # to its stored request (chat.user_request / chat.request) and its spend.
    if _child_request_id:
        result.metadata.setdefault("request_id", str(_child_request_id))
    _spine_execution_id = getattr(_spine_settle, "execution_id", None) if _spine_settle else None
    if _spine_execution_id:
        result.metadata.setdefault("runtime_execution_id", str(_spine_execution_id))

    # A DECISION TURN'S ANSWER IS A TYPED PART, never recovered from text: the
    # ``decision_answers`` part the assistant message carries IS the parsed
    # result every consumer (mandates, workflow steps, MCP) reads.
    if not execution_failed:
        from matrx_ai.decisions.result import decision_answers_part

        decision_part = decision_answers_part(getattr(execute_result, "assistant_response", None))
        if decision_part is not None:
            result.parsed = decision_part  # type: ignore[assignment]
            result.metadata.setdefault("output_kind", "decision_answers")
            return result

    if isinstance(json_schema, type) and issubclass(json_schema, BaseModel) and not execution_failed:
        parsed, parse_error = _parse_with_schema(result.output, json_schema, label)
        result.parsed = parsed
        result.parse_error = parse_error
        if parse_error is not None:
            result.error_kind = "parse"

    return result
