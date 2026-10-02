"""The MCP server updates itself through uvx, but the addon inside Blender only
changes when the user reinstalls it. New tools and arguments must therefore
degrade cleanly on older addons (protocol 9 shipped up to 2.0.4)."""
import asyncio
import json

import pytest

from blender_mcp import server
from blender_mcp.addon_manager import AddonHandshake


class FakeBlender:
    def __init__(self, error=None):
        self.sent = []
        self.error = error

    def send_command(self, command, params=None):
        if command == "get_telemetry_consent":
            return {"consent": False}
        self.sent.append((command, params))
        if self.error:
            raise Exception(f"Communication error with Blender: {self.error}")
        return {"Response": {"JobId": "a"}}


def _connect(monkeypatch, protocol, error=None):
    blender = FakeBlender(error)
    monkeypatch.setattr(server, "get_blender_connection", lambda: blender)
    handshake = None if protocol is None else AddonHandshake(True, protocol, [2, 1], [], "4.2", "native")
    monkeypatch.setattr(server, "_addon_handshake", handshake)
    return blender


@pytest.mark.parametrize("protocol, sends_quality", [(None, False), (9, False), (10, False), (11, True)])
def test_hunyuan_quality_reaches_only_addons_that_accept_it(monkeypatch, protocol, sends_quality):
    blender = _connect(monkeypatch, protocol)
    out = asyncio.run(server.generate_hunyuan3d_model(None, text_prompt="stool", quality="high", user_prompt=""))
    assert json.loads(out) == {"job_id": "job_a"}
    assert ("quality" in blender.sent[0][1]) is sends_quality


@pytest.mark.parametrize("tool, kwargs", [
    ("get_tripo_status", {"user_prompt": ""}),
    ("generate_tripo_model", {"text_prompt": "stool", "user_prompt": ""}),
    ("poll_tripo_job_status", {"request_id": "r"}),
    ("import_generated_asset_tripo", {"request_id": "r", "name": "n"}),
])
def test_tripo_explains_itself_when_the_addon_has_no_tripo(monkeypatch, tool, kwargs):
    _connect(monkeypatch, 9, error="Unknown command type: x")
    out = asyncio.run(getattr(server, tool)(None, **kwargs))
    assert out == server.TRIPO_UNAVAILABLE
