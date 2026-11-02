"""Exact scientific and framework compatibility declared by a checkpoint-producing adapter."""

from dataclasses import asdict, dataclass

from labqoat.json_document import JsonDocument


@dataclass(frozen=True, kw_only=True)
class CheckpointCompatibility:
    """Bind configuration, data, model and runtime identities independently of checkpoint progress."""

    config_digest: str
    seed_digest: str
    data_digest: str
    model_digest: str
    runtime_digest: str
    optimizer: str
    scheduler: str
    precision: str
    world_size: int = 1

    def document(self) -> JsonDocument:
        """Return the compatibility inventory for canonical manifest capture."""
        return JsonDocument.expect_dict(asdict(self))
