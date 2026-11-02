"""``lab compute offerings``: the GPU models and shapes this account may buy."""

from __future__ import annotations

import click

from labqoat.cli.compute.offering_summary import OfferingSummary
from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.output.error_reporter import ErrorReporter
from labqoat.cli.output.result_writer import ResultWriter
from labqoat.cli.strict_command import StrictCommand
from labqoat.json_document import JsonDocument


class OfferingsCommand(StrictCommand):
    """Summarize the observed catalog by GPU model; one model's shapes or the raw catalog on request."""

    def __init__(self) -> None:
        """Declare the model filter and the raw-catalog switch."""
        super().__init__(
            "offerings",
            params=[
                click.Option(["--gpu"], help="List the purchasable shapes of one GPU model, cheapest first."),
                click.Option(["--all", "raw"], is_flag=True, help="Print every shape in every location as observed."),
            ],
            help="Show the GPU models you can buy with memory, cheapest shape and price.",
        )

    def invoke(self, ctx: click.Context) -> object:
        """Read the catalog once and render the requested view."""
        client = ContextAccessor.current().compute()
        try:
            catalog = client.offerings()
            items = [JsonDocument.expect_dict(item) for item in JsonDocument.expect_list(catalog.get("items", []))]
            document = catalog if ctx.params["raw"] else OfferingSummary.summarize(items, ctx.params["gpu"])
            ResultWriter().write_dict(document)
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None
