"""Background tool maintenance must never probe ORM state in a client host."""

from __future__ import annotations

import os
import subprocess
import sys

import pytest
from test_execute_with_store import InMemoryStore

from matrx_ai._ext import configure_ext

pytestmark = pytest.mark.usefixtures("client_host_sandbox")


@pytest.mark.asyncio
async def test_tool_lifecycle_sweeps_skip_orm_when_store_is_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    configure_ext(conversation_store=InMemoryStore())

    from matrx_ai.tools import logger as logger_module
    from matrx_ai.tools.lifecycle import ToolLifecycleManager

    def _orm_probe() -> None:
        raise AssertionError("client-host lifecycle sweep touched cxm")

    monkeypatch.setattr(logger_module, "_cxm", _orm_probe)

    lifecycle = ToolLifecycleManager()
    await lifecycle._sweep_stale_cx_tool_call_rows()
    await lifecycle._sweep_expired_delegated_rows()

    logger = logger_module.ToolExecutionLogger()
    assert await logger.abandon_stale_running_rows(older_than_seconds=1) == 0
    assert await logger.expire_delegated_calls() == 0


def test_tool_lifecycle_sweeps_are_quiet_without_any_host_configuration() -> None:
    code = (
        "import asyncio\n"
        "from matrx_ai.tools.lifecycle import ToolLifecycleManager\n"
        "from matrx_ai.tools.logger import ToolExecutionLogger\n"
        "async def main():\n"
        "    lifecycle = ToolLifecycleManager()\n"
        "    await lifecycle._sweep_stale_cx_tool_call_rows()\n"
        "    await lifecycle._sweep_expired_delegated_rows()\n"
        "    logger = ToolExecutionLogger()\n"
        "    assert await logger.abandon_stale_running_rows(older_than_seconds=1) == 0\n"
        "    assert await logger.expire_delegated_calls() == 0\n"
        "asyncio.run(main())\n"
    )
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": os.environ.get("HOME", ""),
        "LANG": os.environ.get("LANG", "en_US.UTF-8"),
    }
    if "VIRTUAL_ENV" in os.environ:
        env["VIRTUAL_ENV"] = os.environ["VIRTUAL_ENV"]

    proc = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        env=env,
        timeout=120,
    )

    combined = f"{proc.stdout}\n{proc.stderr}"
    assert proc.returncode == 0, combined
    assert "DBNotConfiguredError" not in combined
    assert "Expiry sweep error" not in combined
    assert "query failed" not in combined
