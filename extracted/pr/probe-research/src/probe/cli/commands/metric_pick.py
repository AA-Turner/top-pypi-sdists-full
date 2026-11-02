"""a set verb's metric/goal/reduce and best-pick flags, and the 409 a person's own pick answers with."""

from __future__ import annotations
import sys
from collections.abc import Callable
from enum import Enum
from typing import Any

import typer

from ... import errors
# The option enums only, from `_generated.enums` rather than `probe.models`: that
# seam builds every wire model, ~0.5 s that every command paid at startup -- the
# wizard, the hooks and the status line included -- whether or not it sent one.
# `tests/test_cli_startup_imports.py` holds the CLI to this.
from ...generated.enums import (
    MetricGoal,
    MetricReduce)


# -- the declared headline metric and the best pick ---------------------------
#
# Declarations, never computed: which metric ranks the work, and which
# experiment is best. Who made one comes from the credential, and every CLI key
# is an AGENT's (a person and their agents share it). An agent never writes
# over a person's: the server answers 409 naming theirs, and there is no
# override flag -- the person changes it from the dashboard.


class PersonsDeclaration(str, Enum):
    """The 409 codes of a write over a person's metric or pick (app/metrics/router.py)."""

    METRIC = "METRIC_IS_A_PERSONS"
    PICK = "PICK_IS_A_PERSONS"


def metric_opt() -> Any:
    return typer.Option(None, "--metric", help='headline metric key (`test/acc`); "" clears')


def goal_opt() -> Any:
    return typer.Option(None, "--goal", help="with --metric: which way is better")


def reduce_opt() -> Any:
    return typer.Option(None, "--reduce", help="with --metric: run value used (default final)")


def best_opt() -> Any:
    return typer.Option(None, "--best", help='best experiment (slug or id:<uuid>); "" clears')


def pick_reason_opt() -> Any:
    return typer.Option(None, "--reason", help="with --best: why, 1-2 sentences")


def _metric_args(metric: str, goal: "MetricGoal | None", reduce: "MetricReduce | None") -> bool:
    """Check `--metric`'s companions; True when it CLEARS (`--metric ""`)."""
    if not metric.strip():
        if goal is not None or reduce is not None:
            raise typer.BadParameter('--metric "" takes no --goal or --reduce')
        return True
    if goal is None:
        raise typer.BadParameter("--metric needs --goal max|min")
    return False


def _pick_args(best: str, reason: str | None) -> bool:
    """Check `--best`'s reason; True when it CLEARS (`--best ""`)."""
    if not best.strip():
        return True
    if not (reason and reason.strip()):
        raise typer.BadParameter("--best needs --reason")
    return False


def _persons_declaration(detail: Any) -> list[str] | None:
    """What a 409 over a person's metric or pick names, as lines to print; None
    for any other conflict."""
    if not isinstance(detail, dict):
        return None
    code = detail.get("code")
    if code == PersonsDeclaration.METRIC.value:
        held = detail.get("metric") if isinstance(detail.get("metric"), dict) else {}
        what = (
            "cleared here"
            if held.get("cleared")
            else f"{held.get('key')} ({held.get('goal')}, {held.get('reduce')})"
        )
        return [f"their metric: {what}, by {held.get('set_by')} at {held.get('set_at')}"]
    if code == PersonsDeclaration.PICK.value:
        pick = detail.get("pick") if isinstance(detail.get("pick"), dict) else {}
        experiment = pick.get("experiment") if isinstance(pick.get("experiment"), dict) else None
        if experiment is not None:
            what = f"{experiment.get('name')} ({experiment.get('slug')}, id:{experiment.get('id')})"
        elif pick.get("gone"):
            what = "an experiment no longer here"
        else:
            what = "an experiment you cannot read"
        return [f"their pick: {what}, by {pick.get('by')} at {pick.get('at')}"]
    return None


def _declare(write: Callable[[], Any]) -> None:
    """Run a metric or pick write and print what it answers. A 409 over a
    person's declaration is said plainly -- the server's message, then whose
    and what -- and exits 1; any other error goes to the CLI's own handler."""
    try:
        result = write()
    except errors.ConflictError as exc:
        lines = _persons_declaration(exc.detail)
        if lines is None:
            raise
        print(f"error: {exc}", file=sys.stderr)
        for line in lines:
            print(f"       {line}", file=sys.stderr)
        raise typer.Exit(1) from exc
    _print_json(result)
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
