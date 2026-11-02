"""Run FLUX 3 Action (Black Forest Labs' world action model) on one SO-101 arm.

`dreamscale run so101 --model flux-3-action-so101` does this from the CLI; this script
shows the same loop with the Python SDK.

Prerequisites: `dreamscale login` (in an organization with FLUX 3 Action SO-101
access), then `dreamscale robots so101 setup` and `dreamscale robots so101 calibrate`
(they save the port, both cameras and the calibration this script reads), and
`uv add "dreamscale[so101]"`.

    python so101_flux3.py --instruction "pick up the orange block and put it in the pink bowl"
    python so101_flux3.py --instruction "..." --execute       # moves the arm

The model expects BFL's setup: a fixed top-down or high-angle scene camera (the side
camera) and a wrist camera with the gripper jaw at the top of the image. It predicts
42 joint targets (1.4 s at 30 Hz) per plan and replans while it moves. BFL show
SO-101 task success after a task LoRA on demos of the target setup; the released
checkpoint is a starting point.

Safety: preview is the default and never commands the motors. With --execute,
each command moves at most --max-step-deg per joint from the previous command (the
SDK's clamp_step) and leads the measured position by at most --max-lead-deg, so a
blocked joint cannot wind up. A tight limit against the measured position instead
stalls the SO-101's P-only servos under gravity (sandbox/experiments/flux3-so101).
Ctrl+C stops the loop
and holds position. Keep the E-stop in reach; this is not a substitute for a local
safety controller.
"""

from __future__ import annotations

import argparse

import dreamscale
from dreamscale.config import load_config
from dreamscale.constants import CAMERA_KEY_SO101_SIDE, CAMERA_KEY_SO101_WRIST
from dreamscale.hardware.lerobot_so101 import create_so101
from dreamscale.motion.safety import clamp_step

MODEL = "flux-3-action-so101"
# Per-tick command limit validated on a physical SO-101 (sandbox/experiments/flux3-so101).
DEFAULT_MAX_STEP_DEG = 5.0
DEFAULT_MAX_LEAD_DEG = 45.0


def make_robot():
    """The SO-101 that `dreamscale robots so101 setup` configured."""
    config = load_config()
    if config.robot_port is None or None in (config.camera_index, config.wrist_camera_index):
        raise SystemExit("Run `dreamscale robots so101 setup` first.")
    return create_so101(
        port=config.robot_port,
        side_camera_index=config.camera_index,
        wrist_camera_index=config.wrist_camera_index,
        calibration_path=config.calibration_path,
    )


def run(robot, *, instruction, execute, max_actions, max_step_deg, connect,
        max_lead_deg=DEFAULT_MAX_LEAD_DEG):
    previous = None

    def observe(_context):
        frames = robot.capture_frames()
        return dreamscale.so101.observation(
            side_frame=frames[CAMERA_KEY_SO101_SIDE],
            wrist_frame=frames[CAMERA_KEY_SO101_WRIST],
            joint_positions=robot.read_joint_positions(),
        )

    def act(action, context):
        nonlocal previous
        current = robot.read_joint_positions()
        start = current if previous is None else previous
        target = clamp_step(start, [float(v) for v in action], max_step_deg)
        target = clamp_step(current, target, max_lead_deg)
        previous = target
        if execute:
            robot.send_joint_targets(target)
        elif context.action_index % 30 == 0:
            print(f"preview {context.action_index}: " + " ".join(f"{v:7.2f}" for v in target))
        return dreamscale.ActResult(accepted_action=tuple(target))

    def hold(_context):
        return robot.read_joint_positions()

    with connect(MODEL, region="available") as policy:
        return policy.run(
            instruction=instruction,
            observe=observe,
            act=act,
            read_hold_action=hold,
            max_actions=max_actions,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--instruction", required=True)
    parser.add_argument("--execute", action="store_true", help="Move the arm (default: preview).")
    parser.add_argument("--max-actions", type=int, default=900, help="30 Hz actions; 900 = 30 s.")
    parser.add_argument("--max-step-deg", type=float, default=DEFAULT_MAX_STEP_DEG)
    parser.add_argument("--max-lead-deg", type=float, default=DEFAULT_MAX_LEAD_DEG)
    args = parser.parse_args()
    robot = make_robot()
    robot.connect()
    try:
        result = run(
            robot,
            instruction=args.instruction,
            execute=args.execute,
            max_actions=args.max_actions,
            max_step_deg=args.max_step_deg,
            max_lead_deg=args.max_lead_deg,
            connect=dreamscale.connect,
        )
        print(f"{result.actions} actions, {result.underruns} underruns, stop: {result.stop_reason}")
    except KeyboardInterrupt:
        print("Stopped; holding position.")
    finally:
        robot.disconnect()


if __name__ == "__main__":
    main()
