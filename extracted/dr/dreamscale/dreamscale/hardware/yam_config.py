"""Explicit, resumable YAM rig configuration, separate from legacy Jay files."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import ClassVar

from .rig_file import RigFile, read_rig_file, write_rig_file

ROLES = ("top", "left", "right")
ARM_TYPES = ("YAM", "YAM_PRO", "YAM_ULTRA", "BIG_YAM")
GRIPPER_TYPES = ("CRANK_4310", "LINEAR_3507", "LINEAR_4310", "FLEXIBLE_4310")
# MolmoAct2 research kit joint-mode home (inspect-robots-yam 0.36.0):
# encoder-zero arm joints, normalized open grippers, left then right.
DEFAULT_HOME_POSE = (0.0,) * 6 + (1.0,) + (0.0,) * 6 + (1.0,)


def default_config_path() -> Path:
    """The rig file: ~/.config/dreamscale/yam.json, or a pre-rename one used in place."""
    home = Path.home()
    new = home / ".config/dreamscale/yam.json"
    legacy = home / ".config/dropbear/yam.json"
    return legacy if not new.exists() and legacy.exists() else new


DEFAULT_CONFIG_PATH = default_config_path()


@dataclass(frozen=True)
class ArmConfig:
    can_interface: str
    arm_type: str
    gripper_type: str
    joint_count: int = 6
    # The USB adapter this arm is pinned to; its kernel name can change on reboot.
    adapter_id: str | None = None

    def __post_init__(self):
        if not re.fullmatch(r"[A-Za-z0-9_.-]{1,15}", self.can_interface):
            raise ValueError("Choose an explicit CAN interface, for example can0.")
        if self.adapter_id is not None and not re.fullmatch(
            r"usb(-port)?:[A-Za-z0-9_.:-]{1,200}", str(self.adapter_id)
        ):
            raise ValueError("A CAN adapter identity looks like usb:<vendor>:<serial>.")
        if self.arm_type not in ARM_TYPES or self.gripper_type not in GRIPPER_TYPES:
            raise ValueError("Select a supported six-joint YAM arm and normalized gripper.")
        if type(self.joint_count) is not int or self.joint_count != 6:
            raise ValueError("Molmo requires six joints per arm plus a gripper.")


@dataclass
class YamConfig(RigFile):
    arms: dict[str, ArmConfig] = field(default_factory=dict)
    version: int = 1
    home_pose: tuple[float, ...] | None = None

    ROLES: ClassVar[tuple[str, ...]] = ROLES
    LABEL: ClassVar[str] = "YAM"
    HOME_SIZE: ClassVar[int] = 14
    HOME_HELP: ClassVar[str] = "finite values: six radians and a 0–1 gripper per arm"

    def _check_home(self, pose) -> bool:
        return all(0 <= pose[i] <= 1 for i in (6, 13))

    def validate(self, *, complete=False):
        self.validate_rig()
        if not set(self.arms) <= {"left", "right"}:
            raise ValueError("Arm mappings must be left or right.")
        if len({a.can_interface for a in self.arms.values()}) != len(self.arms):
            raise ValueError("Left and right arms require different CAN interfaces.")
        pinned = [a.adapter_id for a in self.arms.values() if a.adapter_id]
        if len(set(pinned)) != len(pinned):
            raise ValueError("Left and right arms require different CAN adapters.")
        if complete and (set(self.roles) != set(ROLES) or set(self.arms) != {"left", "right"}):
            raise ValueError(
                "Assign top, left and right cameras and both CAN arm/gripper mappings."
            )
        return self

    def to_dict(self):
        value = self.rig_dict()
        value["arms"] = {}
        for side, arm in self.arms.items():
            value["arms"][side] = asdict(arm)
            if arm.adapter_id is None:
                value["arms"][side].pop("adapter_id")
        return value

    @classmethod
    def from_dict(cls, value):
        if not isinstance(value, dict) or set(value) - {
            "version",
            "cameras",
            "roles",
            "arms",
            "home_pose",
        }:
            raise ValueError("Invalid YAM configuration fields.")
        try:
            return cls(
                **cls.rig_fields(value),
                arms={side: ArmConfig(**arm) for side, arm in value.get("arms", {}).items()},
            ).validate()
        except (TypeError, KeyError, AttributeError) as exc:
            raise ValueError("Invalid camera or arm configuration.") from exc


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> YamConfig:
    value = read_rig_file(path)
    return YamConfig.from_dict(value) if value is not None else YamConfig()


def save_config(config: YamConfig, path: Path = DEFAULT_CONFIG_PATH) -> None:
    config.validate()
    write_rig_file(config.to_dict(), path)
