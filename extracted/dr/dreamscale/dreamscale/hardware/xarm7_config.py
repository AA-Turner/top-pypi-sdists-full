"""The bimanual xArm 7 rig file: each arm's controller address and gripper, and which camera
plays each role.

The two arms are named for where they sit on the bench, aft and fore, as recordings on these
rigs name them. Joint limits come from the arm; only what a computer can't measure lives here.
With no home pose, a run starts from wherever the arms are.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import ClassVar

from .rig_file import RigFile, read_rig_file, rig_file_path, write_rig_file
from .xarm_arm import GRIPPER_CONTROLS, GRIPPER_TYPES, JOINTS

ARMS = ("aft", "fore")
# A scene camera above the bench, then the fore and aft wrists, in wire order.
ROLES = ("top", "left", "right")
_HOST = re.compile(r"[A-Za-z0-9]([A-Za-z0-9.-]{0,251}[A-Za-z0-9])?")

DEFAULT_CONFIG_PATH = rig_file_path("xarm7")


@dataclass(frozen=True)
class ArmConfig:
    host: str
    gripper: str = "g2"
    # How a close intent drives the jaw: "position" (that fraction of its travel) or
    # "threshold" (shut at 0.5 or more, open below).
    gripper_control: str = "position"

    def __post_init__(self):
        if not isinstance(self.host, str) or not _HOST.fullmatch(self.host):
            raise ValueError("Arm host is the control box's address, for example 192.168.1.201.")
        if self.gripper not in GRIPPER_TYPES:
            raise ValueError(f"Gripper type must be one of {', '.join(GRIPPER_TYPES)}.")
        if self.gripper_control not in GRIPPER_CONTROLS:
            raise ValueError(
                f"Gripper control must be one of {', '.join(GRIPPER_CONTROLS)}."
            )


@dataclass
class XArm7Config(RigFile):
    arms: dict[str, ArmConfig] = field(default_factory=dict)
    version: int = 1
    home_pose: tuple[float, ...] | None = None

    ROLES: ClassVar[tuple[str, ...]] = ROLES
    LABEL: ClassVar[str] = "xArm 7"
    HOME_SIZE: ClassVar[int] = JOINTS * len(ARMS)
    HOME_HELP: ClassVar[str] = "finite joint positions in radians, aft arm first"

    def validate(self, *, complete: bool = False) -> XArm7Config:
        self.validate_rig()
        if not set(self.arms) <= set(ARMS):
            raise ValueError("Arms are named aft and fore.")
        hosts = [arm.host for arm in self.arms.values()]
        if len(set(hosts)) != len(hosts):
            raise ValueError("Each arm needs its own control box address.")
        if complete and set(self.arms) != set(ARMS):
            raise ValueError("Set both arms' addresses (aft and fore).")
        return self

    def to_dict(self) -> dict:
        value = self.rig_dict()
        value["arms"] = {name: asdict(self.arms[name]) for name in ARMS if name in self.arms}
        return value

    @classmethod
    def from_dict(cls, value) -> XArm7Config:
        if not isinstance(value, dict) or set(value) - {
            "version", "cameras", "roles", "home_pose", "arms",
        }:
            raise ValueError("Invalid xArm 7 configuration fields.")
        try:
            return cls(
                **cls.rig_fields(value),
                arms={name: ArmConfig(**arm) for name, arm in value.get("arms", {}).items()},
            ).validate()
        except (TypeError, KeyError, AttributeError) as exc:
            raise ValueError("Invalid arm or camera entry in the rig file.") from exc


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> XArm7Config:
    value = read_rig_file(path)
    return XArm7Config.from_dict(value) if value is not None else XArm7Config()


def save_config(config: XArm7Config, path: Path = DEFAULT_CONFIG_PATH) -> None:
    config.validate()
    write_rig_file(config.to_dict(), path)
