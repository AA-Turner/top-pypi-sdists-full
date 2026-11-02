"""How much of a sandbox host's budget is in use, and what its sandboxes may start from and see."""

from dataclasses import dataclass

from labqoat.json_document import JsonDocument
from labqoat.sandbox.sandbox_resources import SandboxResources
from labqoat.sandbox.sandbox_state import SandboxState


@dataclass(frozen=True)
class SandboxCapacity:
    """The host's budget, what its sandboxes hold, their identifiers, and the images and volumes it offers.

    Memory in ``used`` never exceeds the budget. CPU is shared, so ``used`` adds up the ceilings of the
    sandboxes and may exceed the budget they run within together.
    """

    budget: SandboxResources
    used: SandboxResources
    sandboxes: tuple[str, ...]
    images: tuple[str, ...]
    volumes: tuple[str, ...]

    @staticmethod
    def decode(document: JsonDocument) -> "SandboxCapacity":
        """Read the host's capacity document."""
        return SandboxCapacity(
            SandboxResources.decode(JsonDocument.expect_dict(document["budget"])),
            SandboxResources.decode(JsonDocument.expect_dict(document["used"])),
            tuple(state.id for state in SandboxState.listed(document)),
            SandboxCapacity._names(document, "images"),
            SandboxCapacity._names(document, "volumes"),
        )

    @staticmethod
    def _names(document: JsonDocument, key: str) -> tuple[str, ...]:
        """Read one list of names."""
        return tuple(JsonDocument.expect_scalar(item, str) for item in JsonDocument.expect_list(document[key]))
