"""Tools for calling an instrument via SCPI commands."""

from __future__ import annotations

import argparse
import base64
import dataclasses
import functools
import json
import logging
import sys
import typing

try:
    # noinspection PyUnusedImports
    from fastmcp import FastMCP

    # noinspection PyUnusedImports
    from starlette.responses import JSONResponse

    MCP_INSTALLED = True
except ImportError:
    MCP_INSTALLED = False
    FastMCP: type | None = None
    JSONResponse: type | None = None

# noinspection PyProtectedMember
from RsInstrument import RsInstrException, RsInstrument, __version__
from RsInstrument.otel import setup_otel

logger = logging.getLogger(__name__)

DEFAULT_MCP_HEALTH_ENDPOINT = "/healthz"

_scpi_header_cache: dict[str, "_ScpiHeaderIndex | None"] = {}


class _TrieNode:
    """Trie node for SCPI help header paths (character edges)."""

    __slots__ = ("children", "terminal")

    def __init__(self) -> None:
        self.children: dict[str, _TrieNode] = {}
        self.terminal = False


@dataclasses.dataclass(frozen=True)
class _ScpiHeaderIndex:
    """Fast lookup for ``SYST:HELP:HEAD?`` lines: O(1) exact + O(len(command)) prefix."""

    exact: frozenset[str]
    _root: _TrieNode

    def match(self, command_normalized: str) -> tuple[bool, str | None]:
        """Return whether ``command_normalized`` matches a header (exact or longest prefix)."""
        if command_normalized in self.exact:
            return True, command_normalized
        node = self._root
        best: str | None = None
        best_len = 0
        i = 0
        n = len(command_normalized)
        while i < n:
            child = node.children.get(command_normalized[i])
            if child is None:
                break
            node = child
            i += 1
            if (
                node.terminal
                and i < n
                and command_normalized[i] in (":", ";")
                and i > best_len
            ):
                best = command_normalized[:i]
                best_len = i
        return best is not None, best


def _build_scpi_header_index(lines: list[str]) -> _ScpiHeaderIndex:
    """Build exact set and trie from normalized ``SYST:HELP:HEAD?`` lines."""
    exact = frozenset(lines)
    root = _TrieNode()
    for line in lines:
        node = root
        for ch in line:
            node = node.children.setdefault(ch, _TrieNode())
        node.terminal = True
    return _ScpiHeaderIndex(exact=exact, _root=root)


@dataclasses.dataclass(frozen=True)
class ToolSpec:
    """Specification for registering an extra MCP tool."""

    name: str
    description: str
    fn: typing.Callable[..., typing.Any]
    annotations: dict[str, typing.Any] | None = None


@dataclasses.dataclass(frozen=True)
class BatchScpiCommand:
    """Single batch SCPI command with optional per-item timeout override."""

    command: str
    opc_timeout: int | None = None


def _normalize_tool(
    item: tuple[str, str, typing.Callable[..., typing.Any]] | ToolSpec,
) -> ToolSpec:
    """Convert legacy tuple tools to :class:`ToolSpec`."""
    if isinstance(item, ToolSpec):
        return item
    name, description, fn = item
    return ToolSpec(name=name, description=description, fn=fn)


def _normalize_scpi_header_lines(raw: str) -> list[str]:
    """Split and normalize SCPI help header lines."""
    lines: list[str] = []
    for line in raw.replace("\r\n", "\n").split("\n"):
        stripped = line.strip().upper()
        if stripped:
            lines.append(stripped)
    return lines


def _get_scpi_headers(resource: str, timeout_ms: int) -> _ScpiHeaderIndex | None:
    """Load SCPI help headers from the instrument (lazy, once per resource).

    Returns a trie-backed index so ``instrument_scpi_exists`` stays fast when the
    instrument exposes very large ``SYST:HELP:HEAD?`` trees (e.g. many options).
    """
    if resource in _scpi_header_cache:
        return _scpi_header_cache[resource]
    try:
        with RsInstrument(resource) as inst:
            previous_timeout = inst.visa_timeout
            try:
                inst.visa_timeout = timeout_ms
                raw = inst.query_str("SYST:HELP:HEAD?")
            finally:
                inst.visa_timeout = previous_timeout
        parsed = _normalize_scpi_header_lines(raw)
        index = _build_scpi_header_index(parsed)
        _scpi_header_cache[resource] = index
        return index
    except RsInstrException:
        _scpi_header_cache[resource] = None
        return None


def _match_scpi_header(
    command_normalized: str,
    headers: list[str] | _ScpiHeaderIndex,
) -> tuple[bool, str | None]:
    """Return whether ``command`` matches a known header and the best prefix match string."""
    index = (
        headers
        if isinstance(headers, _ScpiHeaderIndex)
        else _build_scpi_header_index(headers)
    )
    return index.match(command_normalized)


def safe_tool(fn: typing.Callable[..., typing.Any]) -> typing.Callable[..., typing.Any]:
    """Decorate MCP tools by converting exceptions to ``Error: ...`` strings."""

    @functools.wraps(fn)
    def _wrapper(*args: typing.Any, **kwargs: typing.Any) -> typing.Any:
        try:
            return fn(*args, **kwargs)
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Exception in tool %s", getattr(fn, "__name__", repr(fn)))
            return f"Error: {exc}"

    return _wrapper


@safe_tool
def instrument_query_scpi(
    command: str,
    resource: str,
    opc_timeout: int = 5000,
) -> str:
    """Query a command from an instrument via RsInstrument.

    Args:
        command: The SCPI query command to send to the instrument.
        resource: The VISA resource string of the instrument.
        opc_timeout: Timeout in milliseconds for the operation complete (OPC) query.
            Default is 5000 ms.

    Returns:
        The response from the instrument.
    """
    with RsInstrument(resource) as inst:
        inst.opc_timeout = opc_timeout
        response = inst.query(command)
        return response.strip()


@safe_tool
def instrument_write_scpi(
    command: str,
    resource: str,
    opc_timeout: int = 5000,
) -> str:
    """Write a command to an instrument via RsInstrument.

    Args:
        command: The SCPI write command to send to the instrument.
        resource: The VISA resource string of the instrument.
        opc_timeout: Timeout in milliseconds for the operation complete (OPC) query.
            Default is 5000 ms.

    Returns:
        Status message after a successful write.
    """
    with RsInstrument(resource) as inst:
        inst.opc_timeout = opc_timeout
        inst.write(command)
        return "Write command executed successfully."


@safe_tool
def instrument_fetch_errors(resource: str, opc_timeout: int = 5000) -> str:
    """Fetch errors from an instrument via RsInstrument.

    Args:
        resource: The VISA resource string of the instrument.
        opc_timeout: Timeout in milliseconds for the operation complete (OPC) query.
            Default is 5000 ms.

    Returns:
        The response from the instrument.
    """
    with RsInstrument(resource) as inst:
        inst.opc_timeout = opc_timeout
        errors = inst.query_all_errors_with_codes()
        if not errors:
            return "No errors."

        return json.dumps([{"code": code, "message": msg} for code, msg in errors])


@safe_tool
def instrument_reset(resource: str, opc_timeout: int = 5000) -> str:
    """Reset an instrument via RsInstrument.

    Args:
        resource: The VISA resource string of the instrument.
        opc_timeout: Timeout in milliseconds for the operation complete (OPC) query.
            Default is 5000 ms.

    Returns:
        Status message after a successful reset.
    """
    with RsInstrument(resource) as inst:
        inst.opc_timeout = opc_timeout
        inst.reset()
        return "Instrument reset successfully."


@safe_tool
def instrument_go_to_local(resource: str) -> str:
    """Send instrument to local front-panel control (GTL)."""
    try:
        with RsInstrument(resource) as inst:
            try:
                inst.go_to_local(True)
            except RsInstrException:
                try:
                    inst.go_to_local()
                except RsInstrException:
                    inst.write("@LOC")
    except RsInstrException as exc:
        logger.warning(
            "Local front-panel control restore (GTL) skipped for %s: %s",
            resource,
            exc,
        )
    return "Local front-panel control restored."


@safe_tool
def instrument_get_screenshot(
    resource: str,
    opc_timeout: int = 10000,
    screenshot_path: str = "/var/screenshot.png",
) -> str:
    """Capture a PNG screenshot from the instrument display.

    Args:
        resource: The VISA resource string of the instrument.
        opc_timeout: Timeout in milliseconds for OPC-sensitive steps.
        screenshot_path: Instrument-side file path for the hardcopy image.

    Returns:
        JSON string with ``mime_type`` and base64-encoded ``data`` (PNG).
    """
    with RsInstrument(resource) as inst:
        inst.opc_timeout = opc_timeout
        inst.write("HCOPy:DEVice:LANGuage PNG")
        inst.write("HCOPy:IMMediate")
        img_data = inst.query_bin_block(f"MMEM:DATA? '{screenshot_path}'")
    encoded = base64.b64encode(img_data).decode("ascii")
    return json.dumps({"mime_type": "image/png", "data": encoded})


def _parse_batch_entry(
    entry: str | BatchScpiCommand | dict[str, typing.Any], default_timeout: int
) -> BatchScpiCommand:
    """Normalize one batch entry to ``BatchScpiCommand``."""
    if isinstance(entry, str):
        return BatchScpiCommand(command=entry, opc_timeout=default_timeout)
    if isinstance(entry, BatchScpiCommand):
        timeout = (
            default_timeout if entry.opc_timeout is None else int(entry.opc_timeout)
        )
        return BatchScpiCommand(command=entry.command, opc_timeout=timeout)
    if isinstance(entry, dict):
        if "command" not in entry:
            raise ValueError("Missing key 'command' in batch command object")
        timeout = (
            default_timeout if "opc_timeout" not in entry else int(entry["opc_timeout"])
        )
        return BatchScpiCommand(command=str(entry["command"]), opc_timeout=timeout)
    raise TypeError(
        "Each batch entry must be a string, BatchScpiCommand, or object "
        "{'command': '...', 'opc_timeout': ...}"
    )


@safe_tool
def instrument_batch_scpi(
    commands: list[str | BatchScpiCommand | dict[str, typing.Any]],
    resource: str,
    opc_timeout: int = 5000,
) -> str:
    """Execute multiple SCPI entries in order using one session.

    Queries are detected by ``?`` in the command string; others are writes.
    Each list item may be either:
    - ``"SCPI:CMD?"``
    - ``BatchScpiCommand(command="SCPI:CMD?", opc_timeout=12000)``
    - ``{"command": "SCPI:CMD?", "opc_timeout": 12000}`` (per-item timeout override)

    Args:
        commands: SCPI command entries to run in order.
        resource: The VISA resource string of the instrument.
        opc_timeout: Default timeout in milliseconds for OPC-sensitive steps.

    Returns:
        JSON list of ``{"command": "...", "result": "..."}``; per-command errors use
        ``Error: ...`` without stopping the batch.
    """
    results: list[dict[str, str]] = []
    with RsInstrument(resource) as inst:
        inst.opc_timeout = opc_timeout
        for entry in commands:
            cmd = ""
            try:
                parsed = _parse_batch_entry(entry, opc_timeout)
                cmd = parsed.command
                effective_timeout = (
                    opc_timeout if parsed.opc_timeout is None else parsed.opc_timeout
                )
                inst.opc_timeout = int(effective_timeout)

                if "?" in cmd:
                    out = inst.query(cmd).strip()
                else:
                    inst.write(cmd)
                    out = "Write command executed successfully."
                results.append({"command": cmd, "result": out})
            except Exception as exc:  # pylint: disable=broad-except
                shown_cmd = cmd or str(entry)
                results.append({"command": shown_cmd, "result": f"Error: {exc}"})
    return json.dumps(results)


@safe_tool
def instrument_scpi_exists(
    command: str,
    resource: str,
    opc_timeout: int = 10000,
) -> str:
    """Check whether a SCPI command path appears in the instrument help header tree.

    Uses ``SYST:HELP:HEAD?`` when supported; results are cached per resource for the process.

    Args:
        command: SCPI command or subtree path to check (trailing ``?`` is ignored).
        resource: The VISA resource string of the instrument.
        opc_timeout: Temporary VISA timeout (ms) while loading help headers.

    Returns:
        JSON with ``exists``, ``matched_header``, and ``supported`` keys.
    """
    normalized = command.strip().upper().rstrip("?")
    headers = _get_scpi_headers(resource, opc_timeout)
    if headers is None:
        return json.dumps(
            {"exists": False, "matched_header": None, "supported": False},
        )
    exists, matched = _match_scpi_header(normalized, headers)
    return json.dumps(
        {"exists": exists, "matched_header": matched, "supported": True},
    )


def _register_one_tool(
    fastmcp: typing.Any,
    spec: ToolSpec,
) -> None:
    """Register a single tool, forwarding annotations when supported."""
    tool_kwargs: dict[str, typing.Any] = {
        "name": spec.name,
        "description": spec.description,
    }
    if spec.annotations:
        tool_kwargs["annotations"] = spec.annotations
    try:
        decorator = fastmcp.tool(**tool_kwargs)
        decorator(spec.fn)
    except TypeError:
        fastmcp.tool(name=spec.name, description=spec.description)(spec.fn)


def create_fastmcp_server(
    *args: typing.Any,
    tools: typing.Sequence[tuple[str, str, typing.Callable[..., typing.Any]] | ToolSpec]
    | None = None,
    health_endpoint: str = DEFAULT_MCP_HEALTH_ENDPOINT,
    **kwargs: typing.Any,
):
    """Create a FastMCP tool for SCPI commands.

    Args:
        *args: Positional arguments to pass to FastMCP.
        tools: Extra tools as legacy ``(name, description, fn)`` tuples or ``ToolSpec``.
        health_endpoint: The FastMCP health endpoint.
        **kwargs: Keyword arguments to pass to FastMCP.

    Note:
        Inbound W3C trace context on MCP ``tools/call`` is handled by **FastMCP**
        (``server_span`` / ``fastmcp.telemetry.extract_trace_context`` on request
        ``meta``). Use top-level ``traceparent`` / ``tracestate`` on params ``meta``
        as documented for FastMCP; no RsInstrument middleware is involved.
    """
    if not MCP_INSTALLED:
        raise ImportError(
            "mcp is required for this module. Please install with 'pip install RsInstrument[mcp]'"
        )
    assert FastMCP is not None and JSONResponse is not None
    _json_response = JSONResponse
    if tools is None:
        tools = []
    name = f"{__package__}-mcp"
    kwargs.setdefault("name", name)
    # noinspection PyCallingNonCallable
    fastmcp = FastMCP(*args, **kwargs)

    @fastmcp.custom_route(health_endpoint, methods=["GET"])
    async def health_check(_: typing.Any) -> typing.Any:
        """Health check endpoint."""
        # noinspection PyCallingNonCallable
        return _json_response(
            {"status": "healthy", "service": name, "version": __version__}
        )

    _register_one_tool(
        fastmcp,
        ToolSpec(
            name="Instrument-Query-SCPI",
            description="Query a command from an instrument via RsInstrument.",
            fn=instrument_query_scpi,
        ),
    )
    _register_one_tool(
        fastmcp,
        ToolSpec(
            name="Instrument-Write-SCPI",
            description="Write a command to an instrument via RsInstrument.",
            fn=instrument_write_scpi,
        ),
    )
    _register_one_tool(
        fastmcp,
        ToolSpec(
            name="Instrument-Fetch-Errors",
            description="Fetch errors from an instrument via RsInstrument.",
            fn=instrument_fetch_errors,
        ),
    )
    _register_one_tool(
        fastmcp,
        ToolSpec(
            name="Instrument-Reset",
            description="Reset the instrument",
            fn=instrument_reset,
        ),
    )
    _register_one_tool(
        fastmcp,
        ToolSpec(
            name="Instrument-Go-To-Local",
            description="Restore local front-panel control (GTL).",
            fn=instrument_go_to_local,
        ),
    )
    _register_one_tool(
        fastmcp,
        ToolSpec(
            name="Instrument-Get-Screenshot",
            description="Capture a PNG screenshot from the instrument display.",
            fn=instrument_get_screenshot,
        ),
    )
    _register_one_tool(
        fastmcp,
        ToolSpec(
            name="Instrument-Batch-SCPI",
            description="Run multiple SCPI commands in one session (query if '?' present).",
            fn=instrument_batch_scpi,
        ),
    )
    _register_one_tool(
        fastmcp,
        ToolSpec(
            name="Instrument-SCPI-Exists",
            description="Check SCPI command against SYST:HELP:HEAD? tree when supported.",
            fn=instrument_scpi_exists,
        ),
    )
    for item in tools:
        _register_one_tool(fastmcp, _normalize_tool(item))
    return fastmcp


def run(
    *args: typing.Any,
    host: str = "localhost",
    port: int = 8000,
    transport: typing.Literal["stdio", "sse", "streamable-http"] = "stdio",
    tools: typing.Sequence[tuple[str, str, typing.Callable[..., typing.Any]] | ToolSpec]
    | None = None,
    health_endpoint: str = DEFAULT_MCP_HEALTH_ENDPOINT,
    show_fastmcp_banner: bool = False,
    **kwargs: typing.Any,
):
    """Run the MCP server.

    Args:
        *args: Positional arguments to pass to FastMCP.
        host: The FastMCP Hostname/IP to bind.
        port: The FastMCP port to bind.
        transport: The FastMCP transport protocol to use. Options are 'stdio', 'sse', and 'streamable-http'.
        tools: Register a sequence of tuples containing tool names, descriptions and their corresponding callables.
        health_endpoint: The FastMCP health endpoint.
        show_fastmcp_banner: Whether to show the FastMCP banner on startup. Defaults to False.
        **kwargs: Keyword arguments to pass to FastMCP.
    """
    setup_otel()
    mcp = create_fastmcp_server(
        *args,
        tools=tools,
        health_endpoint=health_endpoint,
        **kwargs,
    )
    if transport != "stdio":
        run_kwargs = {"host": host, "port": port}
    else:
        run_kwargs = {}
    if not show_fastmcp_banner:
        logger.info("Starting RsInstrument-mcp server...")
    mcp.run(transport=transport, show_banner=show_fastmcp_banner, **run_kwargs)


def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(description="Run the RsInstrument MCP server.")
    parser.add_argument(
        "-V",
        "--version",
        help="Show version number and exit",
        action="version",
        version=__version__,
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        help="Increase output (Option is additive to increase verbosity)",
        action="count",
        default=0,
    )
    parser.add_argument(
        "-q",
        "--quiet",
        dest="quiet",
        help="Reduce output (Option is additive to decrease verbosity)",
        action="count",
        default=0,
    )
    parser.add_argument(
        "--host",
        dest="host",
        default="localhost",
        help="FastMCP Hostname/IP to bind (default: %(default)s)",
    )
    parser.add_argument(
        "--port",
        dest="port",
        type=int,
        default=8000,
        help="FastMCP port to bind (default: %(default)s)",
    )
    parser.add_argument(
        "--transport",
        dest="transport",
        type=str,
        choices=["stdio", "sse", "streamable-http"],
        default="streamable-http",
        help="FastMCP transport protocol (default: %(default)s)",
    )
    parser.add_argument(
        "--health-endpoint",
        dest="health_endpoint",
        type=str,
        default=DEFAULT_MCP_HEALTH_ENDPOINT,
        help="FastMCP health endpoint (default: %(default)s)",
    )
    parser.add_argument(
        "--show-fastmcp-banner",
        dest="show_fastmcp_banner",
        action="store_true",
        help="Show FastMCP banner on startup",
    )
    return parser


def main(argv: typing.Sequence[str] | None = None):
    """Main entry point for command line execution."""
    args = create_parser().parse_args(argv)

    logging.basicConfig(
        format="{asctime} [{levelname:^8}] ({filename}:{lineno}) {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{",
    )

    default_log_level = logging.WARNING
    verbosity = default_log_level - ((args.verbose - args.quiet) * 10)
    log_level = min(logging.CRITICAL, max(logging.DEBUG, verbosity))
    logger.setLevel(log_level)
    try:
        run(
            transport=args.transport,
            host=args.host,
            port=args.port,
            health_endpoint=args.health_endpoint,
            show_fastmcp_banner=args.show_fastmcp_banner,
        )
    except (
        Exception
    ) as error:  # pragma: no cover - exercised in tests with forced exception
        if verbosity < default_log_level or default_log_level <= logging.DEBUG:
            logger.exception("%s", error)
        else:
            logger.exception("%s", error)
            logger.warning("Hint: Rerun with '--verbose' to show exception traceback.")
        sys.exit(1)
    except KeyboardInterrupt:  # pragma: no cover - exercised in tests
        logger.warning("Aborted by user")
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
