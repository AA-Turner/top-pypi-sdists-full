"""Authoritative Build completion with nonzero remote failure status."""

from collections.abc import Sequence
from typing import TYPE_CHECKING
from contextlib import closing

import click

from labqoat.cli.completion_waiter import CompletionWaiter
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.observation_deadline import ObservationDeadline
from labqoat.cli.output.cli_failure import CliFailure
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.cli.console.console_options import ConsoleOptions
from labqoat.cli.console.run_console import RunConsole
from labqoat.json_document import JsonDocument

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient


class BuildWatchCommand(StrictCommand):
    """Wait for retained completion then read the Build's final authoritative record."""

    def __init__(self, params: Sequence[click.Parameter]) -> None:
        """Accept the Build selector and an independent observation timeout."""
        super().__init__(
            "watch",
            params=[
                *params,
                *ConsoleOptions.parameters(),
                click.Option(["--silent"], is_flag=True),
                ObservationDeadline.option(),
            ],
            help="Watch live build output; --silent prints only the final outcome.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Never report failed or incomplete Builds as successful waits."""
        client = ContextAccessor.current().management()
        console = RunConsole(ConsoleOptions.current(ctx.params))
        try:
            with ObservationDeadline.current(str(ctx.params["build_ref"])).watching():
                current = client.get("/api/v1/builds/item", {"ref": ctx.params["build_ref"]})
                if not ctx.params["silent"]:
                    self.follow(client, str(current["id"]), console)
                final = CompletionWaiter.wait(
                    client, current, frozenset({"upload_pending", "queued", "building"}), "/api/v1/builds/item", "build"
                )
                if final.get("status") != "succeeded":
                    console.accept(JsonDocument(content="", event_type="run.submission.build.failed"))
                    raise CliFailure(
                        f"Build {final['id']} ended with status {final.get('status')}.", 1, resource_id=str(final["id"])
                    )
                ResultWriter(pretty=False).write_dict(final)
        finally:
            console.close()
            client.close()
        return None

    @staticmethod
    def follow(client: "ManagementClient", reference: str, console: RunConsole) -> None:
        """Drain the builder's durable log end marker before checking its final status."""
        console.accept(JsonDocument(content="", event_type="run.submission.build.started"))
        with closing(client.stream_events("/api/v1/builds/item/logs/stream", {"ref": reference})) as events:
            for event in events:
                data = JsonDocument.expect_dict(event.get("data", {}))
                if event.get("event") == "log.entry":
                    console.accept(JsonDocument(data, stream="build"))
                elif event.get("event") == "log.error":
                    raise CliFailure(str(data.get("detail", "Build log stream failed.")), 1)
