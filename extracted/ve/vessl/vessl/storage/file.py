from dataclasses import dataclass


@dataclass
class VolumeFile:
    # Relative path (ending with filename) inside the volume.
    path: str

    # Size, in bytes
    size: int
