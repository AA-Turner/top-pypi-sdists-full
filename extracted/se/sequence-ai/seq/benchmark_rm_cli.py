"""
`seq benchmark rm <name>`.

A deleted benchmark is gone for good, at once: what it stores goes, its name and its place in your account's quota are free,
a build in flight stops, and nothing can bring it back. The evals that ran it keep their reports and recordings, the
recordings billed as storage until those evals are deleted. An eval running or waiting
on it refuses the delete unless --force cancels it; --dry-run says what it would touch and does nothing. {the user 11-01:
"delete is permanent no save"} `seq benchmark rm <name>@vN` deletes that version alone, the benchmark and its other
versions staying: every version is kept until you delete it.
"""
from __future__ import annotations

from typing import Callable


def _client(base_url: str | None):
    from seq._eval_gateway import EvalGatewayClient

    return EvalGatewayClient(base_url=base_url)


def rm(name: str, *, dry_run: bool = False, force: bool = False, base_url: str | None = None,
       echo: Callable[[str], None] = print) -> dict:
    """Delete a benchmark for good (or, `dry_run`, say what deleting it would touch), printed - or, `name@vN`, that
    version alone (_rm_version)."""
    from seq.cli_parser import at_version

    name, version = at_version(name)
    if version is not None:
        return _rm_version(name, version, dry_run=dry_run, base_url=base_url, echo=echo)
    out = _client(base_url).delete_benchmark(name, dry_run=dry_run, force=force)
    if dry_run:
        echo(f"deleting benchmark {out['benchmark']} (v{out.get('version')}, {out.get('status')}) would:")
        echo("  delete it for good, and what it stores: nothing can bring it back")
        echo("  free its name and its place in your quota at once")
        evals = out.get("evals")
        if evals is None:
            echo("  keep the reports and recordings of the evals that ran it (how many could not be read): the recordings are billed as storage until you delete those evals")
        elif evals:
            echo(f"  keep the reports and recordings of the {evals} eval{'' if evals == 1 else 's'} that ran it: the recordings are billed as storage until you delete those evals")
        if out.get("build_in_flight"):
            echo("  stop its build in flight")
        for e in out.get("evals_running") or []:
            echo(f"  refuse while eval {e} runs or waits on it — or cancel it, with --force")
        _copies(out, echo)
        return out
    echo(f"deleted benchmark {out['deleted']} for good: its name is free, and nothing can bring it back")
    for e in out.get("evals_canceled") or []:
        echo(f"  canceled eval {e}")
    if out.get("build_canceled"):
        echo("  its build in flight was stopped")
    _copies(out, echo)
    return out


def _rm_version(name: str, version: int, *, dry_run: bool, base_url: str | None, echo: Callable[[str], None]) -> dict:
    """`seq benchmark rm NAME@vN`: that version deleted for good, the benchmark and its other versions staying (DELETE
    .../versions/N) - a kept one goes once no eval runs it, a failed one at once; its latest is refused, as the one
    evals run while the latest is out is - as `seq policy rm NAME@vN`."""
    out = _client(base_url).delete_benchmark_version(name, version, dry_run=dry_run)
    if dry_run:
        echo(f"deleting {name}@v{version} would delete that version for good: nothing can bring it back; {name} and its "
             "other versions stay")
    elif out.get("state") == "deleting":
        echo(f"deleted {name}@v{version} for good: what it holds goes once no eval runs it, and nothing can bring it "
             "back")
    else:
        echo(f"deleted {name}@v{version} for good")
    return out


def _copies(out: dict, echo: Callable[[str], None]) -> None:
    """What the delete takes of its versions' own copies."""
    from seq import deps_cost

    gone = deps_cost.delete_line(out.get("dependencies"))
    if gone:
        echo(f"  {gone}")
