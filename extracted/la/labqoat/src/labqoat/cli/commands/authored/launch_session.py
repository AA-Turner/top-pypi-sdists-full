"""Watch everything a local launcher submits as one group while the launcher runs on this machine."""

from __future__ import annotations

import sys
from collections.abc import Callable
from threading import Thread
from typing import TYPE_CHECKING

import click

from labqoat.cli.console.console_options import ConsoleOptions
from labqoat.cli.console.run_banner import RunBanner
from labqoat.cli.console.run_console import RunConsole
from labqoat.cli.output.cli_failure import CliFailure
from labqoat.cli.output.output_style import OutputStyle
from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonDocument

if TYPE_CHECKING:
    from labqoat.client import Client
    from labqoat.compute.client_group import ClientGroup


class LaunchSession:
    """Open a group for the launch, follow it like a run, and close it with the launcher's outcome."""

    def __init__(self, client: Client, name: str, options: ConsoleOptions) -> None:
        """Bind the launcher's client; nothing is requested until the session runs."""
        self.client = client
        self.name = name
        self.options = options
        self.console: RunConsole | None = None
        self.watcher: Thread | None = None

    def run(self, launcher: Callable[[Client], object]) -> object:
        """Run the launcher with a client scoped to the group; a service without groups runs it plainly."""
        try:
            group = self.client.group(self.name)
            group.__enter__()
        except ApiError:
            return launcher(self.client)
        self.follow(group)
        try:
            value = launcher(group.client)
        except BaseException as error:
            group.__exit__(type(error), error, error.__traceback__)
            self.conclude(group)
            raise self.reported(error) from error
        group.__exit__(None, None, None)
        self.conclude(group)
        return value

    def reported(self, error: BaseException) -> BaseException:
        """The console already stated a launcher's failure; only structured modes and usage errors say it again."""
        if self.options.json or self.options.silent or isinstance(error, (click.ClickException, KeyboardInterrupt)):
            return error
        return CliFailure(str(error), 1, reported=True)

    def follow(self, group: ClientGroup) -> None:
        """Announce the group and stream its members' progress beside the running launcher."""
        link = f"{self.client.transport.base_url.rstrip('/')}/runs/{group.id}"
        self.console = RunConsole(self.options, diagnostics=True, observing=True, link=link)
        if not (self.options.json or self.options.silent):
            for line in RunBanner.lines(OutputStyle.current(sys.stderr), group.id, self.name, link):
                click.echo(line, err=True)
        self.watcher = Thread(target=self.watch, args=(group.id,), daemon=True)
        self.watcher.start()

    def watch(self, group: str) -> None:
        """Feed the group's log stream to the console until the group ends or the stream is lost."""
        assert self.console is not None
        try:
            for entry in self.client.runs.logs(group, include_metrics=True, build_output="unfinished"):
                self.console.accept(entry)
        except ApiError:
            return

    def conclude(self, group: ClientGroup) -> None:
        """Let the stream drain, then state the group's authoritative outcome once."""
        assert self.console is not None and self.watcher is not None
        self.watcher.join(timeout=30)
        try:
            self.console.finish(JsonDocument(self.client.runs.get(group.id).to_dict()))
        finally:
            self.console.close()
