"""MuJoCo child process. Benchmark JSON and upstream judge_success are authoritative."""

from __future__ import annotations

import contextlib
import os
import sys
import traceback

if __package__:
    from .molmospaces_catalog import BENCHMARKS, REVISION
    from .native_process import read_message, write_message
else:
    from molmospaces_catalog import BENCHMARKS, REVISION
    from native_process import read_message, write_message


def action_dict(action):
    import numpy as np

    values = np.asarray(action, dtype=np.float64)
    if values.shape != (8,) or not np.isfinite(values).all():
        raise ValueError("MolmoSpaces DROID requires eight finite action values")
    # Match qualified Cosmos/RoboLab binary gripper: 0=open, 1=closed.
    return {"arm": values[:7], "gripper": np.array([255.0 if values[7] > 0.5 else 0.0])}


def set_benchmark_joint_values(env, spec):
    """Apply the JSON articulation state without requiring datagen grasp files.

    Upstream's sampler rejects articulated THOR objects during a grasp-library
    lookup even though evaluation uses only the specified joint and position.
    This preserves those exact initial values and leaves the task oracle intact.
    """
    task = spec.task
    if "joint_name" not in task:
        return
    obj = env.object_managers[env.current_batch_index].get_object_by_name(
        task["pickup_obj_name"]
    )
    index = list(obj.joint_names).index(task["joint_name"])
    obj.set_joint_position(index, task["joint_start_position"][0])


class MolmoEpisode:
    def __init__(self, setup):
        import mujoco
        from molmo_spaces.evaluation.benchmark_schema import load_all_episodes
        from molmo_spaces.molmo_spaces_constants import ASSETS_DIR, get_resource_manager

        self.setup = setup
        self.benchmark = BENCHMARKS[setup["suite"]]
        renderer = getattr(mujoco, "mjRENDERER", "classic")
        if renderer != self.benchmark.renderer:
            raise ValueError(f"Benchmark requires {self.benchmark.renderer}, got {renderer}")
        get_resource_manager()
        self.path = ASSETS_DIR / "benchmarks" / self.benchmark.path
        self.episodes = load_all_episodes(self.path)
        index = setup["task_id"]
        if not 0 <= index < len(self.episodes):
            raise ValueError(f"Episode index must be 0–{len(self.episodes) - 1}")
        self.spec = self.episodes[index]
        self.horizon_steps = round(
            float(self.spec.task.get("task_horizon_sec", self.benchmark.horizon_s)) * 15
        )
        self.sampler = None
        self.reset()

    def reset(self):
        from molmo_spaces.configs.policy_configs import DummyPolicyConfig
        from molmo_spaces.configs.robot_configs import FrankaRobotConfig
        from molmo_spaces.evaluation.configs.evaluation_configs import JsonBenchmarkEvalConfig
        from molmo_spaces.tasks.json_eval_task_sampler import JsonEvalTaskSampler

        class BenchmarkTaskSampler(JsonEvalTaskSampler):
            def set_joint_values(inner, env):
                set_benchmark_joint_values(env, inner.episode_spec)

        self.close()
        seed = self.spec.seed if self.spec.seed is not None else self.setup["task_id"]
        config = JsonBenchmarkEvalConfig(
            robot_config=FrankaRobotConfig(),
            policy_config=DummyPolicyConfig(),
            policy_dt_ms=66.0,
            ctrl_dt_ms=2.0,
            sim_dt_ms=2.0,
            seed=seed + self.setup["seed"],
            task_horizon=self.horizon_steps,
            terminate_upon_success=True,
        )
        self.sampler = BenchmarkTaskSampler(config, self.spec)
        self.task = self.sampler.sample_task(house_index=self.spec.house_index)
        if self.task is None:
            raise RuntimeError("Benchmark task could not be initialized")
        self.raw = self.task.reset()[0][0]
        self.oracle_success = False
        return self.observation()

    def observation(self):
        import numpy as np

        obs = self.raw
        if self.benchmark.cameras:
            exterior, wrist = self.benchmark.cameras
        else:
            exterior = (
                "droid_shoulder_light_randomization"
                if "droid_shoulder_light_randomization" in obs
                else "exo_camera_1"
            )
            wrist = "wrist_camera_zed_mini" if "wrist_camera_zed_mini" in obs else "wrist_camera"
        state = self.sampler.env.current_robot.robot_view.get_qpos_dict()
        return {
            "exterior": np.ascontiguousarray(obs[exterior]),
            "wrist": np.ascontiguousarray(obs[wrist]),
            "joint_positions": state["arm"][:7].tolist(),
            "gripper": float(np.clip(state["gripper"][0] / 0.824033, 0, 1)),
            "instruction": self.task.get_task_description(),
            "episode_count": len(self.episodes),
            "horizon_steps": self.horizon_steps,
            "benchmark_info": {
                "revision": REVISION,
                "renderer": self.benchmark.renderer,
                "benchmark_path": self.benchmark.path,
                "house_index": self.spec.house_index,
                "cameras": [exterior, wrist],
                "second_exterior": "duplicate_first",
                "success_condition": "upstream_judge_success_oracle",
                "oracle_success": self.oracle_success,
                "physics_policy_dt_ms": self.task._n_ctrl_steps_per_policy * 2.0,
            },
        }

    def step(self, action):
        self.raw = self.task.step(action_dict(action))[0][0]
        success = bool(self.task.judge_success())
        self.oracle_success |= success
        return self.observation(), success

    def close(self):
        if self.sampler is not None:
            self.sampler.close()
            self.sampler = None


def main():
    incoming = sys.stdin.buffer
    # Native Filament writes directly to fd 1. Keep IPC on a private duplicate
    # and route both native and Python diagnostics into the simulator log.
    outgoing = os.fdopen(os.dup(sys.stdout.fileno()), "wb", buffering=0)
    os.dup2(sys.stderr.fileno(), sys.stdout.fileno())
    episode = None
    with contextlib.redirect_stdout(sys.stderr):
        try:
            setup = read_message(incoming)
            if setup.get("catalog_only"):
                from molmo_spaces.evaluation.benchmark_schema import load_all_episodes
                from molmo_spaces.molmo_spaces_constants import ASSETS_DIR, get_resource_manager

                get_resource_manager()
                counts = {
                    name: len(load_all_episodes(ASSETS_DIR / "benchmarks" / BENCHMARKS[name].path))
                    for name in setup["suites"]
                }
                write_message(outgoing, {"ok": counts})
                return
            episode = MolmoEpisode(setup)
            write_message(outgoing, {"ok": episode.observation()})
            while True:
                request = read_message(incoming)
                op = request["op"]
                if op == "close":
                    break
                if op == "reset":
                    result = episode.reset()
                elif op == "step":
                    result = episode.step(request["action"])
                elif op == "render":
                    import cv2
                    import numpy as np

                    obs = episode.observation()
                    frame = np.concatenate([obs["exterior"], obs["wrist"]], axis=1)
                    cv2.imshow("Dreamscale MolmoSpaces sim", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                    cv2.waitKey(1)
                    result = None
                else:
                    raise ValueError("Unknown simulator operation")
                write_message(outgoing, {"ok": result})
        except EOFError:
            pass
        except BaseException as exc:
            traceback.print_exc()
            write_message(outgoing, {"error": f"{type(exc).__name__}: {exc}"})
        finally:
            if episode is not None:
                episode.close()
            if "cv2" in sys.modules:
                sys.modules["cv2"].destroyAllWindows()
            outgoing.close()


if __name__ == "__main__":
    main()
