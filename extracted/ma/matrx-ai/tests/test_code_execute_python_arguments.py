from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai.tools._generated_declarations import CodeExecutePythonArgs
from matrx_ai.tools.implementations import code as code_module


def test_code_execute_python_accepts_conventional_code_alias() -> None:
    parsed = CodeExecutePythonArgs.model_validate(
        {"code": "print('ok')", "timeout_seconds": 90}
    )

    assert parsed.code_input == "print('ok')"
    assert parsed.timeout_seconds == 90


def test_code_execute_python_keeps_declared_code_input_contract() -> None:
    parsed = CodeExecutePythonArgs.model_validate({"code_input": "print('ok')"})

    assert parsed.code_input == "print('ok')"
    assert parsed.timeout_seconds == 30


@pytest.mark.asyncio
async def test_code_alias_executes_in_process(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(code_module, "_workspace_dir", lambda _ctx: tmp_path)

    result = await code_module.code_execute_python(
        {"code": "print(6 * 7)", "timeout_seconds": 5},
        SimpleNamespace(),
    )

    assert result.success is True
    assert result.output["stdout"] == "42\n"
    assert result.output["exit_code"] == 0
