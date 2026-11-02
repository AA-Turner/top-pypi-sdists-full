"""Foreground observation without taking ownership of remote cancellation."""

from contextlib import closing
from typing import TypeVar

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.cli_failure import CliFailure

from labqoat.json_document import JsonDocument
from labqoat.runs.run_handle import RunHandle
from labqoat.cli.console.console_options import ConsoleOptions
from labqoat.cli.console.run_console import RunConsole

T = TypeVar("T")


class RunObserver:
    """Stream diagnostics to stderr before reading an authoritatively validated result."""

    @staticmethod
    def result(handle: RunHandle[T]) -> T:
        """Close the log response on interruption and retain the accepted Run independently."""
        context = click.get_current_context(silent=True)
        values = context.parent.params if context is not None and context.parent is not None else {}
        options = ConsoleOptions.current(values)
        link = f"{ContextAccessor.current().profile.base_url.rstrip('/')}/runs/{handle.id}"
        console = RunConsole(options, diagnostics=True, observing=True, link=link)
        logs = handle.client.logs(
            handle.id,
            depth=values.get("depth"),
            run=values.get("run"),
            include_metrics=True,
            build_output=options.delivered_builds(),
        )
        final = JsonDocument()
        with closing(console), closing(logs) as entries:
            for entry in entries:
                console.accept(entry)
                final = entry
            run = RunObserver.outcome(handle, final)
            console.finish(run)
        if run["status"] != "completed" and console.live:
            raise CliFailure(f"Run {handle.id} ended with status {run['status']}.", 1, None, handle.id, reported=True)
        if run["status"] != "completed":
            return handle.result()
        inline = run.get("result")
        return handle.decoded(inline) if isinstance(inline, dict) else handle.retained()

    @staticmethod
    def outcome(handle: RunHandle[T], final: JsonDocument) -> JsonDocument:
        """Use the outcome a completed stream already delivered; older services need an authoritative read."""
        if final.get("type") == "run.logs.complete" and final.get("id") == handle.id and "status" in final:
            return final
        return JsonDocument(handle.client.get(handle.id).to_dict())
