from __future__ import annotations

import asyncio
import gzip
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta
from http.server import ThreadingHTTPServer
from io import BytesIO
from pathlib import Path
from runpy import run_module, run_path
from typing import Any, Dict, List, Optional, Union

import click
import httpx
import msgpack

from .cli_mcp_shared import (
    format_trace_for_display,
    get_compact_traces,
    get_formatted_traces,
    get_node_data,
    parse_trace_timestamp,
)
from .config import load_config
from .core import enable
from .db import (
    TraceNotFoundError,
    convert_json_to_msgpack,
    delete_traces_before,
    delete_traces_by_id,
    get_db_path,
    get_migration_status,
    get_pinned_traces,
    list_traces_from_db,
    load_trace_from_db,
    migrate_traces_to_files,
    pin_trace,
    save_trace,
    setup_db,
    trace_exists,
    unpin_trace,
    vacuum_db,
)
from ._kolotxt import update_kolotxt
from .serialize import load_msgpack
from .trace import Trace
from .upload import upload_to_dashboard
from .utils import (
    maybe_format,
)
from .version import __version__
from .web.server import KoloRequestHandler

logger = logging.getLogger("kolo")

DATETIME_FORMATS = click.DateTime(
    (
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%d %H:%M:%S.%f",
    )
)


TRACE_NOT_FOUND_ERROR = "Could not find trace_id: `{trace_id}`"


def _run_auto_migration_if_needed():
    """
    Check if migration is needed and run it automatically.

    This is called before CLI commands to ensure traces are migrated
    from SQLite to file-based storage. Errors are logged but don't block
    CLI commands.
    """
    try:
        db_path = get_db_path()
        if not db_path.exists():
            return

        migration_status = get_migration_status(db_path)
        if migration_status["needs_migration"] == 0:
            return

        migrate_traces_to_files(db_path)
    except Exception as e:
        # Don't let migration errors block CLI commands
        logger.debug(f"Auto-migration failed: {e}")


# Commands that should NOT trigger auto-migration (performance-sensitive or migration-related)
_SKIP_MIGRATION_COMMANDS = {"run", "migrate"}


@click.group(invoke_without_command=True)
@click.version_option(__version__, "--version", "-v", "-V")
@click.pass_context
def cli(ctx):
    # Ensure the current working directory is on the path.
    # Important when running the `kolo` script installed by setuptools.
    # Not really necessary when using `python -m kolo`, but doesn't hurt.
    # Note, we use 1, not 0: https://stackoverflow.com/q/10095037
    # This probably doesn't matter for our use case, but it doesn't hurt.
    sys.path.insert(1, ".")

    # Run auto-migration if needed before interactive commands
    # Skip for performance-sensitive commands like `run`
    if ctx.invoked_subcommand not in _SKIP_MIGRATION_COMMANDS:
        _run_auto_migration_if_needed()

    if ctx.invoked_subcommand is None:
        # Show help and last 5 traces as a preview
        click.echo(ctx.get_help())
        click.echo()
        click.echo("Recent traces:")
        db_path = setup_db()
        preview_count = 5
        shown = 0
        for formatted_trace in get_formatted_traces(
            db_path, count=preview_count, reverse=False
        ):
            shown += 1
            click.echo(f"  {formatted_trace}")
        if shown == 0:
            click.echo("  No traces found")
        elif shown == preview_count:
            click.echo("  ... use `kolo trace list` to see all")

        if shown > 0:
            try:
                kolotxt_path = update_kolotxt(db_path)
            except Exception:
                logger.debug("Failed to update kolo.txt", exc_info=True)
            else:
                click.echo()
                click.echo(f"  kolo.txt: {kolotxt_path}")


def python_noop_profiler(frame, event, arg):  # pragma: no cover
    pass


@cli.command(context_settings={"ignore_unknown_options": True})
@click.argument("path")
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
@click.option(
    "--one-trace-per-test",
    default=False,
    is_flag=True,
    help="Generate a trace for each test traced by Kolo.",
)
@click.option("--noop", default=False, is_flag=True, hidden=True)
@click.option(
    "--inline",
    default=False,
    is_flag=True,
    help="Output the compact tree representation of the trace to stderr after execution.",
)
@click.option(
    "--returns",
    default=False,
    is_flag=True,
    help="Include return values in the compact tree representation.",
)
def run(path, args, one_trace_per_test, noop, inline, returns):
    """
    Trace Python code using Kolo.

    PATH is the path to the python file or module being traced.
    """
    if path == "python":
        path, *args = args
        if path == "-m":
            path, *args = args
            module = True
        else:
            module = False
    elif path.endswith(".py"):
        module = False
    else:
        module = True

    existing_profiler = sys.getprofile()
    if existing_profiler:
        raise click.ClickException(
            f"Cannot run Kolo: {existing_profiler} is already active."
        )

    # Monkeypatch sys.argv, so the profiled code doesn't get confused
    # Without this, the profiled code would see extra args it doesn't
    # know how to handle.
    sys.argv = [path, *args]

    if noop:  # pragma: no cover
        config = load_config()
        if config.get("use_rust", True):
            from ._kolo import register_noop_profiler

            register_noop_profiler()
        else:
            sys.setprofile(python_noop_profiler)

        try:
            if module:
                run_module(path, run_name="__main__", alter_sys=True)
            else:
                run_path(path, run_name="__main__")
        finally:
            sys.setprofile(None)
        return

    config = load_config()
    with enable(
        config,
        source="kolo run",
        _one_trace_per_test=one_trace_per_test,
        _inline=inline,
        _inline_returns=returns,
    ):
        if module:
            run_module(path, run_name="__main__", alter_sys=True)
        else:
            run_path(path, run_name="__main__")


@cli.command()
@click.option(
    "--port",
    default=5656,
    help="Custom port for the server to run on. Defaults to 5656.",
)
@click.option(
    "--ip",
    default="127.0.0.1",
    help="Custom ip for the server to run on. Defaults to 127.0.0.1",
)
def server(port, ip):
    """
    Start a server to view traces.
    """
    server = ThreadingHTTPServer((ip, port), KoloRequestHandler)
    click.echo(f"View Kolo traces at http://{ip}:{port}/_kolo/")
    server.serve_forever()


@cli.group()
def trace():
    """
    Subcommands for working with Kolo traces.
    """


@trace.command(hidden=True)
@click.argument("trace_id")
@click.option("--file", help="The name of the file to save the trace to.")
@click.option(
    "--as-python",
    default=False,
    is_flag=True,
    help="Show the trace as readable Python types.",
)
def dump(trace_id, file, as_python):
    """
    Dump a trace from the Kolo database to stdout or a specified file.
    """
    db_path = setup_db()

    try:
        msgpack_data, _ = load_trace_from_db(db_path, trace_id)
    except TraceNotFoundError:
        raise click.ClickException(TRACE_NOT_FOUND_ERROR.format(trace_id=trace_id))

    if as_python:
        data = load_msgpack(msgpack_data)
        data = repr(data)
        data = maybe_format(data)
        if file:
            with open(file, "w") as f:
                f.write(data)
        else:
            click.echo(data)
    elif file:
        with open(file, "wb") as f:
            f.write(msgpack_data)

    else:
        click.echo(msgpack_data, nl=False)


@trace.command()
@click.option("--count", help="The number of rows to show.", default=500)
@click.option(
    "--reverse",
    help="Reverse the order of the rows: newest at the bottom.",
    default=False,
    is_flag=True,
)
@click.option(
    "--pinned",
    help="Show only pinned traces.",
    default=False,
    is_flag=True,
)
def list(count, reverse, pinned):
    """
    Concisely list available traces, ordered by most recent first.

    This is useful for getting an overview of what traces are available and
    finding specific traces you might want to analyze further.

    Use `kolo cat <trace_id>` to view a trace or `kolo cat --recent` to view recent traces.

    If you're an LLM, use `kolo trace list` often to orient yourself.
    """
    db_path = setup_db()
    found_any = False

    if not pinned:
        # Regular trace listing
        for formatted_trace in get_formatted_traces(
            db_path, count=count, reverse=reverse
        ):
            found_any = True
            click.echo(formatted_trace)

        if not found_any:
            click.echo("No traces found")
        return

    # Pinned trace listing
    for (
        trace_id,
        timestamp_str,
        size,
        msgpack_data,
        auto_generated_name,
    ) in get_pinned_traces(db_path):
        found_any = True
        timestamp = parse_trace_timestamp(timestamp_str)

        trace_name = Trace.resolve_display_name(
            msgpack_data, auto_generated_name, db_path, trace_id
        )

        formatted_trace = format_trace_for_display(
            trace_id, timestamp, size, trace_name
        )
        click.echo(formatted_trace)

    if not found_any:
        click.echo("No pinned traces found")


@trace.command()
@click.argument("trace_id")
@click.argument("node_index", type=int)
@click.option(
    "-t",
    "--thread_id",
    "thread_id",
    default=None,
    help=(
        "Look the node up in this thread's tree instead of the main thread. "
        "Per-thread node indices restart at 0, so this is required to "
        "disambiguate nodes from non-main threads. Omit to target the main "
        "thread (the thread that was active when profiling started)."
    ),
)
def node(trace_id: str, node_index: int, thread_id: Optional[str]):
    """Get detailed information about a specific node in a trace.
    This is useful when you need to deeply understand what happened at a specific
    point in the execution, like examining function arguments, local variables,
    or the exact line of code being executed.
    """
    db_path = setup_db()

    try:
        trace_data, _ = load_trace_from_db(db_path, trace_id)
        node_data = get_node_data(trace_id, node_index, trace_data, thread_id=thread_id)
        click.echo(json.dumps(node_data, indent=2))
    except TraceNotFoundError:
        raise click.ClickException(TRACE_NOT_FOUND_ERROR.format(trace_id=trace_id))
    except ValueError as e:
        raise click.ClickException(str(e))


@trace.command()
@click.argument("trace_ids", required=False, nargs=-1)
@click.option(
    "--old",
    is_flag=True,
    default=False,
    help="Delete old traces. Defaults to traces older than 30 days.",
)
@click.option(
    "--before",
    help="Delete traces older than this datetime. Must be used with `--old`.",
    type=DATETIME_FORMATS,
)
@click.option(
    "--vacuum",
    help="Recover disk space from the Kolo database.",
    default=False,
    is_flag=True,
)
def delete(trace_ids, old, before, vacuum):
    """
    Delete one or more traces stored by Kolo.
    """

    if before is not None and old is False:
        raise click.ClickException("--before requires --old")

    if old is False and not trace_ids and vacuum is False:
        raise click.ClickException("Must specify either TRACE_IDS, --old, or --vacuum")

    if trace_ids and old:
        raise click.ClickException("Cannot specify TRACE_IDS and --old together")

    db_path = setup_db()

    if trace_ids:
        delete_traces_by_id(db_path, trace_ids)
    elif old:
        if before is None:
            before = datetime.now() - timedelta(days=30)

        deleted_count = delete_traces_before(db_path, before)
        click.echo(f"Deleted {deleted_count} old traces created before {before}.")

    if vacuum:
        vacuum_db(db_path)


@trace.command()
@click.argument("trace_id")
def pin(trace_id):
    """Pin a trace.
    This includes the trace in the output of using `kolo cat --pinned`,
    which can be helpful to give an LLM an overview of the key transactions in your project.
    """
    db_path = setup_db()
    try:
        if pin_trace(db_path, trace_id):
            click.echo(f"Pinned trace {trace_id}")
        else:
            raise click.ClickException(TRACE_NOT_FOUND_ERROR.format(trace_id=trace_id))
    except TraceNotFoundError:
        raise click.ClickException(TRACE_NOT_FOUND_ERROR.format(trace_id=trace_id))


@trace.command()
@click.argument("trace_id")
def unpin(trace_id):
    """Unpin a previously pinned trace."""
    db_path = setup_db()
    try:
        if unpin_trace(db_path, trace_id):
            click.echo(f"Unpinned trace {trace_id}")
        else:
            raise click.ClickException(TRACE_NOT_FOUND_ERROR.format(trace_id=trace_id))
    except TraceNotFoundError:
        raise click.ClickException(TRACE_NOT_FOUND_ERROR.format(trace_id=trace_id))


@trace.command()
@click.argument("trace_id", required=False)
@click.option(
    "--pinned", is_flag=True, help="Show compact representation of all pinned traces"
)
@click.option(
    "--returns",
    is_flag=True,
    help="Include return values in compact representation (warning: can be verbose)",
)
@click.option(
    "--recent",
    type=int,
    is_flag=False,
    flag_value=5,
    help="Show compact representation of the N most recent traces (default: 5)",
)
def compact(trace_id: str | None, pinned: bool, returns: bool, recent: int | None):
    """Get a compact representation of a specific trace.

    [LEGACY] This command is deprecated. Use `kolo cat` instead.

    Get a concise yet detailed overview of everything that happened in the trace.
    You will see a tree representation of all function calls (and optionally return values),
    as well as other relevant information and points of interest in the trace like logs or sql queries.

    When called without arguments, shows the most recent trace.
    """
    # Default to showing the most recent trace if no arguments provided
    if not any([pinned, trace_id is not None, recent is not None]):
        recent = 1

    db_path = setup_db()

    try:
        results = get_compact_traces(
            db_path,
            trace_id,
            pinned=pinned,
            returns=returns,
            recent=recent or 0,
        )
        for tid, compact_repr in results:
            if pinned or recent is not None:
                click.echo(f"\n=== Trace {tid} ===")
            click.echo(compact_repr)
    except TraceNotFoundError as e:
        raise click.ClickException(TRACE_NOT_FOUND_ERROR.format(trace_id=e.args[0]))


@cli.command(hidden=True)
def dbshell():  # pragma: no cover
    """
    Open a sqlite3 shell to the Kolo database.
    """
    db_path = setup_db()
    subprocess.run(["sqlite3", db_path], check=True)


@trace.command()
@click.argument("trace_id")
def upload(trace_id):
    """
    Upload a trace to the Kolo dashboard
    """
    db_path = setup_db()

    try:
        msgpack_data, _ = load_trace_from_db(db_path, trace_id)
    except TraceNotFoundError:
        raise click.ClickException(TRACE_NOT_FOUND_ERROR.format(trace_id=trace_id))

    response = upload_to_dashboard(msgpack_data)

    if response.status_code == 201:
        click.echo(f"{trace_id} uploaded successfully!")
    else:
        errors = response.json()
        raise click.ClickException(errors)


@trace.command()
@click.argument("trace_id")
def download(trace_id):
    """
    Download a trace from the Kolo dashboard
    """
    db_path = setup_db()

    # TODO(later): The ability to download will ultimately likely be guarded by authenticating
    # against a given project/organisation etc so that you cannot download someone else's trace
    # just by guessing a ULID, so we'll probably need to pass those along eventually too...
    base_url = os.environ.get("KOLO_BASE_URL", "https://my.kolo.app")
    url = f"{base_url}/api/traces/{trace_id}/download"
    response = httpx.get(url)

    if response.status_code == 404:
        raise click.ClickException(f"`{trace_id}` was not found by the server.")
    elif response.status_code != 200:
        raise click.ClickException(f"Unexpected status code: {response.status_code}.")

    raw_data = response.content

    try:
        msgpack.unpackb(raw_data, strict_map_key=False)
    except Exception:
        raise click.ClickException("Downloaded trace was not valid msgpack.")

    if trace_exists(trace_id, db_path):
        raise click.ClickException(f"`{trace_id}` already exists.")

    save_trace(trace_id, raw_data)
    click.echo(f"`{trace_id}` downloaded successfully!")


@trace.command()
def json_to_msgpack():  # pragma: no cover
    """
    Convert all legacy json traces to msgpack
    """
    db_path = setup_db()
    count = convert_json_to_msgpack(db_path)
    click.echo(f"{count} traces converted!")


@cli.command(hidden=True)
@click.option(
    "--status",
    is_flag=True,
    help="Show migration status without running migration.",
)
def migrate(status):
    """
    Migrate traces from SQLite database to file-based storage.

    This command migrates trace data from the SQLite database to individual
    files in the .kolo/.internal/raw/ directory. The database will only store
    metadata (id, created_at, is_pinned) after migration.

    File-based storage provides better performance and makes traces
    easier to manage and search.
    """
    db_path = setup_db()

    if status:
        migration_status = get_migration_status(db_path)
        click.echo(f"Traces in database: {migration_status['db_traces']}")
        if migration_status["json_traces"] > 0:
            click.echo(f"Legacy JSON traces: {migration_status['json_traces']}")
        click.echo(f"Traces in files: {migration_status['file_traces']}")
        click.echo(f"Total traces: {migration_status['total_traces']}")

        needs_migration = migration_status["needs_migration"]
        if needs_migration > 0:
            trace_word = "trace" if needs_migration == 1 else "traces"
            click.echo(
                f"\nRun `kolo migrate` to migrate {needs_migration} {trace_word} to file storage."
            )
        else:
            click.echo("\nAll traces are already migrated to file storage.")
        return

    # Check if migration is needed
    migration_status = get_migration_status(db_path)
    needs_migration = migration_status["needs_migration"]
    if needs_migration == 0:
        click.echo("All traces are already migrated to file storage.")
        return

    trace_word = "trace" if needs_migration == 1 else "traces"
    click.echo(f"Migrating {needs_migration} {trace_word} to file storage...")

    def progress_callback(migrated: int, remaining: int):
        click.echo(f"  Migrated {migrated} traces, {remaining} remaining...")

    total_migrated = migrate_traces_to_files(db_path, callback=progress_callback)
    click.echo(f"Migration complete: {total_migrated} traces migrated.")
    click.echo("Run `kolo delete --vacuum` to reclaim disk space.")


@trace.command()
@click.argument("trace_id", required=False)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
    default=None,
    help="Directory where the trace directory will be created. Defaults to .kolo/traces/",
)
def emit(trace_id: Optional[str], output_dir: Optional[Path]):
    """
    Emit a trace into a browsable directory structure.

    When called without arguments, emits/updates the 5 most recent traces.

    Creates a directory tree that mirrors the trace's execution tree,
    with human-readable files for each node (.py for syntax highlighting, .sql for SQL). This makes it easy to:

    \b
    - Browse trace data by clicking through directories
    - Search with grep: `grep -r "team_id" trace_dir/`
    - Let AI agents explore trace data efficiently

    The output includes:
    \b
    - {trace_id}.txt: Trace metadata and compact tree (overview)
    - Nested directories mirroring execution flow
    - call.py/return.py for function calls with locals (Python syntax highlighting)
    - request.txt/response.txt for HTTP (plain text)
    - .sql for SQL queries
    """
    from ._emit_auto import write_manual_emit_marker
    from .emit import emit_trace

    db_path = setup_db()

    # Default to .kolo/traces/ directory (db_path is .kolo/.internal/db.sqlite3)
    if output_dir is None:
        output_dir = db_path.parent.parent / "traces"
    output_dir = output_dir.resolve()
    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    # If specific trace_id provided, emit just that one
    if trace_id is not None:
        try:
            msgpack_data, _ = load_trace_from_db(db_path, trace_id)
        except TraceNotFoundError:
            raise click.ClickException(TRACE_NOT_FOUND_ERROR.format(trace_id=trace_id))

        data = load_msgpack(msgpack_data)
        trace = Trace(unprocessed_data=data, size=len(msgpack_data))
        trace_dir = emit_trace(trace, output_dir)
        write_manual_emit_marker(trace_dir)
        click.echo(f"Browse: {trace_dir}/{trace_id}.txt")
        return

    # No trace_id: emit/update the 5 most recent traces
    traces = list_traces_from_db(db_path, count=5)
    if not traces:
        raise click.ClickException("No traces found in the database.")

    first_trace_dir = None
    first_trace_id = None
    for row in traces:
        tid = row[0]
        try:
            msgpack_data, _ = load_trace_from_db(db_path, tid)
            data = load_msgpack(msgpack_data)
            trace = Trace(unprocessed_data=data, size=len(msgpack_data))
            trace_dir = emit_trace(trace, output_dir)
            write_manual_emit_marker(trace_dir)
            if first_trace_dir is None:
                first_trace_dir = trace_dir
                first_trace_id = tid
        except (TraceNotFoundError, KeyError, ValueError):
            continue

    if first_trace_dir:
        click.echo(f"Browse: {first_trace_dir}/{first_trace_id}.txt")


@trace.command(hidden=True)
@click.argument("trace_id", required=False)
def flat(trace_id: Optional[str]):
    """
    Emit a trace as a single flat markdown file.

    Uses the same emit logic as `kolo trace emit` but outputs to a single
    markdown file instead of a directory tree. The file uses markdown headers
    for editor folding support.

    When called without arguments, emits the most recent trace.

    \b
    Example:
        kolo trace flat > trace.md
        kolo trace flat trc_abc123 > trace.md
    """
    from .emit_flat import emit_trace_flat

    db_path = setup_db()

    # Default to most recent trace if no trace_id provided
    if trace_id is None:
        traces = list_traces_from_db(db_path, count=1)
        if not traces:
            raise click.ClickException("No traces found in the database.")
        trace_id = traces[0][0]
        click.echo(f"Using most recent trace: {trace_id}", err=True)

    # Load trace
    try:
        msgpack_data, _ = load_trace_from_db(db_path, trace_id)
    except TraceNotFoundError:
        raise click.ClickException(TRACE_NOT_FOUND_ERROR.format(trace_id=trace_id))

    data = load_msgpack(msgpack_data)
    trace_obj = Trace(unprocessed_data=data, size=len(msgpack_data))

    # Emit to stdout
    content = emit_trace_flat(trace_obj)
    click.echo(content)


@cli.command()
@click.argument("trace_id", required=False)
@click.option(
    "--pinned", is_flag=True, help="Show compact representation of all pinned traces"
)
@click.option(
    "--returns",
    is_flag=True,
    help="Include return values in compact representation (warning: can be verbose)",
)
@click.option(
    "--recent",
    type=int,
    is_flag=False,
    flag_value=5,
    help="Show compact representation of the N most recent traces (default: 5)",
)
def cat(trace_id: str | None, pinned: bool, returns: bool, recent: int | None):
    """Get a compact, text-based representation of a trace.

    Shows a concise yet detailed overview of everything that happened in the trace.
    You will see a tree representation of all function calls (and optionally return values),
    as well as other relevant information and points of interest in the trace like logs or sql queries.

    This is the canonical command for viewing compact trace representations.

    When called without arguments, shows the most recent trace.
    """
    # Default to showing the most recent trace if no arguments provided
    if not any([pinned, trace_id is not None, recent is not None]):
        recent = 1

    db_path = setup_db()

    try:
        results = get_compact_traces(
            db_path,
            trace_id,
            pinned=pinned,
            returns=returns,
            recent=recent or 0,
        )
        for tid, compact_repr in results:
            if pinned or recent is not None:
                click.echo(f"\n=== Trace {tid} ===")
            click.echo(compact_repr)
    except TraceNotFoundError as e:
        raise click.ClickException(TRACE_NOT_FOUND_ERROR.format(trace_id=e.args[0]))


@cli.group(hidden=True)
def ci():
    """
    Subcommands for CI-related operations.
    """
    pass


def compress_trace(trace_data: bytes) -> bytes:
    compressed_data = BytesIO()
    with gzip.GzipFile(fileobj=compressed_data, mode="wb") as gz:
        gz.write(trace_data)
    return compressed_data.getvalue()


def create_trace_group() -> str:
    auth_token = os.environ["KOLO_TOKEN"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    base_url = os.environ.get("KOLO_BASE_URL", "https://my.kolo.app")
    response = httpx.post(
        f"{base_url}/api/trace-groups", headers=headers, json={"name": "ci"}
    )
    if response.status_code != 201:
        error_message = f"Failed to create trace group. Status code: {response.status_code}\n{response.text}"

        click.echo(click.style(error_message, fg="red"), err=True)
        raise click.Abort()

    trace_group = response.json()

    return trace_group["id"]


async def upload_trace(
    client: Union[httpx.Client, httpx.AsyncClient],
    trace_id: str,
    upload_url: str,
    db_path: Path,
    max_retries: int = 3,
    initial_backoff: float = 1.0,
) -> Optional[str]:
    loaded_trace = load_trace_from_db(db_path, trace_id)

    msgpack = loaded_trace[0]
    compressed_data = compress_trace(msgpack)

    for attempt in range(max_retries):
        try:
            if isinstance(client, httpx.AsyncClient):
                response = await client.put(
                    upload_url,
                    content=compressed_data,
                    headers={"Content-Type": "application/gzip"},
                    timeout=30.0,
                )
            else:
                response = client.put(
                    upload_url,
                    content=compressed_data,
                    headers={"Content-Type": "application/gzip"},
                    timeout=30.0,
                )

            if response.status_code != 200:
                error_message = (
                    f"Failed to upload {trace_id}.msgpack.gz. Status code: {response.status_code}\n"
                    f"{response.text}"
                )
                click.echo(click.style(error_message, fg="red"), err=True)
                return error_message

            return None  # Success case

        except (httpx.TimeoutException, httpx.RequestError) as e:
            if attempt < max_retries - 1:
                backoff = initial_backoff * (2**attempt)
                error_message = f"Error uploading {trace_id}.msgpack.gz (attempt {attempt + 1}/{max_retries}): {str(e)}. Retrying in {backoff:.2f} seconds..."
                click.echo(click.style(error_message, fg="yellow"), err=True)
                if isinstance(client, httpx.AsyncClient):
                    await asyncio.sleep(backoff)
                else:
                    time.sleep(backoff)
            else:
                error_message = f"Failed to upload {trace_id}.msgpack.gz after {max_retries} attempts: {str(e)}"
                click.echo(click.style(error_message, fg="red"), err=True)
                return error_message

    return f"Failed to upload {trace_id}.msgpack.gz after {max_retries} attempts"


def sync_ci_upload(traces: List[Dict[str, Any]], db_path: Path):
    with httpx.Client() as client:
        with click.progressbar(traces, label="Uploading traces", show_pos=True) as bar:
            for trace in bar:
                result = asyncio.run(
                    upload_trace(
                        client=client,
                        trace_id=trace["id"],
                        upload_url=trace["upload_url"],
                        db_path=db_path,
                    )
                )
                if result:
                    click.echo(f"\n{result}", err=True)


async def async_ci_upload(traces: List[Dict[str, Any]], db_path: Path):
    async with httpx.AsyncClient(limits=httpx.Limits(max_connections=20)) as client:
        tasks = [
            upload_trace(
                client=client,
                trace_id=trace["id"],
                upload_url=trace["upload_url"],
                db_path=db_path,
            )
            for trace in traces
        ]

        bar: click._termui_impl.ProgressBar[Any]
        with click.progressbar(
            length=len(tasks), label="Uploading traces", show_pos=True
        ) as bar:
            results = []
            for task in asyncio.as_completed(tasks):
                result = await task
                bar.update(1)
                if result:
                    results.append(result)
                    click.echo(f"\n{result}", err=True)


@ci.command("upload")
@click.option("--sync", is_flag=True, help="Use synchronous upload instead of async")
def ci_upload(sync: bool):
    """
    Upload all traces in the local Kolo db to Kolo Cloud
    """
    db_path = setup_db()
    auth_token = os.environ["KOLO_TOKEN"]

    traces_in_local_db = list_traces_from_db(db_path, count=10000)

    trace_group_id = create_trace_group()

    traces_registered = []
    page_size = 500

    for i in range(0, len(traces_in_local_db), page_size):
        page = traces_in_local_db[i : i + page_size]

        base_url = os.environ.get("KOLO_BASE_URL", "https://my.kolo.app")
        response = httpx.post(
            f"{base_url}/api/traces/bulk",
            headers={"Authorization": f"Bearer {auth_token}"},
            json={
                "trace_group_id": trace_group_id,
                "traces": [{"id": trace[0], "recorded_at": trace[1]} for trace in page],
            },
        )

        if response.status_code != 201:
            error_message = f"Failed to bulk create traces. Status code: {response.status_code}\n{response.text}"
            click.echo(click.style(error_message, fg="red"), err=True)
            raise click.Abort()

        traces_registered.extend(response.json()["traces"])

        click.echo(
            f"Registered {min(i + page_size, len(traces_in_local_db))} of {len(traces_in_local_db)} traces"
        )

    if sync:
        sync_ci_upload(traces=traces_registered, db_path=db_path)
    else:
        asyncio.run(async_ci_upload(traces=traces_registered, db_path=db_path))


@cli.command(hidden=True)
def mcp():
    """
    Start the Kolo MCP server.
    """
    import asyncio

    from .mcp_server import mcp

    asyncio.run(mcp.run_stdio())


if __name__ == "__main__":
    cli()  # pragma: no cover
