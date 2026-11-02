from __future__ import annotations

import argparse
import os
import socket
import sys
import tempfile
import threading
import time
import webbrowser
from pathlib import Path
from typing import Any

# Maps a --format value to the file suffix load_source already understands.
# stdin has no extension to dispatch on, so we spill it to a temp file with the
# suffix the named format implies and let the existing readers take over.
STDIN_FORMAT_SUFFIXES = {
    "parquet": ".parquet",
    "csv": ".csv",
    "tsv": ".tsv",
    "arrow": ".arrow",
    "feather": ".feather",
    "ipc": ".ipc",
    "json": ".json",
    "ndjson": ".ndjson",
    "jsonl": ".jsonl",
}

# Environment variables the generated notebook reads to locate the data source.
# A file source sets TABLESCOPE_SOURCE; a Databricks source sets the
# DATABRICKS_* trio instead. The notebook picks whichever is present.
SOURCE_ENV = "TABLESCOPE_SOURCE"
PAGE_SIZE_ENV = "TABLESCOPE_PAGE_SIZE"
MAX_CELL_BYTES_ENV = "TABLESCOPE_MAX_CELL_BYTES"
DATABRICKS_PROFILE_ENV = "TABLESCOPE_DATABRICKS_PROFILE"
DATABRICKS_TABLE_ENV = "TABLESCOPE_DATABRICKS_TABLE"
DATABRICKS_QUERY_ENV = "TABLESCOPE_DATABRICKS_QUERY"

# A self-contained marimo notebook. It is served in read-only ("run") mode, so
# the code is never shown; it only loads the file named by TABLESCOPE_SOURCE and
# hands it to tablescope.view. We keep the body tiny and defer all real work to
# the library so the notebook stays a thin shell.
NOTEBOOK_TEMPLATE = '''import marimo

# width="full" so the table uses the whole window instead of marimo's narrow
# default reading column.
app = marimo.App(width="full")


@app.cell
def _():
    import os

    import tablescope
    from tablescope._cli import resolve_source

    source = resolve_source(os.environ)
    page_size = int(os.environ.get("{page_size_env}", "100"))
    max_cell_bytes = int(os.environ.get("{max_cell_bytes_env}", "8192"))
    tablescope.view(source, page_size=page_size, max_cell_bytes=max_cell_bytes)
    return


if __name__ == "__main__":
    app.run()
'''


def load_source(path_str: str):
    """Load a file into a polars frame that narwhals can normalize.

    Uses polars `scan_*` for lazy pushdown where the format supports it. The
    reader is chosen by the file extension.
    """
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"No such file: {path}")

    suffix = path.suffix.lower()
    import polars as pl

    if suffix == ".parquet":
        return pl.scan_parquet(path)

    if suffix in {".csv", ".tsv"}:
        separator = "\t" if suffix == ".tsv" else ","
        return pl.scan_csv(path, separator=separator)

    if suffix in {".arrow", ".feather", ".ipc"}:
        return pl.read_ipc(path)

    if suffix in {".json", ".ndjson", ".jsonl"}:
        if suffix == ".json":
            return pl.read_json(path)
        return pl.scan_ndjson(path)

    raise ValueError(
        f"Unsupported file type {suffix!r}. Supported: .parquet, .csv, .tsv, "
        ".arrow/.feather/.ipc, .json/.ndjson/.jsonl."
    )


def load_databricks_source(
    *,
    profile: str | None = None,
    table: str | None = None,
    query: str | None = None,
):
    """Open a Databricks table or query as a lazy Spark DataFrame.

    Returns a Spark Connect DataFrame (via databricks-connect). narwhals treats
    it as a LazyFrame, so the engine's filter/sort/limit pushdown reaches Spark
    and the table is never fully materialized. Exactly one of `table`/`query`
    must be given.
    """
    if (table is None) == (query is None):
        raise ValueError("Provide exactly one of table= or query= for a Databricks source.")

    try:
        from databricks.connect import DatabricksSession
    except ImportError as exc:  # pragma: no cover - depends on optional extra
        raise ImportError(
            "Databricks sources require the 'databricks' extra. Install with "
            "`pip install tablescope[databricks]`."
        ) from exc

    _quiet_spark_connect_rpc_logging()

    builder = DatabricksSession.builder
    if profile:
        # databricks-connect reads host + auth from the named ~/.databrickscfg
        # profile (the same profiles `databricks auth login -p <name>` writes).
        builder = builder.profile(profile)
    spark = builder.getOrCreate()

    if table is not None:
        return spark.table(table)
    return spark.sql(query)


def _quiet_spark_connect_rpc_logging() -> None:
    """Stop Spark Connect from logging expected query-resolution errors.

    Spark Connect's client logs *every* gRPC error via
    ``logger.exception("GRPC Error received")`` on the
    ``pyspark.sql.connect.logging`` logger (see pyspark's client/core.py), at
    ERROR level with a full stack trace. That fires for ordinary user mistakes
    too — e.g. a derived-column expression referencing a column that doesn't
    exist. tablescope already catches that exception and surfaces it in the
    browser, so the terminal copy is pure duplication that buries genuine
    server errors.

    This logger is *disabled by default* in pyspark (it only turns on when
    SPARK_CONNECT_LOG_LEVEL is set), but databricks-connect enables it. We
    restore the upstream default of disabling it. Other pyspark loggers are
    untouched, so real infrastructure problems (auth, connectivity) still show
    up via their normal channels.
    """
    import logging

    logging.getLogger("pyspark.sql.connect.logging").disabled = True


def resolve_source(env: dict[str, str] | Any):
    """Reopen the source described by environment variables in the notebook.

    The CLI sets either TABLESCOPE_SOURCE (a file path) or the Databricks trio.
    The generated notebook runs in a separate process and calls this to rebuild
    the source it should display.
    """
    profile = env.get(DATABRICKS_PROFILE_ENV)
    table = env.get(DATABRICKS_TABLE_ENV)
    query = env.get(DATABRICKS_QUERY_ENV)
    if table or query:
        return load_databricks_source(
            profile=profile or None,
            table=table or None,
            query=query or None,
        )

    return load_source(env[SOURCE_ENV])


def _spill_stdin(fmt: str, dest_dir: Path) -> Path:
    """Read piped stdin into a temp file named by the chosen format.

    stdin is read as raw bytes (parquet/arrow are binary), so the file lands
    byte-identical and load_source can open it by extension just like a path
    the user passed directly.
    """
    suffix = STDIN_FORMAT_SUFFIXES.get(fmt)
    if suffix is None:
        supported = ", ".join(sorted(STDIN_FORMAT_SUFFIXES))
        raise ValueError(f"Unsupported stdin format {fmt!r}. Supported: {supported}.")

    if sys.stdin is None or sys.stdin.isatty():
        raise ValueError(
            "Reading from '-' but stdin is a terminal; pipe data in, e.g. "
            "`... | tablescope -`."
        )

    data = sys.stdin.buffer.read()
    if not data:
        raise ValueError("Reading from '-' but stdin was empty.")

    dest = dest_dir / f"stdin{suffix}"
    dest.write_bytes(data)
    return dest


def _parse_source(raw: str) -> str:
    """Parse a '<backend>:<profile>' source, returning the Databricks profile.

    Only the 'databricks' backend exists today. 'databricks' alone (no colon)
    means the default profile, represented as an empty name.
    """
    backend, _, name = raw.partition(":")
    if backend != "databricks":
        raise ValueError(
            f"Unsupported source backend {backend!r}. Only 'databricks' is "
            "supported, e.g. --source databricks:dev."
        )
    return name


def _bind_socket(host: str, requested: int) -> socket.socket:
    """Bind `requested`, counting upward from it until a port is free.

    The bound socket is handed to uvicorn directly, avoiding the race where
    a probed port is released and grabbed by another process before the
    server binds it. Requesting port 0 yields an OS-assigned port.
    """
    last_error: OSError | None = None
    end = min(requested + 100, 65536)
    for port in range(requested, end):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind((host, port))
        except OSError as exc:
            sock.close()
            last_error = exc
            continue
        sock.set_inheritable(True)
        return sock
    msg = f"No free port found in range {requested}-{end - 1}."
    raise OSError(msg) from last_error


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="tablescope",
        description=(
            "Serve an interactive table viewer for a data file in your browser."
        ),
    )
    parser.add_argument(
        "file",
        nargs="?",
        help=(
            "Path to a data file (.parquet, .csv, .tsv, .arrow, .json, ...), "
            "or '-' to read piped data from stdin (see --format). Omit when "
            "using --table/--query to read from Databricks."
        ),
    )
    parser.add_argument(
        "--source",
        help=(
            "Remote data source, as '<backend>:<profile>'. Only 'databricks' "
            "is supported, e.g. --source databricks:dev selects the Databricks "
            "CLI profile 'dev'. Use 'databricks' alone for the default profile. "
            "Required with --table/--query."
        ),
    )
    query_group = parser.add_mutually_exclusive_group()
    query_group.add_argument(
        "--table",
        help=(
            "Fully-qualified Databricks table to view, e.g. "
            "catalog.schema.table. Requires --source."
        ),
    )
    query_group.add_argument(
        "--query",
        help=(
            "SQL query to run against Databricks; the result is viewed lazily. "
            "Requires --source."
        ),
    )
    parser.add_argument(
        "--format",
        default="parquet",
        choices=sorted(STDIN_FORMAT_SUFFIXES),
        help=(
            "Format of data piped to stdin when file is '-' (default: parquet). "
            "Ignored when reading a real file, which dispatches on extension."
        ),
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=6767,
        help="Port to serve on (default: 6767; counts upward if taken).",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host/interface to bind (default: 127.0.0.1).",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=100,
        help="Rows fetched per page (default: 100).",
    )
    parser.add_argument(
        "--max-cell-bytes",
        type=int,
        default=8192,
        help=(
            "Truncate any cell whose serialized value exceeds this many bytes "
            "(default: 8192). Keeps pages with large blobs/arrays from "
            "overwhelming the browser; the full value is fetched on demand "
            "from the row preview. Use 0 to disable truncation."
        ),
    )
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Do not open a browser automatically (use over SSH).",
    )
    args = parser.parse_args()

    is_databricks = bool(args.table or args.query)

    # The notebook runs in a separate marimo/uvicorn process and reopens the
    # source itself, so it can't see our stdin. For a file source, spill piped
    # data to a temp file up front and treat it like a named file. The
    # generated notebook is written to this dir either way.
    notebook_dir = Path(tempfile.mkdtemp(prefix="tablescope-"))

    # Env handed to the notebook process. We pass a copy through to uvicorn's
    # subprocess via os.environ below; collect the source-locating vars here.
    source_env: dict[str, str] = {}

    if is_databricks:
        if args.file is not None:
            parser.error("Give a file or --table/--query, not both.")
        if args.source is None:
            parser.error("--table/--query require --source (e.g. --source databricks:dev).")
        try:
            profile_name = _parse_source(args.source)
        except ValueError as exc:
            parser.error(str(exc))

        if args.table:
            source_env[DATABRICKS_TABLE_ENV] = args.table
            description = f"databricks table {args.table}"
        else:
            source_env[DATABRICKS_QUERY_ENV] = args.query
            description = "databricks query"
        if profile_name:
            source_env[DATABRICKS_PROFILE_ENV] = profile_name

        # Fail fast: open the source here so auth/permission/typo errors surface
        # at the prompt instead of inside the served notebook.
        try:
            load_databricks_source(
                profile=profile_name or None,
                table=args.table or None,
                query=args.query or None,
            )
        except Exception as exc:  # noqa: BLE001 - surface any connection error cleanly
            parser.error(str(exc))
    else:
        if args.source is not None:
            parser.error("--source only applies to --table/--query.")
        if args.file is None:
            parser.error("Provide a data file, or --table/--query with --source.")

        if args.file == "-":
            try:
                source_path = _spill_stdin(args.format, notebook_dir)
            except Exception as exc:  # noqa: BLE001 - surface any read error cleanly
                parser.error(str(exc))
        else:
            source_path = Path(args.file)
            if not source_path.exists():
                parser.error(f"No such file: {source_path}")

        # Fail fast on unreadable files / unsupported types before serving.
        try:
            load_source(str(source_path))
        except Exception as exc:  # noqa: BLE001 - surface any reader error cleanly
            parser.error(str(exc))

        source_env[SOURCE_ENV] = str(source_path.resolve())
        description = str(source_path)

    import uvicorn
    from marimo import create_asgi_app

    notebook_path = notebook_dir / "app.py"
    notebook_path.write_text(
        NOTEBOOK_TEMPLATE.format(
            page_size_env=PAGE_SIZE_ENV,
            max_cell_bytes_env=MAX_CELL_BYTES_ENV,
        )
    )

    os.environ.update(source_env)
    os.environ[PAGE_SIZE_ENV] = str(args.page_size)
    os.environ[MAX_CELL_BYTES_ENV] = str(args.max_cell_bytes)

    host = args.host
    sock = _bind_socket(host, args.port)
    port = sock.getsockname()[1]

    builder = create_asgi_app(quiet=True).with_app(path="", root=str(notebook_path))
    asgi_app = builder.build()

    display_host = "localhost" if host in {"127.0.0.1", "0.0.0.0"} else host
    url = f"http://{display_host}:{port}"

    # Flush immediately: when piped over SSH (no TTY) stdout is block-buffered,
    # and the URL is the whole point of the message, so it must not wait for exit.
    print(f"tablescope: serving {description} at {url}", flush=True)
    print("Press Ctrl+C to stop.", flush=True)

    if not args.no_open:
        def _open_when_ready() -> None:
            for _ in range(100):
                try:
                    with socket.create_connection((host, port), timeout=0.1):
                        break
                except OSError:
                    time.sleep(0.1)
            webbrowser.open(url)

        threading.Thread(target=_open_when_ready, daemon=True).start()

    config = uvicorn.Config(asgi_app, host=host, port=port, log_level="warning")
    server = uvicorn.Server(config)

    # The notebook runs in this same process, so its widget can stop this
    # server when the in-page "Stop server" button is clicked.
    from tablescope._server_control import register_server

    register_server(server)

    try:
        server.run(sockets=[sock])
    except KeyboardInterrupt:
        pass
