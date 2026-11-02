"""The environment a restored workload was started with, which its process still has to take up."""

import os
from pathlib import Path


class SpecEnvironment:
    """Replace this process's environment with the one the runtime started this copy of the workload with.

    A process restored from a memory snapshot still holds the environment of the worker that saved it: its run,
    attempt, credentials and secrets. The runtime publishes this copy's own; platform variables the new one lacks go.
    """

    def __init__(self, source: Path = Path("/proc/gvisor/spec_environ")) -> None:
        """Name where the runtime publishes the environment without reading it."""
        self.source = source

    def adopt(self) -> None:
        """Take up the published environment."""
        values = dict(entry.split("=", 1) for entry in self.source.read_bytes().decode().split("\0") if "=" in entry)
        for name in [name for name in os.environ if name.startswith("LABQOAT_") and name not in values]:
            del os.environ[name]
        os.environ.update(values)
