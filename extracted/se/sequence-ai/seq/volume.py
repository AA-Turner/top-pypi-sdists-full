"""
`seq.Volume` — a named volume you uploaded (`seq volume put`): a policy's weights
(`weights=seq.Volume.from_name("pi05-ft")`) or a benchmark's assets (`assets=`), each lowered to the wire
`vol://<name>`.

WHY a handle object rather than a raw string: the name is checked and lowered in one place, and the call reads as what
it is. A policy mounts no volumes of its own: `@seq.policy(volumes=...)`, which the platform refused, is gone
.
"""
from __future__ import annotations

from sequence_base.contract import VolumeRef


class Volume:
    """A named volume."""

    __slots__ = ("name",)

    def __init__(self, name: str) -> None:
        self.name = name

    @classmethod
    def from_name(cls, name: str) -> "Volume":
        """Reference a volume by name."""
        return cls(name)

    def _ref(self, mount: str) -> VolumeRef:
        """Lower to the wire `VolumeRef` mounted at `mount`.

        WHY a `vol://` scheme: the ref must name the source unambiguously, and a named (not URI) volume
        has no bucket or hf:// URI — `vol://<name>` is the platform's internal scheme for "the named volume".
        """
        return VolumeRef(uri=f"vol://{self.name}", mount=mount)

    def __repr__(self) -> str:
        return f"Volume.from_name({self.name!r})"
