"""A Verne V0.5 deployment's server-described contract (dreamscale_transport.verne_v05_deploy).

Verne V0.5 reads and predicts end-effector poses, both arms in one robot frame: each request
carries the pose state (per arm: xyz in metres, rotation-matrix rows 0 and 1, the jaw opening
0-1) now and one executed step before, the instruction, and one 256x256 tile per camera. The
server keeps the episode's memory: the frames of every 4th executed step are sent ahead
(``context.EpisodeTicks``). Each chunk row is the poses of the arms and the instruction's
progress, absolute in the robot frame; the robot side turns them into joint targets.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dreamscale_transport.images import STRETCH_256_OPENCV
from dreamscale_transport.verne_v05_deploy import (
    ACTION_HORIZON,
    ACTION_HZ,
    ARM_ORDER,
    CAMERAS,
    MAX_EXECUTED_ACTIONS,
    MAX_TRAINED_RTC_DELAY,
    MIN_EXECUTED_ACTIONS,
    MIN_REPLAN_STEPS,
    POSE_WIDTH,
    PRESET,
    PRESETS,
    SINGLE_ARM,
    TICK_STEPS,
    TRAINED_RTC_CONTRACT,
    VERNE_V05_BASE_MODEL,
    VERNE_V05_SOURCE_FORMAT,
    VerneV05Camera,
    gripper_indices,
    jaw,
    raw_gripper,
)


@dataclass(frozen=True)
class VerneV05SessionDeployment:
    id: str
    preset: str
    cameras: tuple[VerneV05Camera, ...]
    arms: tuple[str, ...]
    state_dim: int
    action_dim: int
    action_horizon: int
    executed_actions: int
    action_hz: float
    action_space: str
    trained_rtc_max_delay: int
    rtc_method: str
    rtc_max_delay: int | None
    # The fine-tune's gripper per arm in the robot's own units, [closed, open]; None: 0-1.
    gripper_range: tuple[tuple[float, float], ...] | None = None
    # The frame the robot's poses must be in (the fine-tune's training); None: the release's.
    ee_frame: str | None = None
    # No joint layout of its own: the robot side owns kinematics.
    layout: None = None
    robot: None = None
    joints: bool = False

    @property
    def camera_keys(self) -> tuple[str, ...]:
        return tuple(camera.key for camera in self.cameras)

    def jaw(self, arm: int, raw: float) -> float:
        """Arm ``arm``'s gripper reading as the wire's jaw (0 closed, 1 open), by the
        deployment's gripper range (the one its fine-tune trained with)."""
        return jaw(self.gripper_range[arm] if self.gripper_range else None, raw)

    def raw_gripper(self, arm: int, value: float) -> float:
        """Arm ``arm``'s returned jaw (0 closed, 1 open) in your gripper's units."""
        return raw_gripper(self.gripper_range[arm] if self.gripper_range else None, value)

    @classmethod
    def from_json(cls, data: Any) -> VerneV05SessionDeployment:
        """Strict on what it reads, tolerant of fields it doesn't."""
        if not isinstance(data, dict) or data.get("base_model") != VERNE_V05_BASE_MODEL:
            raise ValueError("the server returned no Verne V0.5 deployment contract")
        try:
            result = cls(
                **{key: data[key] for key in (
                    "id", "preset", "state_dim", "action_dim", "action_horizon",
                    "executed_actions", "action_hz", "action_space", "trained_rtc_max_delay",
                    "rtc_method",
                )},
                cameras=tuple(VerneV05Camera.model_validate(camera)
                              for camera in data["cameras"]),
                arms=tuple(data["arms"]),
                rtc_max_delay=data.get("rtc_max_delay"),
                gripper_range=(tuple(tuple(float(v) for v in span)
                                     for span in data["gripper_range"])
                               if data.get("gripper_range") is not None else None),
                ee_frame=data.get("ee_frame"),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("incomplete Verne V0.5 deployment contract") from error
        trained = result.trained_rtc_max_delay
        features = [camera.feature for camera in result.cameras]
        memory = data.get("memory") or {}
        if (
            data.get("source_format", VERNE_V05_SOURCE_FORMAT) != VERNE_V05_SOURCE_FORMAT
            or not isinstance(result.id, str) or not result.id
            or result.preset not in PRESETS
            or result.arms not in (ARM_ORDER, SINGLE_ARM)
            or result.state_dim != POSE_WIDTH * len(result.arms)
            or result.action_dim != POSE_WIDTH * len(result.arms) + 1
            or result.action_horizon != ACTION_HORIZON
            or type(result.executed_actions) is not int
            or not MIN_EXECUTED_ACTIONS <= result.executed_actions <= MAX_EXECUTED_ACTIONS
            or isinstance(result.action_hz, bool)
            or not isinstance(result.action_hz, int | float)
            or result.action_hz != ACTION_HZ
            or result.action_space != "model_defined"
            or data.get("rotation_6d", "rows") != "rows"
            or list(data.get("gripper_indices", gripper_indices(result.arms)))
            != list(gripper_indices(result.arms))
            or memory.get("tick_steps", TICK_STEPS) != TICK_STEPS
            or type(trained) is not int or not 0 <= trained <= MAX_TRAINED_RTC_DELAY
            or not features or features != sorted(set(features))
            or len(set(result.camera_keys)) != len(result.cameras)
            or (result.arms == SINGLE_ARM and "camera_0" in features)
        ):
            raise ValueError("invalid Verne V0.5 deployment shape or action contract")
        if result.preset == PRESET and (
            tuple((camera.key, camera.feature) for camera in result.cameras) != CAMERAS
            or result.arms != ARM_ORDER
        ):
            raise ValueError("the server's bimanual YAM Verne V0.5 deployment isn't the YAM wire")
        if result.rtc_method == "off":
            if result.rtc_max_delay is not None:
                raise ValueError("a Verne V0.5 deployment with RTC off has no prefix cap")
        elif result.rtc_method != "trained" or (
            type(result.rtc_max_delay) is not int
            or not 1 <= result.rtc_max_delay <= trained
        ):
            raise ValueError(
                f"the server returned an unknown RTC setting {result.rtc_method!r} for this "
                "Verne V0.5 deployment"
            )
        return result


def runtime_contract(resolved, deployment):
    from dreamscale.policy.runtime.contract import RuntimeContract, _optional_attr

    if not isinstance(deployment, VerneV05SessionDeployment):
        deployment = VerneV05SessionDeployment.from_json(deployment)
    trained = deployment.rtc_method == "trained"
    # Pose rows: the robot waits for each chunk rather than holding a joint position.
    hold = "wait"
    expected = {
        "backend": "pytorch",
        "rtc": "on" if trained else "off",
        "rtc_contract": TRAINED_RTC_CONTRACT if trained else None,
        "action_hz": deployment.action_hz,
        "chunk_size": deployment.executed_actions,
        "action_dim": deployment.action_dim,
        "action_space": deployment.action_space,
        "hold_behavior": hold,
    }
    if any(_optional_attr(resolved, key) != value for key, value in expected.items()):
        raise ValueError("Verne V0.5 runtime differs from the deployment's sealed contract")
    return RuntimeContract(
        action_hz=float(deployment.action_hz),
        chunk_size=deployment.executed_actions,
        action_dim=deployment.action_dim,
        action_space=deployment.action_space,
        hold_behavior=hold,
        fixed_rate=True,
        execution_horizon=deployment.executed_actions,
        wire_image=STRETCH_256_OPENCV,
        episode_tick_steps=TICK_STEPS,
        min_replan_steps=min(MIN_REPLAN_STEPS, deployment.executed_actions - 1),
    )
