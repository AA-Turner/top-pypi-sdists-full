"""The Universal Robots rig file: the arm's model and address, its gripper, and which
camera plays each role.

Joint limits come from the arm model and the gripper is probed; only what a computer
can't measure lives here. With no home pose, a run starts from wherever the arm is.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import ClassVar

from .rig_file import RigFile, read_rig_file, rig_file_path, write_rig_file
from .ur_arm import ARM_MODELS, DEFAULT_PROGRAM

# π0.5's UR5e data: an over-the-shoulder scene camera and a wrist camera, in wire order.
ROLES = ("scene", "wrist")
GRIPPER_LABELS = {
    "robotiq_2f85": "Robotiq 2F-85", "robotiq_2f140": "Robotiq 2F-140",
    "robotiq_hande": "Robotiq Hand-E", "none": "None",
}
GRIPPER_TYPES = tuple(GRIPPER_LABELS)
_HOST = re.compile(r"[A-Za-z0-9]([A-Za-z0-9.-]{0,251}[A-Za-z0-9])?")

DEFAULT_CONFIG_PATH = rig_file_path("ur")


@dataclass(frozen=True)
class ArmConfig:
    host: str
    model: str = "ur7e"
    # The pendant program with the External Control node; in Remote control it is played
    # from this computer.
    program: str = DEFAULT_PROGRAM

    def __post_init__(self):
        if self.model not in ARM_MODELS:
            raise ValueError(f"Arm model must be one of {', '.join(ARM_MODELS)}.")
        if not isinstance(self.host, str) or not _HOST.fullmatch(self.host):
            raise ValueError("Arm host is the control box's address, for example 192.168.100.10.")
        if not isinstance(self.program, str) or not self.program.strip():
            raise ValueError("Arm program is the pendant program's name, for example dreamscale.")


@dataclass(frozen=True)
class GripperConfig:
    type: str = "robotiq_2f85"

    def __post_init__(self):
        if self.type not in GRIPPER_TYPES:
            raise ValueError(f"Gripper type must be one of {', '.join(GRIPPER_TYPES)}.")


@dataclass
class URConfig(RigFile):
    arm: ArmConfig | None = None
    gripper: GripperConfig = field(default_factory=GripperConfig)
    version: int = 1
    home_pose: tuple[float, ...] | None = None

    ROLES: ClassVar[tuple[str, ...]] = ROLES
    LABEL: ClassVar[str] = "Universal Robots"
    HOME_SIZE: ClassVar[int] = 6
    HOME_HELP: ClassVar[str] = "finite joint positions in radians"

    def validate(self, *, complete: bool = False) -> URConfig:
        self.validate_rig()
        if complete and self.arm is None:
            raise ValueError("Set the arm's address.")
        return self

    def to_dict(self) -> dict:
        value = self.rig_dict()
        if self.arm is not None:
            value["arm"] = asdict(self.arm)
        value["gripper"] = asdict(self.gripper)
        return value

    @classmethod
    def from_dict(cls, value) -> URConfig:
        if not isinstance(value, dict) or set(value) - {
            "version", "cameras", "roles", "home_pose", "arm", "gripper",
        }:
            raise ValueError("Invalid Universal Robots configuration fields.")
        try:
            arm = value.get("arm")
            return cls(
                **cls.rig_fields(value),
                arm=ArmConfig(**arm) if arm is not None else None,
                gripper=GripperConfig(**value.get("gripper", {})),
            ).validate()
        except (TypeError, KeyError, AttributeError) as exc:
            raise ValueError("Invalid arm, gripper or camera entry in the rig file.") from exc


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> URConfig:
    value = read_rig_file(path)
    return URConfig.from_dict(value) if value is not None else URConfig()


def save_config(config: URConfig, path: Path = DEFAULT_CONFIG_PATH) -> None:
    config.validate()
    write_rig_file(config.to_dict(), path)
