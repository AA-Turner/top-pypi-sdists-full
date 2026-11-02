"""Native RoboCasa worker. Executed by an isolated Python; no SDK/cloud dependencies.

Local pipe messages use pickle only between our own parent and child processes.
Model and network messages never enter this channel. stdout is reserved for IPC.
"""

from __future__ import annotations

import contextlib
import sys
import warnings

if __package__:
    from .native_process import read_message, write_message
else:
    from native_process import read_message, write_message

CAMERAS = ("robot0_agentview_left", "robot0_agentview_right", "robot0_eye_in_hand")
# DROID policies command absolute Franka joint targets at 15 Hz from DROID's home
# pose, with 16:9 camera views; the PandaOmron arm is the same Franka.
DROID_HOME = (0.0, -0.785, 0.0, -2.356, 0.0, 1.571, 0.785)
DROID_SETTLE_STEPS = 30
FINGER_OPEN_QPOS = 0.04
DROID_ARM_CONTROLLER = {
    "type": "JOINT_POSITION",
    "input_type": "absolute",
    "input_max": 4.0,
    "input_min": -4.0,
    "output_max": 0.05,
    "output_min": -0.05,
    "kp": 150.0,
    "damping_ratio": 1,
    "impedance_mode": "fixed",
    "kp_limits": [0, 1000],
    "damping_ratio_limits": [0, 10],
    "qpos_limits": None,
    "interpolation": None,
    "ramp_ratio": 0.2,
}


def observation(raw):
    # The upstream Gym wrapper performs camera orientation and state extraction.
    names = ("base_position", "base_rotation", "end_effector_position_relative",
             "end_effector_rotation_relative", "gripper_qpos")
    return {"images": {key: raw["video." + key] for key in CAMERAS},
            "state": {key: raw["state." + key].tolist() for key in names},
            "instruction": raw["annotation.human.task_description"]}


def droid_observation(raw, inner):
    import numpy as np

    robot = inner.robots[0]
    joints = inner.sim.data.qpos[robot._ref_joint_pos_indexes]
    fingers = inner.sim.data.qpos[robot._ref_gripper_joint_pos_indexes["right"]]
    # DROID: 0 open, 1 closed.
    gripper = 1.0 - float(np.clip(np.mean(np.abs(fingers)) / FINGER_OPEN_QPOS, 0.0, 1.0))
    return {"images": {key: raw["video." + key] for key in CAMERAS},
            "joint_positions": [float(value) for value in joints],
            "gripper": gripper,
            "instruction": raw["annotation.human.task_description"]}


def install_droid_joint_control(env_utils):
    """Swap the arm's delta-EEF controller for absolute joint targets before env creation."""

    original = env_utils.load_composite_controller_config

    def joint_controller_config(*args, **kwargs):
        config = original(*args, **kwargs)
        gripper = config["body_parts"]["right"].get("gripper")
        config["body_parts"]["right"] = {**DROID_ARM_CONTROLLER, "gripper": gripper}
        return config

    env_utils.load_composite_controller_config = joint_controller_config


def droid_step(env, inner, joints, gripper_closed):
    import numpy as np

    controller = inner.robots[0].composite_controller
    action = np.zeros(controller.action_limits[0].shape)
    start, end = controller._action_split_indexes["right"]
    action[start:end] = joints
    start, end = controller._action_split_indexes["right_gripper"]
    action[start:end] = 1.0 if gripper_closed else -1.0
    action[-1] = -1.0  # arm mode; the mobile base and torso stay still
    raw, _, _, _ = inner.step(action)
    return env.get_observation(raw), bool(inner._check_success())


def main():
    incoming, outgoing = sys.stdin.buffer, sys.stdout.buffer
    env = None
    # Native packages print import/reset diagnostics. Keep the binary pipe clean.
    with contextlib.redirect_stdout(sys.stderr):
        try:
            import gymnasium as gym
            import numpy as np
            with warnings.catch_warnings():
                for category in (DeprecationWarning, SyntaxWarning):
                    warnings.filterwarnings("ignore", message=r"invalid escape sequence '\\ '$",
                        category=category, module=r".*[/\\](robocasa|robosuite)[/\\]__init__$")
                import robocasa  # noqa: F401 - register the pinned task catalog
            from robocasa.utils import env_utils
            from robocasa.utils.env_utils import convert_action

            setup = read_message(incoming)
            droid = setup.get("control", "eef_delta") == "droid_joint"
            options = {}
            if droid:
                install_droid_joint_control(env_utils)
                options = {"camera_widths": 320, "camera_heights": 180, "control_freq": 15}
            env = gym.make(f"robocasa/{setup['task']}", split="pretrain", seed=setup["seed"],
                           disable_env_checker=True, **options)
            inner = env.unwrapped.env

            def reset():
                raw, _ = env.reset(seed=setup["seed"])
                if not droid:
                    return observation(raw)
                for _ in range(DROID_SETTLE_STEPS):
                    raw, _ = droid_step(env, inner, DROID_HOME, False)
                return droid_observation(raw, inner)

            latest = reset()
            write_message(outgoing, {"ok": latest})
            while True:
                request = read_message(incoming)
                if request["op"] == "close":
                    break
                if request["op"] == "reset":
                    result = latest = reset()
                elif request["op"] == "step" and droid:
                    action = np.asarray(request["action"], dtype=np.float64)
                    if action.shape != (8,) or not np.isfinite(action).all():
                        raise ValueError("DROID control requires eight finite action values")
                    raw, success = droid_step(env, inner, action[:7], action[7] > 0.5)
                    latest = droid_observation(raw, inner)
                    result = (latest, success)
                elif request["op"] == "step":
                    action = np.asarray(request["action"], dtype=np.float32)
                    if action.shape != (12,) or not np.isfinite(action).all():
                        raise ValueError("RoboCasa365 requires twelve finite action values")
                    raw, _, _, _, info = env.step(convert_action(action))
                    latest = observation(raw)
                    result = (latest, bool(info["success"]))
                elif request["op"] == "render":
                    import cv2

                    frame = np.concatenate([latest["images"][key] for key in CAMERAS], axis=1)
                    cv2.imshow("Dreamscale RoboCasa365 sim",
                               cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    cv2.waitKey(1)
                    result = None
                else:
                    raise ValueError("unknown simulator operation")
                write_message(outgoing, {"ok": result})
        except EOFError:
            pass
        except Exception as exc:
            write_message(outgoing, {"error": f"{type(exc).__name__}: {exc}"})
        finally:
            if env is not None:
                env.close()
            if "cv2" in sys.modules:
                sys.modules["cv2"].destroyAllWindows()


if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "encode-video":
        import imageio.v3 as iio
        import numpy as np

        frames = np.load(sys.argv[2], allow_pickle=False)
        iio.imwrite(sys.argv[3], frames, plugin="pyav", codec="libx264", fps=float(sys.argv[4]))
    else:
        main()
