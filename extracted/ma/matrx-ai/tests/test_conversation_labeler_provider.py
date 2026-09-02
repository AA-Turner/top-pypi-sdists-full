from types import SimpleNamespace

import matrx_ai.agent_runners.conversation_labeler as labeler


async def test_labeler_uses_groq_recommended_production_replacement(monkeypatch) -> None:
    captured: dict = {}

    class _Completions:
        async def create(self, **kwargs):
            captured.update(kwargs)
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(
                            content='{"label":"Fixed","description":"Works","keywords":[]}'
                        )
                    )
                ]
            )

    class _Client:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=_Completions())

    monkeypatch.setattr(labeler, "AsyncGroq", _Client)
    monkeypatch.setattr("matrx_ai.providers.keys.resolve_api_key", lambda _: "test-key")

    result = await labeler._call_groq_direct("system", "user")

    assert result.success is True
    assert captured["model"] == "openai/gpt-oss-20b"
    assert captured["max_tokens"] == 2048
    assert captured["reasoning_effort"] == "low"
    assert captured["response_format"] == {"type": "json_object"}


async def test_labeler_budget_allows_reasoning_before_valid_json(monkeypatch) -> None:
    """Regress the provider's json_validate_failed capacity boundary."""
    calls: list[dict] = []

    class _Completions:
        async def create(self, **kwargs):
            calls.append(kwargs)
            if kwargs["max_tokens"] < 2048:
                raise RuntimeError("json_validate_failed: completion budget exhausted")
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(
                            content='{"label":"Budgeted","description":"Valid","keywords":[]}'
                        )
                    )
                ]
            )

    class _Client:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=_Completions())

    monkeypatch.setattr(labeler, "AsyncGroq", _Client)
    monkeypatch.setattr("matrx_ai.providers.keys.resolve_api_key", lambda _: "test-key")

    result = await labeler._call_groq_direct("system", "user")

    assert result.success is True
    assert len(calls) == 1
    assert calls[0]["max_tokens"] == 2048


def test_agent_labeler_bounds_every_untrusted_prompt_section() -> None:
    """Regress the provider TPM failure caused by a 227K-character prompt."""
    huge = "distinct-start " + ("x" * 120_000) + " distinct-end"

    prompt = labeler._build_system_prompt(
        recent_titles=huge,
        agent_name=huge,
        agent_description=huge,
        user_variables=huge,
        user_prompt=huge,
    )

    assert len(prompt) < 20_000
    assert prompt.count("[... content trimmed ...]") == 5
    assert "distinct-start" in prompt
    assert "distinct-end" in prompt


async def test_oversized_agent_context_stays_below_provider_admission_boundary(
    monkeypatch,
) -> None:
    huge = "distinct-start " + ("x" * 120_000) + " distinct-end"

    class _Completions:
        async def create(self, **kwargs):
            prompt_chars = sum(len(message["content"]) for message in kwargs["messages"])
            if prompt_chars >= 30_000:
                raise RuntimeError("simulated provider TPM admission rejection")
            return SimpleNamespace(
                choices=[
                    SimpleNamespace(
                        message=SimpleNamespace(
                            content='{"label":"Bounded","description":"Works","keywords":[]}'
                        )
                    )
                ]
            )

    class _Client:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=_Completions())

    monkeypatch.setattr(labeler, "AsyncGroq", _Client)
    monkeypatch.setattr("matrx_ai.providers.keys.resolve_api_key", lambda _: "test-key")

    result = await labeler.label_agent_conversation(
        conversation_content=labeler._trim_content(huge, 5000),
        recent_titles=huge,
        agent_name=huge,
        agent_description=huge,
        user_variables=huge,
        user_prompt=huge,
    )

    assert result.success is True


async def test_labeler_failure_reaches_central_capture(monkeypatch) -> None:
    captured: dict = {}

    class _Completions:
        async def create(self, **kwargs):
            raise RuntimeError("provider model unavailable")

    class _Client:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=_Completions())

    async def _capture(exc, *, kind, **fields):
        captured.update({"exc": exc, "kind": kind, **fields})

    monkeypatch.setattr(labeler, "AsyncGroq", _Client)
    monkeypatch.setattr("matrx_ai.providers.keys.resolve_api_key", lambda _: "test-key")
    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", _capture)

    result = await labeler._call_groq_direct("system", "user")

    assert result.success is False
    assert result.error == "provider model unavailable"
    assert captured["kind"] == "conversation_labeler_failed"
    assert captured["payload"]["model"] == "openai/gpt-oss-20b"


async def test_labeler_client_initialization_failure_is_captured(monkeypatch) -> None:
    captured: dict = {}

    class _BrokenClient:
        def __init__(self, **kwargs):
            raise RuntimeError("missing provider credential")

    async def _capture(exc, *, kind, **fields):
        captured.update({"exc": exc, "kind": kind, **fields})

    monkeypatch.setattr(labeler, "AsyncGroq", _BrokenClient)
    monkeypatch.setattr("matrx_ai.providers.keys.resolve_api_key", lambda _: None)
    monkeypatch.setattr("matrx_connect.streaming.error_capture.capture_error", _capture)

    result = await labeler._call_groq_direct("system", "user")

    assert result.success is False
    assert result.error == "missing provider credential"
    assert captured["kind"] == "conversation_labeler_failed"
