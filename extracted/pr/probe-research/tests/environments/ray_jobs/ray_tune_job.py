"""Ray Tune: 4 trials, one Probe run per trial opened inside the trainable.

    ray_tune_job.py [function|class]

* trials 0 and 1 run to the end; trial 0 calls probe.finish(), trial 1
  just returns (most trainables never close their run);
* trial 2 SIGKILLs its own actor at step KILL_AT (an OOM kill): Tune marks it
  ERROR (max_failures=0) and carries on;
* trial 3 is STOPPED by the scheduler after its STOP_AFTER-th result -- the
  way ASHA / median stopping prune a bad trial -- so its function never gets
  to probe.finish().

``function`` (the default): a function trainable, which Ray runs on a thread
of the trial's actor; Ray ends trials 1 and 3 with ``sys.exit(0)`` on that
thread, from the ``tune.report()`` they wait in, and kills the actor's
process group 200 ms after its SIGTERM. ``class``: a ``tune.Trainable`` whose
``setup()`` opens the run and whose ``cleanup()`` -- which Tune runs, and
waits for, whenever it stops a trial -- calls probe.finish(); every trial
closes there, trial 3 too.

The driver opens no Probe run: the trials are the runs.
"""

from __future__ import annotations

import os
import signal
import sys
import time

import envchild

STEPS = 10
KILL_AT = 3
STOP_AFTER = 3


def trainable(config: dict) -> None:
    import envchild
    import probe
    from ray import tune

    trial = config["trial"]
    run = probe.init(
        project=envchild.PROJECT, name=f"ray-tune-trial-{trial}", config={"trial": trial}
    )
    envchild.result(f"trial{trial}-start", trial=trial, run_id=str(run.id), pid=os.getpid(), **envchild.sdk_info())
    for step in range(STEPS):
        probe.log(envchild.payload(step, salt=trial), step=step)
        envchild.result(f"trial{trial}-logged", trial=trial, step=step)
        if trial == 2 and step == KILL_AT:
            os.kill(os.getpid(), signal.SIGKILL)
        tune.report({"score": envchild.value("score", step, trial), "step": step})
        time.sleep(0.3)
    if trial == 0:
        probe.finish()
    envchild.result(f"trial{trial}-done", trial=trial, run_id=str(run.id))


def trainable_class():
    from ray import tune

    class TrialTrainable(tune.Trainable):
        def setup(self, config: dict) -> None:
            import envchild
            import probe

            self.trial = config["trial"]
            self.step_index = 0
            run = probe.init(
                project=envchild.PROJECT, name=f"ray-tune-trial-{self.trial}", config={"trial": self.trial}
            )
            envchild.result(
                f"trial{self.trial}-start", trial=self.trial, run_id=str(run.id), pid=os.getpid(),
                **envchild.sdk_info(),
            )

        def step(self) -> dict:
            import envchild
            import probe

            step, trial = self.step_index, self.trial
            probe.log(envchild.payload(step, salt=trial), step=step)
            envchild.result(f"trial{trial}-logged", trial=trial, step=step)
            if trial == 2 and step == KILL_AT:
                os.kill(os.getpid(), signal.SIGKILL)
            self.step_index += 1
            time.sleep(0.3)
            return {
                "score": envchild.value("score", step, trial), "step": step,
                "done": self.step_index >= STEPS,
            }

        def cleanup(self) -> None:
            import probe

            probe.finish()

        # Tune checkpoints a class trainable when it ends; there is nothing to keep.
        def save_checkpoint(self, checkpoint_dir: str) -> None:
            return None

        def load_checkpoint(self, checkpoint) -> None:
            return None

    return TrialTrainable


def main() -> None:
    import ray
    from ray import tune
    from ray.tune.schedulers import FIFOScheduler, TrialScheduler

    api = sys.argv[1] if len(sys.argv) > 1 else "function"

    class StopTrialThree(FIFOScheduler):
        """Stops trial 3 after STOP_AFTER results, deterministically."""

        def on_trial_result(self, tune_controller, trial, result):
            if trial.config["trial"] == 3 and result.get("training_iteration", 0) >= STOP_AFTER:
                return TrialScheduler.STOP
            return TrialScheduler.CONTINUE

    env_vars = {
        key: os.environ[key]
        for key in ("PROBE_BASE_URL", "PROBE_TOKEN", "PROBE_ENV_RESULTS_FILE", "PROBE_ENV_PROJECT", "PYTHONPATH")
        if os.environ.get(key)
    }
    ray.init(
        num_cpus=4, include_dashboard=False, _temp_dir=os.environ["RAY_SHORT_TMP"],
        runtime_env={"env_vars": env_vars},
    )
    tuner = tune.Tuner(
        trainable if api == "function" else trainable_class(),
        param_space={"trial": tune.grid_search([0, 1, 2, 3])},
        tune_config=tune.TuneConfig(scheduler=StopTrialThree(), max_concurrent_trials=4),
        run_config=tune.RunConfig(
            name="ray-tune-env-matrix",
            storage_path=os.path.join(os.getcwd(), "ray_results"),
            failure_config=tune.FailureConfig(max_failures=0),
        ),
    )
    results = tuner.fit()
    states = {}
    for res in results:
        states[res.config["trial"]] = {
            "error": type(res.error).__name__ if res.error else None,
            "iterations": (res.metrics or {}).get("training_iteration"),
        }
    envchild.result("tune-done", states=states, ray_version=ray.__version__)
    ray.shutdown()


if __name__ == "__main__":
    main()
