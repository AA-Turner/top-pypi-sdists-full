"""A tool-call log on a person's computer lands under THEIR home, never the cloud container's.

Found 2026-10-02 by the Matrx 2 local-tools live run: on a ``local_machine`` binding every
shell_execute / shell_python log write went to ``/home/agent/.matrx/…`` — a path that does not
exist on a Mac or Windows — so the device refused it and the agent lost its full-output log.
"""

from __future__ import annotations

from typing import Any

import pytest

from matrx_ai.tools import _call_logger
from matrx_ai.tools._sandbox_proxy import SandboxBinding

pytestmark = pytest.mark.asyncio


async def _written_path(monkeypatch: pytest.MonkeyPatch, binding: SandboxBinding) -> str:
    seen: dict[str, Any] = {}

    async def fake_write(
        _binding: SandboxBinding, path: str, _body: str, **_kw: Any
    ) -> dict[str, Any]:
        seen["path"] = path
        return {}

    monkeypatch.setattr(_call_logger, "get_active_sandbox", lambda: binding)
    monkeypatch.setattr(_call_logger, "_proxy_fs_write", fake_write)
    agent_path = await _call_logger.write_tool_call_log(
        tool="shell_execute",
        call_id="toolu_abcdef123456",
        inputs={"command": "pwd"},
        success=True,
        conversation_id="conv-1",
    )
    assert agent_path is not None and agent_path.startswith("~/.matrx/runtime/tool-calls/conv-1/")
    return seen["path"]


async def test_a_desktop_log_lands_under_the_devices_own_home(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mac = SandboxBinding("dev", "https://x/api/local-proxy/1", "t", "/Users/pat", "local_machine")
    assert (await _written_path(monkeypatch, mac)).startswith(
        "/Users/pat/.matrx/runtime/tool-calls/conv-1/"
    )
    win = SandboxBinding(
        "dev", "https://x/api/local-proxy/1", "t", "C:/Users/pat/", "local_machine"
    )
    assert (await _written_path(monkeypatch, win)).startswith(
        "C:/Users/pat/.matrx/runtime/tool-calls/conv-1/"
    )


async def test_a_cloud_sandbox_log_stays_in_the_agent_home(monkeypatch: pytest.MonkeyPatch) -> None:
    box = SandboxBinding(
        "sbx-1", "https://orch/sandboxes/sbx-1", "t", "/home/agent/work", "sandbox"
    )
    assert (await _written_path(monkeypatch, box)).startswith(
        "/home/agent/.matrx/runtime/tool-calls/conv-1/"
    )
