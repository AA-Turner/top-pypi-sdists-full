"""PRO-1937 child-startup latency: tool-schema memoization, bounded cache, org-headers
await (no run_sync hop), and gathered deps/tools legs in build_agent_args."""

from types import SimpleNamespace

import pytest

from xpander_sdk.models.configuration import Configuration
from xpander_sdk.modules.agents.sub_modules.agent import Agent, AgentGraph
from xpander_sdk.modules.tools_repository.tools_repository_module import ToolsRepository
from xpander_sdk.modules.tools_repository.sub_modules import tool as tool_module
from xpander_sdk.modules.tools_repository.sub_modules.tool import Tool
from xpander_sdk.modules.agents.models.agent import AgentGraphItemSchema
from xpander_sdk.modules.backend.frameworks import agno as agno_module
from xpander_sdk.utils import cache as cache_module
from xpander_sdk.utils.cache import BoundedCache, cached_tool_json_schema, tool_schema_cache


def _agent_instance(**over):
    """Build a real Agent the way Agent.aload does (model_validate then attach graph/tools)."""
    from tests.helpers.factories import make_agent

    data = make_agent(**over)
    agent = Agent.model_validate({**data, "graph": None, "tools": None, "configuration": Configuration()})
    agent.graph = AgentGraph(data.get("graph") or [])
    agent.tools = ToolsRepository(
        configuration=agent.configuration, tools=data.get("tools") or [], agent_graph=agent.graph
    )
    return agent


@pytest.fixture(autouse=True)
def _clear_schema_caches():
    tool_schema_cache.clear()
    cache_module._tool_json_schema_cache.clear()
    yield
    tool_schema_cache.clear()
    cache_module._tool_json_schema_cache.clear()


def _tool(id="op-x", params=None, is_local=False, overrides=None) -> Tool:
    return Tool(
        id=id,
        name=id,
        method="POST",
        path=f"/{id}",
        is_local=is_local,
        parameters=params or {"type": "object", "properties": {"q": {"type": "string"}}},
        schema_overrides=overrides,
    )


# ── change 1: Tool.schema memoization ──

def test_schema_built_once_for_identical_inputs(monkeypatch):
    calls = {"n": 0}
    real = tool_module.build_model_from_schema

    def _counting(**kwargs):
        calls["n"] += 1
        return real(**kwargs)

    monkeypatch.setattr(tool_module, "build_model_from_schema", _counting)

    t1, t2 = _tool(), _tool()
    a, b = t1.schema, t2.schema  # two instances, several accesses
    _ = t1.schema
    assert a is b            # shared cached class across instances
    assert calls["n"] == 1   # build_model_from_schema ran once, not per access


def test_different_params_are_distinct_classes():
    a = _tool(params={"type": "object", "properties": {"q": {"type": "string"}}}).schema
    b = _tool(params={"type": "object", "properties": {"q": {"type": "number"}}}).schema
    assert a is not b


def test_different_is_local_is_distinct():
    assert _tool(is_local=False).schema is not _tool(is_local=True).schema


def test_schema_overrides_isolate_tenants():
    # Same tool id, different graph/org-scoped schema_overrides must NOT share a cached
    # schema — else one tenant's overridden shape leaks to another.
    ov = AgentGraphItemSchema(
        input={"type": "object", "properties": {"q": {"type": "string", "description": "tenant-A override"}}}
    )
    plain = _tool(id="op-shared").schema
    overridden = _tool(id="op-shared", overrides=ov).schema
    assert plain is not overridden


# ── payload-wrapper hint stays present + concrete (won't confuse agents) ──

def test_schema_description_carries_concrete_payload_hint():
    cls = _tool(params={"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}).schema
    desc = cached_tool_json_schema(cls, "serialization").get("description", "")
    assert "payload" in desc          # wrap-in-payload rule present on the schema
    assert "city" in desc             # concrete field name, matches the function docstring
    assert "<fields>" not in desc     # no leftover placeholder


# ── json-schema per-mode memo ──

def test_json_schema_memoized_per_mode():
    cls = _tool().schema
    js1 = cached_tool_json_schema(cls, "serialization")
    js2 = cached_tool_json_schema(cls, "serialization")
    assert js1 is js2                        # same object returned (memoized)
    val = cached_tool_json_schema(cls, "validation")
    assert val is not js1                    # distinct entry per mode


# ── BoundedCache eviction (memory bound) ──

def test_bounded_cache_evicts_oldest():
    built = []

    def mk(v):
        return lambda: (built.append(v), v)[1]

    c = BoundedCache(maxsize=2)
    c.get_or_build("a", mk("a"))
    c.get_or_build("b", mk("b"))
    assert c.get_or_build("a", mk("a")) == "a"  # cached, no rebuild; a now MRU
    c.get_or_build("c", mk("c"))                # over cap -> evicts b (LRU)
    assert len(c) == 2
    assert built == ["a", "b", "c"]
    c.get_or_build("a", mk("a"))                # a survived -> no rebuild
    assert built == ["a", "b", "c"]
    c.get_or_build("b", mk("b"))                # b was evicted -> rebuilt
    assert built == ["a", "b", "c", "b"]


def test_bounded_cache_ttl_backstop(monkeypatch):
    clock = {"now": 1000.0}
    monkeypatch.setattr(cache_module.time, "monotonic", lambda: clock["now"])
    built = []
    c = BoundedCache(maxsize=10, ttl_seconds=600)

    c.get_or_build("k", lambda: (built.append(1), "v")[1])
    clock["now"] += 300  # within TTL -> served cached
    c.get_or_build("k", lambda: (built.append(1), "v")[1])
    assert len(built) == 1
    clock["now"] += 400  # now 700s elapsed > 600 TTL -> rebuilt
    c.get_or_build("k", lambda: (built.append(1), "v")[1])
    assert len(built) == 2


# ── functions() uses the memo end-to-end ──

def test_functions_builds_each_schema_once(monkeypatch):
    from xpander_sdk.modules.tools_repository.tools_repository_module import ToolsRepository

    calls = {"n": 0}
    real = tool_module.build_model_from_schema

    def _counting(**kwargs):
        calls["n"] += 1
        return real(**kwargs)

    monkeypatch.setattr(tool_module, "build_model_from_schema", _counting)

    repo = ToolsRepository(tools=[_tool(id="op-a"), _tool(id="op-b")])
    fns1 = repo.functions
    fns2 = repo.functions  # second access (e.g. plan retry) must not rebuild
    assert len(fns1) == 2 and len(fns2) == 2
    assert calls["n"] == 2  # once per distinct tool, not per access (was 3x/tool/access)


# ── change 2: org headers awaited, not run_sync ──

def test_load_llm_model_skips_run_sync_when_headers_passed(monkeypatch):
    agent = _agent_instance()

    def _boom(*a, **k):  # run_sync must not be hit when headers are supplied
        raise AssertionError("run_sync called despite headers passed in")

    monkeypatch.setattr(agno_module, "run_sync", _boom)
    # Should build the model without falling back to the blocking fetch.
    agno_module._load_llm_model(agent=agent, org_default_llm_headers={})


@pytest.mark.asyncio
async def test_aget_org_headers_coalesces(monkeypatch):
    cache_module.backend_config_cache.invalidate()
    agent = SimpleNamespace(configuration=Configuration())
    calls = {"n": 0}

    async def _fake_request(*a, **k):
        calls["n"] += 1
        return {"x-org": "h"}

    monkeypatch.setattr(agno_module.APIClient, "make_request", _fake_request)
    r1 = await agno_module._aget_org_default_llm_headers(agent)
    r2 = await agno_module._aget_org_default_llm_headers(agent)
    assert r1 == r2 == {"x-org": "h"}
    assert calls["n"] == 1  # second call served from the 60s cache
    cache_module.backend_config_cache.invalidate()


# change 3 (gather the deps + tools legs) is behavior-preserving — the same two
# awaits, now concurrent — and covered by the existing build/MCP regression suite
# (tests/test_mcp_parallel_connect.py et al). A standalone runtime overlap test would
# have to drive the full ~1200-line build_agent_args tail, which adds brittleness
# without covering new logic.
