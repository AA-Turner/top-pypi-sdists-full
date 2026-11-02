from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class FakeEmitter:
    """Minimal Emitter stand-in for tests.

    Records every call as ``(method_name, payload_dict)`` so tests can assert
    against exact event sequences without standing up the real NDJSON queue.

    It implements the WHOLE ``matrx_connect.context.emitter_protocol.Emitter``
    protocol, and ``test_fake_emitter_satisfies_protocol`` fails the moment it
    stops doing so. A partial fake is a trap for anything that drives real
    provider code: the LLM path calls ``send_warning`` on a degraded provider
    response, and a missing method there surfaced as a non-retryable
    ``AttributeError`` that errored a whole judge-tier run — a harness hole
    wearing the costume of a product failure.
    """

    events: list[tuple[str, Any]] = field(default_factory=list)

    async def send_chunk(self, text: str) -> None:
        self.events.append(("chunk", text))

    async def send_reasoning_chunk(self, text: str) -> None:
        self.events.append(("reasoning_chunk", text))

    async def send_phase(self, phase: Any) -> None:
        self.events.append(("phase", phase))

    async def send_data(self, payload: Any) -> None:
        # The scheduler emits TYPED WorkflowEvent models; the wire edge (a
        # host emitter) is where they become dicts. Mirror that here so the
        # suite keeps asserting against the JSON wire shape.
        if hasattr(payload, "model_dump"):
            payload = payload.model_dump(mode="json")
        self.events.append(("data", payload))

    async def send_init(self, payload: Any) -> None:
        self.events.append(("init", payload))

    async def send_completion(self, payload: Any) -> None:
        self.events.append(("completion", payload))

    async def send_error(self, *args: Any, **kwargs: Any) -> None:
        self.events.append(("error", {"args": args, "kwargs": kwargs}))

    async def send_tool_event(self, event_data: Any) -> None:
        self.events.append(("tool_event", event_data))

    async def send_end(self, reason: str = "complete") -> None:
        self.events.append(("end", reason))

    async def send_warning(self, payload: Any) -> None:
        self.events.append(("warning", payload))

    async def send_info(self, payload: Any) -> None:
        self.events.append(("info", payload))

    async def send_reasoning_state(self, state: Any) -> None:
        self.events.append(("reasoning_state", state))

    async def send_record_reserved(self, payload: Any) -> None:
        self.events.append(("record_reserved", payload))

    async def send_record_update(self, payload: Any) -> None:
        self.events.append(("record_update", payload))

    async def send_resource_changed(self, **kwargs: Any) -> None:
        self.events.append(("resource_changed", kwargs))

    async def send_structured_output(self, payload: Any) -> None:
        self.events.append(("structured_output", payload))

    async def send_injection_consumed(self, payload: Any) -> None:
        self.events.append(("injection_consumed", payload))

    async def send_provider_retry(self, payload: Any) -> None:
        self.events.append(("provider_retry", payload))

    async def send_citation(self, payload: Any) -> None:
        self.events.append(("citation", payload))

    async def send_context_analysis(self, payload: Any) -> None:
        self.events.append(("context_analysis", payload))

    async def send_context_state(self, payload: Any) -> None:
        self.events.append(("context_state", payload))

    async def send_context_trimmed(self, payload: Any) -> None:
        self.events.append(("context_trimmed", payload))

    async def send_cancelled(self) -> None:
        self.events.append(("cancelled", None))

    async def fatal_error(self, *args: Any, **kwargs: Any) -> None:
        self.events.append(("fatal_error", {"args": args, "kwargs": kwargs}))

    def reset_turn_text(self) -> None:
        self._turn_text = ""

    def get_turn_text(self) -> str:
        return "".join(text for kind, text in self.events if kind == "chunk")

    def kinds(self) -> list[str]:
        return [kind for kind, _ in self.events]


def make_app_context(
    emitter: FakeEmitter | None = None,
    initial_variables: dict[str, Any] | None = None,
    *,
    user_id: str = "test-user",
    conversation_id: str = "test-conv",
    request_id: str = "test-req",
) -> Any:
    """Construct an AppContext stand-in suitable for driving the scheduler.

    Uses the real AppContext so fork_for_workflow_step semantics are exercised.
    ``initial_variables`` are the run variables behind {'$var': name}
    references in node static inputs.

    ``user_id``/``conversation_id``/``request_id`` default to the opaque
    unit-test strings — fine for the level1 tier, which never reaches
    persistence. Any test that drives a REAL ``ai.llm.chat`` node must pass
    UUIDs for all three: the conversation gate rejects a non-UUID user outright
    (``ConversationGateError``), and ``chat.request_snapshot`` /
    ``chat.request`` are uuid-typed, so the defaults fail the run — and then
    the write — for reasons that have nothing to do with what the test checks.
    """
    from matrx_connect.context.app_context import AppContext

    return AppContext(
        emitter=emitter or FakeEmitter(),
        user_id=user_id,
        is_authenticated=True,
        conversation_id=conversation_id,
        request_id=request_id,
        initial_variables=dict(initial_variables or {}),
    )
