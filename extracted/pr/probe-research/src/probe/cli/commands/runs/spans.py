"""probe span add/list/get: trajectory spans on a run."""

from __future__ import annotations
from typing import Optional

import typer
from probe.cli.connection import (
    _client,
    _default_client,
    _kick_drainer,
    _resolve_write_mode,
    write_mode_opt,
)


# -- spans ------------------------------------------------------------------
span_app = typer.Typer(no_args_is_help=True, help="trajectory spans")


@span_app.command("add")
def span_add(
    run: str = typer.Argument(...),
    span_type: str = typer.Option(..., "--type"),
    name: str = typer.Option(None, "--name"),
    step: int = typer.Option(None, "--step"),
    provider: str = typer.Option(None, "--provider"),
    external_key: str = typer.Option(None, "--external-key"),
    parent: str = typer.Option(None, "--parent"),
    status: str = typer.Option("running", "--status"),
    attr: list[str] = typer.Option(None, "--attr", metavar="k=v"),
    write_mode: Optional[bool] = write_mode_opt(),
) -> None:
    """Upsert a span."""
    _check_ref_shape(run)
    with _default_client(_resolve_write_mode(write_mode)) as c:
        if c.async_writes:
            handle = _async_run(c, run).span(
                span_type,
                name=name,
                step_index=step,
                provider=provider,
                external_key=external_key,
                parent_span_id=parent,
                status=status,
                attributes=_kv_pairs(attr) if attr else None,
            )
            _kick_drainer()
            # The span id is minted CLIENT-SIDE, so queueing still hands back the
            # real id -- this is the whole reason `span add` can be queued at all
            # while a verb whose id the server mints cannot.
            print(handle)
            return
        span_id = _run_handle(c, run).span(
            span_type,
            name=name,
            step_index=step,
            provider=provider,
            external_key=external_key,
            parent_span_id=parent,
            status=status,
            attributes=_kv_pairs(attr) if attr else None,
        )
    print(span_id)


@span_app.command("list")
def span_list(
    run: str = typer.Argument(...),
    span_type: str = typer.Option(None, "--type"),
    parent: str = typer.Option(None, "--parent"),
    step_from: int = typer.Option(None, "--step-from"),
    step_to: int = typer.Option(None, "--step-to"),
    limit: int = typer.Option(None, "--limit"),
) -> None:
    """Read a run's spans back."""
    with _client() as c:
        _print_json(
            c.run_spans(
                # GET /v1/runs/{run_id}/spans types its path param as a UUID, so a
                # petname reached it as a 422 -- on the one kind whose petname is
                # the handle people are handed. `span add` two commands up already
                # resolves (via _run_handle); this read did not.
                _ref(c, "run", run).id,
                span_type=span_type,
                parent_span_id=parent,
                step_from=step_from,
                step_to=step_to,
                limit=limit,
            )
        )


@span_app.command("get")
def span_get(span_id: str = typer.Argument(...)) -> None:
    """Print one span."""
    with _client() as c:
        _print_json(c.get_span(span_id))
from probe.cli.commands.flag_values import _kv_pairs  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.refs import _check_ref_shape, _ref  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.run_handle import _async_run, _run_handle  # noqa: E402 -- pieces need each other; the front door loads this one first
