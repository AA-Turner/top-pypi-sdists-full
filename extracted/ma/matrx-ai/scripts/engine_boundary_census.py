"""Phase 0 — the authoritative engine-boundary census.

Runs a full streaming request WITH a tool call in a COLD interpreter, using only
host-injected client seams, and records every reach from the engine into host
material — the ORM registry (``matrx_ai.db._registry``) and the modules that
trigger it.

Why a cold subprocess: ``matrx_ai/db/cx_managers.py`` is a PEP-562 lazy facade
whose impl materialises 12 ORM bases + 12 models at module scope on FIRST
attribute access. Once any earlier code in the same process has touched it, the
module is cached in ``sys.modules`` and the reach never happens again. An
in-process guard therefore reports green because of module caching, not because
the invariant holds (aidream AD182). Only a fresh interpreter tells the truth.

Usage:
    uv run python packages/matrx-ai/scripts/engine_boundary_census.py [--json]

Output: every ``kind:name`` reach with the importing module that caused it, then
a per-module rollup. Exit code is always 0 — this is a REPORT, not a gate. The
gate is ``tests/client_host/test_no_db_streaming_with_tool.py``, which is
xfail(strict) until the ports land (agent-engine-extraction PLAN.md Phase 3).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

_CHILD = r'''
import asyncio, json, sys, traceback, uuid
from typing import Any

REACHES = []

def _install_poison():
    from matrx_ai.db import _registry as reg

    def wrap(kind, original):
        def fn(name, *a, **k):
            # Walk the stack for the first frame outside matrx_ai/db/_registry
            # and outside this wrapper — that is the module that caused it.
            culprit = "?"
            for fr in traceback.extract_stack()[::-1]:
                f = fr.filename.replace("\\", "/")
                if "/matrx_ai/db/_registry.py" in f or "<string>" in f:
                    continue
                if "/matrx_ai/" in f:
                    culprit = f.split("/matrx_ai/", 1)[1] + ":" + str(fr.lineno)
                    break
                culprit = f.rsplit("/", 1)[-1] + ":" + str(fr.lineno)
                break
            REACHES.append({"kind": kind, "name": name, "from": culprit})
            return original(name, *a, **k)
        return fn

    reg.get_base = wrap("base", reg.get_base)
    reg.get_instance = wrap("instance", reg.get_instance)
    reg.get_model = wrap("model", reg.get_model)


class FakeEmitter:
    def __init__(self): self.events = []
    async def send_chunk(self, *a, **k): pass
    async def send_data(self, *a, **k): pass
    async def send_status_update(self, *a, **k): pass
    async def send_end(self, *a, **k): pass
    async def send_error(self, *a, **k): pass
    async def send_info(self, *a, **k): pass
    def __getattr__(self, n):
        async def _f(*a, **k): pass
        return _f


class InMemoryStore:
    def __init__(self):
        self.tool_rows, self.messages, self.completed = {}, [], []
    async def __getattr__(self, n): pass


async def main():
    # The suite's conftest registers stub ORM models process-wide. Mirror that
    # ONLY when --with-stubs is passed, so we can measure both truths:
    #   (default)     what a real client host hits — where it HARD-FAILS
    #   --with-stubs  the full reach list, which is the Phase 3 worklist
    if WITH_STUBS:
        from matrx_ai.testing.tests.conftest import _configure_stubs
        _configure_stubs()

    _install_poison()
    from matrx_ai._ext import configure_ext

    sys.path.insert(0, str(__import__("pathlib").Path(TESTS_DIR)))
    from test_execute_with_store import _MOCK_MODEL, InMemoryStore as Store, StaticCatalog

    store = Store()
    configure_ext(
        conversation_store=store,
        model_catalog=StaticCatalog([_MOCK_MODEL]),
        api_key_resolver=lambda name: "not-a-real-key",
    )

    from matrx_ai.tools.registry import ToolRegistry
    from matrx_ai.tools.models import ToolDefinition, ToolType

    registry = ToolRegistry.get_instance()

    async def probe(args, ctx):
        return {"probe": "ran", "args": dict(args or {})}

    registry.register(
        ToolDefinition(
            name="census_probe_tool",
            description="census probe",
            tool_type=ToolType.LOCAL,
            parameters={"type": "object", "properties": {"anything": {"type": "string"}}},
            function=probe,
        )
    )

    from matrx_connect.context.app_context import AppContext, set_app_context
    conv, req_id = str(uuid.uuid4()), str(uuid.uuid4())
    set_app_context(AppContext(
        emitter=FakeEmitter(), user_id=str(uuid.uuid4()), request_id=req_id,
        conversation_id=conv, is_internal_agent=True, store=True,
        source_app="engine_boundary_census", source_feature="census",
    ))

    from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
    from matrx_ai.orchestrator.executor import execute_until_complete
    from matrx_ai.orchestrator.requests import AIMatrixRequest
    from matrx_ai.providers.unified_client import UnifiedAIClient

    config = UnifiedConfig(
        model="mock-model",
        tools=["census_probe_tool"],
        messages=MessageList(_messages=[
            UnifiedMessage(role="user", content=[TextContent(text="use the probe tool")])
        ]),
        metadata={"mock": {"latency_ms": 1, "ttft_ms": 0, "chunks": 1, "mode": "text",
                           "text": "done", "tool_calls": [
                               {"name": "census_probe_tool", "arguments": {"anything": "x"}}]}},
    )
    await execute_until_complete(
        AIMatrixRequest(conversation_id=conv, config=config, request_id=req_id),
        UnifiedAIClient(),
    )

asyncio.run(main())
print("__CENSUS__" + json.dumps(REACHES))
'''


class CensusFailed(RuntimeError):
    """The census child never reported — the scenario itself broke."""


def run_census(with_stubs: bool = False) -> list[dict]:
    """Run the cold-process census and return the reach list.

    Importable so the invariant TEST and the CLI share one mechanism. Always a
    fresh interpreter: that is the whole point (AD182 — an in-process guard is
    defeated by module caching and by modules that bind ``cxm`` directly at
    import time, so no amount of ``sys.modules`` surgery makes it honest).
    """
    pkg = Path(__file__).resolve().parents[1]
    tests_dir = pkg / "tests" / "client_host"
    child = f"TESTS_DIR = {str(tests_dir)!r}\nWITH_STUBS = {with_stubs!r}\n" + _CHILD
    proc = subprocess.run(
        [sys.executable, "-c", child],
        capture_output=True,
        text=True,
        cwd=str(pkg.parents[1]),
        timeout=300,
    )
    marker = "__CENSUS__"
    line = next((l for l in proc.stdout.splitlines() if l.startswith(marker)), None)
    if line is None:
        raise CensusFailed(
            "census child never reported\n"
            f"--- stdout ---\n{proc.stdout[-4000:]}\n"
            f"--- stderr ---\n{proc.stderr[-4000:]}"
        )
    return json.loads(line[len(marker) :])


def main() -> int:
    with_stubs = "--with-stubs" in sys.argv
    try:
        reaches = run_census(with_stubs=with_stubs)
    except CensusFailed as exc:
        print(exc)
        return 0
    if "--json" in sys.argv:
        print(json.dumps(reaches, indent=2))
        return 0

    mode = "WITH stub ORM models (full reach list)" if with_stubs else "NO ORM registry (a real client host)"
    print(f"\nENGINE BOUNDARY CENSUS — {len(reaches)} ORM-registry reaches in a cold run")
    print(f"mode: {mode}\n")
    if not reaches:
        print("  none. The engine ran a full streaming tool call with zero host reach.")
        return 0

    by_module: dict[str, list[str]] = {}
    for r in reaches:
        by_module.setdefault(r["from"].split(":")[0], []).append(f"{r['kind']}:{r['name']}")

    print(f"{'MODULE':<44} REACHES")
    print("-" * 78)
    for mod, names in sorted(by_module.items(), key=lambda kv: -len(kv[1])):
        print(f"{mod:<44} {len(names):>3}")
        seen: set[str] = set()
        for n in names:
            if n not in seen:
                seen.add(n)
        print(f"{'':<44} {', '.join(sorted(seen))}")
    print("-" * 78)
    print(f"{'TOTAL':<44} {len(reaches):>3} reaches across {len(by_module)} module(s)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
