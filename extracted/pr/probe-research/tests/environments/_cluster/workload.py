#!/usr/bin/env python3
"""The customer loop, the way a researcher's training script writes it.

Runs INSIDE a test container under the released probe-research. One process is one
rank: under srun (SLURM_PROCID/SLURM_NTASKS), torchrun (RANK/WORLD_SIZE) or alone.

  init -> DDP (torch gloo) -> per step log() with nested dicts -> update_config
  -> log_artifact (small file; one > 64 MiB with --big-mb) -> finish

Ground truth for the test: after every ``log()`` RETURNS, the flattened
(step, key, value) rows it was given are appended to ``<out>/logged-rank<R>.jsonl``
(line-buffered, fsynced), so a test that kills this process knows exactly which
points the SDK had accepted. ``<out>/result-rank<R>-<attempt>.json`` is written at
the end; ``<out>/events-rank<R>.jsonl`` gets one line per milestone.

A requeued attempt (``--resume``) continues from ``<out>/ckpt-rank<R>.json``, the
last step this rank completed, as a checkpointed trainer would.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import socket
import sys
import time
from datetime import timedelta
from pathlib import Path


#: A single log() call slower than this is reported as a `slow_log` event.
SLOW_LOG_SECONDS = 1.0


def _rank_world() -> tuple[int, int]:
    for rank_var, world_var in (("RANK", "WORLD_SIZE"), ("SLURM_PROCID", "SLURM_NTASKS")):
        if os.environ.get(rank_var) is not None and os.environ.get(world_var):
            return int(os.environ[rank_var]), int(os.environ[world_var])
    return 0, 1


def _flatten(prefix: str, value, out: dict) -> None:
    if isinstance(value, dict):
        for k, v in value.items():
            _flatten(f"{prefix}/{k}" if prefix else str(k), v, out)
    else:
        out[prefix] = value


class Recorder:
    def __init__(self, out: Path, rank: int, attempt: str):
        self.out = out
        self.rank = rank
        self.attempt = attempt
        out.mkdir(parents=True, exist_ok=True)
        self._logged = open(out / f"logged-rank{rank}.jsonl", "a", buffering=1)
        # Per rank: O_APPEND is not atomic across NFS clients, so two nodes appending
        # to one file overwrite each other's lines.
        self._events = open(out / f"events-rank{rank}.jsonl", "a", buffering=1)

    def logged(self, step: int, payload: dict) -> None:
        flat: dict = {}
        _flatten("", payload, flat)
        for key, value in flat.items():
            self._logged.write(json.dumps({"step": step, "key": key, "value": value}) + "\n")
        self._logged.flush()
        os.fsync(self._logged.fileno())

    def event(self, what: str, **kw) -> None:
        row = {"t": time.time(), "rank": self.rank, "attempt": self.attempt,
               "host": socket.gethostname(), "pid": os.getpid(), "event": what, **kw}
        self._events.write(json.dumps(row) + "\n")
        self._events.flush()
        os.fsync(self._events.fileno())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--steps", type=int, default=30)
    ap.add_argument("--sleep", type=float, default=0.0, help="seconds per step")
    ap.add_argument("--project")
    ap.add_argument("--name")
    ap.add_argument("--mode", default=None, help="probe.init(mode=...): online|offline")
    ap.add_argument("--big-mb", type=int, default=0, help="also log one artifact this big")
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--no-ddp", action="store_true")
    ap.add_argument("--hold-at-step", type=int, default=-1,
                    help="write <out>/holding-rank<R> at this step and keep stepping slowly")
    args = ap.parse_args()

    rank, world = _rank_world()
    attempt = os.environ.get("SLURM_RESTART_COUNT", "0")
    out = Path(args.out)
    rec = Recorder(out, rank, attempt)
    rec.event("start", world=world, env={k: v for k, v in os.environ.items()
                                          if k.startswith(("SLURM_JOB_ID", "SLURM_PROCID",
                                                           "SLURM_RESTART", "PROBE_RUN",
                                                           "HTTP_PROXY", "HTTPS_PROXY",
                                                           "RANK", "WORLD_SIZE", "MASTER"))})

    start_step = 0
    ckpt = out / f"ckpt-rank{rank}.json"
    if args.resume and ckpt.exists():
        start_step = json.loads(ckpt.read_text())["step"] + 1

    import torch

    dist = None
    if world > 1 and not args.no_ddp:
        import torch.distributed as dist

        t = time.time()
        dist.init_process_group("gloo", init_method="env://", rank=rank, world_size=world,
                                timeout=timedelta(seconds=60))
        rec.event("ddp_ready", seconds=round(time.time() - t, 2))

    import probe

    t = time.time()
    if os.environ.get("PROBE_RUN_ID"):
        # A launcher opened the run (probe exec / sbatch --export): join it.
        run = probe.init(mode=args.mode)
    else:
        run = probe.init(project=args.project, name=args.name, mode=args.mode,
                         config={"lr": 0.05, "model": {"kind": "linear", "width": 8},
                                 "world": world})
    init_s = time.time() - t
    rec.event("init", run_id=run.id, seconds=round(init_s, 2),
              sdk=getattr(probe, "__version__", None))

    torch.manual_seed(1234 + rank)
    model = torch.nn.Linear(8, 1)
    if dist is not None:
        model = torch.nn.parallel.DistributedDataParallel(model)
    opt = torch.optim.SGD(model.parameters(), lr=0.05)
    x = torch.randn(64, 8)
    y = x.sum(dim=1, keepdim=True)

    log_times: list[float] = []
    for step in range(start_step, args.steps):
        t0 = time.time()
        opt.zero_grad()
        loss = torch.nn.functional.mse_loss(model(x), y)
        loss.backward()
        opt.step()
        value = round(float(loss.item()), 6)
        payload = {f"rank{rank}": {"loss": value, "step_time": round(time.time() - t0, 6)}}
        if rank == 0:
            payload["loss"] = value
            payload["opt"] = {"lr": 0.05, "grad_norm": round(float(sum(
                p.grad.norm() ** 2 for p in model.parameters()) ** 0.5), 6)}
        t_log = time.time()
        run.log(payload, step=step)
        log_s = time.time() - t_log
        log_times.append(log_s)
        if log_s > SLOW_LOG_SECONDS:
            # log() must never hold up the training loop; say so the moment it does.
            rec.event("slow_log", step=step, seconds=round(log_s, 3))
        rec.logged(step, payload)
        ckpt.write_text(json.dumps({"step": step}))
        if step == args.hold_at_step:
            (out / f"holding-rank{rank}").write_text(str(step))
            rec.event("holding", step=step)
        if args.sleep:
            time.sleep(args.sleep)
    ordered = sorted(log_times) or [0.0]
    rec.event("trained", last_step=args.steps - 1, log_calls=len(log_times),
              log_p50=round(ordered[len(ordered) // 2], 4),
              log_p99=round(ordered[min(len(ordered) - 1, int(len(ordered) * 0.99))], 4),
              log_max=round(ordered[-1], 4))

    artifacts = []
    if rank == 0:
        run.update_config({"phase": "trained", "optim": {"name": "sgd", "momentum": 0.0}})
        small = out / "summary.json"
        small.write_text(json.dumps({"steps": args.steps, "world": world, "final_loss": value}))
        run.log_artifact("summary.json", path=str(small))
        artifacts.append({"name": "summary.json",
                          "sha256": hashlib.sha256(small.read_bytes()).hexdigest(),
                          "size": small.stat().st_size})
        if args.big_mb:
            big = out / "weights.bin"
            with open(big, "wb") as fh:
                block = os.urandom(1 << 20)
                for i in range(args.big_mb):
                    fh.write(block[:-8] + i.to_bytes(8, "little"))
            t = time.time()
            run.log_artifact("weights.bin", path=str(big))
            artifacts.append({"name": "weights.bin", "size": big.stat().st_size,
                              "sha256": hashlib.sha256(big.read_bytes()).hexdigest(),
                              "seconds": round(time.time() - t, 2)})
    rec.event("artifacts", artifacts=artifacts)

    if dist is not None:
        dist.barrier()
    t = time.time()
    probe.finish()
    finish_s = time.time() - t
    rec.event("finished", seconds=round(finish_s, 2))
    result = {
        "run_id": run.id, "rank": rank, "world": world, "attempt": attempt,
        "host": socket.gethostname(), "start_step": start_step, "steps": args.steps,
        "init_seconds": round(init_s, 2), "finish_seconds": round(finish_s, 2),
        "artifacts": artifacts,
    }
    (out / f"result-rank{rank}-{attempt}.json").write_text(json.dumps(result))
    if dist is not None:
        dist.destroy_process_group()
    return 0


if __name__ == "__main__":
    sys.exit(main())
