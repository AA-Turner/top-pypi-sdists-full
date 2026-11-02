"""Run Isaac 0.5 (or your imported fine-tune) on one SO-101 arm with the Python SDK.

Prerequisites: `dreamscale login`, then `dreamscale robots so101 setup` and
`dreamscale robots so101 calibrate` (they save the port, both cameras and the
calibration this script reads), and `uv add "dreamscale[so101]"`.

    python so101_isaac.py --instruction "pick up the cube"                 # preview: arm holds
    python so101_isaac.py --instruction "pick up the cube" --execute       # moves the arm
    python so101_isaac.py --checkpoint ckpt_... --instruction "..."        # your fine-tune
    python so101_isaac.py --context on --instruction "..."                 # 3-frame history

Safety: preview is the default and never commands the motors. With --execute,
every action is clamped to --max-step-deg per joint against the measured
position (the SDK's clamp_step), and Ctrl+C stops the loop and holds position.
Keep the E-stop in reach; this is not a substitute for a local safety controller.
"""

from __future__ import annotations

import argparse

import dreamscale
from dreamscale.config import load_config
from dreamscale.constants import CAMERA_KEY_SO101_SIDE, CAMERA_KEY_SO101_WRIST, MAX_STEP_DEG
from dreamscale.hardware.lerobot_so101 import create_so101
from dreamscale.motion.safety import clamp_step

MODEL = "perceptron-isaac05-so101"


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


def run(
    robot, *, instruction, checkpoint, execute, max_actions, max_step_deg, connect, context="auto"
):
    def observe(_context):
        frames = robot.capture_frames()
        return dreamscale.so101.observation(
            side_frame=frames[CAMERA_KEY_SO101_SIDE],
            wrist_frame=frames[CAMERA_KEY_SO101_WRIST],
            joint_positions=robot.read_joint_positions(),
        )

    def act(action, context):
        current = robot.read_joint_positions()
        target = clamp_step(current, [float(v) for v in action], max_step_deg)
        if execute:
            robot.send_joint_targets(target)
        elif context.action_index % 30 == 0:
            print(f"preview {context.action_index}: " + " ".join(f"{v:7.2f}" for v in target))
        return dreamscale.ActResult(accepted_action=tuple(target))

    def hold(_context):
        return robot.read_joint_positions()

    options = {"region": "available"}
    if checkpoint:
        options["checkpoint"] = checkpoint
    if context != "auto":
        options["context"] = context
    with connect(MODEL, **options) as policy:
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
    parser.add_argument(
        "--checkpoint", help="ckpt_... or base (default: your organization's default)"
    )
    parser.add_argument(
        "--context",
        choices=("auto", "on", "off"),
        default="auto",
        help="Observation history: the checkpoint's own (auto), the last three frames 1/30 s "
        "apart (on) or one frame (off).",
    )
    parser.add_argument("--execute", action="store_true", help="Move the arm (default: preview).")
    parser.add_argument("--max-actions", type=int, default=900, help="30 Hz actions; 900 = 30 s.")
    parser.add_argument("--max-step-deg", type=float, default=MAX_STEP_DEG)
    args = parser.parse_args()
    robot = make_robot()
    robot.connect()
    try:
        result = run(
            robot,
            instruction=args.instruction,
            checkpoint=args.checkpoint,
            execute=args.execute,
            max_actions=args.max_actions,
            max_step_deg=args.max_step_deg,
            connect=dreamscale.connect,
            context=args.context,
        )
        print(f"{result.actions} actions, {result.underruns} underruns, stop: {result.stop_reason}")
    except KeyboardInterrupt:
        print("Stopped; holding position.")
    finally:
        robot.disconnect()


if __name__ == "__main__":
    main()
