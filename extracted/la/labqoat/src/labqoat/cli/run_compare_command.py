"""``lab run compare``: runs side by side with their arguments and latest metrics, instead of grepping logs."""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from fnmatch import fnmatchcase
from typing import TYPE_CHECKING

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument, JsonValue

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class RunCompareCommand(StrictCommand):
    """One row per run: status, the chosen arguments and the newest value of each matching metric."""

    def __init__(self) -> None:
        """Declare the run selection, the metric patterns and the argument columns."""
        super().__init__(
            "compare",
            params=[
                click.Option(["--app"], help="Runs of this app."),
                click.Option(["--tags"], help="Runs carrying every one of these comma-separated tags."),
                click.Option(["--owner"], help="The child runs this run started."),
                click.Option(["--limit"], type=click.IntRange(1, 200), default=50, show_default=True),
                click.Option(
                    ["--metrics"],
                    default="val/*,test/*",
                    show_default=True,
                    help="Comma-separated metric names or glob patterns; each match is a column.",
                ),
                click.Option(["--args", "arguments"], help="Comma-separated argument names to show as columns."),
            ],
            help="Compare runs side by side: status, chosen arguments and each metric's latest value.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """List the runs, then read their latest metrics (and arguments when asked) in parallel."""
        query = {key: ctx.params[key] for key in ("app", "tags", "owner", "limit") if ctx.params[key] is not None}
        patterns = [pattern.strip() for pattern in str(ctx.params["metrics"]).split(",") if pattern.strip()]
        arguments = [name.strip() for name in str(ctx.params["arguments"] or "").split(",") if name.strip()]
        client = ContextAccessor.current().management()
        try:
            runs = JsonDocument.expect_list(client.get("/api/v1/runs", query)["items"])
            with ThreadPoolExecutor(8) as pool:
                rows = list(
                    pool.map(lambda run: self.row(client, JsonDocument.expect_dict(run), patterns, arguments), runs)
                )
            ResultWriter().write_dict({"items": rows})
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

    @staticmethod
    def row(
        client: ManagementClient, run: dict[str, JsonValue], patterns: list[str], arguments: list[str]
    ) -> JsonValue:
        """The run's identity and status, then one column per chosen argument and matching metric."""
        row: dict[str, JsonValue] = {key: run.get(key) for key in ("id", "name", "status")}
        if arguments:
            given = JsonDocument.expect_dict(client.get("/api/v1/runs/{ref}", {"ref": run["id"]}).get("manifest") or {})
            values = JsonDocument.expect_dict(given.get("args") or {})
            row.update({name: values.get(name) for name in arguments})
        latest = client.get("/api/v1/runs/{ref}/metrics", {"ref": run["id"], "latest": "true"})
        for item in map(JsonDocument.expect_dict, JsonDocument.expect_list(latest.get("items", []))):
            name = str(item.get("name"))
            if any(fnmatchcase(name, pattern) for pattern in patterns):
                row[name] = item.get("value")
        return row
