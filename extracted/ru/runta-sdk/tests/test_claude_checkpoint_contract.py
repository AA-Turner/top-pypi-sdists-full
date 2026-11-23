"""Exercise Claude creation options against the real SDK request builder."""

import importlib.util
import json
from pathlib import Path
import sys

import httpx
import pytest

from http_mock import set_handler
from test_openapi_transport import _runtime_json
from runta import AsyncRunta

# Options depend only on runta. Test them without requiring the optional Claude SDK.
OPTIONS_PATH = (
    Path(__file__).resolve().parents[1]
    / "integrations/anthropic-agent-sdk/src/anthropic_agent_runta/options.py"
)
spec = importlib.util.spec_from_file_location("claude_contract_options", OPTIONS_PATH)
options_module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = options_module
spec.loader.exec_module(options_module)


@pytest.mark.asyncio
@pytest.mark.parametrize("checkpoint_id", [None, "checkpoint-1"])
@pytest.mark.parametrize("resources", [{}, {"vcpus": 4, "memory_mib": 4096}])
async def test_claude_creation_options_reach_http(checkpoint_id, resources):
    options = options_module.RuntaClaudeAgentOptions(
        checkpoint_id=checkpoint_id, idle_timeout_secs=30, **resources
    )
    bodies = []

    def handler(request):
        assert request.method == "POST"
        assert request.url.path == "/v2/runtimes"
        bodies.append(json.loads(request.content))
        return httpx.Response(201, json={"data": _runtime_json()})

    async with AsyncRunta(endpoint="http://runta.test", token="rt_test") as client:
        set_handler(client._http, handler)
        runtime = await client.runtimes.create(
            checkpoint_id=options.checkpoint_id,
            wait=False,
            **options.creation_options(),
        )
        assert runtime.id == "sb-1"

    assert len(bodies) == 1
    body = bodies[0]
    assert body["idle_policy"] == {
        "mode": "suspend_and_wakeup",
        "suspend_after_secs": 30,
    }
    if checkpoint_id is not None:
        assert body["checkpoint_id"] == checkpoint_id
        assert "resources" not in body
    else:
        assert "checkpoint_id" not in body
        assert body["resources"]["requests"] == {
            "vcpus": options.vcpus,
            "memory_mib": options.memory_mib,
        }
