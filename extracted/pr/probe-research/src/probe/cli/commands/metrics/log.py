"""probe log: append metric points (queued or direct), failing when the outbox dropped them."""

from __future__ import annotations
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from probe import analytics as probe_telemetry
    from ....sdk.client.client import Client
else:
    #: The SDK client class: a module global so the CLI package can monkeypatch
    #: it in tests, and None until then. The SDK client imports every wire model,
    #: so a command imports it when it builds one (`_client_class`), not at start.
    Client = None

import typer
from probe.cli.cli import app
from probe.cli.connection import (
    _UNDELIVERED,
    _client,
    _default_client,
    _kick_drainer,
    _resolve_write_mode,
    write_mode_opt,
)


@app.command()
def log(
    run: str = typer.Argument(...),
    metric: list[str] = typer.Argument(..., metavar="key=value..."),
    write_mode: Optional[bool] = write_mode_opt(),
    step: int = typer.Option(None, "--step"),
    kind: str = typer.Option("model", "--kind"),
    dim: list[str] = typer.Option(
        None,
        "--dim",
        metavar="k=v",
        help="LOW-CARDINALITY grouping axis (split/seed/rank). Never an id — each "
        "distinct value is its own one-point series, i.e. a tile, not a graph",
    ),
    agg: Agg = typer.Option(
        None, "--agg", help="declare the key's reduce fn for grouped reads (0062)"
    ),
    derived: bool = typer.Option(
        False,
        "--derived",
        help="these values were COMPUTED after the fact, not measured live; needs --producer",
    ),
    producer: str = typer.Option(
        None, "--producer", help="what computed them, e.g. claude-code or score_auc.py"
    ),
    note: str = typer.Option(None, "--note", help="why/how, free text"),
    input_key: list[str] = typer.Option(
        None, "--input", metavar="KEY", help="repeatable; stored series the computation read"
    ),
    code_ref: str = typer.Option(None, "--code-ref", help="repo path / commit / script"),
) -> None:
    """Append metric points. --dim adds series dimensions (fold #9).

    Shape first: a series is (run, kind, key, dims), so every distinct --dim
    combination is a SEPARATE series, and a one-point series renders as a scalar
    tile, not a graph. Only --step makes a curve; spreading values across a
    dimension does not. Budget series ≈ the product of your --dim cardinalities
    and keep it under ~50. This fails SILENTLY — every call succeeds and the
    values are right; the only symptom is an unreadable run page — so check with
    `probe metrics grouped` / the run's series list rather than assuming.

    Per-sample identity (example_id, row id, uuid, filename) has NO door here:
    the SDK puts it in `labels`, and this command has no --label. Log per-item
    detail as an artifact (`probe artifact add`) and leave metrics for the
    handful of numbers a human should see.

    --derived marks the batch as computed rather than measured — the door for
    backfilling a metric onto a run that has already finished. It requires
    --producer and a --step, and records provenance beside the points so a
    reader can always tell a computed curve from a captured one.
    """
    metrics = _kv_pairs(metric, cast_float=True)
    dims = _kv_pairs(dim) if dim else None

    if producer and not derived:
        raise typer.BadParameter("--producer only applies to --derived")
    if derived:
        if not producer:
            raise typer.BadParameter(
                "--derived needs --producer: a computed series without provenance is "
                "indistinguishable from a logged one"
            )
        if step is None:
            raise typer.BadParameter(
                "--derived needs an explicit --step: a backfill lands on steps that "
                "already exist, so there is no counter to auto-increment"
            )
        # Deliberately synchronous: the async outbox carries `log` bodies, and a
        # derived batch is a different shape. A backfill is not on the hot path.
        with _client() as c:
            _run_handle(c, run).log_derived(
                metrics,
                step=step,
                producer=producer,
                note=note,
                # `if input_key` and not `list(...) or None`: typer hands back
                # None, not (), for a repeatable option nobody passed, so the
                # bare list() raised TypeError on every --derived write without
                # --input. The one test covering this path always passed --input.
                inputs=list(input_key) if input_key else None,
                code_ref=code_ref,
                kind=kind,
                dimensions=dims,
                agg=agg.value if agg else None,
            )
        print(f"logged {len(metrics)} derived metric(s) to {run} (producer={producer})")
        return

    _check_ref_shape(run)
    with _default_client(_resolve_write_mode(write_mode)) as c:
        if c.async_writes:
            # `_async_run`, not `_run_handle`: the sync path reads the run first
            # (a GET per write), which is the round trip queueing exists to
            # avoid. The server validates the ref at replay.
            dropped_before = c.dropped_writes
            direct_before = c.direct_sends
            _async_run(c, run).log(
                metrics,
                step=step,
                kind=kind,
                dimensions=dims,
                agg=agg.value if agg else None,
            )
            _fail_if_dropped(c, dropped_before, f"{len(metrics)} metric(s) for {run}")
            if c.direct_sends > direct_before:
                # Below the outbox's free-space floor it went straight to the
                # server instead (plan 1.5): say what happened.
                print(f"logged {len(metrics)} metric(s) to {run} (sent: outbox low on disk)")
                return
            _kick_drainer()
            print(f"logged {len(metrics)} metric(s) to {run} (queued)")
            return
        _run_handle(c, run).log(
            metrics, step=step, kind=kind, dimensions=dims, agg=agg.value if agg else None
        )
        # A sync write the server did not answer is queued (L14): say so, not
        # "delivered" -- the word a script trusts.
        word = _UNDELIVERED.word()
    # The delivery word is ALWAYS present, in both branches. Whether a write
    # queued or landed now depends on credentials, PROBE_ASYNC and a flag that
    # may be on either side of the subcommand -- none of which the caller can see
    # from the outside. A stable `(queued|delivered)` suffix is what lets a
    # script decide deterministically instead of inferring from three shapes.
    print(f"logged {len(metrics)} metric(s) to {run} ({word})")


def _fail_if_dropped(client: Client, before: int, what: str) -> None:
    """Exit non-zero when the outbox swallowed the write we just handed it.

    `Client._enqueue` fails OPEN by design: a broken outbox must not kill a
    training step, so it records the gap, warns, and returns normally. The bool
    it returns then dies in `write()`, which returns None either way -- so
    without this check the CLI prints "(queued)" for data that reached nothing
    and exits 0. A queued write may be undelivered; it may not be imaginary.
    """
    if client.dropped_writes > before:
        typer.echo(
            f"probe: {what} was NOT queued - the outbox could not be written "
            "(see the warning above). Fix the spool, then re-run; "
            "`probe outbox status` shows what is on disk.",
            err=True,
        )
        raise typer.Exit(2)
from probe.cli.commands.flag_values import _kv_pairs  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.metrics.metrics import Agg  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.refs import _check_ref_shape  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.run_handle import _async_run, _run_handle  # noqa: E402 -- pieces need each other; the front door loads this one first
