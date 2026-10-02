"""Probe and W&B (offline) in ONE script, the way a team migrating runs both.

    wb_job.py <order> <end> [--tb]

order: ``probe-first`` | ``wandb-first`` -- which SDK is imported AND
initialised first (each installs exit hooks at import / init).
end:   ``ok``     finish both, exit 0
       ``exit2``  sys.exit(2) with both runs open
       ``raise``  an uncaught RuntimeError with both runs open
       ``sigint`` print READY and wait: the test sends SIGINT to the process
                  group, as Ctrl-C in a terminal does
--tb:  wandb.init(sync_tensorboard=True) and a torch SummaryWriter logging
       beside both SDKs.
"""

from __future__ import annotations

import os
import sys
import time

import envchild

order, end = sys.argv[1], sys.argv[2]
tb = "--tb" in sys.argv
STEPS = 12
TAG = f"wb-{order}-{end}{'-tb' if tb else ''}"

if order == "probe-first":
    import probe
    import wandb
else:
    import wandb
    import probe


def init_probe():
    return probe.init(project=envchild.PROJECT, name=TAG, config={"lr": 0.01, "order": order})


def init_wandb():
    return wandb.init(
        project="env-matrix", name=TAG, mode="offline", dir=os.getcwd(),
        config={"lr": 0.01, "order": order}, sync_tensorboard=tb,
    )


if order == "probe-first":
    prun, wrun = init_probe(), init_wandb()
else:
    wrun, prun = init_wandb(), init_probe()

hooks = {
    "excepthook": repr(sys.excepthook),
    "sigint": repr(__import__("signal").getsignal(2)),
    "sigterm": repr(__import__("signal").getsignal(15)),
}

writer = None
if tb:
    from torch.utils.tensorboard import SummaryWriter

    writer = SummaryWriter(log_dir=os.path.join(os.getcwd(), "tb"))

for step in range(STEPS):
    metrics = envchild.payload(step)
    probe.log(metrics, step=step)
    wandb.log(metrics, step=step)
    if writer is not None:
        writer.add_scalar("tb/loss", envchild.value("tb/loss", step), step)
probe.update_config({"phase": "after-loop"})
wandb.config.update({"phase": "after-loop"})
names = []
for name, path in envchild.write_artifacts(TAG, big=(end == "ok" and not tb)).items():
    probe.log_artifact(name, path=path)
    names.append(name)
if writer is not None:
    writer.flush()
    writer.close()

envchild.result(
    "wb", run_id=str(prun.id), wandb_id=wrun.id, wandb_dir=wrun.dir, artifacts=names,
    hooks=hooks, wandb_version=wandb.__version__, **envchild.sdk_info(),
)

if end == "ok":
    if order == "probe-first":
        wandb.finish()
        probe.finish()
    else:
        probe.finish()
        wandb.finish()
    sys.exit(0)
if end == "exit2":
    sys.exit(2)
if end == "raise":
    raise RuntimeError("env-matrix: the training loop blew up")
if end == "sigint":
    print("READY", flush=True)
    deadline = time.time() + 120
    while time.time() < deadline:
        time.sleep(0.1)
    print("NO-SIGNAL", flush=True)
    sys.exit(3)
