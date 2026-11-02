"""What every robot's rig file shares: its cameras, the role each one plays, a home pose.

~/.config/dreamscale/<robot>.json holds these keys for every robot, beside the robot's
own hardware keys (YAM's arms, Franka's arm and gripper). Subclasses declare those
fields, then `version: int = 1` and `home_pose: tuple | None = None` (so existing
positional constructors keep their order), plus their roles, home-pose shape and
to_dict/from_dict additions.
"""

from __future__ import annotations

import json
import math
import os
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import ClassVar

from .camera_sources import CameraSpec

MAX_CAMERAS = 12


def rig_file_path(robot: str) -> Path:
    return Path.home() / f".config/dreamscale/{robot}.json"


@dataclass
class RigFile:
    cameras: list[CameraSpec] = field(default_factory=list)
    roles: dict[str, str] = field(default_factory=dict)

    ROLES: ClassVar[tuple[str, ...]] = ()
    LABEL: ClassVar[str] = "rig"
    HOME_SIZE: ClassVar[int] = 0
    HOME_HELP: ClassVar[str] = "finite values"

    def camera(self, role: str) -> CameraSpec:
        camera_id = self.roles[role]
        return next(c for c in self.cameras if c.id == camera_id)

    def _check_home(self, pose) -> bool:
        """Robot-specific home-pose rules beyond size and finiteness."""
        return True

    def validate_rig(self):
        """Version, cameras, roles and home pose; robot-specific checks come after."""
        if type(self.version) is not int or self.version != 1:
            raise ValueError(f"Unsupported {self.LABEL} configuration version.")
        pose = self.home_pose
        if pose is not None and (
            not isinstance(pose, (tuple, list))
            or len(pose) != self.HOME_SIZE
            or any(type(v) not in (int, float) or not math.isfinite(v) for v in pose)
            or not self._check_home(pose)
        ):
            raise ValueError(f"Home pose needs {self.HOME_SIZE} {self.HOME_HELP}.")
        if len(self.cameras) > MAX_CAMERAS:
            raise ValueError(f"Choose at most {MAX_CAMERAS} camera sources.")
        ids = [c.id for c in self.cameras]
        if len(set(ids)) != len(ids):
            raise ValueError("Camera IDs must be unique.")
        if len({c.physical_id for c in self.cameras}) != len(self.cameras):
            raise ValueError("The same physical camera was selected more than once.")
        if not set(self.roles) <= set(self.ROLES) or not set(self.roles.values()) <= set(ids):
            raise ValueError(
                f"Camera roles must reference configured {_or(self.ROLES)} cameras."
            )
        if len(set(self.roles.values())) != len(self.roles):
            raise ValueError("Assign a different physical camera to each role.")
        return self

    def rig_dict(self) -> dict:
        value = {
            "version": self.version,
            "cameras": [asdict(c) for c in self.cameras],
            "roles": dict(self.roles),
        }
        if self.home_pose is not None:
            value["home_pose"] = list(self.home_pose)
        return value

    @staticmethod
    def rig_fields(value: dict) -> dict:
        """The shared keys of a parsed rig file, as constructor arguments."""
        return {
            "cameras": [CameraSpec(**c) for c in value.get("cameras", [])],
            "roles": dict(value.get("roles", {})),
            "version": value.get("version", 1),
            "home_pose": value.get("home_pose"),
        }


def read_rig_file(path: Path) -> dict | None:
    path = Path(path)
    return json.loads(path.read_text()) if path.exists() else None


def write_rig_file(value: dict, path: Path) -> None:
    """Atomic: a crash mid-save leaves the previous file, never half of one."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w") as stream:
            json.dump(value, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _or(roles) -> str:
    return roles[0] if len(roles) == 1 else ", ".join(roles[:-1]) + ", or " + roles[-1]
