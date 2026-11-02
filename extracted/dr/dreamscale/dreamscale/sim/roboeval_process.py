"""Native RoboEval worker. Executed by an isolated Python; no SDK/cloud dependencies.

Local pipe messages use pickle only between our own parent and child processes.
Model and network messages never enter this channel. stdout is reserved for IPC.

Policy coordinates (verified against microsoft/roboeval-data-for-rho): per arm,
left then right, [x, y, z] in the RoboEval world frame, the first two columns of
the rotation matrix from RoboEval's xyz Euler angles, then the gripper. Observed
grippers are openness (1 = open); commanded grippers are 1 = close.
"""

from __future__ import annotations

import contextlib
import importlib
import sys

if __package__:
    from .native_process import read_message, write_message
else:
    from native_process import read_message, write_message

CAMERAS = ("head", "left_wrist", "right_wrist")
CAMERA_KEYS = tuple(f"observation.images.{name}" for name in CAMERAS)
IMAGE_SIZE = 224
CONTROL_HZ = 20


def main():
    incoming, outgoing = sys.stdin.buffer, sys.stdout.buffer
    env = None
    with contextlib.redirect_stdout(sys.stderr):
        try:
            import numpy as np
            from roboeval.action_modes import JointPositionActionMode
            from roboeval.robots.configs.panda import BimanualPanda
            from roboeval.utils.observation_config import CameraConfig, ObservationConfig
            from scipy.spatial.transform import Rotation

            def pose_to_policy(pose):
                rotation = Rotation.from_euler("xyz", pose[3:6]).as_matrix()
                return [*pose[:3], *rotation[:, 0], *rotation[:, 1]]

            def policy_to_pose(values):
                first = values[3:6] / np.linalg.norm(values[3:6])
                second = values[6:9] - first * (first @ values[6:9])
                second /= np.linalg.norm(second)
                matrix = np.stack([first, second, np.cross(first, second)], axis=1)
                return [*values[:3], *Rotation.from_matrix(matrix).as_euler("xyz")]

            latest = {}

            def images():
                # Rendering three cameras costs ~20x the physics step; render on request only,
                # once per step (the viewer reuses what the policy or recorder already rendered).
                if "images" not in latest:
                    raw = env.get_observation()
                    latest["images"] = {
                        key: np.ascontiguousarray(raw[f"rgb_{name}"].transpose(1, 2, 0))
                        for key, name in zip(CAMERA_KEYS, CAMERAS, strict=True)}
                return latest["images"]

            def observation():
                robot = env.robot
                base = robot.floating_base.dof_amount if robot.floating_base else 0
                joints = np.asarray(robot.qpos_actuated)[base:base + len(robot.limb_actuators)]
                pose = robot.forward_kinematics(joints)
                grippers = [float(gripper.qpos) for gripper in robot.grippers.values()]
                state = []
                for arm in range(2):
                    state += [*pose_to_policy(pose[arm * 6:arm * 6 + 6]), grippers[arm]]
                return {"state": [float(value) for value in state],
                        "instruction": setup["instruction"]}

            setup = read_message(incoming)
            module = importlib.import_module(f"roboeval.envs.{setup['module']}")
            env = getattr(module, setup["variant"])(
                action_mode=JointPositionActionMode(
                    floating_base=True, absolute=True, ee=True, floating_dofs=[]),
                observation_config=ObservationConfig(cameras=[
                    CameraConfig(name=name, rgb=True, depth=False,
                                 resolution=(IMAGE_SIZE, IMAGE_SIZE))
                    for name in CAMERAS
                ]),
                render_mode=None, robot_cls=BimanualPanda, control_frequency=CONTROL_HZ,
                start_seed=setup["seed"],
            )
            env.reset(seed=setup["seed"])
            write_message(outgoing, {"ok": {**observation(), "images": images()}})
            while True:
                request = read_message(incoming)
                if request["op"] == "close":
                    break
                if request["op"] in ("reset", "step"):
                    latest.clear()
                if request["op"] == "reset":
                    env.reset(seed=setup["seed"])
                    result = {**observation(), "images": images()}
                elif request["op"] == "step":
                    action = np.asarray(request["action"], dtype=np.float64)
                    if action.shape != (20,) or not np.isfinite(action).all():
                        raise ValueError("RoboEval requires twenty finite action values")
                    left, right = action[:10], action[10:]
                    command = np.array([*policy_to_pose(left), *policy_to_pose(right),
                                        *np.clip([left[9], right[9]], 0.0, 1.0)], np.float32)
                    env.step(command, fast=True)
                    result = (observation(), bool(env.success))
                elif request["op"] == "images":
                    result = images()
                elif request["op"] == "render":
                    import cv2

                    # Shown from this process's own frames: arrays never cross the pipe from
                    # the SDK, whose numpy (possibly 2.x) pickles do not load under numpy 1.26.
                    frame = np.concatenate([images()[key] for key in CAMERA_KEYS], axis=1)
                    cv2.imshow("Dreamscale RoboEval sim", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
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
    main()
