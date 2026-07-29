"""Memory and resource diagnostics — strictly read-only helpers.

The motivating bug class needs visibility: on Jetson Thor unified memory,
top/ps/cgroup all under-report the actual GPU-driver-held memory. These
helpers parse the data sources the team had to assemble by hand during the
incident (``/proc/meminfo``, cgroup, NvMap, tegrastats, nvidia-smi, CuPy
mempools) and give a single ``snapshot()`` and ``delta()`` API.
"""

from .memory import MemorySnapshot, delta, format_table, snapshot

__all__ = ["MemorySnapshot", "snapshot", "delta", "format_table"]
