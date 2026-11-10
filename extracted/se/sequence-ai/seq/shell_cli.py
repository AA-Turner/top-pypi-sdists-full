"""
`seq policy shell <name> -- <command>`: one command run in a container of your deployment's worker serving now, to look
into it - what is installed, where its files are, what its card says - its output printed and its exit code this
command's own. It runs as your policy's code does there, with none of the platform's secrets nor your own; one command
at a time on a worker, up to 120 s. (The gateway's POST /v1/deployments/{name}/shell; the worker's harness/transport/
shell.py.)

`seq benchmark shell <name> -- <command>`: the same on a machine of your benchmark's newest version, in its image on the
card it declares - opened for it once its image is there to load, waited for, what it waits on said as it moves on - which
ends ten minutes after its last command, or at `--stop`.


With no command, or with one typed at a terminal, either opens a terminal on that machine instead (seq/terminal.py): your
keys go to it as typed and its screen comes back, with no time limit, until you leave it or the machine ends. Piped,
redirected to a file or from a script, a command runs once, as above. `seq policy debug <name>` opens a machine of its own on the version your
deployment serves - its image, its card, its files and settings, no robot sent to it - which plays the policy's sample
episode, or a saved one (--episode), with any breakpoint() in its code stopping in your terminal, then leaves a terminal on
it; it ends ten minutes after you leave it, or at `--stop`. (The gateway's POST and DELETE /v1/deployments/{name}/debug.)

"""
from __future__ import annotations

import os
import shlex
import sys
import time

from sequence_ai._core.names import segment
from sequence_ai.errors import InvalidRequest, Unavailable

TIMED_OUT = 124


WAIT_MOST_S = 3600.0
POLL_S = 5.0
IDLE_MIN = 10
SAID_AGAIN_S = 120


def _words(words: list[str]) -> list[str]:
    return words[1:] if words[:1] == ["--"] else words


def in_terminal(words: list[str], *, as_json: bool = False, stdin=None, stdout=None) -> bool:
    """Whether a shell opens a terminal: with no command always - there is nothing else to run - and with one where your
    stdin and stdout are both a terminal, as ssh decides it, no JSON asked for (that is its output, captured) and the
    system one this terminal runs on (not Windows); piped, redirected to a file or run from a script, it runs once, as
    before - a terminal's bytes, \r\n and all, are no file's.
"""
    from seq.terminal import isatty

    if not _words(words):
        return True
    return (not as_json and os.name != "nt" and isatty(sys.stdin if stdin is None else stdin)
            and isatty(sys.stdout if stdout is None else stdout))


def _say(text: str) -> None:
    """What a terminal's opening says, on stderr: stdout is the machine's screen alone."""
    print(text, file=sys.stderr, flush=True)


def _here() -> None:
    """A terminal opens from macOS or Linux alone: said before anything is asked of the platform, so no machine is
    opened for one that cannot be used."""
    if os.name == "nt":
        raise InvalidRequest("a terminal opens from macOS or Linux: on Windows, give a command after -- (e.g. -- pip "
                             "list) and it runs once")


def _terminal(info: dict, words: list[str], old: str) -> int:
    from seq.terminal import Terminal

    rest = _words(words)
    return Terminal(info, command=command_of(rest) if rest else None, old=old).run()


def _old(name: str, version, *, kind: str) -> str:
    """A version built before terminals, in the words a command's refusal has for one (the gateway's shell_not_in_version):
    deployed or registered again, its machines have one."""
    at = f" v{version}" if version else ""
    if kind == "benchmark":
        return (f"{name}{at} was built by a previous version of the platform, whose machines open no terminal: register "
                "it again and its new machines will")
    return (f"{name}{at} was built by a previous version of the platform, whose workers open no terminal: deploy it "
            "again and its new workers will")


def terminal(name: str, words: list[str], *, worker: str | None = None, base_url: str | None = None) -> int:
    """`seq policy shell NAME [-- COMMAND]` in a terminal on a worker of `name` serving now (`worker`, else one): the
    command's exit code, or the shell's. (POST /v1/deployments/{name}/shell with no command: where and by what.)"""
    from seq.deployments_cli import _call

    _here()
    info = _call("POST", f"/v1/deployments/{segment(name)}/shell", base_url, {"worker": worker} if worker else {})
    _say(f"a terminal on worker {info.get('worker')} of {name} v{info.get('version')}: it ends as you leave it, or as "
         "the worker does")
    return _terminal(info, words, _old(name, info.get("version"), kind="policy"))


def debug(name: str, *, episode: str | None = None, base_url: str | None = None, clock=time.monotonic) -> int:
    """`seq policy debug NAME [--episode ID]`: a debug machine of `name`, opened and waited for as a benchmark's shell
    machine is - its 202 the same body, read by the same code - then a terminal on it: its exit code.
    (POST /v1/deployments/{name}/debug.)"""
    _here()
    out = _machine_up(f"/v1/deployments/{segment(name)}/debug", {"episode": episode} if episode else {},
                      base_url=base_url, echo=_say, clock=clock, what=f"the debug machine for {name}",
                      opening=f"opening a debug machine for {name} v{{version}}, set up as its workers are: it stays "
                              f"up {IDLE_MIN} minutes after you leave it (seq policy debug {name} --stop ends it)")
    _say(f"a terminal on the debug machine of {name} v{out.get('version')}")
    return _terminal(out, [], _old(name, out.get("version"), kind="policy"))


def debug_stop(name: str, *, base_url: str | None = None, echo=print) -> dict:
    """Its debug machine ended now: {"ended": [its name]} - none where none runs."""
    from seq.deployments_cli import _call

    out = _call("DELETE", f"/v1/deployments/{segment(name)}/debug", base_url)
    echo(f"ended the debug machine of {name}" if out.get("ended") else f"no debug machine of {name} runs")
    return out


def command_of(words: list[str], kind: str = "policy") -> str:
    """What runs: one word as it is - a line with pipes, `&&` and quotes your shell left whole - else the words quoted
    and joined, as you typed them."""
    words = _words(words)
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
    body = {"command": command_of(words, "benchmark"), "timeout_s": timeout_s,
            **({"version": version} if version is not None else {})}
    out = _machine_up(_bench_path(name), body, base_url=base_url, echo=echo, clock=clock, timeout=timeout_s + 45,
                      what=f"the machine for {name}", opening=_bench_opening(name, "your last command"))
    return _said(out, timeout_s, echo)


def benchmark_terminal(name: str, words: list[str], *, version: int | None = None, base_url: str | None = None,
                       clock=time.monotonic) -> int:
    """`seq benchmark shell NAME [-- COMMAND]` in a terminal on its shell machine, opened as for a command: its exit
    code. (POST /v1/benchmarks/{name}/shell with no command: 202 as it opens, then where and by what.)"""
    _here()
    body = {"version": version} if version is not None else {}
    out = _machine_up(_bench_path(name), body, base_url=base_url, echo=_say, clock=clock, what=f"the machine for {name}",
                      opening=_bench_opening(name, "you leave it"))
    _say(f"a terminal on the shell machine of {name} v{out.get('version')}")
    return _terminal(out, words, _old(name, out.get("version"), kind="benchmark"))


def _bench_path(name: str) -> str:
    return f"/v1/benchmarks/{segment(name)}/shell"


def _bench_opening(name: str, after: str) -> str:
    return (f"opening a machine for {name} v{{version}}, set up as its evals' machines are: it stays up {IDLE_MIN} "
            f"minutes after {after} "
            f"(seq benchmark shell {name} --stop ends it)")


def _machine_up(path: str, body: dict, *, base_url: str | None, echo, clock, what: str, opening: str,
                timeout: float = 60) -> dict:
    """A shell or debug machine's answer once it is up, asked again while it opens - 202 {"state": "starting", ...}, the
    gateway's _starting - for WAIT_MOST_S at most: `opening` said once (its {version} filled in), then what it waits on as
    the platform words it, once a step and once each SAID_AGAIN_S it lasts."""
    from seq.deployments_cli import _call

    began, said, seen = clock(), False, None
    while (out := _call("POST", path, base_url, body, timeout=timeout)).get("state") == "starting":
        if not said:
            echo(opening.format(version=out.get("version")))
            said = True

        mark = (out.get("machine"), out.get("what"), int(out.get("since_s") or 0) // SAID_AGAIN_S)
        if out.get("sentence") and mark != seen:
            echo(f"  {out['sentence']}")
            seen = mark
        if clock() - began > WAIT_MOST_S:
            raise Unavailable(f"{what} did not open in {WAIT_MOST_S / 60:g} minutes: run it again")
        time.sleep(POLL_S)
    return out


def benchmark_stop(name: str, *, base_url: str | None = None, echo=print) -> dict:
    """Its shell machine ended now: {"ended": [its name]} - none where none runs. Said by its benchmark's name, a machine's own
    being the platform's. [CONFIRMED 100% - printed on c983e6bf]"""
    from seq.deployments_cli import _call

    out = _call("DELETE", f"/v1/benchmarks/{segment(name)}/shell", base_url)
    ended = out.get("ended") or []
    many = f"{len(ended)} shell machines" if len(ended) > 1 else "the shell machine"
    echo(f"ended {many} of {name}" if ended else f"no shell machine of {name} runs")
    return out


def _said(out: dict, timeout_s: float, echo) -> dict:
    """A command's answer echoed: its output, then its cut - and its time limit, when that stopped it, on stderr, stdout
    being the command's own (`echo` takes print's file=; under --json it drops the line, the answer's timed_out saying
    it).
"""
    if out.get("output"):
        echo(out["output"].rstrip("\n"))
    if out.get("truncated"):
        echo("(its output past the first 64 KB is not shown)")
    if out.get("timed_out"):
        echo(f"stopped after --timeout {timeout_s:g} s, before the command ended: --timeout gives it up to 120 s",
             file=sys.stderr)
    return out


def exit_code(out: dict) -> int:
    """This command's exit code: the command's own, TIMED_OUT at its time limit."""
    return TIMED_OUT if out.get("timed_out") else int(out.get("exit_code") or 0)
