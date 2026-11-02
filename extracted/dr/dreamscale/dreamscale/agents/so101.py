"""Bounded gripper tools over the SO-101 rig and its five-joint kinematics."""

from __future__ import annotations

import asyncio
import base64
import io
import math
import time
from uuid import uuid4

import numpy as np
from dreamscale_transport.llm import Observation, RobotProfile, ToolReceipt
from PIL import Image

from dreamscale.so101_kinematics import ARM_JOINTS, IKFailure, solve, tool_state

from .runner import ExecutionInterrupted

PROFILE_ID = "so101/v1"
CAMERAS = ("side", "wrist")
MAX_MOVE_M = 0.08
MAX_TILT_CHANGE_DEG = 30.0
MAX_ROLL_CHANGE_DEG = 45.0
STEPS = 45  # 1.5 s of interpolated commands at 30 Hz
MAX_JOINT_STEP_DEG = 6.0  # between interpolated IK samples; larger means a branch jump
GRIPPER = {"type": "number", "minimum": 0, "maximum": 1}
VECTOR3 = {"type": "array", "items": {"type": "number"}, "minItems": 3, "maxItems": 3}


def profile():
    return RobotProfile(
        id=PROFILE_ID,
        description=(
            "One SO-101 arm (five joints and a parallel gripper) on a tabletop. "
            "Positions are the gripper's tool point, between the jaw tips, in the arm's base "
            "frame: right-handed metres, origin at the base on the table, x forward along the "
            "arm's middle pan, y to the arm's left, z up. The arm cannot reach every "
            "orientation: a target sets the tool position, its tilt (how far the jaws point "
            "below horizontal: 90 straight down, 0 level, negative upward) and its roll (the "
            "wrist_roll joint in degrees, turning the jaws about the direction they point). "
            "The pan joint turns the arm toward the target, so the jaws always point away "
            "from the base. Gripper: 0=closed, 1=open. Each call moves the tool at most "
            "0.08 m, tilt 30 degrees and roll 45 degrees; motion is interpolated locally "
            "over about 1.5 s and checked by inverse kinematics and the arm's calibrated "
            "joint ranges. There is no collision planner: the table is z=0 and the arm can "
            "push objects or the table. Receipts distinguish dispatch from measured arrival. "
            "Observation state: position_m, tilt_deg, roll_deg and gripper (0..1) as "
            "measured, and measured_joints_deg [shoulder_pan, shoulder_lift, elbow_flex, "
            "wrist_flex, wrist_roll, gripper 0..100]. Cameras: side (fixed, looking at the "
            "workspace) and wrist (on the gripper, looking along the jaws)."
        ),
        groups={
            "arm": {
                "frame": "base",
                "end_effector": "gripper_frame_link",
                "joint_unit": "deg",
                "position_unit": "m",
                "capabilities": ["bounded_cartesian_motion", "normalized_gripper", "measured_hold"],
                "observation_fields": {
                    "position_m": {"shape": [3], "unit": "m", "frame": "base"},
                    "tilt_deg": {"unit": "deg", "convention": "jaws below horizontal"},
                    "roll_deg": {"unit": "deg", "convention": "wrist_roll joint"},
                    "gripper": {"unit": "normalized", "closed": 0, "open": 1},
                },
            },
        },
        cameras=list(CAMERAS),
        tools=[
            {
                "name": "move_gripper",
                "description": (
                    "Move the gripper's tool point to position_m along a straight line, "
                    "optionally changing tilt_deg, roll_deg and the gripper opening on the way."
                    " Omitted values keep their measured value."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "position_m": VECTOR3,
                        "tilt_deg": {"type": "number", "minimum": -60, "maximum": 90},
                        "roll_deg": {"type": "number", "minimum": -180, "maximum": 180},
                        "gripper": GRIPPER,
                    },
                    "required": ["position_m"],
                    "additionalProperties": False,
                },
            },
            {
                "name": "set_gripper",
                "description": "Open or close the gripper while holding the arm where it is.",
                "parameters": {
                    "type": "object",
                    "properties": {"gripper": GRIPPER},
                    "required": ["gripper"],
                    "additionalProperties": False,
                },
            },
        ],
    )


def _jpeg(frame):
    output = io.BytesIO()
    image = Image.fromarray(frame)
    image.thumbnail((1024, 1024))
    image.save(output, format="JPEG", quality=85)
    return base64.b64encode(output.getvalue()).decode()


class So101Adapter:
    def __init__(self, rig, *, owns_rig=True):
        self.rig = rig
        # An attended lifecycle can keep the arm connected after this task stops,
        # return it home, then perform the final disconnect itself.
        self.owns_rig = owns_rig
        self.last_observed = None
        self.stopped = False

    def describe(self):
        return profile()

    def describe_action(self, call, observation):
        def grip(value):
            return "closed" if value == 0 else "open" if value == 1 else f"{value:.0%} open"

        prior = observation.state.get("gripper")
        changed = call.arguments.get("gripper")
        if changed is not None and prior is not None and math.isclose(changed, prior, abs_tol=0.01):
            changed = None
        if call.name == "set_gripper":
            return [] if changed is None else [f"Gripper → {grip(changed)}"]
        if call.name != "move_gripper":
            return None
        xyz = ", ".join(f"{v:.3f}" for v in call.arguments["position_m"])
        line = f"Move gripper → ({xyz}) m"
        for key, unit in (("tilt_deg", "tilt"), ("roll_deg", "roll")):
            value = call.arguments.get(key)
            if value is not None and not math.isclose(
                value, observation.state.get(key, value), abs_tol=1.0
            ):
                line += f" · {unit} {value:.0f}°"
        if changed is not None:
            line += f" · gripper {grip(changed)}"
        return [line]

    async def observe(self):
        raw = self.rig.observe()
        self.last_observed = np.asarray(raw.joint_positions, dtype=float)
        state = {
            **tool_state(self.last_observed).as_dict(),
            "gripper": round(float(self.last_observed[ARM_JOINTS]) / 100, 3),
            "measured_joints_deg": [round(float(v), 2) for v in self.last_observed],
        }
        images = {"side": _jpeg(raw.side_frame), "wrist": _jpeg(raw.wrist_frame)}
        return Observation(id=str(uuid4()), captured_at=time.time(), state=state, images=images)

    def plan(self, call, seed):
        """Interpolated joint commands (degrees, gripper 0-100) and the goal tool state."""
        from jsonschema import Draft202012Validator

        spec = next((t for t in profile().tools if t.name == call.name), None)
        if spec is None:
            raise ValueError("Unsupported tool.")
        Draft202012Validator(spec.parameters).validate(call.arguments)
        limits = self.rig.limits["arm"]
        start = tool_state(seed)
        start_grip = float(seed[ARM_JOINTS])
        grip = 100 * call.arguments.get("gripper", start_grip / 100)
        if call.name == "set_gripper":
            return [[*seed[:ARM_JOINTS], start_grip + u / STEPS * (grip - start_grip)]
                    for u in range(1, STEPS + 1)], (start, grip)
        target = np.asarray(call.arguments["position_m"], dtype=float)
        tilt = float(call.arguments.get("tilt_deg", start.tilt_deg))
        roll = float(call.arguments.get("roll_deg", start.roll_deg))
        if np.linalg.norm(target - np.asarray(start.position_m)) > MAX_MOVE_M:
            raise ValueError("Target is more than 0.08 m away; request a smaller motion.")
        if abs(tilt - start.tilt_deg) > MAX_TILT_CHANGE_DEG:
            raise ValueError("Tilt changes more than 30 degrees; request a smaller change.")
        if abs(roll - start.roll_deg) > MAX_ROLL_CHANGE_DEG:
            raise ValueError("Roll changes more than 45 degrees; request a smaller change.")
        if target[2] < 0.0:
            raise ValueError("Target is below the table (z < 0).")
        commands, previous = [], np.asarray(seed[:ARM_JOINTS], dtype=float)
        for index in range(1, STEPS + 1):
            u = index / STEPS
            point = np.asarray(start.position_m) + u * (target - np.asarray(start.position_m))
            try:
                joints = solve(point, start.tilt_deg + u * (tilt - start.tilt_deg),
                               start.roll_deg + u * (roll - start.roll_deg), previous, limits)
            except IKFailure as exc:
                raise ValueError(f"Step {index}/{STEPS}: {exc}") from exc
            if np.max(np.abs(joints - previous)) > MAX_JOINT_STEP_DEG:
                raise ValueError("IK branch jump; request a smaller target from the current pose.")
            commands.append([*joints, start_grip + u * (grip - start_grip)])
            previous = joints
        return commands, (tool_state([*previous, 0.0]), grip)

    def _hold(self):
        holds = self.rig.stop()
        confirmed = isinstance(holds, dict) and bool(holds) and all(
            held is True for held in holds.values()
        )
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
                raise RuntimeError("Measured-pose hold unconfirmed. Support the arm.")
        if not held:
            return result.model_copy(update={
                "status": "partial" if result.applied else "unknown",
                "measured": {**result.measured, "hold_confirmed": False},
                "detail": "Measured-pose hold unconfirmed. Support the arm.",
            })
        return result.model_copy(update={"measured": {**result.measured, "hold_confirmed": True}})

    async def _execute(self, call):
        applied, dispatched = [], False
        try:
            if self.stopped:
                raise ValueError("Adapter stopped; start a fresh run.")
            seed = np.asarray(self.rig.observe().joint_positions, dtype=float)
            if self.last_observed is None or np.max(np.abs(seed - self.last_observed)) > 3.0:
                raise ValueError("Measured robot moved since observation; observe again first.")
            commands, (goal, goal_grip) = self.plan(call, seed)
        except Exception as exc:
            return ToolReceipt(call_id=call.id, status="rejected", requested=call.arguments,
                               detail=str(exc)[:4000])
        try:
            await asyncio.sleep(0)
            if asyncio.current_task().cancelling():
                raise asyncio.CancelledError
            self.rig.enable_dispatch()
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
                        applied.append([round(v, 3) for v in accepted])
                        await asyncio.sleep(1 / 30)
                        # The rig caps speed and lead; repeat a capped sample until sent.
                        if np.allclose(accepted, command, rtol=0, atol=1e-6):
                            break
                # Let the arm settle on the last command before measuring arrival.
                for _ in range(15):
                    self.rig.act(commands[-1])
                    await asyncio.sleep(1 / 30)
            measured = np.asarray(self.rig.observe().joint_positions, dtype=float)
            state = tool_state(measured)
            position_error = float(np.linalg.norm(
                np.asarray(state.position_m) - np.asarray(goal.position_m)
            ))
            gripper_error = abs(float(measured[ARM_JOINTS]) - goal_grip) / 100
            arrived = (position_error <= 0.015 and abs(state.tilt_deg - goal.tilt_deg) <= 8
                       and (call.name != "set_gripper" or gripper_error <= 0.1))
            return ToolReceipt(
                call_id=call.id,
                status="completed",
                requested=call.arguments,
                applied={"commands": applied, "command_kind": "interpolated_joint_samples_deg"},
                measured={
                    "state": {
                        **state.as_dict(), "gripper": round(float(measured[ARM_JOINTS]) / 100, 3),
                    },
                    "arrived": bool(arrived),
                    "position_error_m": round(position_error, 4),
                    "gripper_error": round(gripper_error, 3),
                },
                detail=(
                    "Dispatch completed. Arrival is measured separately; a gripper that "
                    "closes on an object stops short of its target. Task success is unverified."
                ),
            )
        except asyncio.CancelledError as exc:
            raise ExecutionInterrupted(ToolReceipt(
                call_id=call.id,
                status="partial" if dispatched else "unknown",
                requested=call.arguments,
                applied={"commands": applied, "command_kind": "interpolated_joint_samples_deg"},
                detail="Execution cancelled. Arrival unverified; never replay pending motion.",
            )) from exc
        except Exception as exc:
            return ToolReceipt(
                call_id=call.id,
                status="partial" if dispatched else "rejected",
                requested=call.arguments,
                applied={"commands": applied, "command_kind": "interpolated_joint_samples_deg"},
                detail=str(exc)[:4000],
            )

    async def stop(self):
        self.stopped = True
        self.rig.block_dispatch()
        if not self._hold():
            raise RuntimeError("Measured-pose hold unconfirmed. Support the arm.")

    async def close(self):
        if self.owns_rig:
            self.rig.close()
