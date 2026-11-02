"""The sandbox runtime's checkpoint of this workload, taken from inside it."""

import gc
import os
from pathlib import Path


class MemoryCheckpoint:
    """Ask the runtime to save this workload's memory, once, and learn which copy of the workload continues.

    Writing to the runtime's trigger starts the checkpoint; reading it waits until the workload runs again and says
    ``resume`` in the workload that saved it, ``restore`` in a workload continuing from the snapshot, or ``error``
    when the runtime could not save it, in which case the workload simply continues.
    """

    def __init__(self, trigger: Path = Path("/proc/gvisor/checkpoint")) -> None:
        """Name the runtime's trigger without touching it."""
        self.trigger = trigger

    def take(self) -> tuple[str, str]:
        """Checkpoint now and return the outcome with what the runtime said when it could not checkpoint."""
        gc.collect()
        try:
            descriptor = os.open(self.trigger, os.O_RDWR)
        except OSError as error:
            return "error", f"the runtime offers no checkpoint here: {error}"
        try:
            os.write(descriptor, b"1")
            outcome = os.read(descriptor, 16).decode().strip()
        except OSError as error:
            return "error", f"the runtime refused the checkpoint: {error}"
        finally:
            os.close(descriptor)
        return outcome, "" if outcome != "error" else "the runtime could not write the checkpoint"
