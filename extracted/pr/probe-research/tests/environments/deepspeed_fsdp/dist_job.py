"""A 2-rank CPU training job (gloo): torch FSDP or DeepSpeed ZeRO-1.

    torchrun --nproc_per_node 2 dist_job.py <fsdp|deepspeed> <exec|broadcast>

How the ranks find the run (``handoff``):

* ``exec``      -- the job runs under ``probe exec -- torchrun ...``: the
                   launcher opened the run and exported PROBE_RUN_ID, and every
                   rank calls ``probe.init()`` with no arguments.
* ``broadcast`` -- plain torchrun: rank 0 calls ``probe.init(project=...)``
                   and broadcasts (run id, write epoch) over the process
                   group; every other rank exports them and calls
                   ``probe.init()``.

Only rank 0 logs metrics, config and artifacts. Every rank finishes.
"""

from __future__ import annotations

import os
import sys

import torch
import torch.distributed as dist

import envchild
import probe

fw, handoff = sys.argv[1], sys.argv[2]
STEPS = int(os.environ.get("DIST_STEPS", "20"))

if fw == "deepspeed":
    import deepspeed

    deepspeed.init_distributed(dist_backend="gloo")
else:
    dist.init_process_group("gloo")
rank, world = dist.get_rank(), dist.get_world_size()

if handoff == "exec":
    run = probe.init()
else:
    ids = [None, None]
    if rank == 0:
        run = probe.init(project=envchild.PROJECT, name=f"{fw}-broadcast", config={"fw": fw})
        ids = [str(run.id), run.write_epoch]
    dist.broadcast_object_list(ids, src=0)
    if rank != 0:
        os.environ["PROBE_RUN_ID"] = ids[0]
        if ids[1] is not None:
            os.environ["PROBE_RUN_EPOCH"] = str(ids[1])
        run = probe.init()

torch.manual_seed(0)
model = torch.nn.Sequential(torch.nn.Linear(16, 32), torch.nn.ReLU(), torch.nn.Linear(32, 1))
if fw == "deepspeed":
    engine, optimizer, _, _ = deepspeed.initialize(
        model=model,
        optimizer=torch.optim.SGD(model.parameters(), lr=0.05),
        config={
            "train_micro_batch_size_per_gpu": 8,
            "gradient_accumulation_steps": 1,
            "zero_optimization": {"stage": 1},
            "zero_allow_untested_optimizer": True,
            "steps_per_print": 10_000,
        },
    )
    step_fn_model = engine
else:
    from torch.distributed.fsdp import FullyShardedDataParallel as FSDP

    step_fn_model = FSDP(model, device_id=torch.device("cpu"), use_orig_params=True)
    optimizer = torch.optim.SGD(step_fn_model.parameters(), lr=0.05)

g = torch.Generator().manual_seed(1 + rank)
ledger = []
for step in range(STEPS):
    x = torch.randn(8, 16, generator=g)
    y = x.sum(dim=1, keepdim=True)
    loss = torch.nn.functional.mse_loss(step_fn_model(x), y)
    if fw == "deepspeed":
        engine.backward(loss)
        engine.step()
    else:
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    mean = loss.detach().clone()
    dist.all_reduce(mean)
    mean /= world
    if rank == 0:
        probe.log({"train": {"loss": mean, "local_loss": loss.detach()}, "world": world}, step=step)
        ledger += [
            [step, "train/loss", float(mean)],
            [step, "train/local_loss", float(loss.detach())],
            [step, "world", float(world)],
        ]

names = []
if rank == 0:
    probe.update_config({"phase": "after-loop", "zero": 1 if fw == "deepspeed" else "fsdp"})
    for name, path in envchild.write_artifacts(f"{fw}-{handoff}", big=(handoff == "exec")).items():
        probe.log_artifact(name, path=path)
        names.append(name)

dist.barrier()
finish_raised = None
try:
    probe.finish()
except BaseException as exc:  # noqa: BLE001
    finish_raised = f"{type(exc).__name__}: {exc}"
envchild.result(
    f"rank{rank}", rank=rank, world=world, run_id=str(run.id), write_epoch=run.write_epoch,
    ledger=ledger, artifacts=names, finish_raised=finish_raised, fw=fw,
    torch_version=torch.__version__,
    ds_version=(sys.modules["deepspeed"].__version__ if "deepspeed" in sys.modules else None),
    **envchild.rank_env(), **envchild.sdk_info(),
)
dist.destroy_process_group()
