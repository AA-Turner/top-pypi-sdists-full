"""Portable progress coordinates at a durable optimizer or epoch boundary."""

from dataclasses import asdict, dataclass

from labqoat.json_document import JsonDocument


@dataclass(frozen=True)
class CheckpointProgress:
    """Identify the next input independently of the cumulative compute consumption ledger."""

    epoch: int
    update: int
    next_sample: int

    def document(self) -> JsonDocument:
        """Return exact integer cursors for canonical manifest capture."""
        return JsonDocument.expect_dict(asdict(self))
