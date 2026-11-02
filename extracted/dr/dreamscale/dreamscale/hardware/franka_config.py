"""The Franka rig file: which arm, which gripper, and which camera plays each role.

Only what a computer can't measure lives here. Joint limits come from the arm model,
the FCI protocol version and gripper width are probed, and models name the camera roles
they need (Embodiment.model_cameras).
"""

from __future__ import annotations

import math
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import ClassVar

from .rig_file import RigFile, read_rig_file, rig_file_path, write_rig_file

# DROID's own camera slots, in wire order.
ROLES = ("exterior_1", "exterior_2", "wrist")
ARM_MODELS = ("fr3", "panda")
GRIPPER_TYPES = ("franka_hand", "robotiq_2f85", "none")
# DROID's RobotEnv.reset_joints: the pose DROID policies start every episode from.
DROID_HOME = (0.0, -math.pi / 5, 0.0, -4 * math.pi / 5, 0.0, 3 * math.pi / 5, 0.0)
_HOST = re.compile(r"[A-Za-z0-9]([A-Za-z0-9.-]{0,251}[A-Za-z0-9])?")

DEFAULT_CONFIG_PATH = rig_file_path("franka")


@dataclass(frozen=True)
class ArmConfig:
    model: str
    host: str

    def __post_init__(self):
        if self.model not in ARM_MODELS:
            raise ValueError(f"Arm model must be one of {', '.join(ARM_MODELS)}.")
        if not isinstance(self.host, str) or not _HOST.fullmatch(self.host):
            raise ValueError("Arm host is the robot's FCI address, for example 172.16.0.2.")


@dataclass(frozen=True)
class GripperConfig:
    type: str = "franka_hand"

    def __post_init__(self):
        if self.type not in GRIPPER_TYPES:
            raise ValueError(f"Gripper type must be one of {', '.join(GRIPPER_TYPES)}.")


@dataclass
class FrankaConfig(RigFile):
    arm: ArmConfig | None = None
    gripper: GripperConfig = field(default_factory=GripperConfig)
    version: int = 1
    home_pose: tuple[float, ...] | None = None

    ROLES: ClassVar[tuple[str, ...]] = ROLES
    LABEL: ClassVar[str] = "Franka"
    HOME_SIZE: ClassVar[int] = 7
    HOME_HELP: ClassVar[str] = "finite joint positions in radians"

    @property
    def home(self) -> tuple[float, ...]:
        """The configured home pose, or DROID's reset pose."""
        return tuple(self.home_pose) if self.home_pose is not None else DROID_HOME

    def validate(self, *, complete: bool = False) -> FrankaConfig:
        self.validate_rig()
        if complete and self.arm is None:
            raise ValueError("Set the arm's model and FCI address.")
        return self

    def to_dict(self) -> dict:
        value = self.rig_dict()
        if self.arm is not None:
            value["arm"] = asdict(self.arm)
        value["gripper"] = asdict(self.gripper)
        return value

    @classmethod
    def from_dict(cls, value) -> FrankaConfig:
        if not isinstance(value, dict) or set(value) - {
            "version", "cameras", "roles", "home_pose", "arm", "gripper",
        }:
            raise ValueError("Invalid Franka configuration fields.")
        try:
            arm = value.get("arm")
            return cls(
                **cls.rig_fields(value),
                arm=ArmConfig(**arm) if arm is not None else None,
                gripper=GripperConfig(**value.get("gripper", {})),
            ).validate()
        except (TypeError, KeyError, AttributeError) as exc:
            raise ValueError("Invalid arm, gripper or camera entry in the rig file.") from exc


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> FrankaConfig:
    value = read_rig_file(path)
    return FrankaConfig.from_dict(value) if value is not None else FrankaConfig()


def save_config(config: FrankaConfig, path: Path = DEFAULT_CONFIG_PATH) -> None:
    config.validate()
    write_rig_file(config.to_dict(), path)
