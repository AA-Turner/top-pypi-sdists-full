"""Click commands for `montecarlo agent-traces ...`.

Single subcommand today (`export`); group exists so we can add others later
(e.g. `list-recent` if/when an mcon-discoverability helper lands on the server).
"""

import click
from click.exceptions import Exit

from montecarlodata.agent_traces.export_service import (
    AgentTraceExportService,
    parse_trace_link,
)
from montecarlodata.errors import complain_and_abort


@click.group()
def agent_traces():
    """Commands for exporting agent traces."""


@agent_traces.command(
    "export",
    help=(
        "Export a full agent trace (tree + span content) to a gzipped JSON file.\n\n"
        "Kicks off an async export job on the server, polls until the artifact is "
        "ready, then downloads the presigned URL contents to disk."
    ),
)
@click.option(
    "--trace-link",
    required=True,
    help=(
        "Trace page URL copied from the Monte Carlo UI. The CLI parses out "
        "the trace table MCON and trace ID from the URL — the UI has a "
        "copy-link button on each trace page. Example: "
        "https://app.getmontecarlo.com/agents/MCON++.../ai-agent/traces/abc..."
    ),
)
@click.option(
    "--output",
    type=click.Path(dir_okay=False),
    help=(
        "Path to write the gzipped JSON to. "
        "Defaults to ./trace-<traceId>.json.gz in the current directory."
    ),
)
@click.option(
    "--timeout",
    "timeout_seconds",
    type=int,
    default=600,
    show_default=True,
    help="Max seconds to wait for the export to reach DONE before giving up.",
)
@click.option(
    "--poll-interval",
    "poll_interval_seconds",
    type=float,
    default=2.0,
    show_default=True,
    help="Seconds between status polls.",
)
@click.pass_obj
def export_agent_trace(
    ctx,
    trace_link: str,
    output: str,
    timeout_seconds: int,
    poll_interval_seconds: float,
):
    """Export an agent trace to gzipped JSON."""
    try:
        mcon, trace_id = parse_trace_link(trace_link)
    except ValueError as exc:
        # complain_and_abort writes "Error - <msg>" to stderr and raises
        # click.Abort, which Click renders as the standard "Aborted!" exit.
        complain_and_abort(str(exc))
        return  # unreachable; satisfies type narrowing for mcon/trace_id below

    service = AgentTraceExportService(
        config=ctx["config"],
        command_name="agent_traces_export",
    )
    # `service.export` returns False when the export is incomplete — either it
    # timed out before reaching a terminal status, or it landed on DONE_PARTIAL
    # (artifact downloaded but missing one or more spans, unusable for Agent
    # Preflight golden data). Both translate to Exit(2) so downstream shell /
    # Make tooling can detect the non-success case. Exit raised inside
    # @manage_errors gets converted to Abort — see
    # collector/commands.py:run_validations for the canonical
    # return-then-Exit pattern.
    completed = service.export(
        mcon=mcon,
        trace_id=trace_id,
        output=output,
        timeout_seconds=timeout_seconds,
        poll_interval_seconds=poll_interval_seconds,
    )
    if not completed:
        raise Exit(2)
