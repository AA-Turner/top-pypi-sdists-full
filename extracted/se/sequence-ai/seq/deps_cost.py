"""
How a size reads in what the CLI prints: `size` ("222.3 MB" under a GB, "8.41 GB" from one), and `money`, as `seq
storage` prices what you keep.
"""
from __future__ import annotations

from sequence_ai._core.money import money


def size(n) -> str:
    """Bytes as `seq volume ls` reads them: "222.3 MB" under a GB, "8.41 GB" from one."""
    n = float(n or 0)
    return f"{n / 1e9:.2f} GB" if n >= 1e9 else f"{n / 1e6:.1f} MB"
