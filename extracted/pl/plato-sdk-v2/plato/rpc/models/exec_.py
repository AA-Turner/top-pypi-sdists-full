"""Exec service models (module name has a trailing underscore: ``exec`` is a
Python builtin).

Short, typed command execution — replaces the ``run_ssh`` one-shots (env setup,
runner-path resolution, install stamp checks, transport setup commands). rc,
stdout, stderr come back as separate typed fields, ending the SSH habit of
folding stderr into stdout and parsing sentinels.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from plato.rpc.protocol import DEFAULT_EXEC_OUTPUT_BYTES


class ExecRunRequest(BaseModel):
    # Prefer argv (no shell parsing); shell is the escape hatch for pipes etc.
    argv: list[str] | None = None
    shell: str | None = None
    cwd: str | None = None
    env: dict[str, str] = Field(default_factory=dict)
    # Extra env layered on top of the daemon's inherited environment, rather
    # than replacing it, so PATH etc. survive.
    inherit_env: bool = True
    stdin: str | None = None
    timeout_s: float = 300.0
    max_output_bytes: int = DEFAULT_EXEC_OUTPUT_BYTES


class ExecRunResponse(BaseModel):
    rc: int
    stdout: str
    stderr: str
    truncated_stdout: bool = False
    truncated_stderr: bool = False
    duration_s: float
    timed_out: bool = False
