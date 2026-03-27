"""Tests for workflow LLM response caching (#988).

Tests cover cache key computation, get/put round-trip, TTL expiry,
space isolation, cache hit/miss integration with the engine,
structured output through cache, fallback+cache interaction,
cache disabled no-op, invalidation, and field parsing/validation.
"""

from __future__ import annotations

import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from unittest.mock import AsyncMock, MagicMock

import pytest

from anteroom.config import WorkflowConfig
from anteroom.db import init_db
from anteroom.services.workflow_cache import (
    compute_cache_key,
    get_cached_response,
    invalidate_cache,
    put_cached_response,
)
from anteroom.services.workflow_engine import (
    WorkflowEngine,
    load_definition,
    register_gate_condition,
)
from anteroom.services.workflow_runners import create_default_registry
from anteroom.services.workflow_storage import list_workflow_steps

# ---------------------------------------------------------------------------
# Test YAML definitions
# ---------------------------------------------------------------------------

LLM_CACHE_WORKFLOW = """\
kind: workflow
id: test_llm_cache
version: 0.1.0
inputs: {}
steps:
  - id: summarize
    type: llm
    prompt: "Summarize this"
    model: primary-model
    cache:
      enabled: true
      ttl: 3600
"""

LLM_CACHE_NO_TTL_WORKFLOW = """\
kind: workflow
id: test_llm_cache_no_ttl
version: 0.1.0
inputs: {}
steps:
  - id: summarize
    type: llm
    prompt: "Summarize this"
    model: primary-model
    cache:
      enabled: true
"""

LLM_CACHE_DISABLED_WORKFLOW = """\
kind: workflow
id: test_llm_cache_disabled
version: 0.1.0
inputs: {}
steps:
  - id: summarize
    type: llm
    prompt: "Summarize this"
    model: primary-model
    cache:
      enabled: false
"""

LLM_NO_CACHE_WORKFLOW = """\
kind: workflow
id: test_llm_no_cache
version: 0.1.0
inputs: {}
steps:
  - id: summarize
    type: llm
    prompt: "Summarize this"
    model: primary-model
"""

LLM_CACHE_JSON_WORKFLOW = """\
kind: workflow
id: test_llm_cache_json
version: 0.1.0
inputs: {}
steps:
  - id: classify
    type: llm
    prompt: "Classify this"
    model: primary-model
    response_format: json_object
    cache:
      enabled: true
      ttl: 600
"""

LLM_CACHE_FALLBACK_WORKFLOW = """\
kind: workflow
id: test_llm_cache_fallback
version: 0.1.0
inputs: {}
steps:
  - id: summarize
    type: llm
    prompt: "Summarize this"
    model: primary-model
    cache:
      enabled: true
      ttl: 3600
    fallback:
      - model: fallback-model-1
"""

LLM_CACHE_BAD_TTL_WORKFLOW = """\
kind: workflow
id: test_llm_cache_bad_ttl
version: 0.1.0
inputs: {}
steps:
  - id: summarize
    type: llm
    prompt: "Summarize this"
    cache:
      enabled: true
      ttl: -5
"""

LLM_CACHE_BAD_ENABLED_WORKFLOW = """\
kind: workflow
id: test_llm_cache_bad_enabled
version: 0.1.0
inputs: {}
steps:
  - id: summarize
    type: llm
    prompt: "Summarize this"
    cache:
      enabled: "yes"
"""

LLM_CACHE_MISSING_ENABLED_WORKFLOW = """\
kind: workflow
id: test_llm_cache_missing_enabled
version: 0.1.0
inputs: {}
steps:
  - id: summarize
    type: llm
    prompt: "Summarize this"
    cache:
      ttl: 3600
"""

LLM_CACHE_ON_RUNNER_WORKFLOW = """\
kind: workflow
id: test_cache_on_runner
version: 0.1.0
inputs: {}
steps:
  - id: run_it
    type: runner
    runner: shell
    command: "echo hi"
    cache:
      enabled: true
"""


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db():
    with tempfile.TemporaryDirectory() as td:
        conn = init_db(Path(td) / "test.db")
        yield conn
        conn.close()


def _make_ai_service(
    response_text: str = "LLM response",
    usage: dict[str, int] | None = None,
    model: str = "primary-model",
) -> MagicMock:
    if usage is None:
        usage = {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
    svc = MagicMock()
    svc.config = MagicMock()
    svc.config.model = model
    svc.config.provider = "openai"
    svc.complete_with_usage = AsyncMock(return_value=(response_text, usage))
    return svc


@pytest.fixture()
def ai_service() -> MagicMock:
    return _make_ai_service()


@pytest.fixture()
def engine(db: Any, ai_service: MagicMock) -> WorkflowEngine:
    config = WorkflowConfig()
    registry = create_default_registry()
    return WorkflowEngine(db, config, registry, ai_service=ai_service)


# ---------------------------------------------------------------------------
# Unit tests for workflow_cache module
# ---------------------------------------------------------------------------


class TestComputeCacheKey:
    def test_deterministic(self) -> None:
        key1 = compute_cache_key("m", "p", "s", 0.5, 100, None)
        key2 = compute_cache_key("m", "p", "s", 0.5, 100, None)
        assert key1 == key2

    def test_different_model(self) -> None:
        k1 = compute_cache_key("model-a", "p", "s", 0.5, 100, None)
        k2 = compute_cache_key("model-b", "p", "s", 0.5, 100, None)
        assert k1 != k2

    def test_different_prompt(self) -> None:
        k1 = compute_cache_key("m", "prompt1", "s", 0.5, 100, None)
        k2 = compute_cache_key("m", "prompt2", "s", 0.5, 100, None)
        assert k1 != k2

    def test_different_temperature(self) -> None:
        k1 = compute_cache_key("m", "p", "s", 0.5, 100, None)
        k2 = compute_cache_key("m", "p", "s", 0.7, 100, None)
        assert k1 != k2

    def test_different_max_tokens(self) -> None:
        k1 = compute_cache_key("m", "p", "s", 0.5, 100, None)
        k2 = compute_cache_key("m", "p", "s", 0.5, 200, None)
        assert k1 != k2

    def test_different_response_format(self) -> None:
        k1 = compute_cache_key("m", "p", "s", 0.5, 100, None)
        k2 = compute_cache_key("m", "p", "s", 0.5, 100, "json_object")
        assert k1 != k2

    def test_different_system_prompt(self) -> None:
        k1 = compute_cache_key("m", "p", "sys1", 0.5, 100, None)
        k2 = compute_cache_key("m", "p", "sys2", 0.5, 100, None)
        assert k1 != k2

    def test_key_is_hex_sha256(self) -> None:
        key = compute_cache_key("m", "p", "s", None, None, None)
        assert len(key) == 64
        assert all(c in "0123456789abcdef" for c in key)


class TestGetPutRoundTrip:
    def test_round_trip(self, db: Any) -> None:
        put_cached_response(
            db,
            cache_key="abc123",
            space_id="sp1",
            workflow_id="wf1",
            model="gpt-4",
            response="Hello world",
            prompt_tokens=10,
            completion_tokens=20,
            response_format=None,
            ttl_seconds=3600,
        )
        result = get_cached_response(db, "abc123", "sp1")
        assert result is not None
        assert result["response"] == "Hello world"
        assert result["prompt_tokens"] == 10
        assert result["completion_tokens"] == 20
        assert result["model"] == "gpt-4"
        assert result["response_format"] is None

    def test_miss_returns_none(self, db: Any) -> None:
        result = get_cached_response(db, "nonexistent", "sp1")
        assert result is None

    def test_space_isolation(self, db: Any) -> None:
        put_cached_response(
            db,
            cache_key="key1",
            space_id="space-a",
            workflow_id="wf1",
            model="m",
            response="response-a",
            prompt_tokens=1,
            completion_tokens=2,
            response_format=None,
            ttl_seconds=3600,
        )
        put_cached_response(
            db,
            cache_key="key1",
            space_id="space-b",
            workflow_id="wf1",
            model="m",
            response="response-b",
            prompt_tokens=3,
            completion_tokens=4,
            response_format=None,
            ttl_seconds=3600,
        )
        a = get_cached_response(db, "key1", "space-a")
        b = get_cached_response(db, "key1", "space-b")
        assert a is not None and a["response"] == "response-a"
        assert b is not None and b["response"] == "response-b"

    def test_ttl_expiry(self, db: Any) -> None:
        now = datetime.now(timezone.utc)
        expired = (now - timedelta(seconds=10)).isoformat()
        db.execute(
            "INSERT INTO workflow_llm_cache"
            " (cache_key, space_id, workflow_id, model, response, prompt_tokens,"
            " completion_tokens, response_format, created_at, expires_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("expired_key", "", "wf1", "m", "old", 1, 2, None, now.isoformat(), expired),
        )
        db.commit()
        result = get_cached_response(db, "expired_key", "")
        assert result is None

    def test_no_ttl_never_expires(self, db: Any) -> None:
        put_cached_response(
            db,
            cache_key="forever",
            space_id="",
            workflow_id="wf1",
            model="m",
            response="persistent",
            prompt_tokens=1,
            completion_tokens=2,
            response_format=None,
            ttl_seconds=0,
        )
        result = get_cached_response(db, "forever", "")
        assert result is not None
        assert result["response"] == "persistent"


class TestInvalidateCache:
    def test_invalidate_all(self, db: Any) -> None:
        for i in range(3):
            put_cached_response(
                db,
                cache_key=f"k{i}",
                space_id="sp",
                workflow_id="wf",
                model="m",
                response="r",
                prompt_tokens=0,
                completion_tokens=0,
                response_format=None,
                ttl_seconds=3600,
            )
        deleted = invalidate_cache(db)
        assert deleted == 3
        assert get_cached_response(db, "k0", "sp") is None

    def test_invalidate_by_space(self, db: Any) -> None:
        put_cached_response(
            db,
            cache_key="k1",
            space_id="keep",
            workflow_id="wf",
            model="m",
            response="r",
            prompt_tokens=0,
            completion_tokens=0,
            response_format=None,
            ttl_seconds=3600,
        )
        put_cached_response(
            db,
            cache_key="k2",
            space_id="delete",
            workflow_id="wf",
            model="m",
            response="r",
            prompt_tokens=0,
            completion_tokens=0,
            response_format=None,
            ttl_seconds=3600,
        )
        deleted = invalidate_cache(db, space_id="delete")
        assert deleted == 1
        assert get_cached_response(db, "k1", "keep") is not None
        assert get_cached_response(db, "k2", "delete") is None


# ---------------------------------------------------------------------------
# Parsing and validation tests
# ---------------------------------------------------------------------------


class TestCacheFieldParsing:
    def test_cache_parsed_correctly(self) -> None:
        defn = load_definition(LLM_CACHE_WORKFLOW)
        step = defn.steps[0]
        assert step.cache is not None
        assert step.cache["enabled"] is True
        assert step.cache["ttl"] == 3600

    def test_cache_default_ttl(self) -> None:
        defn = load_definition(LLM_CACHE_NO_TTL_WORKFLOW)
        step = defn.steps[0]
        assert step.cache is not None
        assert step.cache["enabled"] is True
        assert "ttl" not in step.cache

    def test_cache_disabled(self) -> None:
        defn = load_definition(LLM_CACHE_DISABLED_WORKFLOW)
        step = defn.steps[0]
        assert step.cache is not None
        assert step.cache["enabled"] is False

    def test_no_cache_field(self) -> None:
        defn = load_definition(LLM_NO_CACHE_WORKFLOW)
        step = defn.steps[0]
        assert step.cache is None

    def test_bad_ttl_rejected(self) -> None:
        with pytest.raises(ValueError, match="cache.ttl must be a non-negative integer"):
            load_definition(LLM_CACHE_BAD_TTL_WORKFLOW)

    def test_bad_enabled_rejected(self) -> None:
        with pytest.raises(ValueError, match="cache.enabled must be a boolean"):
            load_definition(LLM_CACHE_BAD_ENABLED_WORKFLOW)

    def test_missing_enabled_rejected(self) -> None:
        with pytest.raises(ValueError, match="cache.*must include an 'enabled' field"):
            load_definition(LLM_CACHE_MISSING_ENABLED_WORKFLOW)

    def test_cache_on_non_llm_rejected(self) -> None:
        with pytest.raises(ValueError, match="'cache' is only allowed on llm steps"):
            load_definition(LLM_CACHE_ON_RUNNER_WORKFLOW)


# ---------------------------------------------------------------------------
# Engine integration tests
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _register_test_gates():
    async def always_pass(run: Any, step: Any, inputs: Any) -> bool:
        return True

    register_gate_condition("always_pass", always_pass)
    yield


@pytest.mark.asyncio
async def test_cache_hit_skips_api(db: Any, engine: WorkflowEngine, ai_service: MagicMock) -> None:
    """When cache has a hit, the AI service should NOT be called."""
    defn = load_definition(LLM_CACHE_WORKFLOW)

    # First run: populates cache
    run1 = await engine.start_run(defn, target_kind="generic", target_ref="t1", inputs={})
    assert run1["status"] == "completed"
    assert ai_service.complete_with_usage.call_count == 1

    ai_service.complete_with_usage.reset_mock()

    # Second run: should hit cache
    run2 = await engine.start_run(defn, target_kind="generic", target_ref="t2", inputs={})
    assert run2["status"] == "completed"
    assert ai_service.complete_with_usage.call_count == 0

    steps = list_workflow_steps(db, run2["id"])
    arts = steps[0].get("result_artifacts") or {}
    assert arts.get("cache_hit") is True
    assert arts.get("total_tokens") == 0
    assert arts.get("original_tokens") == 30


@pytest.mark.asyncio
async def test_cache_miss_calls_api_and_stores(db: Any, engine: WorkflowEngine, ai_service: MagicMock) -> None:
    """On cache miss, the AI service is called and the result is stored."""
    defn = load_definition(LLM_CACHE_WORKFLOW)
    run = await engine.start_run(defn, target_kind="generic", target_ref="t1", inputs={})
    assert run["status"] == "completed"
    assert ai_service.complete_with_usage.call_count == 1

    steps = list_workflow_steps(db, run["id"])
    arts = steps[0].get("result_artifacts") or {}
    assert arts.get("cache_hit") is False

    # Verify cache was populated
    from anteroom.services.workflow_cache import compute_cache_key, get_cached_response

    key = compute_cache_key(
        model="primary-model",
        prompt="Summarize this",
        system_prompt="",
        temperature=None,
        max_tokens=4096,
        response_format=None,
    )
    cached = get_cached_response(db, key, "")
    assert cached is not None
    assert cached["response"] == "LLM response"


@pytest.mark.asyncio
async def test_cache_disabled_no_interaction(db: Any, ai_service: MagicMock) -> None:
    """When cache.enabled is false, no cache interaction occurs."""
    config = WorkflowConfig()
    registry = create_default_registry()
    eng = WorkflowEngine(db, config, registry, ai_service=ai_service)

    defn = load_definition(LLM_CACHE_DISABLED_WORKFLOW)

    # Run twice
    await eng.start_run(defn, target_kind="generic", target_ref="t1", inputs={})
    await eng.start_run(defn, target_kind="generic", target_ref="t2", inputs={})

    # Both runs should call API (no caching)
    assert ai_service.complete_with_usage.call_count == 2


@pytest.mark.asyncio
async def test_no_cache_field_no_interaction(db: Any, ai_service: MagicMock) -> None:
    """When no cache field present, no cache interaction occurs."""
    config = WorkflowConfig()
    registry = create_default_registry()
    eng = WorkflowEngine(db, config, registry, ai_service=ai_service)

    defn = load_definition(LLM_NO_CACHE_WORKFLOW)

    await eng.start_run(defn, target_kind="generic", target_ref="t1", inputs={})
    await eng.start_run(defn, target_kind="generic", target_ref="t2", inputs={})

    assert ai_service.complete_with_usage.call_count == 2


@pytest.mark.asyncio
async def test_cache_with_structured_output(db: Any) -> None:
    """JSON structured output round-trips through cache correctly."""
    json_response = '{"category": "tech", "confidence": 0.95}'
    svc = _make_ai_service(response_text=json_response)
    config = WorkflowConfig()
    registry = create_default_registry()
    eng = WorkflowEngine(db, config, registry, ai_service=svc)

    defn = load_definition(LLM_CACHE_JSON_WORKFLOW)

    # First run: API call, stores in cache
    run1 = await eng.start_run(defn, target_kind="generic", target_ref="t1", inputs={})
    assert run1["status"] == "completed"

    svc.complete_with_usage.reset_mock()

    # Second run: cache hit, structured_output should be present
    run2 = await eng.start_run(defn, target_kind="generic", target_ref="t2", inputs={})
    assert run2["status"] == "completed"
    assert svc.complete_with_usage.call_count == 0

    steps = list_workflow_steps(db, run2["id"])
    arts = steps[0].get("result_artifacts") or {}
    assert arts.get("cache_hit") is True
    assert arts.get("structured_output") == {"category": "tech", "confidence": 0.95}


@pytest.mark.asyncio
async def test_cache_with_fallback_primary_miss_fallback_hit(db: Any) -> None:
    """Primary model cache miss + API fail -> fallback model cache hit."""
    svc = _make_ai_service(model="primary-model")
    config = WorkflowConfig()
    registry = create_default_registry()
    eng = WorkflowEngine(db, config, registry, ai_service=svc)

    defn = load_definition(LLM_CACHE_FALLBACK_WORKFLOW)

    # Pre-populate cache for fallback model
    from anteroom.services.workflow_cache import compute_cache_key, put_cached_response

    fallback_key = compute_cache_key(
        model="fallback-model-1",
        prompt="Summarize this",
        system_prompt="",
        temperature=None,
        max_tokens=4096,
        response_format=None,
    )
    put_cached_response(
        db,
        cache_key=fallback_key,
        space_id="",
        workflow_id="test",
        model="fallback-model-1",
        response="fallback cached response",
        prompt_tokens=5,
        completion_tokens=10,
        response_format=None,
        ttl_seconds=3600,
    )

    # Make primary model API fail
    svc.complete_with_usage = AsyncMock(side_effect=Exception("primary down"))

    run = await eng.start_run(defn, target_kind="generic", target_ref="t1", inputs={})
    assert run["status"] == "completed"

    steps = list_workflow_steps(db, run["id"])
    arts = steps[0].get("result_artifacts") or {}
    assert arts.get("cache_hit") is True
    assert arts.get("fallback_used") is True
    assert arts.get("model") == "fallback-model-1"


@pytest.mark.asyncio
async def test_cache_does_not_store_failures(db: Any) -> None:
    """Failed API calls should NOT be cached."""
    svc = _make_ai_service()
    svc.complete_with_usage = AsyncMock(side_effect=Exception("API error"))
    config = WorkflowConfig()
    registry = create_default_registry()
    eng = WorkflowEngine(db, config, registry, ai_service=svc)

    defn = load_definition(LLM_CACHE_WORKFLOW)
    run = await eng.start_run(defn, target_kind="generic", target_ref="t1", inputs={})
    assert run["status"] == "failed"

    # Verify nothing was cached
    from anteroom.services.workflow_cache import compute_cache_key, get_cached_response

    key = compute_cache_key(
        model="primary-model",
        prompt="Summarize this",
        system_prompt="",
        temperature=None,
        max_tokens=4096,
        response_format=None,
    )
    assert get_cached_response(db, key, "") is None
