"""The SO-101 rig file: its serial port, calibration, home pose, and which camera plays
each role.

Lives at ~/.config/dreamscale/so101.json beside yam.json and franka.json. Until setup
writes it, it is built from the pre-rig-file keys in config.toml ([robot] port,
calibration_path and home; [camera] side_index and wrist_index), each saved OpenCV
index resolved to a stable camera identity.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar

from .camera_sources import camera_for_index
from .rig_file import RigFile, read_rig_file, rig_file_path, write_rig_file

ROLES = ("side", "wrist")
DEFAULT_CONFIG_PATH = rig_file_path("so101")


def default_config_path() -> Path:
    return rig_file_path("so101")


@dataclass
class So101Config(RigFile):
    port: str | None = None
    calibration_path: str | None = None
    version: int = 1
    home_pose: tuple[float, ...] | None = None
    # True when built from config.toml's legacy keys rather than read from so101.json.
    migrated: bool = False
    # Measured gripper.pos readings at physical closed/open for closure-based models.
    gripper_range: tuple[float, float] | None = None

    ROLES: ClassVar[tuple[str, ...]] = ROLES
    LABEL: ClassVar[str] = "SO-101"
    HOME_SIZE: ClassVar[int] = 6
    HOME_HELP: ClassVar[str] = "values: five joints in degrees, then the gripper 0-100"

    def validate(self, *, complete: bool = False) -> So101Config:
        self.validate_rig()
        if self.gripper_range is not None:
            from dreamscale_transport.praxis import validate_so101_grip_range

            self.gripper_range = validate_so101_grip_range(self.gripper_range)
        if self.port is not None and (not isinstance(self.port, str) or not self.port):
            raise ValueError("The SO-101 serial port is a device path, for example /dev/ttyACM0.")
        if complete and (self.port is None or set(self.roles) != set(ROLES)):
            raise ValueError("Set the SO-101 serial port and its side and wrist cameras.")
        return self

    def to_dict(self) -> dict:
        value = self.rig_dict()
        if self.port is not None:
            value["port"] = self.port
        if self.calibration_path is not None:
            value["calibration_path"] = self.calibration_path
        if self.gripper_range is not None:
            value["gripper_range"] = list(self.gripper_range)
        return value

    @classmethod
    def from_dict(cls, value) -> So101Config:
        if not isinstance(value, dict) or set(value) - {
            "version", "cameras", "roles", "home_pose", "port", "calibration_path", "gripper_range",
        }:
            raise ValueError("Invalid SO-101 configuration fields.")
        try:
            fields = cls.rig_fields(value)
            if isinstance(fields["home_pose"], list):
                fields["home_pose"] = tuple(fields["home_pose"])
            return cls(
                **fields,
                port=value.get("port"),
                calibration_path=value.get("calibration_path"),
                gripper_range=value.get("gripper_range"),
            ).validate()
        except (TypeError, KeyError, AttributeError) as exc:
            raise ValueError("Invalid port, camera or home entry in the SO-101 rig file.") from exc


def from_legacy(legacy, *, resolve=camera_for_index) -> So101Config:
    """The rig file config.toml's pre-rig-file keys describe. A saved camera index that
    no longer resolves (unplugged, or no stable identity) is left unmapped for setup."""
    cameras, roles = [], {}
    for role, index in (("side", legacy.camera_index), ("wrist", legacy.wrist_camera_index)):
        spec = resolve(int(index)) if index is not None else None
        if spec is None or any(c.physical_id == spec.physical_id for c in cameras):
            continue
        cameras.append(spec)
        roles[role] = spec.id
    home = legacy.home_position
    return So101Config(
        cameras=cameras, roles=roles, port=legacy.robot_port,
        calibration_path=legacy.calibration_path,
        home_pose=tuple(float(v) for v in home) if home is not None else None,
        # Only when config.toml held something to move; a fresh rig starts empty.
        migrated=bool(cameras or legacy.robot_port or home is not None),
    )


def load_config(path: Path | None = None, *, legacy=None) -> So101Config:
    """so101.json, else the rig config.toml's legacy keys describe (not saved)."""
    value = read_rig_file(path or default_config_path())
    if value is not None:
        return So101Config.from_dict(value)
    if legacy is None:
        from dreamscale.config import load_legacy_robot

        legacy = load_legacy_robot()
    return from_legacy(legacy)


def save_config(config: So101Config, path: Path | None = None) -> None:
    config.validate()
    write_rig_file(config.to_dict(), path or default_config_path())

