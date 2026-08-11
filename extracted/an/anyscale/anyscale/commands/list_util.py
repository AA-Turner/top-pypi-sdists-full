import itertools
import sys
from typing import Any, Callable, Dict, Iterator, List, Optional

import click
from rich.console import Console
from rich.table import Table

from anyscale.commands.output_format import OutputFormat, render_output
from anyscale.util import validate_non_negative_arg


MAX_PAGE_SIZE = 50
NON_INTERACTIVE_DEFAULT_MAX_ITEMS = 10


def is_interactive_terminal() -> bool:
    """Whether both stdin and stdout are attached to a real terminal.

    Read at call time (not import) so runtime redirection is honored. A closed
    or missing stream is treated as non-interactive rather than raising.
    """
    for stream in (sys.stdin, sys.stdout):
        isatty = getattr(stream, "isatty", None)
        if not callable(isatty):
            return False
        try:
            if not isatty():
                return False
        except (ValueError, OSError):
            # isatty() raises on a closed file descriptor.
            return False
    return True


def resolve_interactive(interactive: bool, json_output: bool) -> bool:
    """Resolve the effective interactive mode against the terminal.

    A non-terminal wins over an explicit --interactive so piped list commands
    cannot hang on input(). JSON output is likewise treated as non-interactive
    (batch): it is machine-readable, so it is capped by --max-items /
    NON_INTERACTIVE_DEFAULT_MAX_ITEMS like any other batch run rather than
    draining every page, while still emitting a single valid JSON array.

    Call this before the "--max-items only allowed with --no-interactive" guard
    so the guard tests the resolved value: a piped or --json run accepts
    --max-items instead of rejecting it against its own "use --max-items" hint.
    """
    return interactive and not json_output and is_interactive_terminal()


def validate_page_size(ctx, param, value):
    """Click callback to validate page size argument."""
    value = validate_non_negative_arg(ctx, param, value)
    if value is not None and value > MAX_PAGE_SIZE:
        raise click.BadParameter(f"must be less than or equal to {MAX_PAGE_SIZE}.")
    return value


def create_table(
    columns: List[tuple[str, Optional[str], bool]], is_first: bool = True
) -> Table:
    """Create a Rich table with specified columns.

    Args:
        columns: List of (column_name, style, no_wrap) tuples.
                 E.g., [("ID", "cyan", True), ("Name", None, False)]
        is_first: Show headers (True for first page, False for subsequent pages).

    Returns:
        Configured Rich Table ready for adding rows.

    Example:
        >>> columns = [("ID", "cyan", True), ("Name", None, False)]
        >>> table = create_table(columns, is_first=True)
        >>> table.add_row("123", "My Job")
    """
    table = Table(show_header=is_first, header_style="bold")
    for name, style, no_wrap in columns:
        table.add_column(name, style=style, no_wrap=no_wrap)
    return table


def _paginate(iterator: Iterator[Any], page_size: Optional[int]) -> Iterator[List[Any]]:
    if page_size is None:
        yield list(iterator)
    else:
        while True:
            page = list(itertools.islice(iterator, page_size))
            if not page:
                return
            yield page


def _render_page(
    page: List[Any],
    item_formatter: Callable[[Any], Dict[str, Any]],
    table_creator: Callable[[bool], Table],
    is_first: bool,
    page_num: int,
    console: Console,
) -> int:
    """Render a single page of items as a table.

    JSON output does not flow through here: it is collected across all pages and
    emitted once as a single valid document by ``display_list``.
    """
    if page_num > 1:  # Only show page number for pages after first
        console.print(f"[dim]Page {page_num}[/dim]")

    rows = [item_formatter(item) for item in page]
    tbl = table_creator(is_first)
    for row in rows:
        tbl.add_row(*row.values())
    console.print(tbl)

    return len(page)


def _should_continue_pagination(
    page_size: int, current_page_size: int, console: Console
) -> bool:
    """Prompt user to continue pagination if needed."""
    if current_page_size < page_size:
        return False  # Last page, no need to prompt

    # Defense-in-depth: never block on input() when not attached to a terminal
    # (e.g. piped), even if a caller passed interactive=True.
    if not is_interactive_terminal():
        return False

    console.print()
    console.print(
        "[dim]Press [bold]Enter[/bold] to continue, [bold]q[/bold] to quit…[/]"
    )
    return input("> ").strip().lower() != "q"


def display_list(  # noqa: PLR0913, PLR0912
    iterator: Iterator[Any],
    item_formatter: Callable[[Any], Dict[str, Any]],
    table_creator: Callable[[bool], Table],
    json_output: bool,
    page_size: int,
    interactive: bool,
    max_items: Optional[int],
    console: Console,
) -> int:
    """Displays a list of items from an iterator, handling pagination and output format.

    Args:
        iterator: The iterator yielding items to display.
        item_formatter: A callable that takes an item and returns a dictionary
            representing the row data (for table) or the JSON object.
        table_creator: A callable that takes a boolean (is_first_page) and
            returns a rich.Table instance. Used only if json_output is False.
        json_output: If True, output items as a JSON list. Otherwise, display
            them in a table created by table_creator.
        page_size: The number of items to display per page in interactive mode.
        interactive: If True, enables interactive pagination. If False, displays
            up to max_items (or all items if max_items is None) without prompting.
        max_items: The maximum total number of items to display when interactive
            is False. If None, all items are displayed.
        console: The rich.Console object to use for output.

    Returns:
        The total number of items displayed.
    """
    # JSON output is machine-readable: stdout carries exactly one valid JSON
    # document. Every item is collected first (bounded by max_items when set)
    # and emitted as a single array, keeping pagination markers and interactive
    # prompts out of the stream.
    #
    # The shared renderer writes plain JSON: no color codes or terminal-width
    # wrapping even when stdout is a terminal, and values with no JSON
    # representation (NaN/Infinity) raise a clean error instead of being
    # emitted.
    if json_output:
        items = (
            list(itertools.islice(iterator, max_items))
            if max_items is not None
            else list(iterator)
        )
        rows = [item_formatter(item) for item in items]
        print(
            render_output(rows, OutputFormat.JSON.value), file=console.file, flush=True
        )
        return len(rows)

    total_count = 0
    pages = _paginate(iterator, page_size if interactive else max_items)

    # Start interactive session if needed
    if interactive:
        try:
            from anyscale.telemetry import (  # noqa: PLC0415 - codex_reason("gpt5.2", "lazy import to avoid telemetry startup unless interactive")
                start_interactive_session,
            )

            start_interactive_session()
        except Exception:  # noqa: BLE001
            pass

    # Fetch and render first page
    with console.status("Retrieving items…", spinner="dots"):
        try:
            first_page = next(pages)
        except StopIteration:
            first_page = []

    if first_page:
        total_count += _render_page(
            first_page, item_formatter, table_creator, True, 1, console
        )

    # For interactive commands, mark when command logic completes
    if interactive:
        try:
            from anyscale.telemetry import (  # noqa: PLC0415 - codex_reason("gpt5.2", "lazy import to avoid telemetry startup unless interactive")
                mark_command_complete,
            )

            mark_command_complete()
        except Exception:  # noqa: BLE001
            pass

    # Non-interactive: stop after first page
    if not interactive:
        return total_count

    # Interactive: check if user wants to continue
    if not _should_continue_pagination(page_size, len(first_page), console):
        return total_count

    # Render remaining pages with correct telemetry timing
    page_num = 2
    while True:
        # Start page fetch timing and generate new trace ID BEFORE fetching
        try:
            from anyscale.telemetry import (  # noqa: PLC0415 - codex_reason("gpt5.2", "lazy import to avoid telemetry startup unless interactive")
                mark_page_fetch_start,
            )

            mark_page_fetch_start(page_num)
        except Exception:  # noqa: BLE001
            pass

        # Now fetch the page (with the new trace ID)
        try:
            page = next(pages)
        except StopIteration:
            break

        # Render the page
        total_count += _render_page(
            page, item_formatter, table_creator, False, page_num, console
        )

        # Complete page fetch telemetry
        try:
            from anyscale.telemetry import (  # noqa: PLC0415 - codex_reason("gpt5.2", "lazy import to avoid telemetry startup unless interactive")
                mark_page_fetch_complete,
            )

            mark_page_fetch_complete(page_num)
        except Exception:  # noqa: BLE001
            pass

        # Check if user wants to continue or if this was the last page
        if not _should_continue_pagination(page_size, len(page), console):
            break

        page_num += 1

    return total_count
