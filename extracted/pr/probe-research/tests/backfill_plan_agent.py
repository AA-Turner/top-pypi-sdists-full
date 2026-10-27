"""A fake classifier that files through the REAL `probe-backfill-plan` launcher.

The classifier no longer answers with a list of paths; it selects files with the
tool, and the import reads the tool's log. A fake that hands back JSON therefore
proves nothing (the import ignores the reply), and a fake that writes the log
directly would skip the launcher, the per-session state and the validation --
the parts that broke in production. So these fakes run the actual launcher
script the import put on the agent's PATH, exactly as an agent's shell would.

`filing(fake)` keeps the older tests' fakes readable: they still say what the
agent decided as `{"assignments": [...], "left_out": [...], "projects": [...]}`,
and the wrapper turns that into tool calls. A path the walk lacks is REFUSED by
the tool, as it would be for a real agent -- it never reaches the plan.
"""

from __future__ import annotations

import json
import re
import subprocess
import time
import uuid
from pathlib import Path

from probe.cli import backfill as bf


#: Bound at import: several suites replace `subprocess.Popen` with a fake child
#: for the import worker, and the agent's shell is not that worker.
_POPEN = subprocess.Popen


class _OwnClock:
    """`time` for one module, except its `sleep` (`patch_own_sleep`)."""

    def __init__(self, sleep) -> None:
        self.sleep = sleep

    def __getattr__(self, name: str):
        return getattr(time, name)


def patch_own_sleep(monkeypatch, module, sleep) -> None:
    """Replace `time.sleep` for `module`'s OWN calls, never the process's.

    `monkeypatch.setattr(module.time, "sleep", ...)` replaces `time.sleep` in
    every thread, and `tool` below waits on a REAL child: CPython's
    `Popen.wait(timeout=...)` polls with `time.sleep(0.001, 0.002, ... 0.05)`
    until the child is reaped, on the import's worker thread. On a loaded
    machine the child is still exiting when its output ends, so those polls
    landed in a test's record of the import worker's retry waits (agent-ci:
    `[2, 0.001, 0.002, 0.004, 0.008, 0.016, 0.032, 0.05, 0.05, ...]`, 698 of
    the 0.05s) or tripped a sleep that must never happen."""
    monkeypatch.setattr(module, "time", _OwnClock(sleep))


def tool(kwargs: dict, *args: str) -> tuple[int, str]:
    """Run the session's own `probe-backfill-plan`, as the agent's shell would."""
    exe = Path(kwargs["path_prepend"]) / bf.PLAN_TOOL_COMMAND
    proc = _POPEN([str(exe), *args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                  text=True, cwd=str(kwargs.get("workdir") or "."))
    out, _ = proc.communicate(timeout=60)
    return proc.returncode, out


def answer_of(tail: str) -> dict | None:
    """The decisions an older fake meant, out of its stream-json reply."""
    for line in reversed(tail.splitlines()):
        for key in ("assignments", "left_out"):
            found = list(bf._embedded_summaries(line.strip(), key=key))
            if found:
                return found[-1]
    return None


def ops_for(answer: dict, *, declare: bool) -> list[dict]:
    ops: list[dict] = []
    if declare:
        for spec in answer.get("projects") or []:
            spec = spec if isinstance(spec, dict) else {"slug": spec}
            ops.append({"op": "project", "slug": spec.get("slug"), "name": spec.get("name") or "",
                        "description": spec.get("description") or "", "tags": spec.get("tags") or []})
    for row in answer.get("assignments") or []:
        if not isinstance(row, dict):
            continue
        ops.append({"op": "assign", "project": row.get("project"),
                    "under": row.get("path") or row.get("dir"),
                    "low": (row.get("confidence") or "high") != "high", "why": row.get("why") or ""})
    for row in answer.get("left_out") or []:
        path = (row.get("path") or row.get("dir")) if isinstance(row, dict) else row
        why = (row.get("why") if isinstance(row, dict) else "") or "not research"
        ops.append({"op": "leave_out", "under": path, "why": why})
    return ops


def file_answer(answer: dict, kwargs: dict, prompt: str = "") -> str:
    """Apply `answer` through the tool in one `apply --from`, like a real agent."""
    declare = "File one slice" not in prompt
    ops = ops_for(answer, declare=declare)
    source = Path(kwargs["workdir"]) / f"ops-{uuid.uuid4().hex[:8]}.jsonl"
    source.write_text("\n".join(json.dumps(op) for op in ops), encoding="utf-8")
    _, out = tool(kwargs, "apply", "--from", str(source))
    return out


def filing(fake):
    """Wrap a JSON-answering fake so its filing answers go through the tool."""

    def run(folder, prompt, **kwargs):
        ok, tail = fake(folder, prompt, **kwargs)
        if kwargs.get("path_prepend") and tail:
            answer = answer_of(tail)
            if answer is not None:
                file_answer(answer, kwargs, prompt)
        return ok, tail

    return run


def unit_paths(prompt: str) -> list[str]:
    """The files an upload unit's prompt lists as the agent's own."""
    block = re.search(r"Your [\d,]+ files:\n\n(.*?)\n\nFor each file", prompt, re.S).group(1)
    return [p.strip() for p in block.splitlines() if p.strip()]


def note(kwargs: dict, notes: dict[str, str]) -> str:
    """Write notes the way an upload agent must: through the tool, by path."""
    source = Path(kwargs["workdir"]) / f"notes-{uuid.uuid4().hex[:8]}.jsonl"
    source.write_text("\n".join(json.dumps({"op": "note", "file": p, "notes": t})
                                for p, t in notes.items()), encoding="utf-8")
    _, out = tool(kwargs, "apply", "--from", str(source))
    return out
