"""Kinds for the code/shell execution tool results.

Ledger rows (KIND_TOOL_LEDGER, agent ``lead-w2b``): ``shell_execute``
``shell_python`` ``code_execute_python`` ``math_calculate``.

THREE TOOLS, ONE SHAPE. ``shell_execute``, ``shell_python`` and
``code_execute_python`` all return "a process ran: stdout, stderr, exit code" —
one kind (``shell_execution``), not three near-duplicate slugs
(NOMENCLATURE.md). What differs between them is the INPUT (a command line vs a
script body), and inputs are not part of a result kind.

CONVERT EVERY BRANCH (the ``fs_*`` trap 1). ``shell_execute`` has THREE
success branches — sandbox proxy, durable VFS (``vfs_shell.py``), real disk —
and the live server takes the durable-VFS one. ``shell_python`` and
``code_execute_python`` have sandbox/real-disk branches. All of them return
this model; the branch-only keys (``stdout_truncated`` / ``cwd`` /
``log_path``) are declared OPTIONAL — the union across branches is the shape
(the ``fs_*`` trap 2).

FAILED RUNS STILL CARRY THE KIND. A nonzero exit code is a *result*, not a
transport error: those branches return ``success=False`` WITH this payload so
the caller sees stdout/stderr. Only transport-level failures (blocked command,
timeout, proxy error) return no output at all.

All PLACEHOLDER tier: process output is raw text by definition — there is no
richer provider payload being flattened away.
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "shell_execution",
    label="Shell Execution",
    family="tool_execution",
    example={
        "stdout": "hello\n",
        "stderr": "",
        "exit_code": 0,
        "stdout_truncated": False,
        "stderr_truncated": False,
        "cwd": "/home/agent",
        "log_path": "/home/agent/.matrx/runtime/tool-calls/conv/call.md",
    },
    maturity="placeholder",
)
class ShellExecution(KindModel):
    """What running a command or script produced: stdout, stderr, exit code.

    Shared by ``shell_execute`` / ``shell_python`` / ``code_execute_python``
    across every backend branch (sandbox proxy, durable VFS, real disk).
    """

    #: May be tail-truncated to the 10KB soft cap; the truncation is announced
    #: either by ``stdout_truncated`` (sandbox branch) or by an inline
    #: ``...(Truncated N bytes. Full output: <path>)...`` header (disk branch).
    stdout: str = ""
    stderr: str = ""
    exit_code: int | None = None
    #: SANDBOX-BRANCH-ONLY keys — absent on the VFS and real-disk branches,
    #: which announce truncation inline in the text instead.
    stdout_truncated: bool | None = None
    stderr_truncated: bool | None = None
    #: The directory the command ran in — sandbox ``shell_execute`` only.
    cwd: str | None = None
    #: Full untruncated transcript on disk (``write_tool_call_log``), readable
    #: later via ``fs_read`` — sandbox branch only.
    log_path: str | None = None


@kind(
    "calculation_result",
    label="Calculation Result",
    family="tool_execution",
    example={"expression": "sqrt(144) + 2**3", "result": "20.0"},
    maturity="placeholder",
)
class CalculationResult(KindModel):
    """One evaluated math expression and its value.

    ``result`` is the stringified value — the evaluator can produce an int, a
    float, or a sequence (``min``/``max``/``sum`` over a literal list), and the
    tool has always returned the string form; declaring it wider would invent
    structure the implementation does not produce.
    """

    expression: str = ""
    result: str = ""
