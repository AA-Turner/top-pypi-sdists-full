"""A Hugging Face Trainer job with ProbeCallback on 2 CPU processes (gloo).

    hf_job.py launch [--finish]    under `accelerate launch --num_machines 2`
    hf_job.py notebook [--finish]  calls accelerate.notebook_launcher itself

``launch``: this process is one rank of a 2-"node" job (two separate
``accelerate launch`` invocations with --machine_rank 0 / 1).
``notebook``: the script is the notebook kernel; notebook_launcher forks two
workers that train (its CPU path: torch elastic, start_method="fork").

ProbeCallback opens the run on world zero and hands (run id, epoch) to rank 1
through the process group's store (#2091); rank 1 holds a lease-only writer's
lease. World zero records what the callback was given (``rewrite_logs`` per
global step) so the test can reconcile, then update_config + log_artifact,
and with ``--finish`` probe.finish(); without it the process exit closes the
run (a forked worker's exit runs no atexit -- multiprocessing's finalizers).
"""

from __future__ import annotations

import os
import sys

import envchild

MODE = sys.argv[1]
FINISH = "--finish" in sys.argv
MAX_STEPS = 8


def train() -> None:
    import torch
    from transformers import Trainer, TrainerCallback, TrainingArguments
    from transformers.integrations.integration_utils import rewrite_logs

    import probe
    from probe.integrations.huggingface import ProbeCallback

    class Tiny(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.lin = torch.nn.Linear(4, 1)

        def forward(self, x, labels=None):
            out = self.lin(x).squeeze(-1)
            loss = torch.nn.functional.mse_loss(out, labels)
            return {"loss": loss, "logits": out}

    class Data(torch.utils.data.Dataset):
        def __init__(self) -> None:
            g = torch.Generator().manual_seed(0)
            self.x = torch.randn(64, 4, generator=g)
            self.y = self.x.sum(dim=1)

        def __len__(self) -> int:
            return len(self.x)

        def __getitem__(self, i):
            return {"x": self.x[i], "labels": self.y[i]}

    ledger: list = []
    seen: set = set()

    class Recorder(TrainerCallback):
        def on_log(self, args, state, control, logs=None, **kwargs):
            if not state.is_world_process_zero or not logs:
                return
            for key, value in rewrite_logs(logs).items():
                if isinstance(value, (int, float)) and (state.global_step, key) not in seen:
                    seen.add((state.global_step, key))
                    ledger.append([state.global_step, key, float(value)])

    cb = ProbeCallback(project=envchild.PROJECT, name=f"accelerate-{MODE}")
    args = TrainingArguments(
        output_dir=os.path.join(os.getcwd(), "out"),
        per_device_train_batch_size=4,
        max_steps=MAX_STEPS,
        logging_steps=1,
        save_strategy="no",
        report_to=[],
        use_cpu=True,
        ddp_backend="gloo",
        disable_tqdm=True,
        seed=0,
    )
    trainer = Trainer(model=Tiny(), args=args, train_dataset=Data(), callbacks=[cb, Recorder()])
    trainer.train()

    import torch.distributed as dist

    rank = dist.get_rank() if dist.is_initialized() else 0
    names = []
    run = probe.active_run()
    if trainer.is_world_process_zero():
        probe.update_config({"phase": "after-train", "mode": MODE})
        for name, path in envchild.write_artifacts(f"accelerate-{MODE}-r{rank}", big=MODE == "launch").items():
            probe.log_artifact(name, path=path)
            names.append(name)
    lease = getattr(cb, "_rank_lease", None)
    envchild.result(
        f"rank{rank}",
        rank=rank,
        run_id=str(run.id) if run is not None else (lease.run_id if lease is not None else None),
        lease_session=(lease.session_id if lease is not None else None),
        world_zero=trainer.is_world_process_zero(),
        ledger=ledger,
        artifacts=names,
        pid=os.getpid(),
        **envchild.rank_env(),
        **envchild.sdk_info(),
    )
    if FINISH and trainer.is_world_process_zero():
        probe.finish()


if MODE == "launch":
    train()
elif MODE == "notebook":
    from accelerate import notebook_launcher

    port = os.environ.get("HF_JOB_PORT", "29577")
    notebook_launcher(train, num_processes=2, use_port=port)
    envchild.result("kernel", pid=os.getpid())
else:
    raise SystemExit(f"unknown mode {MODE}")
