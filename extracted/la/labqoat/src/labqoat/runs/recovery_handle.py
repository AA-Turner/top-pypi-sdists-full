"""A recovery decision with nullable admission identity and explicit captured-cycle waiting."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from labqoat._generated.recovery_operation import RecoveryOperation

if TYPE_CHECKING:
    from labqoat.runs.recovery_client import RecoveryClient


@dataclass(frozen=True)
class RecoveryHandle:
    """Preserve original acceptance while offering fresh operation reads and eventual execution outcome."""

    accepted: RecoveryOperation
    operation_key: str
    client: "RecoveryClient"

    @property
    def id(self) -> str:
        """Expose the durable operation identity even before an attempt exists."""
        return self.accepted.id

    def refresh(self) -> RecoveryOperation:
        """Read the current admission phase and captured execution outcome."""
        return self.client.get(self.accepted.run_id, self.id)

    def cancel(self) -> RecoveryOperation:
        """Cancel this decision before admission without affecting a later cycle."""
        return self.client.cancel(self.accepted.run_id, self.id)

    def wait(self, *, max_reconnects: int = 8) -> RecoveryOperation:
        """Follow pushed events through admission and the entire captured cycle, raising on failure."""
        from labqoat.runs.recovery_waiter import RecoveryWaiter

        return RecoveryWaiter(self, max_reconnects).run()
