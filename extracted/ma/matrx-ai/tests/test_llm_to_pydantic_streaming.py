"""``llm_to_pydantic`` streaming + wire-kind tagging — additive display only.

The contract (built for content-plan deepen, generic to every strict-JSON call):

1. ``on_delta`` receives every answer token of the FIRST attempt, so a caller
   can put the structured output on its live stream while validation stays on
   the final text.
2. Those tokens never ALSO reach the wrapped emitter — the caller decides what
   goes on the wire (deepen forwards them; a judge passes ``on_delta=None``).
3. ``wire_kind`` injects a REQUIRED ``__kind`` const as the FIRST property of
   the provider-enforced schema (a natively-enforcing provider would otherwise
   forbid the model from emitting it) and strips it before Pydantic validation,
   so ``extra="forbid"`` output classes stay valid and persisted shapes never
   carry the tag.
4. The validation-repair retry is NOT streamed: the client already rendered the
   first attempt's bytes; appending a second JSON object would corrupt it.
"""

from __future__ import annotations

import pytest
from pydantic import BaseModel, ConfigDict

from matrx_ai.graph_nodes import _strict_json
from matrx_ai.graph_nodes._strict_json import llm_to_pydantic


class _RecordingEmitter:
    def __init__(self) -> None:
        self.chunks: list[str] = []

    async def send_chunk(self, text: str) -> None:
        self.chunks.append(text)


class _Brief(BaseModel):
    model_config = ConfigDict(extra="forbid")

    brief: list[str]


def _install_ctx(monkeypatch, emitter):
    from matrx_connect.context.app_context import get_app_context, set_app_context

    try:
        ctx = get_app_context().with_overrides(emitter=emitter)
    except Exception:
        from matrx_connect.context.app_context import AppContext

        ctx = AppContext(user_id="u", emitter=emitter)  # type: ignore[call-arg]
    set_app_context(ctx)


async def test_first_attempt_streams_and_wire_kind_is_schema_backed(monkeypatch):
    base = _RecordingEmitter()
    seen: list[str] = []
    captured_formats: list[object] = []

    payload = '{"__kind": "page_brief", "brief": ["line one", "line two"]}'

    async def _fake_run_completion(messages, system_text, **kwargs):
        from matrx_connect.context.app_context import get_app_context

        captured_formats.append(kwargs.get("response_format"))
        emitter = get_app_context().emitter
        for i in range(0, len(payload), 7):
            await emitter.send_chunk(payload[i : i + 7])
        return payload, "stop"

    monkeypatch.setattr(_strict_json, "_run_completion", _fake_run_completion)
    _install_ctx(monkeypatch, base)

    async def _on_delta(text: str) -> None:
        seen.append(text)

    result = await llm_to_pydantic(
        model="m",
        system="s",
        user="u",
        output_cls=_Brief,
        on_delta=_on_delta,
        wire_kind="page_brief",
    )

    # 1. every token reached the caller; 2. none leaked onto the wire directly
    assert "".join(seen) == payload
    assert base.chunks == []
    # 3a. the tag was stripped before validation (extra="forbid" would raise)
    assert result.brief == ["line one", "line two"]
    # 3b. the ENFORCED schema carries __kind first and required — a provider
    # that validates server-side must permit (and steer) the tag
    fmt = captured_formats[0]
    schema = fmt["json_schema"]["schema"]
    assert next(iter(schema["properties"])) == "__kind"
    assert schema["properties"]["__kind"] == {"type": "string", "enum": ["page_brief"]}
    assert schema["required"][0] == "__kind"


async def test_repair_retry_is_not_streamed(monkeypatch):
    base = _RecordingEmitter()
    seen: list[str] = []
    calls: list[str] = []

    async def _fake_run_completion(messages, system_text, **kwargs):
        from matrx_connect.context.app_context import get_app_context

        emitter = get_app_context().emitter
        if not calls:
            calls.append("first")
            broken = '{"__kind": "page_brief", "brief": "not-a-list"}'
            await emitter.send_chunk(broken)
            return broken, "stop"
        calls.append("second")
        fixed = '{"__kind": "page_brief", "brief": ["fixed"]}'
        await emitter.send_chunk(fixed)  # provider still streams; wrapper must mute
        return fixed, "stop"

    monkeypatch.setattr(_strict_json, "_run_completion", _fake_run_completion)
    _install_ctx(monkeypatch, base)

    async def _on_delta(text: str) -> None:
        seen.append(text)

    result = await llm_to_pydantic(
        model="m",
        system="s",
        user="u",
        output_cls=_Brief,
        on_delta=_on_delta,
        wire_kind="page_brief",
    )

    assert calls == ["first", "second"]
    assert result.brief == ["fixed"]
    # 4. only the FIRST attempt's bytes reached the caller's stream
    assert "".join(seen) == '{"__kind": "page_brief", "brief": "not-a-list"}'
    assert base.chunks == []


async def test_no_kwargs_means_no_behavior_change(monkeypatch):
    """The default call is byte-identical to the pre-streaming funnel: chunks
    suppressed, schema untouched (no __kind anywhere)."""
    base = _RecordingEmitter()
    captured_formats: list[object] = []

    async def _fake_run_completion(messages, system_text, **kwargs):
        from matrx_connect.context.app_context import get_app_context

        captured_formats.append(kwargs.get("response_format"))
        assert "__kind" not in system_text
        await get_app_context().emitter.send_chunk("internal")
        return '{"brief": ["a"]}', "stop"

    monkeypatch.setattr(_strict_json, "_run_completion", _fake_run_completion)
    _install_ctx(monkeypatch, base)

    result = await llm_to_pydantic(model="m", system="s", user="u", output_cls=_Brief)

    assert result.brief == ["a"]
    assert base.chunks == []
    schema = captured_formats[0]["json_schema"]["schema"]
    assert "__kind" not in schema["properties"]


@pytest.fixture(autouse=True)
def _clear_ctx():
    yield
    from matrx_connect.context.app_context import clear_app_context

    try:
        clear_app_context()
    except Exception:
        pass
