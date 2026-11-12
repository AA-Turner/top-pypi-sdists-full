"""Native abc_sim worker. Executed by an isolated Python; no SDK/cloud dependencies.

Local pipe messages use pickle only between our own parent and child processes.
Model and network messages never enter this channel. stdout is reserved for IPC.

One abc_sim world (amazon-far/abc), stepped one 14-value action at a time as upstream's eval
does (``abc_minimal/sim_env.py``). Policy coordinates are abc_sim's own: left six joints (rad)
and gripper (0 closed to 1 open), then right. Images cross the pipe as height x width x 3 RGB.

The cameras are free-running, as a robot's are: a thread renders the newest physics state as
fast as this machine can, and a reader takes the newest frames without waiting. The scenes
render with a large shadow map and 16 samples a pixel, about 55 ms for the three views on a
laptop; a model that plans every other tick would otherwise stop the world to wait for them.
"""

from __future__ import annotations

import contextlib
import sys
import threading
import time

if __package__:
    from .native_process import read_message, write_message
else:
    from native_process import read_message, write_message


def episode_over(task_eval):
    """Upstream's ``rollout_over``: the first success ends an episode, except on a
    maintenance task (ball tray), which is over once it has failed."""
    if "ever_failed" in task_eval:
        return bool(task_eval["ever_failed"])
    return bool(task_eval.get("ever_success", False))


def plain_scalars(task_eval):
    """The evaluator's scalar metrics as Python values (numpy scalars do not cross the pipe:
    the SDK's numpy may not load them)."""
    plain = {}
    for key, value in task_eval.items():
        if getattr(value, "ndim", None) == 0:
            value = value.item()
        if isinstance(value, (bool, int, float, str)):
            plain[key] = value
    return plain


class Cameras:
    """The station's cameras, rendered off the physics thread with MuJoCo's rasterizer exactly
    as abc_sim's own ``mujoco`` camera backend does (one Renderer on the scene's model, one
    ``update_scene`` and ``render`` a camera).

    ``publish`` hands over a copy of the physics state after every step and reset; the thread
    renders the newest one it has not shown yet (a state published while it renders replaces
    the one waiting). ``frames`` returns the newest frames, or waits for those of a given
    state.
    """

    def __init__(self, mujoco, names, height, width):
        self._mujoco, self._names, self._size = mujoco, tuple(names), (height, width)
        self._ready = threading.Condition()
        self._model = None
        self._pool = []  # spare MjData of the current model
        self._staged = None  # (model, data, stamp): the newest state, not rendered yet
        self._frames = None
        self._stamp = 0  # the newest published state
        self._shown = 0  # the state the frames show
        self._rendered = 0
        self._render_s = 0.0
        self._error = None
        self._closed = False
        self._thread = threading.Thread(target=self._run, name="abc-cameras", daemon=True)
        self._thread.start()

    def publish(self, model, data):
        """The cameras see this physics state next. Returns its stamp."""
        with self._ready:
            if model is not self._model:
                # A reset that rebuilt the scene (other bottles, other sizes): new buffers.
                self._model, self._pool = model, []
            copy = self._pool.pop() if self._pool else self._mujoco.MjData(model)
            self._mujoco.mj_copyData(copy, model, data)
            if self._staged is not None and self._staged[0] is model:
                self._pool.append(self._staged[1])
            self._stamp += 1
            self._staged = (model, copy, self._stamp)
            self._ready.notify_all()
            return self._stamp

    def frames(self, at_least=None, timeout_s=120.0):
        """(frames by camera, how many states behind the newest they are). ``at_least``: wait
        for the frames of that state or a newer one."""
        deadline = time.monotonic() + timeout_s
        with self._ready:
            while self._error is None and (
                self._frames is None or (at_least is not None and self._shown < at_least)
            ):
                if not self._ready.wait(max(0.0, deadline - time.monotonic())):
                    raise TimeoutError("the simulator's cameras did not render in time")
            if self._error is not None:
                raise RuntimeError(f"the simulator's cameras failed: {self._error}")
            return self._frames, self._stamp - self._shown

    def stats(self):
        with self._ready:
            return {"camera_frames": self._rendered,
                    "camera_render_ms": (1000.0 * self._render_s / self._rendered
                                         if self._rendered else None)}

    def close(self):
        with self._ready:
            self._closed = True
            self._ready.notify_all()
        self._thread.join(timeout=10)

    def _run(self):
        renderer = rendered_model = None
        height, width = self._size
        try:
            while True:
                with self._ready:
                    while self._staged is None and not self._closed:
                        self._ready.wait()
                    if self._closed:
                        return
                    model, data, stamp = self._staged
                    self._staged = None
                if model is not rendered_model:
                    if renderer is not None:
                        renderer.close()
                    # Created and used on this thread: an OpenGL context belongs to one.
                    renderer = self._mujoco.Renderer(model, height=height, width=width)
                    rendered_model = model
                started = time.perf_counter()
                frames = {}
                for name in self._names:
                    renderer.update_scene(data, camera=name)
                    frames[name] = renderer.render().copy()
                elapsed = time.perf_counter() - started
                with self._ready:
                    self._frames, self._shown = frames, stamp
                    self._rendered += 1
                    self._render_s += elapsed
                    if model is self._model:
                        self._pool.append(data)
                    self._ready.notify_all()
        except Exception as exc:  # surfaced to the next reader: a dead thread must not hang it
            with self._ready:
                self._error = f"{type(exc).__name__}: {exc}"
                self._ready.notify_all()
        finally:
            if renderer is not None:
                with contextlib.suppress(Exception):
                    renderer.close()


def main():
    incoming, outgoing = sys.stdin.buffer, sys.stdout.buffer
    env = cameras = None
    with contextlib.redirect_stdout(sys.stderr):
        try:
            setup = read_message(incoming)
            sys.path.insert(0, setup["source"])
            import abc_sim
            import mujoco
            import numpy as np
            from abc_sim.randomization.core import RandomizationSamplingError

            spec = abc_sim.get_task_spec(setup["task"])
            names = tuple(setup["cameras"])
            height, width = setup["image_size"]
            # The canonical task name, not its scene: shared scenes attach the right
            # evaluator and prompt only when the env knows which task it runs. The env
            # renders nothing itself: the cameras do, from copies of its state.
            env = abc_sim.make_env(
                task=spec.name, prompt=spec.prompt, render_cameras=False,
                camera_backend="mujoco", camera_height=height, camera_width=width,
            )
            cameras = Cameras(mujoco, names, height, width)
            recorded = []
            episode = {}

            def state():
                return [float(value) for value in env.get_state()]

            def reset(seed):
                # Every episode starts from the station's home pose (upstream's eval carries
                # the last episode's arm pose into the next: its worlds depend on their order).
                env.forget_arm_state()
                try:
                    obs, _ = env.reset(seed=seed, randomize=True)
                except RandomizationSamplingError:
                    # Upstream's eval resamples a seed whose scene cannot be placed.
                    seed += 100_000
                    obs, _ = env.reset(seed=seed, randomize=True)
                recorded.clear()
                episode.update(seed=seed, prompt=str(obs["prompt"]), max_reward=0.0)
                # The episode's first frames are of its own scene, not the last one's.
                frames, _ = cameras.frames(at_least=cameras.publish(env.model, env.data))
                return {"state": state(), "images": frames, "instruction": episode["prompt"],
                        "seed": seed, "task": spec.name,
                        "scored": spec.evaluator_name is not None}

            def evaluate():
                result = env.evaluate_task()
                if result is None:
                    return {"reward": 0.0, "success": False, "ever_success": False}
                return result.to_info(squeeze=True)

            write_message(outgoing, {"ok": reset(int(setup["seed"]))})
            while True:
                request = read_message(incoming)
                op = request["op"]
                if op == "close":
                    break
                if op == "reset":
                    result = reset(int(request["seed"]))
                elif op == "step":
                    action = np.asarray(request["action"], dtype=np.float32)
                    if action.shape != (14,) or not np.isfinite(action).all():
                        raise ValueError("ABC requires fourteen finite action values")
                    env.step(action, render_obs=False)
                    cameras.publish(env.model, env.data)
                    task_eval = evaluate()
                    episode["max_reward"] = max(
                        episode["max_reward"], float(task_eval.get("reward", 0.0)))
                    result = {
                        "state": state(),
                        "over": episode_over(task_eval),
                        "success": bool(task_eval.get("ever_success", False)),
                        "reward": float(task_eval.get("reward", 0.0)),
                        "max_reward": episode["max_reward"],
                        "eval": plain_scalars(task_eval),
                    }
                elif op == "observe":
                    # The measured joints now and the cameras' newest frames; ``fresh`` waits
                    # for the frames of this very state (a world paused to plan).
                    frames, behind = cameras.frames(
                        at_least=cameras.publish(env.model, env.data)
                        if request.get("fresh") else None)
                    result = {"state": state(), "images": frames, "frames_behind": behind}
                elif op == "frame":
                    # The viewer's and the video's frame: the three cameras side by side,
                    # composed here so arrays never cross the pipe for them.
                    frames, _ = cameras.frames()
                    frame = np.concatenate([frames[name] for name in names], axis=1)
                    if request.get("record"):
                        recorded.append(frame)
                    if request.get("show"):
                        import cv2

                        cv2.imshow("Dreamscale ABC sim",
                                   cv2.cvtColor(np.repeat(np.repeat(frame, 2, 0), 2, 1),
                                                cv2.COLOR_RGB2BGR))
                        cv2.waitKey(1)
                    result = len(recorded)
                elif op == "video":
                    if recorded:
                        import imageio.v3 as iio

                        iio.imwrite(request["path"], np.stack(recorded), plugin="pyav",
                                    codec="libx264", fps=float(request["fps"]))
                    result = len(recorded)
                elif op == "stats":
                    result = cameras.stats()
                else:
                    raise ValueError("unknown simulator operation")
                write_message(outgoing, {"ok": result})
        except EOFError:
            pass
        except Exception as exc:
            write_message(outgoing, {"error": f"{type(exc).__name__}: {exc}"})
        finally:
            if cameras is not None:
                cameras.close()
            if env is not None:
                env.close()
            if "cv2" in sys.modules:
                sys.modules["cv2"].destroyAllWindows()


if __name__ == "__main__":
    main()
