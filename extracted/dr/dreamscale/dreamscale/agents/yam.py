"""Bounded Cartesian tools over the existing native YAM rig and strict FK/IK."""

from __future__ import annotations

import asyncio
import base64
import io
import time
from uuid import uuid4

import numpy as np
from dreamscale_transport.llm import Observation, RobotProfile, ToolReceipt
from PIL import Image

from dreamscale.hardware.yam_end_effector import YamEndEffectorAdapter, pose_from_6d, pose_to_6d

from .runner import ExecutionInterrupted

PROFILE_ID = "yam-bimanual/v1"
SIDES = ("left", "right")
VECTOR3 = {"type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3}
QUATERNION = {"type": "array", "items": {"type": "number"}, "minItems": 4, "maxItems": 4}
GRIPPER = {"type": "number", "minimum": 0, "maximum": 1}
TARGET = {
    "type": "object",
    "properties": {"position_m": VECTOR3, "quaternion_xyzw": QUATERNION, "gripper": GRIPPER},
    "required": ["position_m", "quaternion_xyzw", "gripper"],
    "additionalProperties": False,
}


def profile():
    return RobotProfile(
        id=PROFILE_ID,
        description=(
            "Two YAM arms. Targets use the native grasp_site TCP in each arm's own base frame, "
            "right-handed metres; base frames are independent, not a shared world frame. "
            "Orientation is a unit quaternion [x,y,z,w], active rotation from TCP to base. "
            "Gripper: 0=closed,1=open. Move <=0.10 m and <=0.52 rad per call. "
            "Targets are locally interpolated and verified by native FK/IK. "
            "There is no collision planner. Omitted arms hold. "
            "Receipts distinguish dispatch from measured arrival. "
            "Observation state has left_position/right_position in metres in each arm base; "
            "left_rotation_6d/right_rotation_6d contain the first rotation-matrix column "
            "followed by the second column (third = first cross second). "
            "left_gripper/right_gripper are normalized 0=closed,1=open. "
            "measured_joints is [left six joint radians, left gripper, "
            "right six joint radians, right gripper]. This state uses rotation columns; "
            "tool targets use quaternion_xyzw as defined above."
        ),
        groups={
            side: {
                "frame": side + "_base",
                "end_effector": "grasp_site",
                "joint_unit": "rad",
                "position_unit": "m",
                "capabilities": ["bounded_cartesian_motion", "normalized_gripper", "measured_hold"],
                "observation_fields": {
                    side + "_position": {"shape": [3], "unit": "m", "frame": side + "_base"},
                    side + "_rotation_6d": {
                        "shape": [6],
                        "convention": "rotation column 0 followed by column 1",
                    },
                    side + "_gripper": {"unit": "normalized", "closed": 0, "open": 1},
                },
            }
            for side in SIDES
        },
        cameras=["top", "left", "right"],
        tools=[
            {
                "name": "move_end_effectors",
                "description": (
                    "Move one or both named TCPs together along bounded Cartesian interpolations."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "targets": {
                            "type": "object",
                            "properties": {s: TARGET for s in SIDES},
                            "minProperties": 1,
                            "additionalProperties": False,
                        }
                    },
                    "required": ["targets"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "set_grippers",
                "description": (
                    "Set one or both normalized grippers while holding measured arm poses."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "grippers": {
                            "type": "object",
                            "properties": {s: GRIPPER for s in SIDES},
                            "minProperties": 1,
                            "additionalProperties": False,
                        }
                    },
                    "required": ["grippers"],
                    "additionalProperties": False,
                },
            },
        ],
    )


def native_adapter(config, **kwargs):
    calibration = {
        "version": 1,
        "model_id": PROFILE_ID,
        "coordinate_frame": PROFILE_ID,
        "gripper_unit": "normalized",
        "calibration_id": "native-grasp-site-per-arm-base/v1",
        "arms": {
            s: {
                "can_interface": a.can_interface,
                "arm_type": a.arm_type,
                "gripper_type": a.gripper_type,
                "site_name": "grasp_site",
                "model_T_base": np.eye(4).tolist(),
                "site_T_tool": np.eye(4).tolist(),
                "gripper_closed": 0.0,
                "gripper_open": 1.0,
            }
            for s, a in config.arms.items()
        },
    }
    return YamEndEffectorAdapter.from_profile(calibration, config, **kwargs)


def quaternion_matrix(values):
    q = np.asarray(values, dtype=float)
    if q.shape != (4,) or not np.isfinite(q).all() or abs(np.linalg.norm(q) - 1) > 0.001:
        raise ValueError("quaternion_xyzw must have four finite values with unit norm.")
    x, y, z, w = q / np.linalg.norm(q)
    return np.array(
        [
            [1 - 2 * (y * y + z * z), 2 * (x * y - z * w), 2 * (x * z + y * w)],
            [2 * (x * y + z * w), 1 - 2 * (x * x + z * z), 2 * (y * z - x * w)],
            [2 * (x * z - y * w), 2 * (y * z + x * w), 1 - 2 * (x * x + y * y)],
        ]
    )


def rotation_step(start, end, fraction):
    delta = end @ start.T
    angle = float(np.arccos(np.clip((np.trace(delta) - 1) / 2, -1, 1)))
    if angle < 1e-7:
        return start
    axis = np.array(
        [delta[2, 1] - delta[1, 2], delta[0, 2] - delta[2, 0], delta[1, 0] - delta[0, 1]]
    ) / (2 * np.sin(angle))
    x, y, z = axis
    skew = np.array([[0, -z, y], [z, 0, -x], [-y, x, 0]])
    a = angle * fraction
    return (np.eye(3) + np.sin(a) * skew + (1 - np.cos(a)) * (skew @ skew)) @ start


class YamAdapter:
    def __init__(self, rig, kinematics, *, owns_rig=True):
        self.rig, self.kinematics = rig, kinematics
        # An attended hardware lifecycle can retain the controllers after this
        # task stops, return home, then perform the final disconnect itself.
        self.owns_rig = owns_rig
        self.last_observed = None
        self.stopped = False

    def describe(self):
        return profile()

    def describe_action(self, call, observation):
        def grip(value):
            return "closed" if value == 0 else "open" if value == 1 else f"{value:.0%} open"

        def gripper_changed(side, value):
            prior = observation.state.get(side + "_gripper")
            # Presentation only: suppress measured gripper noise. The full
            # requested target remains in the journal and execution receipt.
            return prior is None or not np.isclose(value, prior, atol=0.01, rtol=0)

        if call.name == "set_grippers":
            return [
                f"Gripper {side} → {grip(value)}"
                for side, value in call.arguments["grippers"].items()
                if gripper_changed(side, value)
            ]
        if call.name != "move_end_effectors":
            return None
        lines = []
        for side, target in call.arguments["targets"].items():
            xyz = ", ".join(f"{v:.3f}" for v in target["position_m"])
            line = f"Move {side} → ({xyz}) m [{side}_base]"
            if gripper_changed(side, target["gripper"]):
                line += f" · gripper {grip(target['gripper'])}"
            # Show meaningful rotation changes, without dumping four quaternion values every turn.
            prior = observation.state.get(side + "_rotation_6d")
            if prior is not None:
                rotation = pose_from_6d(np.r_[np.zeros(3), prior])[:3, :3]
                delta = quaternion_matrix(target["quaternion_xyzw"]) @ rotation.T
                degrees = float(np.degrees(np.arccos(np.clip((np.trace(delta) - 1) / 2, -1, 1))))
                if degrees >= 1:
                    line += f" · rotate {degrees:.0f}°"
            else:
                line += " · q=" + ",".join(f"{v:.2f}" for v in target["quaternion_xyzw"])
            lines.append(line)
        return lines

    def bind(self):
        for side in SIDES:
            self.kinematics.kinematics[side].set_joint_limits(self.rig.limits[side][:6].copy())

    async def observe(self):
        raw = self.rig.observe()
        self.last_observed = np.asarray(raw.hold_action, dtype=float)
        state = self.kinematics.state(self.last_observed).model_dump(mode="json")
        state["measured_joints"] = self.last_observed.tolist()
        # Report rotation columns exactly as measured; the tool's quaternion
        # convention is explicit, so conversion is not hidden in the model ID.
        images = {}
        for camera in ("top", "left", "right"):
            output = io.BytesIO()
            image = Image.fromarray(getattr(raw, camera + "_frame"))
            image.thumbnail((1024, 1024))
            image.save(output, format="JPEG", quality=85)
            images[camera] = base64.b64encode(output.getvalue()).decode()
        return Observation(id=str(uuid4()), captured_at=time.time(), state=state, images=images)

    def plan(self, call, seed):
        from jsonschema import Draft202012Validator

        spec = next((t for t in profile().tools if t.name == call.name), None)
        if spec is None:
            raise ValueError("Unsupported tool.")
        Draft202012Validator(spec.parameters).validate(call.arguments)
        measured = np.asarray(self.kinematics.state(seed).model_state())
        endpoints = []
        for side, offset in [("left", 0), ("right", 10)]:
            start = pose_from_6d(measured[offset : offset + 9])
            end = start.copy()
            grip = measured[offset + 9]
            target = call.arguments.get("targets", {}).get(side)
            if target is not None:
                end[:3, 3] = target["position_m"]
                end[:3, :3] = quaternion_matrix(target["quaternion_xyzw"])
                grip = target["gripper"]
                angle = np.arccos(np.clip((np.trace(end[:3, :3] @ start[:3, :3].T) - 1) / 2, -1, 1))
                if np.linalg.norm(end[:3, 3] - start[:3, 3]) > 0.1 or angle > 0.52:
                    raise ValueError(
                        f"{side} target exceeds 0.10 m / 0.52 rad bound; request a smaller motion."
                    )
            grip = call.arguments.get("grippers", {}).get(side, grip)
            endpoints.append((start, end, measured[offset + 9], grip))
        actions = []
        for index in range(1, 61):
            u = index / 60
            action = []
            for start, end, initial_grip, grip in endpoints:
                pose = np.eye(4)
                pose[:3, 3] = start[:3, 3] + u * (end[:3, 3] - start[:3, 3])
                pose[:3, :3] = rotation_step(start[:3, :3], end[:3, :3], u)
                action.extend((*pose_to_6d(pose), initial_grip + u * (grip - initial_grip)))
            actions.append(action)
        commands = self.kinematics.joint_chunk(actions, seed, self.rig.validate_action)
        # Reject solver branch jumps before dispatch, in addition to native limits.
        previous = np.asarray(seed)
        for command in commands:
            current = np.asarray(command)
            if np.max(np.abs((current - previous)[[0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]])) > 0.15:
                raise ValueError("IK branch jump; request a smaller target from the current pose.")
            previous = current
        return commands, actions[-1]

    def _hold(self):
        holds = self.rig.stop()
        confirmed = isinstance(holds, dict) and all(holds.get(side) is True for side in SIDES)
        if not confirmed:
            self.stopped = True
        return confirmed

    async def execute(self, call):
        result = None
        try:
            result = await self._execute(call)
        finally:
            held = self._hold()
            if not held and result is None:
                raise RuntimeError("Measured-pose hold unconfirmed. Use the hardware E-stop.")
        if not held:
            return result.model_copy(
                update={
                    "status": "partial" if result.applied else "unknown",
                    "measured": {**result.measured, "hold_confirmed": False},
                    "detail": "Measured-pose hold unconfirmed. Use the hardware E-stop.",
                }
            )
        return result.model_copy(update={"measured": {**result.measured, "hold_confirmed": True}})

    async def _execute(self, call):
        applied = []
        dispatched = False
        try:
            if self.stopped:
                raise ValueError("Adapter stopped; start a fresh run.")
            seed = np.asarray(self.rig.observe().hold_action)
            if self.last_observed is None or np.max(np.abs(seed - self.last_observed)) > 0.05:
                raise ValueError(
                    "Measured robot moved since observation; observe again before motion."
                )
            commands, goal = self.plan(call, seed)
        except Exception as exc:
            return ToolReceipt(
                call_id=call.id, status="rejected", requested=call.arguments, detail=str(exc)[:4000]
            )
        try:
            # Deliver cancellation queued during native IK before the motor boundary.
            await asyncio.sleep(0)
            if asyncio.current_task().cancelling():
                raise asyncio.CancelledError
            self.rig.enable_dispatch()
            # SIGINT can arrive inside synchronous enable_dispatch and its final
            # gate.set() can overwrite the handler's clear. Recheck after enabling.
            if self.stopped or asyncio.current_task().cancelling():
                self.rig.block_dispatch()
                raise asyncio.CancelledError
            async with asyncio.timeout(10):
                for command in commands:
                    while True:
                        if self.stopped or asyncio.current_task().cancelling():
                            self.rig.block_dispatch()
                            raise asyncio.CancelledError
                        dispatched = True
                        accepted = self.rig.act(command).accepted_action
                        applied.append(list(accepted))
                        await asyncio.sleep(1 / 30)
                        if np.allclose(accepted, command, rtol=0, atol=1e-8):
                            break
            measured = self.kinematics.state(self.rig.observe().hold_action)
            actual = np.asarray(measured.model_state())
            position_errors = [
                float(np.linalg.norm(actual[o : o + 3] - goal[o : o + 3])) for o in (0, 10)
            ]
            rotation_errors = [
                float(
                    np.arccos(
                        np.clip(
                            (
                                np.trace(
                                    pose_from_6d(actual[o : o + 9])[:3, :3].T
                                    @ pose_from_6d(goal[o : o + 9])[:3, :3]
                                )
                                - 1
                            )
                            / 2,
                            -1,
                            1,
                        )
                    )
                )
                for o in (0, 10)
            ]
            arrived = (
                max(position_errors) <= 0.01
                and max(rotation_errors) <= 0.05
                and max(abs(actual[o] - goal[o]) for o in (9, 19)) <= 0.05
            )
            return ToolReceipt(
                call_id=call.id,
                status="completed",
                requested=call.arguments,
                applied={"commands": applied, "command_kind": "interpolated_joint_samples"},
                measured={
                    "state": measured.model_dump(mode="json"),
                    "arrived": bool(arrived),
                    "position_errors_m": position_errors,
                    "rotation_errors_rad": rotation_errors,
                },
                detail=(
                    "Dispatch completed. Arrival is measured separately; task success "
                    "is unverified."
                ),
            )
        except asyncio.CancelledError as exc:
            raise ExecutionInterrupted(
                ToolReceipt(
                    call_id=call.id,
                    status="partial" if dispatched else "unknown",
                    requested=call.arguments,
                    applied={"commands": applied, "command_kind": "interpolated_joint_samples"},
                    detail="Execution cancelled. Arrival unverified; never replay pending motion.",
                )
            ) from exc
        except Exception as exc:
            return ToolReceipt(
                call_id=call.id,
                status="partial" if dispatched else "rejected",
                requested=call.arguments,
                applied={"commands": applied, "command_kind": "interpolated_joint_samples"},
                detail=str(exc)[:4000],
            )

    async def stop(self):
        self.stopped = True
        self.rig.block_dispatch()
        if not self._hold():
            raise RuntimeError("Measured-pose hold unconfirmed. Use the hardware E-stop.")

    async def close(self):
        if self.owns_rig:
            self.rig.close()
