"""A project's named volume: a filesystem kept in platform storage that functions mount."""

import re
from dataclasses import dataclass

from labqoat.json_document import JsonValue


@dataclass(frozen=True)
class Volume:
    """Name a volume of the run's project; mounting one that does not exist yet creates it empty.

    A mount starts from the volume's latest committed state. Writes reach the volume when committed: at the
    end of every call, every 30 seconds in the background, and whenever the function calls ``commit()``. Other
    runs see them after their own ``reload()`` or when they next mount the volume. Read-only mounts never commit.

    ``subpath`` mounts one directory of the volume instead of all of it, such as ``Volume("data", subpath="runs/c5")``:
    the host fetches and lays out only what that directory holds, the mount shows its contents, and commits land
    inside it. A directory not made yet mounts empty.
    """

    name: str
    read_only: bool = False
    subpath: str = ""

    def __post_init__(self) -> None:
        """Validate a portable identity without contacting the platform or creating storage."""
        if re.fullmatch(r"[a-z0-9][a-z0-9_-]{0,62}", self.name) is None:
            raise ValueError("Volume names require 1..63 lowercase letters, digits, underscores or hyphens")
        if type(self.read_only) is not bool:
            raise ValueError("Volume read_only must be a boolean")
        if type(self.subpath) is not str:
            raise ValueError("Volume subpath must be a string")
        object.__setattr__(self, "subpath", self.subpath.strip("/"))
        segments = self.subpath.split("/")
        if self.subpath and (
            len(self.subpath.encode()) > 1024
            or "\0" in self.subpath
            or any(segment in ("", ".", "..") or len(segment.encode()) > 255 for segment in segments)
        ):
            raise ValueError("Volume subpath must name a directory inside the volume, such as 'runs/c5'")

    def to_dict(self) -> dict[str, JsonValue]:
        """Capture identity and permissions independently of the mounted data's contents."""
        mount: dict[str, JsonValue] = {"name": self.name, "read_only": self.read_only}
        return {**mount, "subpath": self.subpath} if self.subpath else mount

    def commit(self) -> int:
        """Commit what this worker changed in the mounted volume now and return the volume's version."""
        from labqoat.volumes.mounted_volumes import MountedVolumes

        return MountedVolumes.current().named(self.name, self.subpath).commit()

    def reload(self) -> int:
        """Bring other runs' commits into the mounted volume, keeping this worker's uncommitted changes."""
        from labqoat.volumes.mounted_volumes import MountedVolumes

        return MountedVolumes.current().named(self.name, self.subpath).reload()
