"""``lab run wait``: block until runs end and print one line per finished run, instead of a polling loop."""

from __future__ import annotations

import queue
import threading
from time import monotonic
from typing import TYPE_CHECKING

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.observation_deadline import ObservationDeadline
from labqoat.cli.output.cli_failure import CliFailure
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.errors.api_error import ApiError
from labqoat.json_document import JsonValue

if TYPE_CHECKING:
    from labqoat._generated.run import Run
    from labqoat.client import Client


class RunWaitCommand(StrictCommand):
    """Follow every named run's event stream at once and report each as it ends."""

    def __init__(self) -> None:
        """Declare the runs, the any-of switch and the observation timeout."""
        super().__init__(
            "wait",
            params=[
                click.Argument(["runs"], nargs=-1, required=True),
                click.Option(["--any", "first"], is_flag=True, help="Return when the first of the runs ends."),
                ObservationDeadline.option(),
            ],
            help="Block until the runs end (the first of them with --any) and print each one's status as it ends. "
            "Exits 3 when --timeout passes first; the runs continue.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Start one follower per run and print finished runs until enough have ended or time is up."""
        runs = list(dict.fromkeys(str(run) for run in ctx.params["runs"]))
        seconds = ctx.params.get("wait_timeout")
        deadline = None if seconds is None else monotonic() + float(seconds)
        client = ContextAccessor.current().client()
        finished: queue.Queue[dict[str, JsonValue]] = queue.Queue()
        for run in runs:
            threading.Thread(target=self.follow, args=(client, run, finished), daemon=True).start()
        try:
            self.report(finished, 1 if ctx.params["first"] else len(runs), deadline)
        finally:
            client.close()
        return None

    @staticmethod
    def report(finished: queue.Queue[dict[str, JsonValue]], wanted: int, deadline: float | None) -> None:
        """Write each finished run until ``wanted`` have ended, or fail with exit 3 at the deadline."""
        writer = ResultWriter()
        for done in range(wanted):
            remaining = None if deadline is None else max(deadline - monotonic(), 0.0)
            try:
                writer.write_dict(finished.get(timeout=remaining))
            except queue.Empty as error:
                left = wanted - done
                raise CliFailure(
                    f"Observation timed out with {left} run(s) still going. Accepted work continues.", 3
                ) from error

    @classmethod
    def follow(cls, client: Client, run: str, finished: queue.Queue[dict[str, JsonValue]]) -> None:
        """Wait for one run's terminal state; a failed or cancelled run is reported like any other."""
        try:
            finished.put(cls.record(client.runs.wait(run)))
        except ApiError as error:
            ended = getattr(error, "run", None)
            finished.put(
                cls.record(ended) if ended is not None else {"id": run, "status": "unknown", "error": error.message}
            )

    @staticmethod
    def record(run: Run) -> dict[str, JsonValue]:
        """The finished run's identity, status and, when it did not succeed, why."""
        record: dict[str, JsonValue] = {"id": run.id, "name": run.name, "status": run.status}
        failure = run.failure_detail or {}
        reason = failure.get("reason")
        if isinstance(reason, str):
            record["reason"] = reason
        return record
