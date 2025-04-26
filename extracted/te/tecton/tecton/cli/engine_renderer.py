from tecton.cli import printer
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2


class PlanRenderingClient:
    def __init__(
        self,
        response: metadata_service_pb2.QueryStateUpdateResponseV2,
    ):
        self.response = response

    def has_diffs(self) -> bool:
        """Returns True if there are any changes to be applied."""
        return self.num_fcos_changed > 0

    def print_plan(self):
        """Print the tecton plan output to the console."""
        printer.safe_print(self.response.successful_plan_output.string_output)

    def print_empty_plan(self):
        """Print the no changes (empty plan) message to the console."""
        printer.safe_print("🎉 The remote and local state are the same, nothing to do!")

    def print_apply_warnings(self):
        """If tecton apply is run, print relevant plan-level warnings to console."""
        printer.safe_print(self.response.successful_plan_output.apply_warnings)

    def get_json_plan_output(self) -> str:
        """Return plan output as json string."""
        return self.response.successful_plan_output.json_output

    @property
    def num_fcos_changed(self) -> int:
        """Returns the number of FCOs being created, updated, or deleted."""
        return self.response.successful_plan_output.num_fcos_changed
