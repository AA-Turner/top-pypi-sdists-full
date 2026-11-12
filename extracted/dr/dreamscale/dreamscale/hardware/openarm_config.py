"""The OpenARM rig file: which arms the model drives, where each arm's gripper sits in the
model's vector, and which of the cell's cameras the model reads.

An Anvil OpenARM runs from its Devbox, whose control stack owns the motors and the cameras;
this file only says how a model's recording was laid out. The layout follows the recording:
the arms in the model's order, each arm's seven joints in order with the gripper before or
after them. Joint limits come from the stack.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from pathlib import Path

from .rig_file import read_rig_file, rig_file_path, write_rig_file

ARMS = ("left", "right")
JOINTS = 7
ARM_SIZE = JOINTS + 1
# The cell's four camera modules, as its recordings name them.
CAMERAS = ("waist", "chest", "wrist_l", "wrist_r")
GRIPPER_PLACES = ("first", "last")
DEFAULT_URL = "ws://localhost:9090"
DEFAULT_CONFIG_PATH = rig_file_path("openarm")
SETUP = "dreamscale robots openarm setup"
_FIELDS = {"version", "url", "arms", "gripper", "cameras", "home_pose"}


@dataclass
class OpenArmConfig:
    arms: tuple[str, ...] = ()
    cameras: tuple[str, ...] = ()
    # Where each arm's gripper sits among its eight values: Anvil's converter writes it first.
    gripper: str = "first"
    url: str = DEFAULT_URL
    version: int = 1
    # Seven joint positions per arm, in the arms' order; grippers stay as they are.
    home_pose: tuple[float, ...] | None = None

    @property
    def roles(self) -> dict[str, str]:
        """The cameras by role, as other rig files map them (here a role is its camera)."""
        return {camera: camera for camera in self.cameras}

    @property
    def width(self) -> int:
        return ARM_SIZE * len(self.arms)

    def validate(self, *, complete: bool = False) -> OpenArmConfig:
        if type(self.version) is not int or self.version != 1:
            raise ValueError("Unsupported OpenARM configuration version.")
        if not isinstance(self.url, str) or not self.url.startswith(("ws://", "wss://")):
            raise ValueError(f"The stack's address is a rosbridge URL, for example {DEFAULT_URL}.")
        arms, cameras = tuple(self.arms), tuple(self.cameras)
        if not set(arms) <= set(ARMS) or len(set(arms)) != len(arms):
            raise ValueError("Arms are left and right, each at most once.")
        if not set(cameras) <= set(CAMERAS) or len(set(cameras)) != len(cameras):
            raise ValueError(f"Cameras are {', '.join(CAMERAS)}, each at most once.")
        if self.gripper not in GRIPPER_PLACES:
            raise ValueError("Gripper is first or last: where it sits in each arm's values.")
        pose = self.home_pose
        if pose is not None and (
            not isinstance(pose, (tuple, list))
            or len(pose) != JOINTS * len(arms)
            or any(type(v) not in (int, float) or not math.isfinite(v) for v in pose)
        ):
            raise ValueError(
                f"Home pose needs {JOINTS * len(arms)} finite joint positions in radians, "
                "seven per arm."
            )
        if complete and not arms:
            raise ValueError(f"No arms chosen yet. Run {SETUP}.")
        if complete and not cameras:
            raise ValueError(f"No cameras chosen yet. Run {SETUP}.")
        return self

    def to_dict(self) -> dict:
        value = {
            "version": self.version, "url": self.url, "arms": list(self.arms),
            "gripper": self.gripper, "cameras": list(self.cameras),
        }
        if self.home_pose is not None:
            value["home_pose"] = list(self.home_pose)
        return value

    @classmethod
    def from_dict(cls, value) -> OpenArmConfig:
        if not isinstance(value, dict) or set(value) - _FIELDS:
            raise ValueError("Invalid OpenARM configuration fields.")
        pose = value.get("home_pose")
        try:
            return cls(
                arms=tuple(value.get("arms", ())), cameras=tuple(value.get("cameras", ())),
                gripper=value.get("gripper", "first"), url=value.get("url", DEFAULT_URL),
                version=value.get("version", 1),
                home_pose=tuple(pose) if isinstance(pose, list) else pose,
            ).validate()
        except TypeError as exc:
            raise ValueError("Invalid arm or camera entry in the rig file.") from exc


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> OpenArmConfig:
    value = read_rig_file(path)
    return OpenArmConfig.from_dict(value) if value is not None else OpenArmConfig()


def save_config(config: OpenArmConfig, path: Path = DEFAULT_CONFIG_PATH) -> None:
    config.validate()
    write_rig_file(config.to_dict(), path)


def embodiment_for(config: OpenArmConfig):
    """The OpenARM descriptor for one rig: its arms, its cameras and its gripper place."""
    from dreamscale.embodiments import OPENARM

    joints = tuple(f"joint_{i}" for i in range(1, JOINTS + 1))
    values = ("gripper", *joints) if config.gripper == "first" else (*joints, "gripper")
    return replace(
        OPENARM,
        arms=tuple(arm.title() for arm in config.arms),
        joints=tuple(f"{arm}_{value}" for arm in config.arms for value in values),
        camera_roles=tuple(camera for camera in CAMERAS if camera in config.cameras),
        gripper_first=config.gripper == "first",
    )
