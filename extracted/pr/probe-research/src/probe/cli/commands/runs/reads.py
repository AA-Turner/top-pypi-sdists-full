"""print what Probe holds of a run: probe get / run get / bundle / events / coordinates and run check/series/metrics/inputs/upstream."""

from __future__ import annotations
import sys

import typer
from ....sdk.reads.nonfinite import to_wire as nonfinite_to_wire
from ....shared.reads import reads
from probe.cli.cli import app
from probe.cli.commands.json_print import _FIELDS_OPTION, _emit, _print_json, _select_fields
from probe.cli.commands.refs import _api, _ref, run_ref
from probe.cli.commands.runs.runs import run_app


@run_app.command("check")
def run_check(
    run: str = run_ref(),
    verify: bool = typer.Option(False, "--verify"),
) -> None:
    """Assess capture completeness (exit 2 if incomplete).

    Default is `unverified`: nothing is obviously absent, which is NOT the same
    as "this run can be rebuilt". `--verify` resolves the recorded code commit
    against its remote and is the only way to earn `complete`.

    `advisories` lists reported-but-not-blocking gaps (notes, inputs-decision,
    legacy runs without launch context).
    """
    with _client() as c:
        printed = reads.run_check(_api(c, pretty=sys.stdout.isatty()), run, verify)
    _emit(printed)


@run_app.command("series")
def run_series(run: str = run_ref()) -> None:
    """Per-series summary for a run (key/kind/dimensions + first/last/min/max)."""
    with _client() as c:
        _print_json(c.run_series(_ref(c, "run", run).id))


@run_app.command("metrics")
def run_metrics(
    run: str = run_ref(),
    key: str = typer.Option(None, "--key"),
    kind: str = typer.Option(None, "--kind"),
    limit: int = typer.Option(None, "--limit"),
) -> None:
    """Raw metric points for a run."""
    with _client() as c:
        points = c.run_metrics(_ref(c, "run", run).id, key=key, kind=kind, limit=limit)
        _print_json([nonfinite_to_wire(point) for point in points])


# -- what a run READ, and what it built on (lineage plan L5) ------------------
@run_app.command("inputs")
def run_inputs(run: str = run_ref()) -> None:
    """The files a run READ, as the SDK recorded them: path, size, hash and
    when it was first seen.

    Each read carries `stored_as`: the catalog entries holding exactly those
    bytes (`basis` `same_bytes`, or `pre_redaction` when the stored copy was
    redacted), at most 10 (`stored_as_truncated`). That is evidence, never a
    link: record what the run used with `probe dataset use` / `probe
    checkpoint use`. An older server answers `matches` instead. `coverage` is
    what the recorder could see, including whether it stopped listing
    (`truncated`).
    """
    with _client() as c:
        _print_json(c.run_inputs(_ref(c, "run", run).id))


@run_app.command("upstream")
def run_upstream(
    run: str = run_ref(),
    depth: int = typer.Option(2, "--depth", min=1, max=5, help="how many hops back (1-5)"),
) -> None:
    """What a run built on, `--depth` hops back: its parents (retry, fork,
    resume, branch), runs it built on, and the run that made each dataset or
    checkpoint it used, then the same for each of those. `truncated` says the
    walk stopped early."""
    with _client() as c:
        _print_json(c.run_upstream(_ref(c, "run", run).id, depth=depth))


@app.command()
def coordinates(run: str = run_ref()) -> None:
    """The run's coordinate catalog: every coordinate any fact landed on."""
    with _client() as c:
        _print_json(c.list_run_coordinates(run))


@app.command()
def get(run: str = run_ref(), fields: str = _FIELDS_OPTION) -> None:
    """Print a run."""
    with _client() as c:
        _print_json(_select_fields(c.get_run(run), fields))


# `probe get` is a bare verb that silently means "a RUN", while every other noun
# reads with `<noun> get`. Someone who learned `project get` looks for `run get`
# and does not find it. Both spellings work now; the top-level one stays because
# it is the older habit and is in scripts.
@run_app.command("get")
def run_get(run: str = run_ref(), fields: str = _FIELDS_OPTION) -> None:
    """Show one run."""
    with _client() as c:
        _emit(reads.run_get(_api(c, pretty=sys.stdout.isatty()), run, fields))


@app.command()
def bundle(run: str = typer.Argument(...)) -> None:
    """Print a run bundle (run + series + artifacts)."""
    with _client() as c:
        _print_json(c.run_bundle(run))


@app.command()
def events(run: str = run_ref()) -> None:
    """Read the backend lifecycle events for a run (fold #10, read-only)."""
    with _client() as c:
        _print_json(c.events.for_run(run))
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
