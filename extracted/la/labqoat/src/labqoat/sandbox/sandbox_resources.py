"""Processor and memory amounts of a sandbox host, in the units a function declares."""

from dataclasses import dataclass

from labqoat.json_document import JsonDocument


@dataclass(frozen=True)
class SandboxResources:
    """Processor cores and mebibytes of memory."""

    cpu: float
    memory: int

    @staticmethod
    def decode(document: JsonDocument) -> "SandboxResources":
        """Read both amounts from a host document, which counts thousandths of a core."""
        return SandboxResources(
            JsonDocument.expect_scalar(document["cpu_millicores"], int) / 1000,
            JsonDocument.expect_scalar(document["memory_mb"], int),
        )
