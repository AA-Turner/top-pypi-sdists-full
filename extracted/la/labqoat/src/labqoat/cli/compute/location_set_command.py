"""``compute location set`` changes allowed hardware or pauses scheduling in one location."""

from __future__ import annotations

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument, JsonValue


class LocationSetCommand(StrictCommand):
    """Replace the allowed instance types and/or toggle pausing under the location's current revision."""

    def __init__(self) -> None:
        """Declare the location selector and its policy options."""
        params: list[click.Parameter] = [
            click.Argument(["location_id"], type=str, required=True),
            click.Option(
                ["--allow", "instance_types"],
                multiple=True,
                help="Instance type from the location's catalog (see compute offerings); repeat to allow several. Replaces the list.",
            ),
            click.Option(["--pause/--resume", "paused"], default=None, help="Stop or resume new placements here."),
        ]
        super().__init__("set", params=params, help="Change allowed hardware or pause a location.")

    def invoke(self, ctx: click.Context) -> object:
        """Read the location revision and apply one conditional merge patch."""
        patch = self.patch(ctx.params["instance_types"], ctx.params["paused"])
        location_id = str(ctx.params["location_id"])
        client = ContextAccessor.current().compute()
        try:
            revision = str(client.location(location_id)["revision"])
            ResultWriter().write_dict(client.update_location(location_id, patch, revision))
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

    @staticmethod
    def patch(instance_types: tuple[str, ...], paused: bool | None) -> JsonDocument:
        """Include only the requested changes, rejecting an empty update before any request."""
        patch = JsonDocument()
        if instance_types:
            allowed: list[JsonValue] = list(dict.fromkeys(instance_types))
            patch["instance_types"] = allowed
        if paused is not None:
            patch["paused"] = paused
        if not patch:
            ErrorReporter.report_usage("Select --allow, --pause or --resume.")
        return patch
