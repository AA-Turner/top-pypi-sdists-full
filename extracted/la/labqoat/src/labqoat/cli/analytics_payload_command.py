"""Payload command that waits for durable governed analytics."""

from __future__ import annotations

from typing import TYPE_CHECKING
from collections.abc import Sequence
import click
from labqoat.cli.mutation_spec import MutationSpec

from labqoat.cli.analytics_failure import AnalyticsFailure
from labqoat.cli.analytics_waiter import AnalyticsWaiter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.payload_command import PayloadCommand
from labqoat.cli.observation_deadline import ObservationDeadline

if TYPE_CHECKING:
    from labqoat.json_document import JsonDocument
    from labqoat.management_client import ManagementClient


class AnalyticsPayloadCommand(PayloadCommand):
    """Submit a payload-backed query and print its terminal result."""

    def __init__(self, name: str, spec: MutationSpec, params: Sequence[click.Parameter], help_text: str) -> None:
        """Expose an observation limit separately from submitted analytics parameters."""
        super().__init__(name, spec, [*params, ObservationDeadline.option()], help_text)

    def payload(self, values: dict[str, object]) -> JsonDocument:
        """Keep the local wait option out of the remote intent."""
        values.pop("wait_timeout", None)
        return super().payload(values)

    def render_response(
        self,
        client: ManagementClient,
        response: JsonDocument,
    ) -> None:
        """Wait independently of the submission response connection."""
        with ObservationDeadline.current(str(response["id"])).watching():
            final = AnalyticsWaiter.wait(client, response)
        AnalyticsFailure.raise_for(final)
        ResultWriter().write_dict(final)
