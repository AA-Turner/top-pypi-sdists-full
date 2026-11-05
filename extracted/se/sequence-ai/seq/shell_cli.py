"""
`seq policy shell <name> -- <command>`: one command run in a container of your deployment's worker serving now, to look
into it - what is installed, where its files are, what its card says - its output printed and its exit code this
command's own. It runs as your policy's code does there, with none of the platform's secrets nor your own; one command
at a time on a worker, up to 120 s. (The gateway's POST /v1/deployments/{name}/shell; the worker's harness/transport/
shell.py.)

`seq benchmark shell <name>[@vN] -- <command>`: the same on a machine of a version of your benchmark, in its image on the
card it declares - opened for it once its image is there to load, waited for, what it waits on said as it moves on - which
ends ten minutes after its last command, or at `--stop`.

"""
from __future__ import annotations

import shlex
import time

from sequence_ai._core.names import segment
from sequence_ai.errors import InvalidRequest, Unavailable

TIMED_OUT = 124


WAIT_MOST_S = 3600.0
POLL_S = 5.0
IDLE_MIN = 10
SAID_AGAIN_S = 120


def command_of(words: list[str], kind: str = "policy") -> str:
    """What runs: one word as it is - a line with pipes, `&&` and quotes your shell left whole - else the words quoted
    and joined, as you typed them."""
    words = words[1:] if words[:1] == ["--"] else words
    if not words:
        raise InvalidRequest(f"a command is required: seq {kind} shell NAME -- COMMAND (e.g. -- pip list)")
    return words[0] if len(words) == 1 else shlex.join(words)


def shell(name: str, words: list[str], *, worker: str | None = None, timeout_s: float = 30.0,
          base_url: str | None = None, echo=print) -> dict:
    """The command run once on a worker of `name` serving now: its output echoed as it came, its time limit or its cut
    said after it. What it answered: exit_code, output, truncated, timed_out, seconds, worker, version."""
    from seq.deployments_cli import _call

    body = {"command": command_of(words), "timeout_s": timeout_s, **({"worker": worker} if worker else {})}
    out = _call("POST", f"/v1/deployments/{segment(name)}/shell", base_url, body, timeout=timeout_s + 45)
    return _said(out, timeout_s, echo)


def benchmark_shell(name: str, words: list[str], *, version: int | None = None, timeout_s: float = 30.0,
                    base_url: str | None = None, echo=print, clock=time.monotonic) -> dict:
    """The command run once on a shell machine of benchmark `name` (its version `version`, else its newest), asked
    again while the machine opens - for WAIT_MOST_S at most - what it waits on said as the platform words it (the gateway's
    eval/machine_start.of_shell), again when that moves on and each SAID_AGAIN_S it lasts; then as on a policy's worker. What
    it answered: exit_code, output, truncated, timed_out, seconds, machine, version.
"""
    from seq.deployments_cli import _call

    path = f"/v1/benchmarks/{segment(name)}/shell"
    body = {"command": command_of(words, "benchmark"), "timeout_s": timeout_s,
            **({"version": version} if version is not None else {})}
    began, opening, seen = clock(), False, None
    while (out := _call("POST", path, base_url, body, timeout=timeout_s + 45)).get("state") == "starting":
        if not opening:
            echo(f"opening a machine for {name} v{out.get('version')} on its card: it stays up {IDLE_MIN} minutes after "
                 f"your last command (seq benchmark shell {name} --stop ends it)")
            opening = True

        mark = (out.get("machine"), out.get("what"), int(out.get("since_s") or 0) // SAID_AGAIN_S)
        if out.get("sentence") and mark != seen:
            echo(f"  {out['sentence']}")
            seen = mark
        if clock() - began > WAIT_MOST_S:
            raise Unavailable(f"the machine for {name} did not open in {WAIT_MOST_S / 60:g} minutes: run it again")
        time.sleep(POLL_S)
    return _said(out, timeout_s, echo)


def benchmark_stop(name: str, *, base_url: str | None = None, echo=print) -> dict:
    """Its shell machine ended now: {"ended": [its name]} - none where none runs."""
    from seq.deployments_cli import _call

    out = _call("DELETE", f"/v1/benchmarks/{segment(name)}/shell", base_url)
    ended = out.get("ended") or []
    echo(f"ended {', '.join(ended)}" if ended else f"no shell machine of {name} runs")
    return out


def _said(out: dict, timeout_s: float, echo) -> dict:
    """A command's answer echoed: its output, then its cut or its time limit."""
    if out.get("output"):
        echo(out["output"].rstrip("\n"))
    if out.get("truncated"):
        echo("(its output past the first 64 KB is not shown)")
    if out.get("timed_out"):
        echo(f"(ended at its time limit, {timeout_s:g} s: --timeout gives it up to 120 s)")
    return out


def exit_code(out: dict) -> int:
    """This command's exit code: the command's own, TIMED_OUT at its time limit."""
    return TIMED_OUT if out.get("timed_out") else int(out.get("exit_code") or 0)
