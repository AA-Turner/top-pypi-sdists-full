import itertools
from json import dumps as json_dumps
from typing import Any, Callable, Dict, Iterator, List, Optional

from rich.console import Console
from rich.table import Table

from anyscale.util import AnyscaleJSONEncoder


def _paginate(iterator: Iterator[Any], page_size: Optional[int]) -> Iterator[List[Any]]:
    if page_size is None:
        yield list(iterator)
    else:
        while True:
            page = list(itertools.islice(iterator, page_size))
            if not page:
                return
            yield page


def display_list(  # noqa: PLR0913
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
    total_count = 0
    pages = _paginate(iterator, page_size if interactive else max_items)

    # fetch first page under spinner
    with console.status("Retrieving items…", spinner="dots"):
        try:
            first_page = next(pages)
        except StopIteration:
            first_page = []

    def _render(page: List[Any], is_first: bool, page_num: int):
        nonlocal total_count
        total_count += len(page)
        if interactive:
            console.print(f"[dim]Page {page_num}[/dim]")
        rows = [item_formatter(item) for item in page]
        if json_output:
            json_str = json_dumps(rows, indent=2, cls=AnyscaleJSONEncoder)
            console.print_json(json=json_str)
        else:
            tbl = table_creator(is_first)
            for row in rows:
                tbl.add_row(*row.values())
            console.print(tbl)

    # render first page
    if first_page:
        _render(first_page, True, page_num=1)

    # non-interactive: stop after first page
    if not interactive:
        return total_count

    # interactive: prompt after full first page
    if len(first_page) == page_size:
        console.print()
        console.print(
            "[dim]Press [bold]Enter[/bold] to continue, [bold]q[/bold] to quit…[/]"
        )
        if input("> ").strip().lower() == "q":
            return total_count

    # render remaining pages
    page_num = 2
    for page in pages:
        _render(page, False, page_num)
        if len(page) == page_size:
            console.print()
            console.print(
                "[dim]Press [bold]Enter[/bold] to continue, [bold]q[/bold] to quit…[/]"
            )
            if input("> ").strip().lower() == "q":
                break
        page_num += 1

    return total_count
