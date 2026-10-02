"""OpenAI Agents SDK handler for Bitfab tracing.

The OpenAI Agents SDK is instrumented in two layers:

  1. A process-wide tracing processor (see ``get_openai_tracing_processor`` /
     ``BitfabOpenAITracingProcessor``) registered once with
     ``add_trace_processor``. It captures everything *inside* a run (LLM calls,
     tool calls, handoffs) as Bitfab spans.
  2. This handler's ``wrap_run``, which owns the *root*. The processor never
     sees the caller's input (the SDK's trace events don't carry it), so a
     processor-only run records a root span with an empty input and is not
     replayable. ``wrap_run`` is a thin drop-in for ``Runner.run`` that opens a
     ``@bitfab.span`` root carrying the input and final output, so the run is
     replayable with no hand-written ``@span``. The processor's spans nest
     underneath it automatically (it remaps onto the active span context).

When ``wrap_run`` runs inside an enclosing Bitfab span (the replay auto-wrap,
or a caller's own ``@span``), that span is already the replayable root: the
handler skips opening a second one and lets the processor nest the run's spans
under the existing root. This mirrors the Claude Agent SDK and LangGraph
handlers, which no-op their root span under an enclosing span, and keeps a
replayed run's span tree identical to the original (no doubled root agent span).

Use both together: register the processor once at startup, then call
``await handler.wrap_run(agent, input)`` in place of
``await Runner.run(agent, input)``.
"""

from __future__ import annotations

from typing import Any, Callable


class BitfabOpenAIAgentHandler:
    """OpenAI Agents SDK handler that records a replayable root span.

    Example::

        from bitfab import Bitfab
        from agents import Agent, Runner, add_trace_processor

        bitfab = Bitfab(api_key="your-api-key")
        add_trace_processor(bitfab.get_openai_tracing_processor())

        agent = Agent(name="Researcher", instructions="...")
        handler = bitfab.get_openai_agent_handler("research-topic")

        # Swap Runner.run(agent, input) -> handler.wrap_run(agent, input)
        result = await handler.wrap_run(agent, "Find X")
        return result.final_output
    """

    def __init__(
        self,
        *,
        client: Any,
        trace_function_key: str,
        get_active_span_context: Callable[[], Any] | None = None,
    ) -> None:
        # `client` is the Bitfab client; typed loosely to avoid an import cycle
        # (client.py constructs this handler). Only its `span` decorator is used.
        self._client = client
        self._trace_function_key = trace_function_key
        # Returns the active Bitfab span context (or None) so wrap_run can detect
        # an enclosing span and skip opening its own root. Injected by the client
        # alongside the tracing processor, which nests under the same context.
        self._get_active_span_context = get_active_span_context

    def _inside_enclosing_span(self) -> bool:
        """True when a Bitfab span is already open around this run.

        The enclosing span (the replay auto-wrap, or a caller's own ``@span``)
        is the replayable root; opening another here would double the root agent
        span. The tracing processor nests the run's spans under whichever span is
        active, so skipping ours keeps the tree correct.
        """
        return (
            self._get_active_span_context is not None
            and self._get_active_span_context() is not None
        )

    async def wrap_run(self, agent: Any, input: Any, **run_kwargs: Any) -> Any:
        """Drop-in replacement for ``Runner.run`` that records a replayable root.

        The ``input`` is captured as the root span's input (as a single
        positional argument, so ``replay(key, fn)`` re-feeds it), and the run's
        ``final_output`` is recorded as the root output.

        The process-wide tracing processor (``get_openai_tracing_processor``)
        must still be registered: it captures the LLM/tool/handoff spans that
        nest beneath this root.

        Args:
            agent: The OpenAI Agents SDK ``Agent`` to run.
            input: The run input (string or input items). Recorded as the
                replayable root input.
            **run_kwargs: Forwarded verbatim to ``Runner.run`` (e.g. ``context``,
                ``max_turns``, ``run_config``, ``hooks``).

        Returns:
            The ``RunResult`` from ``Runner.run``, unchanged.
        """
        # Imported here so `agents` stays an optional dependency: importing this
        # module never requires openai-agents, only calling wrap_run does.
        from agents import Runner

        # An enclosing span is already the replayable root: run directly and let
        # the processor nest the run's spans under it, instead of opening (and
        # doubling) a second root agent span.
        if self._inside_enclosing_span():
            return await Runner.run(agent, input, **run_kwargs)

        def _finalize(result: Any) -> Any:
            # Record the final answer, not the (non-serializable) RunResult.
            return getattr(result, "final_output", None)

        @self._client._span_impl(
            self._trace_function_key,
            name=self._trace_function_key,
            type="agent",
            finalize=_finalize,
            surface="opt-in",
            instrumentation="openai-agents",
        )
        async def _run(agent_input: Any) -> Any:
            # Runner.run executes inside the span context, so the tracing
            # processor's on_trace_start sees this root and nests the run's
            # internal spans beneath it.
            return await Runner.run(agent, agent_input, **run_kwargs)

        return await _run(input)

    async def wrap_run_streamed(self, agent: Any, input: Any, **run_kwargs: Any) -> Any:
        """Drop-in replacement for ``Runner.run_streamed`` that traces a streamed
        run.

        Unlike ``Runner.run_streamed`` (which returns a ``RunResultStreaming``
        the caller drains), this is an **async generator**: iterate it to consume
        the same stream events, while Bitfab records a root ``agent`` span around
        the run. The ``input`` is captured as the root input and the run's
        ``final_output`` (available once the stream drains) as the root output;
        the span stays open for the whole iteration, so the process-wide tracing
        processor nests the run's LLM/tool/handoff spans beneath this root.

        Example::

            handler = bitfab.get_openai_agent_handler("research-topic")
            async for event in handler.wrap_run_streamed(agent, "Find X"):
                ...  # handle each streamed event

        Args:
            agent: The OpenAI Agents SDK ``Agent`` to run.
            input: The run input (string or input items). Recorded as the
                root input.
            **run_kwargs: Forwarded verbatim to ``Runner.run_streamed`` (e.g.
                ``context``, ``max_turns``, ``run_config``, ``hooks``).

        Yields:
            Each event from the run's ``stream_events()``, unchanged.

        Note:
            Fully iterate the generator to guarantee the span is recorded. If
            you break early, the run's span is best-effort (Python finalizes the
            abandoned generator later), and the recorded output may be missing.

            ``bitfab.replay()`` does not drive this async generator: to replay a
            recorded run as a regression, use the non-streaming ``wrap_run``
            (a coroutine), which replay re-runs directly.
        """
        # Imported here so `agents` stays an optional dependency: importing this
        # module never requires openai-agents, only calling wrap_run_streamed does.
        from agents import Runner

        # An enclosing span is already the replayable root: stream directly and
        # let the processor nest the run's spans under it, instead of opening
        # (and doubling) a second root agent span.
        if self._inside_enclosing_span():
            result = Runner.run_streamed(agent, input, **run_kwargs)
            async for event in result.stream_events():
                yield event
            return

        captured: dict[str, Any] = {}

        def _finalize(_events: Any) -> Any:
            # Record the run's final answer (ready once the stream has drained),
            # not the collected events or the non-serializable result object.
            result = captured.get("result")
            return getattr(result, "final_output", None) if result else None

        @self._client._span_impl(
            self._trace_function_key,
            name=self._trace_function_key,
            type="agent",
            finalize=_finalize,
            surface="opt-in",
            instrumentation="openai-agents",
        )
        async def _run_streamed(agent_input: Any) -> Any:
            # Runner.run_streamed starts the run in a background task created
            # inside this span context, so the tracing processor's
            # on_trace_start nests the run's internal spans beneath this root.
            # Draining happens here, inside the span context, so the span stays
            # open until the stream completes.
            result = Runner.run_streamed(agent, agent_input, **run_kwargs)
            captured["result"] = result
            async for event in result.stream_events():
                yield event

        async for event in _run_streamed(input):
            yield event
