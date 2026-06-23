import click
import humanfriendly

from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.table import format_table


def print_table_formatted(res: dict, name: str):
    limit = 20
    data = [d.values() for d in res["data"][:limit]]
    meta = res["meta"]
    stats = res.get("statistics", {})
    row_count = stats.get("rows_read", 0)
    elapsed = stats.get("elapsed", 0)
    cols = len(meta)
    try:
        table = format_table(data, meta)
        click.echo(FeedbackManager.highlight(message=f"\n» Running {name}\n"))
        click.echo(table)
        click.echo("")
        rows_read = humanfriendly.format_number(stats.get("rows_read", 0))
        bytes_read = humanfriendly.format_size(stats.get("bytes_read", 0))
        elapsed = humanfriendly.format_timespan(elapsed) if elapsed >= 1 else f"{elapsed * 1000:.2f}ms"
        stats_message = f"» {bytes_read} ({rows_read} rows x {cols} cols) in {elapsed}"
        rows_message = f"» Showing first {limit} rows" if row_count > limit else "» Showing all rows"
        click.echo(FeedbackManager.success(message=stats_message))
        click.echo(FeedbackManager.gray(message=rows_message))
    except ValueError as exc:
        # Python 3.11 wording: "max() arg is an empty sequence"
        # Python 3.12 wording: "max() iterable argument is empty"
        if str(exc) in ("max() arg is an empty sequence", "max() iterable argument is empty"):
            click.echo("------------")
        else:
            raise
