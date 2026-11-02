"""probe metrics grouped/wide/export/plot/backfill/delete and probe series latest: read, plot and derive a run's metric series."""

from __future__ import annotations
import json
import sys
from enum import Enum
from pathlib import Path
from typing import Any

import typer
from ....sdk.reads.nonfinite import to_wire as nonfinite_to_wire
from probe.cli.commands.refs import _ref, run_ref


class Agg(str, Enum):
    mean = "mean"
    sum = "sum"
    min = "min"
    max = "max"
    count = "count"


# -- coordinate reads (below-run coordinates, research-os 0059-0062) ---------
metrics_app = typer.Typer(no_args_is_help=True, help="coordinate-aware metric reads")


@metrics_app.command("grouped")
def metrics_grouped(
    run: str = run_ref(),
    key: str = typer.Option(..., "--key"),
    kind: str = typer.Option(None, "--kind"),
    agg: Agg = typer.Option(
        None, "--agg", help="omit for the key's declared reduce fn (else mean)"
    ),
    by: list[str] = typer.Option(
        None, "--by", help="repeatable; one cell per combination of these coordinate axes"
    ),
    where: str = typer.Option(
        None, "--where", metavar="JSON", help='coord filter, e.g. \'{"split": "train"}\''
    ),
    step_bucket: int = typer.Option(None, "--step-bucket"),
    step_from: int = typer.Option(None, "--step-from"),
    step_to: int = typer.Option(None, "--step-to"),
    max_rows: int = typer.Option(None, "--max-rows"),
) -> None:
    """Server-side reduce/group over one metric's stepped points (paging followed)."""
    with _client() as c:
        _print_json(
            c.get_metrics_grouped(
                run,
                key,
                kind=kind,
                agg=agg.value if agg else None,
                by=by or None,
                where=_json_value(where),
                step_bucket=step_bucket,
                step_from=step_from,
                step_to=step_to,
                max_rows=max_rows,
            )
        )


@metrics_app.command("wide")
def metrics_wide(
    run: str = run_ref(),
    key: list[str] = typer.Option(None, "--key", help="repeatable; narrow to these keys"),
    kind: str = typer.Option(None, "--kind"),
    step_from: int = typer.Option(None, "--step-from"),
    step_to: int = typer.Option(None, "--step-to"),
    max_rows: int = typer.Option(None, "--max-rows"),
) -> None:
    """Step x metric table for a run (the DataFrame pivot; paging followed)."""
    with _client() as c:
        _print_json(
            c.get_metrics_wide(
                run,
                key=key or None,
                kind=kind,
                step_from=step_from,
                step_to=step_to,
                max_rows=max_rows,
            )
        )


@metrics_app.command("export")
def metrics_export(
    run: str = run_ref(),
    key: str = typer.Option(None, "--key"),
    kind: str = typer.Option(None, "--kind"),
    step_from: int = typer.Option(None, "--step-from"),
    step_to: int = typer.Option(None, "--step-to"),
    limit: int = typer.Option(None, "--limit", help="page size of the keyset walk"),
) -> None:
    """Lossless raw-point export, one JSON point per line.

    NDJSON rather than one array on purpose: the export is the unbounded read,
    and a stream that prints as it pages can be piped without buffering the run.
    """
    with _client() as c:
        for point in c.export_metric_points(
            run, key=key, kind=kind, step_from=step_from, step_to=step_to, limit=limit
        ):
            print(json.dumps(nonfinite_to_wire(point), default=str))


@metrics_app.command("plot")
def metrics_plot(
    run: str = run_ref(),
    key: list[str] = typer.Option(
        None, "--key", help="repeatable; a panel per matching series. Omit for the whole board"
    ),
    kind: str = typer.Option(None, "--kind"),
    step_from: int = typer.Option(None, "--step-from"),
    step_to: int = typer.Option(None, "--step-to"),
    max_rows: int = typer.Option(None, "--max-rows"),
    overlay: bool = typer.Option(
        False, "--overlay", help="draw the --keys together on one shared y-axis"
    ),
    width: int = typer.Option(None, "--width", help="plot width in cells (default: the terminal)"),
    height: int = typer.Option(12, "--height", help="plot height in cells"),
    no_color: bool = typer.Option(False, "--no-color", help="never emit ANSI color"),
    plain: bool = typer.Option(False, "--ascii", help="ASCII only: no braille, no box drawing"),
) -> None:
    """Draw a run's curves in this terminal, off the same read `metrics wide` does.

    Bare, it prints the BOARD: every series the run logged, one sparkline each,
    with last/min/max beside it -- the overview you want before choosing what to
    look at. `--key` promotes those series to full panels with axes and ticks.

    `--overlay` puts several keys on ONE canvas, which means one y-axis: curves
    on different scales are still drawn truthfully, but the smaller one flattens
    against the floor, and you are told when that has happened. Two metrics that
    do not share a scale are better read as the two panels you get by default.

    Unlike its siblings here this takes any run ref (a slug as well
    as a uuid) -- it is the verb a human types, not one a script pipes.
    """
    from ..runs import charts

    if overlay and not key:
        raise typer.BadParameter("--overlay needs the --key series it should overlay")
    with _client() as c:
        table = c.get_metrics_wide(
            _ref(c, "run", run).id,
            key=key or None,
            kind=kind,
            step_from=step_from,
            step_to=step_to,
            max_rows=max_rows,
        )
    series = charts.series_from_wide(table)
    # Everything the picture cannot show goes to stderr before it is drawn. A
    # chart is read as the whole truth about a run, so a window that was cut
    # short, a key that matched nothing, or a NaN that could not be given a row
    # has to be said in words -- none of them has a shape on the canvas.
    if table.get("truncated"):
        typer.echo(
            f"PARTIAL: the read stopped at step {table.get('next_step')} -- this is not the "
            "whole curve. Narrow with --step-from/--step-to, or raise --max-rows",
            err=True,
        )
    if key:
        missing = [k for k in key if k not in {c.get("key") for c in table.get("columns") or []}]
        if missing:
            typer.echo(f"no series for: {', '.join(missing)}", err=True)
    nonfinite = [s for s in series if s.dropped]
    if nonfinite:
        typer.echo(
            "non-finite points (NaN/inf) cannot be plotted and are not drawn: "
            + ", ".join(f"{s.label} ({s.dropped})" for s in nonfinite),
            err=True,
        )
    series = [s for s in series if s.points]
    if not series:
        typer.echo(
            "no plottable metric points in that window"
            + (f" for {', '.join(key)}" if key else "")
            + " -- `probe run series RUN` lists what the run logged",
            err=True,
        )
        return
    shape = {
        "width": width,
        "color": False if no_color else None,
        "unicode": False if plain else None,
    }
    if not key:
        print(charts.board(series, **shape))
        return
    if overlay:
        kept, dropped = series[: charts.MAX_OVERLAY], series[charts.MAX_OVERLAY :]
        if dropped:
            # Never silently: a chart that shows six of nine series and says so
            # is a partial read; one that shows six and does not is a wrong one.
            typer.echo(
                f"overlaying the first {charts.MAX_OVERLAY}, dropped: "
                + ", ".join(s.label for s in dropped),
                err=True,
            )
        print(
            charts.panel(
                kept,
                title=" + ".join(s.label for s in kept),
                footer=charts.overlay_footer(kept, unicode=shape["unicode"]),
                height=height,
                **shape,
            )
        )
        return
    for index, item in enumerate(series):
        if index:
            print()
        print(
            charts.panel(
                [item],
                title=item.label,
                footer=charts.summarize(item, unicode=shape["unicode"]),
                height=height,
                **shape,
            )
        )


def _derived_series_points(source: str) -> list[tuple[int, float]]:
    """Read a (step, value) series from a file or stdin.

    Three spellings, because three things produce these and none of them should
    have to reshape for the others:

      JSONL   {"step": 0, "value": 1.2}          one object per line
              [0, 1.2]                            or one pair per line
      JSON    [{"step": 0, "value": 1.2}, ...]   a whole document
              {"0": 1.2, "1": 0.9}                a step -> value map

    Detected by trying the whole document as JSON first and falling back to
    line-by-line, so a single-line JSON array is not mistaken for JSONL.
    """
    text = sys.stdin.read() if source == "-" else Path(source).read_text()

    def pair(item: Any, where: str) -> tuple[int, float]:
        if isinstance(item, dict):
            if "step" not in item or "value" not in item:
                raise typer.BadParameter(f'{where}: needs "step" and "value"')
            step, value = item["step"], item["value"]
        elif isinstance(item, (list, tuple)):
            if len(item) != 2:
                raise typer.BadParameter(f"{where}: a pair is [step, value]")
            step, value = item
        else:
            raise typer.BadParameter(f"{where}: expected an object or a [step, value] pair")
        try:
            return int(step), float(value)
        except (TypeError, ValueError) as exc:
            raise typer.BadParameter(f"{where}: {exc}") from exc

    try:
        document = json.loads(text)
    except json.JSONDecodeError:
        document = None
    if document is not None:
        if isinstance(document, dict):
            # A one-row JSONL file parses as a whole JSON document too, so the
            # point spelling has to be recognised BEFORE the map spelling --
            # otherwise a single {"step": 0, "value": 1.2} is read as a map with
            # the steps "step" and "value" and dies converting them.
            if "step" in document and "value" in document:
                return [pair(document, "the point")]
            # A step -> value map, sorted numerically rather than lexically: JSON
            # object keys are strings, so insertion order puts step 10 before
            # step 2 and the curve reads as written out of order.
            return sorted(pair([step, value], f"step {step!r}") for step, value in document.items())
        if isinstance(document, list):
            return [pair(item, f"item {i}") for i, item in enumerate(document)]
        raise typer.BadParameter("expected a JSON array, a step->value object, or JSONL")

    points: list[tuple[int, float]] = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise typer.BadParameter(f"line {lineno}: not JSON: {exc}") from exc
        points.append(pair(item, f"line {lineno}"))
    return points


@metrics_app.command("backfill")
def metrics_backfill(
    run: str = typer.Argument(...),
    key: str = typer.Option(..., "--key", help="the series to write"),
    producer: str = typer.Option(
        ..., "--producer", help="what computed it, e.g. claude-code or score_auc.py"
    ),
    series: str = typer.Option(
        "-",
        "--from",
        metavar="FILE",
        help="JSONL or JSON step/value series; '-' (the default) reads stdin",
    ),
    kind: str = typer.Option("model", "--kind"),
    dim: list[str] = typer.Option(None, "--dim", metavar="k=v"),
    agg: Agg = typer.Option(None, "--agg"),
    note: str = typer.Option(None, "--note", help="why/how, free text"),
    input_key: list[str] = typer.Option(
        None, "--input", metavar="KEY", help="repeatable; stored series the computation read"
    ),
    code_ref: str = typer.Option(None, "--code-ref", help="repo path / commit / script"),
) -> None:
    """Write a whole DERIVED curve in ONE request.

    The batch door beside `probe log --derived`, which takes one step per
    invocation on purpose — the async outbox carries `log` bodies and a derived
    batch is a different shape, so it stayed synchronous and single-step. That is
    fine for a correction and wrong for a backfill: a 20k-step curve through it is
    20k round trips. This is the same provenance, the same series identity, one
    request.

    The series comes from --from FILE or stdin, as JSONL objects
    ({"step": 0, "value": 1.2}), JSONL [step, value] pairs, a JSON array of
    either, or a JSON {step: value} object:

        probe metrics backfill RUN --key eval/auroc --producer score_auc.py \\
            --from curve.jsonl

    Provenance is not optional here for the same reason it is not on --derived:
    a computed series without it is indistinguishable from a measured one.
    """
    points = _derived_series_points(series)
    if not points:
        raise typer.BadParameter(f"no points in {'stdin' if series == '-' else series}")
    dims = _kv_pairs(dim) if dim else None
    with _client() as c:
        _run_handle(c, run).log_derived_series(
            key,
            points,
            producer=producer,
            note=note,
            inputs=list(input_key) if input_key else None,
            code_ref=code_ref,
            kind=kind,
            dimensions=dims,
            agg=agg.value if agg else None,
        )
    steps = f"steps {points[0][0]}..{points[-1][0]}" if len(points) > 1 else f"step {points[0][0]}"
    print(
        f"backfilled {len(points)} derived point(s) of {kind}/{key} to {run} "
        f"({steps}, producer={producer}, 1 request)"
    )


@metrics_app.command("delete")
def metrics_delete(
    run: str = run_ref(),
    key: str = typer.Option(..., "--key"),
    kind: str = typer.Option("model", "--kind"),
    dim: list[str] = typer.Option(None, "--dim", metavar="k=v", help="pin ONE dimension variant"),
    yes: bool = typer.Option(False, "--yes", help="skip the confirmation"),
) -> None:
    """Delete a DERIVED series and its points.

    The undo for a computed metric that was wrong. Derived only — a logged
    series is the run's captured record and the server refuses (409).

    Omitting --dim addresses the dimension-less series, NOT every variant of the
    key: a key logged per-rank needs the pin.
    """
    dims = _kv_pairs(dim) if dim else None
    label = f"{kind}/{key}" + (f" {dims}" if dims else "")
    _confirm_delete(yes, f"derived series {label} on run {run}")
    with _client() as c:
        c.delete_series(run, key=key, kind=kind, dimensions=dims)
    print(f"deleted derived series {label}")


series_app = typer.Typer(no_args_is_help=True, help="cross-run series reads")


@series_app.command("latest")
def series_latest(
    runs: list[str] = typer.Argument(..., metavar="RUN..."),
    key: list[str] = typer.Option(None, "--key", help="repeatable; narrow to these keys"),
    kind: str = typer.Option(None, "--kind"),
) -> None:
    """Cross-run scalar summary (last/min/max per series) from the catalog."""
    with _client() as c:
        _print_json(c.latest_scalars(runs, keys=key or None, kind=kind))
from probe.cli.commands.delete import _confirm_delete  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.flag_values import _json_value, _kv_pairs  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.run_handle import _run_handle  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
