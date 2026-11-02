"""A Hy-VLA deployment's server-described contract (dreamscale_transport.hy_vla_deploy).

Hy-VLA predicts end-effector poses: each request carries a 20-value pose state (per arm, the
model's order: TCP xyz, rotation-matrix rows 0-1, gripper 0-1), the instruction, and per
camera one strip of the frames at 25, 20, 15, 10 and 5 executed ticks back that exist, then
the current one (``context.TickHistory``; the server fills missing older frames with
black). Each chunk row is 40 values: the poses of both arms relative to the request's state
(values 0-19), then absolute in each arm's base frame (values 20-39). The robot side turns
those into joint targets; this module never sees joints.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
from dreamscale_transport.hy_vla_deploy import (
    ACTION_DIM,
    ACTION_HORIZON,
    ACTION_HZ,
    CAMERA_FEATURES,
    DENOISING_STEPS,
    HISTORY_OFFSETS,
    HY_VLA_BASE_MODEL,
    HY_VLA_SOURCE_FORMAT,
    IMAGE_SIZE,
    MAX_INSTRUCTION_CHARS,
    MAX_INSTRUCTION_TOKENS,
    MAX_LABELS,
    MAX_TRAINED_RTC_DELAY,
    POSE_WIDTH,
    PRESETS,
    STATE_DIM,
    TRAINED_RTC_CONTRACT,
    XARM7_ARMS,
    XARM7_CAMERAS,
    XARM7_PRESET,
    HyVlaCamera,
    clean_instruction,
)
from dreamscale_transport.images import WireImage

# The model's 224x224 canvas, letterboxed as Rodeo trained it (ImageOps.pad of 1280x720 frames).
WIRE_IMAGE = WireImage(IMAGE_SIZE, IMAGE_SIZE, mode="letterbox", resample="bilinear", quality=90)


@dataclass(frozen=True)
class HyVlaSessionDeployment:
    id: str
    preset: str
    cameras: tuple[HyVlaCamera, ...]
    arms: tuple[str, str]
    label_arm_pairs: tuple[tuple[str, str], ...]
    state_dim: int
    action_dim: int
    action_horizon: int
    executed_actions: int
    action_hz: float
    action_space: str
    history_offsets: tuple[int, ...]
    trained_rtc_max_delay: int
    rtc_method: str
    rtc_max_delay: int | None
    step: int | None = None
    # No joint layout of its own: the robot side owns kinematics.
    layout: None = None
    robot: None = None
    joints: bool = False

    @property
    def camera_keys(self) -> tuple[str, ...]:
        return tuple(camera.key for camera in self.cameras)

    @property
    def label_arms(self) -> dict[str, str]:
        """Which arm each trained instruction (cleaned) moves."""
        return dict(self.label_arm_pairs)

    def arm_for(self, instruction: str) -> str | None:
        """The arm a trained instruction moves, or None for one it wasn't trained on (the
        lookup cleans it as the model does: stripped, underscores as spaces)."""
        return self.label_arms.get(clean_instruction(instruction))

    @classmethod
    def from_json(cls, data: Any) -> HyVlaSessionDeployment:
        """Strict on what it reads, tolerant of fields it doesn't (as ABC-VLA's)."""
        if not isinstance(data, dict) or data.get("base_model") != HY_VLA_BASE_MODEL:
            raise ValueError("the server returned no Hy-VLA deployment contract")
        try:
            result = cls(
                **{key: data[key] for key in (
                    "id", "preset", "state_dim", "action_dim", "action_horizon",
                    "executed_actions", "action_hz", "action_space", "trained_rtc_max_delay",
                    "rtc_method",
                )},
                cameras=tuple(HyVlaCamera.model_validate(camera) for camera in data["cameras"]),
                arms=tuple(data["arms"]),
                label_arm_pairs=tuple(
                    (label, arm) for label, arm in (data.get("label_arms") or ())
                ),
                history_offsets=tuple(data["history_offsets"]),
                rtc_max_delay=data.get("rtc_max_delay"),
                step=data.get("step"),
            )
        except (KeyError, TypeError, ValueError) as error:
            raise ValueError("incomplete Hy-VLA deployment contract") from error
        trained = result.trained_rtc_max_delay
        labels = [label for label, _ in result.label_arm_pairs]
        if (
            data.get("source_format", HY_VLA_SOURCE_FORMAT) != HY_VLA_SOURCE_FORMAT
            or not isinstance(result.id, str) or not result.id
            or result.preset not in PRESETS
            or any(type(value) is not int or value != expected for value, expected in (
                (result.state_dim, STATE_DIM), (result.action_dim, ACTION_DIM),
                (result.action_horizon, ACTION_HORIZON),
            ))
            or type(result.executed_actions) is not int
            or not 1 <= result.executed_actions <= ACTION_HORIZON
            or isinstance(result.action_hz, bool)
            or not isinstance(result.action_hz, int | float)
            or result.action_hz != ACTION_HZ
            or result.action_space != "model_defined"
            or result.history_offsets != HISTORY_OFFSETS
            or data.get("history_padding", "black") != "black"
            or data.get("image_size", IMAGE_SIZE) != IMAGE_SIZE
            or data.get("max_instruction_tokens", MAX_INSTRUCTION_TOKENS) != MAX_INSTRUCTION_TOKENS
            or data.get("denoising_steps", DENOISING_STEPS) != DENOISING_STEPS
            or type(trained) is not int or not 0 <= trained <= MAX_TRAINED_RTC_DELAY
            or (result.step is not None and (type(result.step) is not int or result.step < 0))
            or tuple(camera.feature for camera in result.cameras) != CAMERA_FEATURES
            or len(set(result.camera_keys)) != len(result.cameras)
            or len(result.arms) != 2 or len(set(result.arms)) != 2
            or not all(isinstance(arm, str) and arm for arm in result.arms)
            or len(result.label_arm_pairs) > MAX_LABELS
            or labels != sorted(set(labels))
            or any(
                not isinstance(label, str) or not label or label != clean_instruction(label)
                or len(label) > MAX_INSTRUCTION_CHARS or arm not in result.arms
                for label, arm in result.label_arm_pairs
            )
        ):
            raise ValueError("invalid Hy-VLA deployment shape or action contract")
        if result.preset == XARM7_PRESET and (
            tuple((camera.key, camera.feature) for camera in result.cameras) != XARM7_CAMERAS
            or result.arms != XARM7_ARMS
        ):
            raise ValueError(
                "the server's bimanual xArm 7 Hy-VLA deployment isn't the xArm 7 wire"
            )
        if result.rtc_method == "off":
            if result.rtc_max_delay is not None:
                raise ValueError("a Hy-VLA deployment with RTC off has no prefix cap")
        elif result.rtc_method != "trained" or (
            type(result.rtc_max_delay) is not int
            or not 1 <= result.rtc_max_delay <= trained
        ):
            raise ValueError(
                f"the server returned an unknown RTC setting {result.rtc_method!r} for this "
                "Hy-VLA deployment"
            )
        return result

    def express_committed(
        self, rows: list[list[float]], state: list[float]
    ) -> list[list[float]]:
        """Committed rows re-expressed against a request's ``state``: each row's relative
        half (values 0-19) recomputed from its absolute half (values 20-39), the poses in
        each arm's base frame, so a row planned against an earlier chunk's state reads as
        the same physical pose against this one (trained RTC's prefix contract)."""
        if not rows:
            return rows
        values = np.asarray(rows, dtype=np.float64)
        anchors = np.asarray(state, dtype=np.float64)
        if values.ndim != 2 or values.shape[1] != ACTION_DIM or anchors.shape != (STATE_DIM,):
            return rows  # the wire check refuses it, naming the shape
        out = values.copy()
        for arm in range(2):
            span = slice(arm * POSE_WIDTH, (arm + 1) * POSE_WIDTH)
            anchor = _decode(anchors[span][None])[0]
            target = _decode(values[:, STATE_DIM:][:, span])
            relative = np.linalg.inv(anchor)[None] @ target
            out[:, span] = _encode(relative, values[:, STATE_DIM + arm * POSE_WIDTH + 9])
        return out.tolist()


def _decode(vectors: np.ndarray) -> np.ndarray:
    """Pose vectors (xyz, rotation rows 0-1, gripper) as 4x4 transforms (rows
    Gram-Schmidt orthonormalized, row 2 their cross product)."""
    a, b = vectors[:, 3:6], vectors[:, 6:9]
    a = a / np.maximum(np.linalg.norm(a, axis=-1, keepdims=True), 1e-12)
    b = b - np.sum(a * b, axis=-1, keepdims=True) * a
    b = b / np.maximum(np.linalg.norm(b, axis=-1, keepdims=True), 1e-12)
    result = np.broadcast_to(np.eye(4), (len(vectors), 4, 4)).copy()
    result[:, :3, :3] = np.stack([a, b, np.cross(a, b)], axis=-2)
    result[:, :3, 3] = vectors[:, :3]
    return result


def _encode(transforms: np.ndarray, gripper: np.ndarray) -> np.ndarray:
    return np.concatenate(
        [transforms[:, :3, 3], transforms[:, :2, :3].reshape(len(transforms), 6),
         gripper[:, None]], axis=-1,
    )


def runtime_contract(resolved, deployment):
    from dreamscale.policy.runtime.contract import RuntimeContract, _optional_attr

    if not isinstance(deployment, HyVlaSessionDeployment):
        deployment = HyVlaSessionDeployment.from_json(deployment)
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
        raise ValueError("Hy-VLA runtime differs from the deployment's sealed contract")
    return RuntimeContract(
        action_hz=float(deployment.action_hz),
        chunk_size=deployment.executed_actions,
        action_dim=deployment.action_dim,
        action_space=deployment.action_space,
        hold_behavior=hold,
        fixed_rate=True,
        execution_horizon=deployment.executed_actions,
        wire_image=WIRE_IMAGE,
        history_ticks=deployment.history_offsets,
    )
