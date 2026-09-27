"""Google Deep Research agents as an ordinary agent turn.

Deep Research (``deep-research-preview-04-2026``) and Deep Research Max
(``deep-research-max-preview-04-2026``) are provider-managed AGENTS, not chat
models: they run on the Interactions API with ``agent=...``, must run in the
background, and take minutes. Arman's ruling (2026-09-26): an agent can be a
text model, video, image, speech, live, decision, or a research model, and it
makes no difference — so a research model is a model in the AGENT system, the
same way a decision model is (see ``UnifiedAIClient._execute_decision``). This
adapter is the research wire translator that ``UnifiedAIClient`` dispatches to
when the resolved model's ``capabilities.interaction == "agent"``.

What one turn does:
  1. Build the Interactions request from the agent's turn: the system
     instruction, the conversation's text, and the research settings the
     author chose (``reasoning_summary`` → ``thinking_summaries``,
     ``visualization``, ``internal_web_search`` / ``internal_url_context`` →
     the hosted tools).
  2. Start it with ``background=True, stream=True`` and relay the live events:
     research thoughts stream as reasoning, searches as progress notes, report
     text as ordinary answer chunks. A dropped stream (Google closes them after
     ~10 minutes) resumes from ``last_event_id``; if resuming keeps failing it
     falls back to polling ``interactions.get``.
  3. Read the FINISHED interaction once (the authoritative record) and turn it
     into one assistant message: the report as ``TextContent`` with normalized
     citations, generated charts as persisted ``ImageContent``, research
     thoughts as ``ThinkingContent``, and the provider's token usage.

Official interface: https://ai.google.dev/gemini-api/docs/deep-research
(read 2026-09-26; google-genai 2.25 ``interactions`` types).

Paid-work rules: the research is billed the moment it starts, so after
creation nothing here is retryable (a retry would start and bill a second
research), billed usage rides every failure, and a cancelled turn cancels the
Google interaction instead of leaving it running unobserved.
"""

from __future__ import annotations

import asyncio
import base64
import warnings
from typing import Any

from google import genai
from google.genai import types as genai_types
from matrx_utils import vcprint

from matrx_ai.config import (
    ImageContent,
    TextContent,
    ThinkingContent,
    UnifiedConfig,
    UnifiedMessage,
    UnifiedResponse,
)
from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.providers.keys import keyed_provider_client

# The research settings an author may set, and their wire values.
_THINKING_SUMMARIES_OFF = frozenset({"never"})
VISUALIZATION_VALUES = frozenset({"auto", "off"})

# Transport resilience, not a product limit: how often a finished-or-not check
# runs when the live stream cannot be resumed, and how many consecutive
# transport failures end the wait. Google itself bounds a research run
# (documented maximum research time), so the loop always terminates.
POLL_SECONDS = 10.0
MAX_CONSECUTIVE_TRANSPORT_FAILURES = 12
MAX_STREAM_RESUMES = 20

_TERMINAL = frozenset({"completed", "failed", "cancelled", "incomplete", "budget_exceeded"})


class DeepResearchFailed(RuntimeError):
    """A research run that ended without a report. Never retried: the run was
    already started (and billed) on Google's side."""

    def __init__(self, message: str, *, status: str, interaction_id: str | None) -> None:
        super().__init__(message)
        from matrx_ai.providers.errors import RetryableError

        self.error_info = RetryableError(
            error_type="google_research_failed",
            message=message,
            is_retryable=False,
            user_message=(
                "The research run ended without a report "
                f"(status: {status}). Nothing was retried, because a retry would "
                "start and bill a new research run. Try again with a narrower question."
            ),
            details={"provider": "google", "interaction_id": interaction_id, "status": status},
        )


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _status(value: Any) -> str:
    return str(_get(value, "status") or "").lower()


def research_input(unified_config: UnifiedConfig) -> str:
    """The conversation as one research brief.

    A research agent takes a single brief. The latest user turn IS the
    request; earlier turns (a follow-up in the same conversation) ride along as
    context so a follow-up question is understood. Only text is sent — the
    catalog declares these models text-input.
    """
    turns: list[tuple[str, str]] = []
    for message in unified_config.messages or []:
        role = _get(message, "role")
        if role not in ("user", "assistant"):
            continue
        text = "\n".join(
            item.text for item in (_get(message, "content") or []) if isinstance(item, TextContent) and item.text
        ).strip()
        if text:
            turns.append((role, text))
    if not turns or turns[-1][0] != "user":
        raise ValueError("A research agent needs a question: the turn has no user text to research.")
    request = turns[-1][1]
    earlier = turns[:-1]
    if not earlier:
        return request
    transcript = "\n\n".join(f"{'User' if r == 'user' else 'Research report'}:\n{t}" for r, t in earlier)
    return f"Earlier in this conversation:\n\n{transcript}\n\nThe request now:\n\n{request}"


#: Google's research agents (``deep-research-preview-04-2026``,
#: ``deep-research-max-preview-04-2026``). The Interactions wire also serves
#: other managed agents (Antigravity sandbox) that take a different agent_config.
RESEARCH_AGENT_PREFIX = "deep-research-"


def is_google_research_agent(provider_model_id: str | None) -> bool:
    return str(provider_model_id or "").startswith(RESEARCH_AGENT_PREFIX)


def build_research_kwargs(unified_config: UnifiedConfig, profile: Any) -> dict[str, Any]:
    """The Interactions create() arguments for one research turn (pure)."""
    summaries = unified_config.reasoning_summary
    visualization = getattr(unified_config, "visualization", None) or "auto"
    if visualization not in VISUALIZATION_VALUES:
        raise ValueError(
            f"visualization={visualization!r} is not a Deep Research value; use one of "
            f"{sorted(VISUALIZATION_VALUES)}."
        )
    # Google refuses `system_instruction` on research agents ("include any
    # specific instructions in the 'input' prompt instead", 400 on
    # 2026-09-26), so the author's instructions lead the brief.
    brief = research_input(unified_config)
    system = unified_config.resolved_system_instruction
    if system:
        brief = f"Instructions:\n{system}\n\n{brief}"
    kwargs: dict[str, Any] = {
        "agent": profile.provider_model_id,
        "input": brief,
        "background": True,
        "store": True,  # background interactions require storage on Google's side
        "agent_config": {
            "type": "deep-research",
            "thinking_summaries": "none" if summaries in _THINKING_SUMMARIES_OFF else "auto",
            "visualization": visualization,
        },
    }
    # Omitted tools = Google's default set (search, URL context, code execution).
    # An author who switched search or URL reading OFF gets exactly that.
    if unified_config.internal_web_search is False or unified_config.internal_url_context is False:
        tools: list[dict[str, Any]] = [{"type": "code_execution"}]
        if unified_config.internal_web_search is not False:
            tools.append({"type": "google_search"})
        if unified_config.internal_url_context is not False:
            tools.append({"type": "url_context"})
        kwargs["tools"] = tools
    return kwargs


#: Hosted research tools Google bills per CALL, by the ``grounding_tool_count``
#: type it reports, mapped to the billing component
#: ``ai.offering.pricing[].component_prices`` prices. Google's pricing page
#: ("Pricing for agents", Gemini Deep Research agent, checked 2026-09-26):
#: inference at standard Gemini list rates, and "Tool usage fees apply per
#: existing pricing structure" — Grounding with Google Search is billed per
#: search request; URL context, File Search and code execution have no per-call
#: fee (what they read is billed as tokens, counted in ``total_tool_use_tokens``).
RESEARCH_TOOL_COMPONENTS: dict[str, str] = {"google_search": "service.google_search"}
#: Tool types with no per-call fee. Anything Google reports that is in neither
#: map is recorded as ``service.<type>``, which no catalog tier prices — so the
#: call's cost is recorded as UNKNOWN (``cost_reconciliation =
#: unknown_component_price``), never as a token-only underestimate.
RESEARCH_TOOLS_WITHOUT_CALL_FEE: frozenset[str] = frozenset(
    {"url_context", "file_search", "code_execution"}
)


def research_usage(interaction: Any, *, model_name: str, provider_model_name: str) -> TokenUsage | None:
    """The billable usage of one Deep Research interaction.

    Google bills the agent's whole loop at the underlying Gemini list rates:
    input (``total_input_tokens`` less the cached part), cached input,
    output + thinking, and the tokens its tools read back into the model
    (``total_tool_use_tokens`` — billed as input: it is prompt the model
    consumed, and ``total_tokens`` is exactly input + output + thought + tool
    use, so nothing else carries it). Hosted-search requests are a separate
    per-call component. See ``RESEARCH_TOOL_COMPONENTS``.
    """
    usage = _get(interaction, "usage")
    if usage is None:
        return None
    cached = int(_get(usage, "total_cached_tokens") or 0)
    input_tokens = int(_get(usage, "total_input_tokens") or 0)
    tool_tokens = int(_get(usage, "total_tool_use_tokens") or 0)
    output_tokens = int(_get(usage, "total_output_tokens") or 0) + int(
        _get(usage, "total_thought_tokens") or 0
    )
    raw = usage.model_dump(mode="json", exclude_none=True) if hasattr(usage, "model_dump") else dict(usage)
    token_usage = TokenUsage(
        input_tokens=max(0, input_tokens - cached) + tool_tokens,
        output_tokens=output_tokens,
        cached_input_tokens=cached,
        matrx_model_name=model_name,
        provider_model_name=provider_model_name,
        api="google",
        response_id=str(_get(interaction, "id") or ""),
        raw_usage=raw,
    )
    if tool_tokens:
        token_usage.metadata["tool_use_tokens"] = tool_tokens
    grounding = raw.get("grounding_tool_count")
    if grounding:
        token_usage.metadata["grounding_tool_count"] = grounding
        for entry in grounding if isinstance(grounding, list) else []:
            if not isinstance(entry, dict):
                continue
            tool_type = str(entry.get("type") or "").strip()
            count = int(entry.get("count") or 0)
            if not tool_type or count <= 0 or tool_type in RESEARCH_TOOLS_WITHOUT_CALL_FEE:
                continue
            component = RESEARCH_TOOL_COMPONENTS.get(tool_type, f"service.{tool_type}")
            token_usage.billing_components[component] = (
                token_usage.billing_components.get(component, 0) + count
            )
    return token_usage


async def research_content(interaction: Any) -> list[Any]:
    """The finished interaction's steps as our content parts.

    Report text parts are joined into ONE ``TextContent`` (citation offsets
    shifted to match), thought summaries become ONE ``ThinkingContent``, and
    generated images are persisted through the same envelope path Gemini's
    inline images use, so they carry a ``file_id``.
    """
    from matrx_ai.config.citations import (
        normalize_google_interaction_annotations,
        normalize_markdown_link_citations,
        unfence_code_span_links,
    )

    report = ""
    citations: list[dict[str, Any]] = []
    thoughts: list[str] = []
    images: list[Any] = []
    dropped_charts = 0
    for step in _get(interaction, "steps") or []:
        kind = _get(step, "type")
        if kind == "thought":
            for item in _get(step, "summary") or []:
                if _get(item, "type") == "text" and _get(item, "text"):
                    thoughts.append(str(_get(item, "text")))
            continue
        if kind != "model_output":
            continue
        for item in _get(step, "content") or []:
            item_type = _get(item, "type")
            if item_type == "text":
                text = str(_get(item, "text") or "")
                if report and text and not report.endswith("\n"):
                    report += "\n\n"
                offset = len(report)
                report += text
                citations.extend(
                    c.model_dump(exclude_none=True)
                    for c in normalize_google_interaction_annotations(
                        _get(item, "annotations"), offset=offset
                    )
                )
            elif item_type == "image":
                data = _get(item, "data")
                if not data:
                    continue
                blob = base64.b64decode(data) if isinstance(data, str) else data
                part = genai_types.Part(
                    inline_data=genai_types.Blob(
                        data=blob, mime_type=str(_get(item, "mime_type") or "image/png")
                    )
                )
                try:
                    image = await ImageContent.from_google_async(part)
                except Exception as exc:  # noqa: BLE001 — announced below, captured
                    # A chart is part of the report, not the report. Losing the
                    # whole paid research because one chart could not be stored
                    # is worse than keeping the report and SAYING a chart is
                    # missing (seen live 2026-09-26: storage refused the upload
                    # and the finished report was thrown away).
                    dropped_charts += 1
                    try:
                        from matrx_connect.streaming.error_capture import capture_error

                        await capture_error(
                            exc,
                            kind="research_chart_storage_failed",
                            route="providers/google/research",
                            payload={"interaction_id": str(_get(interaction, "id") or "")},
                        )
                    except Exception:  # noqa: BLE001 — capture never replaces the report
                        pass
                    continue
                if image is not None:
                    images.append(image)
    if not report.strip():
        report = str(_get(interaction, "output_text") or "")
    if not citations and report.strip():
        # No url_citation annotations came back: the agent wrote its sources as
        # inline markdown links instead (it does whenever its brief asks for
        # them). Those links ARE the citations — store them as structured
        # citations so they persist and render like annotated ones, and unfence
        # any link the model wrapped in a code span so it stays clickable.
        report = unfence_code_span_links(report)
        citations = [
            c.model_dump(exclude_none=True)
            for c in normalize_markdown_link_citations(report, provider="google")
        ]
    if dropped_charts and report.strip():
        report += (
            f"\n\n> Note: {dropped_charts} chart(s) the research produced could not be "
            "saved, so they are not shown. The report text above is complete."
        )
    content: list[Any] = []
    if thoughts:
        content.append(ThinkingContent(text="\n\n".join(thoughts), provider="google"))
    if report.strip():
        metadata: dict[str, Any] = {}
        if citations:
            metadata["citations"] = citations
        content.append(TextContent(text=report, metadata=metadata))
    content.extend(images)
    return content


class GoogleDeepResearchAgent:
    """Runs one Deep Research interaction as an agent turn."""

    provider = "google"

    client = keyed_provider_client(
        "GEMINI_API_KEY",
        "GOOGLE_API_KEY",
        "GOOGLE_AI_STUDIO",
        factory=lambda api_key: genai.Client(
            api_key=api_key,
            http_options={"api_version": "v1beta"},
        ),
    )

    @property
    def _interactions(self) -> Any:
        return self.client.aio.interactions

    async def execute(
        self,
        unified_config: UnifiedConfig,
        profile: Any,
        debug: bool = False,
    ) -> UnifiedResponse:
        from matrx_connect.context.events import InfoPayload

        from matrx_ai.context.app_context import get_app_context
        from matrx_ai.providers.citation_emit import emit_citations_from_response
        from matrx_ai.providers.errors import (
            attach_billed_usage,
            classify_google_error,
            mark_billing_checked,
        )
        from matrx_ai.providers.outbound_capture import stamp_call_meta

        emitter = get_app_context().emitter
        kwargs = build_research_kwargs(unified_config, profile)
        if debug:
            vcprint(
                {k: v for k, v in kwargs.items() if k != "input"},
                "[google research] create",
                color="blue",
            )
        stamp_call_meta(provider="google", model=unified_config.model, is_streaming=True)

        state = _RunState()
        try:
            await self._run(kwargs, state, emitter, InfoPayload)
            if emitter:
                await self._reasoning(emitter, started=False)
            final = await self._final(state)
        except asyncio.CancelledError as exc:
            await self._cancel_quietly(state)
            await self._attach_usage(exc, state, profile, attach_billed_usage, mark_billing_checked)
            raise
        except DeepResearchFailed as exc:
            await self._attach_usage(exc, state, profile, attach_billed_usage, mark_billing_checked)
            raise
        except Exception as exc:
            if state.interaction_id is None:
                # Nothing started on Google's side: classify normally (a
                # retry here cannot double-bill).
                exc.error_info = classify_google_error(exc)  # type: ignore[attr-defined]
                mark_billing_checked(exc)
                raise
            failure = DeepResearchFailed(
                f"Lost track of research interaction {state.interaction_id}: {exc}",
                status="transport_error",
                interaction_id=state.interaction_id,
            )
            await self._attach_usage(failure, state, profile, attach_billed_usage, mark_billing_checked)
            raise failure from exc

        status = _status(final)
        usage = research_usage(
            final, model_name=profile.model_name, provider_model_name=profile.provider_model_id
        )
        if status != "completed":
            errors = [str(_get(e, "message") or e) for e in (_get(final, "errors") or [])]
            failure = DeepResearchFailed(
                f"Google research interaction {state.interaction_id} ended with status={status!r}"
                + (f": {'; '.join(errors)}" if errors else ""),
                status=status,
                interaction_id=state.interaction_id,
            )
            attach_billed_usage(failure, usage)
            mark_billing_checked(failure)
            raise failure

        try:
            content = await research_content(final)
        except Exception as exc:
            # The research is finished and paid for; whatever broke while
            # reading it must still record the cost and must never retry.
            failure = DeepResearchFailed(
                f"Google research interaction {state.interaction_id} finished but its "
                f"result could not be read: {exc}",
                status="result_unreadable",
                interaction_id=state.interaction_id,
            )
            attach_billed_usage(failure, usage)
            mark_billing_checked(failure)
            raise failure from exc
        if not any(isinstance(c, TextContent) for c in content):
            failure = DeepResearchFailed(
                f"Google research interaction {state.interaction_id} completed with no report text.",
                status="empty",
                interaction_id=state.interaction_id,
            )
            attach_billed_usage(failure, usage)
            mark_billing_checked(failure)
            raise failure

        # Live text was streamed as it arrived; anything the stream missed
        # (a resume gap, or a polled run) is in the final message, which is
        # what persists and what every viewer renders on reload.
        response = UnifiedResponse(
            messages=[
                UnifiedMessage(
                    role="assistant",
                    content=content,
                    metadata={
                        "finish_reason": "stop",
                        "google_interaction_id": state.interaction_id,
                    },
                )
            ],
            usage=usage,
            finish_reason="stop",
            metadata={"google_interaction_id": state.interaction_id},
        )
        await emit_citations_from_response(response, emitter, "GOOGLE")
        await self._emit_images(response, emitter)
        return response

    # ── transport ────────────────────────────────────────────────────────

    async def _run(self, kwargs: dict[str, Any], state: _RunState, emitter: Any, info: Any) -> None:
        if emitter:
            await emitter.send_info(
                info(
                    code="research_started",
                    system_message="Deep Research started.",
                    user_message="Research started. This usually takes several minutes.",
                )
            )
        with warnings.catch_warnings():
            warnings.filterwarnings(
                "ignore", message="Interactions usage is experimental.*", category=UserWarning
            )
            stream = await self._interactions.create(**kwargs, stream=True)
        resumes = 0
        while True:
            try:
                async for event in stream:
                    await self._relay(event, state, emitter, info)
                    if state.terminal:
                        return
                if state.terminal:
                    return
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001 — a dropped stream is resumed, not fatal
                vcprint(
                    f"[google research] stream for {state.interaction_id} dropped: {exc}",
                    color="yellow",
                )
            if state.interaction_id is None:
                raise RuntimeError("Google closed the research stream before naming the interaction.")
            resumes += 1
            if resumes > MAX_STREAM_RESUMES:
                await self._poll(state, emitter, info)
                return
            try:
                stream = await self._interactions.get(
                    id=state.interaction_id, stream=True, last_event_id=state.last_event_id
                )
            except asyncio.CancelledError:
                raise
            except Exception as exc:  # noqa: BLE001 — resuming failed; polling still works
                vcprint(
                    f"[google research] resume of {state.interaction_id} failed ({exc}); polling",
                    color="yellow",
                )
                await self._poll(state, emitter, info)
                return

    async def _poll(self, state: _RunState, emitter: Any, info: Any) -> None:
        failures = 0
        while True:
            try:
                snapshot = await self._interactions.get(id=state.interaction_id)
                failures = 0
            except asyncio.CancelledError:
                raise
            except Exception:
                failures += 1
                if failures >= MAX_CONSECUTIVE_TRANSPORT_FAILURES:
                    raise
                await asyncio.sleep(POLL_SECONDS)
                continue
            if _status(snapshot) in _TERMINAL:
                state.terminal = True
                state.final = snapshot
                return
            await asyncio.sleep(POLL_SECONDS)

    async def _final(self, state: _RunState) -> Any:
        """The authoritative finished interaction (read once, retried on transport)."""
        if state.interaction_id is None:
            raise RuntimeError("The research stream ended before Google named the interaction.")
        failures = 0
        while True:
            try:
                snapshot = await self._interactions.get(id=state.interaction_id)
            except asyncio.CancelledError:
                raise
            except Exception:
                failures += 1
                if failures >= MAX_CONSECUTIVE_TRANSPORT_FAILURES:
                    raise
                await asyncio.sleep(POLL_SECONDS)
                continue
            if _status(snapshot) in _TERMINAL:
                return snapshot
            # The stream said done but the record is still settling.
            await asyncio.sleep(POLL_SECONDS)

    async def _relay(self, event: Any, state: _RunState, emitter: Any, info: Any) -> None:
        event_id = _get(event, "event_id")
        if event_id:
            state.last_event_id = event_id
        event_type = _get(event, "event_type")
        if event_type in ("interaction.created", "interaction.completed"):
            interaction = _get(event, "interaction")
            if state.interaction_id is None and _get(interaction, "id"):
                state.interaction_id = _get(interaction, "id")
                vcprint(
                    f"[google research] interaction {state.interaction_id} started",
                    color="cyan",
                )
                if emitter:
                    await emitter.send_info(
                        info(
                            code="research_interaction",
                            system_message=f"Google interaction {state.interaction_id}",
                            user_message="Researching. Progress and findings stream here.",
                        )
                    )
            if event_type == "interaction.completed" or _status(interaction) in _TERMINAL:
                state.terminal = True
            return
        if event_type == "interaction.status_update":
            state.interaction_id = state.interaction_id or _get(event, "interaction_id")
            if _status(event) in _TERMINAL:
                state.terminal = True
            return
        if event_type == "error":
            vcprint(f"[google research] provider error event: {_get(event, 'error')}", color="red")
            return
        if not emitter:
            return
        if event_type == "step.start":
            step = _get(event, "step")
            if _get(step, "type") == "google_search_call":
                queries = _get(_get(step, "arguments"), "queries") or []
                if queries:
                    await emitter.send_info(
                        info(
                            code="research_progress",
                            system_message="Searching the web.",
                            user_message="Searching: " + "; ".join(str(q) for q in queries[:3]),
                        )
                    )
            return
        if event_type != "step.delta":
            return
        delta = _get(event, "delta")
        delta_type = _get(delta, "type")
        if delta_type == "thought_summary":
            text = _get(_get(delta, "content"), "text")
            if text:
                # ONE reasoning block for the whole research phase: open it on
                # the first thought, keep appending, close it when the report
                # starts (a wrapper per summary drew ten "Thought process"
                # boxes for one run).
                await self._reasoning(emitter, started=True)
                await emitter.send_chunk(f"{str(text).strip()}\n\n")
        elif delta_type == "text":
            text = _get(delta, "text")
            if text:
                await self._reasoning(emitter, started=False)
                await emitter.send_chunk(str(text))
        await asyncio.sleep(0)

    @staticmethod
    async def _reasoning(emitter: Any, *, started: bool) -> None:
        from matrx_ai.providers.reasoning_stream_state import reasoning_state_for

        state = reasoning_state_for(emitter)
        if started:
            if not state.signaled:
                state.signaled = True
                await emitter.send_reasoning_state("started")
            if not state.open:
                state.open = True
                await emitter.send_chunk("\n<reasoning>\n")
            return
        if state.open:
            state.open = False
            await emitter.send_chunk("\n</reasoning>\n")
        if state.signaled:
            state.signaled = False
            await emitter.send_reasoning_state("stopped")

    async def _cancel_quietly(self, state: _RunState) -> None:
        if not state.interaction_id:
            return
        try:
            await asyncio.shield(self._interactions.cancel(id=state.interaction_id))
        except Exception as exc:  # noqa: BLE001 — the cancel is best-effort and announced
            vcprint(
                f"[google research] could not cancel interaction {state.interaction_id}: {exc}",
                color="red",
            )

    async def _attach_usage(
        self,
        exc: BaseException,
        state: _RunState,
        profile: Any,
        attach_billed_usage: Any,
        mark_billing_checked: Any,
    ) -> None:
        """Whatever Google billed so far rides the failure, so a failed or
        cancelled research never records $0."""
        usage = None
        if state.interaction_id:
            try:
                snapshot = state.final or await asyncio.shield(
                    self._interactions.get(id=state.interaction_id)
                )
                usage = research_usage(
                    snapshot,
                    model_name=profile.model_name,
                    provider_model_name=profile.provider_model_id,
                )
            except Exception:  # noqa: BLE001 — usage capture never replaces the failure
                usage = None
        attach_billed_usage(exc, usage)
        mark_billing_checked(exc)

    @staticmethod
    async def _emit_images(response: UnifiedResponse, emitter: Any) -> None:
        if not emitter:
            return
        from matrx_connect.context.data_types import MediaBlockData
        from matrx_connect.context.media_block import cloud_file_to_media_block

        for message in response.messages:
            for item in message.content:
                if isinstance(item, ImageContent) and item.file_id:
                    block = cloud_file_to_media_block(
                        {
                            "id": item.file_id,
                            "storage_uri": item.file_uri,
                            "mime_type": item.mime_type,
                            "size_bytes": item.file_size,
                            "metadata": dict(item.metadata or {}),
                        },
                        kind_override="image",
                    )
                    await emitter.send_data(MediaBlockData(block=block))


class _RunState:
    __slots__ = ("final", "interaction_id", "last_event_id", "terminal")

    def __init__(self) -> None:
        self.interaction_id: str | None = None
        self.last_event_id: str | None = None
        self.terminal = False
        self.final: Any = None


__all__ = [
    "DeepResearchFailed",
    "GoogleDeepResearchAgent",
    "build_research_kwargs",
    "research_content",
    "research_input",
    "research_usage",
    "is_google_research_agent",
]
