from __future__ import annotations

import ast
import inspect
import textwrap

from matrx_ai.tools.executor import ToolExecutor


def test_successful_db_trace_always_retains_result_preview() -> None:
    tree = ast.parse(textwrap.dedent(inspect.getsource(ToolExecutor.execute)))
    ok_trace_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "_db_log"
        and node.args
        and isinstance(node.args[0], ast.Constant)
        and node.args[0].value == "OK"
    ]

    assert len(ok_trace_calls) == 1
    preview = next(
        keyword.value
        for keyword in ok_trace_calls[0].keywords
        if keyword.arg == "result_preview"
    )
    assert ast.unparse(preview) == "result.output"
