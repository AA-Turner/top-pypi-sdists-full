from dataclasses import dataclass


@dataclass
class VolumeInfo:
    """Information about a volume."""

    volume_id: str
    """Volume ID."""
    name: str
    """Volume name."""
    quota_size_gib: int = 0
    """Capacity quota in GiB."""
    quota_inodes: int = 0
    """Inode quota."""
    used_size_bytes: int = 0
    """Used size in bytes."""
    used_inodes: int = 0
    """Used inodes."""


@dataclass
class VolumeAndToken(VolumeInfo):
    """Information about a volume and its auth token."""

    token: str = ""
    """Volume auth token."""


__all__ = [
    "VolumeInfo",
    "VolumeAndToken",
]
