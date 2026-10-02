"""Ray Train: a TorchTrainer with 2 CPU workers that Ray starts itself.

    ray_train_job.py <ok|kill>

The documented shape (instrument-code skill, "Ray"): the DRIVER opens the
run with ``probe.init(project=...)`` and passes (run id, epoch) to the
workers through ``runtime_env={"env_vars": ...}`` -- Ray workers do not
inherit the submitter's environment in general. Each worker calls
``probe.init()`` (attach), logs from world rank 0 only, reports to Ray, and
calls ``probe.finish()``. The driver then records config and artifacts and
finishes.

``kill``: world rank 1 SIGKILLs its own actor process at step KILL_AT (an OOM
kill, a preempted node). FailureConfig(max_failures=0): Ray aborts the whole
worker group and ``trainer.fit()`` raises into the driver, which -- like most
scripts -- does not catch it.
"""

from __future__ import annotations

import os
import signal
import sys
import time

import envchild

MODE = sys.argv[1]
STEPS = 10
KILL_AT = 4


def train_loop(config: dict) -> None:
    import torch

    import envchild
    import probe
    import ray.train
    import ray.train.torch

    ctx = ray.train.get_context()
    rank = ctx.get_world_rank()
    run = probe.init()
    envchild.result(
        f"worker{rank}-start", rank=rank, run_id=str(run.id), pid=os.getpid(),
        **envchild.rank_env(), **envchild.sdk_info(),
    )
    model = ray.train.torch.prepare_model(torch.nn.Linear(4, 1))
    opt = torch.optim.SGD(model.parameters(), lr=0.05)
    g = torch.Generator().manual_seed(rank)
    for step in range(STEPS):
        x = torch.randn(8, 4, generator=g)
        loss = torch.nn.functional.mse_loss(model(x).squeeze(-1), x.sum(dim=1))
        opt.zero_grad()
        loss.backward()
        opt.step()
        if rank == 0:
            probe.log(envchild.payload(step), step=step)
            envchild.result("worker0-logged", step=step)
        if config["mode"] == "kill" and rank == 1 and step == KILL_AT:
            envchild.result("worker1-killing", pid=os.getpid(), step=step)
            os.kill(os.getpid(), signal.SIGKILL)
        ray.train.report({"loss": float(loss), "step": step})
        time.sleep(0.2)
    probe.finish()
    envchild.result(f"worker{rank}-done", rank=rank, run_id=str(run.id), pid=os.getpid())


def main() -> None:
    import ray
    from ray.train import FailureConfig, RunConfig, ScalingConfig
    from ray.train.torch import TorchTrainer

    import probe

    run = probe.init(project=envchild.PROJECT, name=f"ray-train-{MODE}", config={"workers": 2})
    envchild.result("driver-start", run_id=str(run.id), write_epoch=run.write_epoch, **envchild.sdk_info())
    handoff = {"PROBE_RUN_ID": str(run.id)}
    if run.write_epoch is not None:
        handoff["PROBE_RUN_EPOCH"] = str(run.write_epoch)
    for key in ("PROBE_BASE_URL", "PROBE_TOKEN", "PROBE_ENV_RESULTS_FILE", "PROBE_ENV_PROJECT", "PYTHONPATH"):
        if os.environ.get(key):
            handoff[key] = os.environ[key]
    ray.init(
        num_cpus=4,
        include_dashboard=False,
        _temp_dir=os.environ["RAY_SHORT_TMP"],
        runtime_env={"env_vars": handoff},
    )
    trainer = TorchTrainer(
        train_loop,
        train_loop_config={"mode": MODE},
        scaling_config=ScalingConfig(num_workers=2, use_gpu=False),
        run_config=RunConfig(
            name=f"ray-train-{MODE}",
            storage_path=os.path.join(os.getcwd(), "ray_results"),
            failure_config=FailureConfig(max_failures=0),
        ),
    )
    envchild.result("driver-fit", run_id=str(run.id))
    trainer.fit()  # `kill`: raises TrainingFailedError, uncaught
    probe.update_config({"phase": "after-fit"})
    names = []
    for name, path in envchild.write_artifacts("ray-train", big=True).items():
        probe.log_artifact(name, path=path)
        names.append(name)
    probe.finish()
    envchild.result("driver-done", run_id=str(run.id), artifacts=names, ray_version=ray.__version__)
    ray.shutdown()


if __name__ == "__main__":
    main()
