# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A diffusion policy's classifier-free guidance split between two processes: the model it calls with its unconditioned
and conditioned inputs together - one batch, a half for each - runs one half in each process, on a GPU of its own, and
the two outputs are gathered back, so the policy's own code gets the whole batch's output as it did.

    torchrun --nproc-per-node 2 my_server.py         # or one process on each of two machines: WORLD_SIZE 2
    from sequence_ai.engine import cfg_parallel

    patches = cfg_parallel.install(policy_user, ["model.transformer"])     # in both processes, alike
    cfg_parallel.uninstall(patches)                                       # the model's own forward again

In one sentence: the group of the two processes (torch.distributed: made from torchrun's environment where the model
made none, gloo for tensors on the CPU, NCCL for those on a GPU) → each call of a module it is installed on whose
tensors lead with one even batch is cut along it: the first half runs on rank 0, the second - rank 0's own, sent to
it - on rank 1, every other value as given → each output that leads with the half is gathered from both, rank 0's half
first, into what one process gives for the whole batch → a call with no such batch runs whole on both. Under serve() of
two processes, trial() tries it on rank 0's warm-up: the module census() finds, kept where the policy's outputs stay
within the tolerance given and its acts are at least 10% faster.

WHY the batch cut in half: a pipeline doubles its batch for the guidance, the unconditioned half first and the
conditioned one after (diffusers: torch.cat([latents] * 2)), and in the model each half's rows are computed apart from
the other's; so each process does half of the model's work, and the two halves are the whole batch's output.
WHY a switch that changes the outputs (optimize's tolerance): half a batch's matrix products can be computed in another
order than the whole batch's, by other kernels, so its outputs may differ from one process's in their last bits.
WHY both processes decide alike what to cut: each sees the same call - the same observation, sent to every rank
(engine/ranks.py) - and cuts by its shapes alone; a gather that one process made and the other did not would wait
forever.
WHY rank 1's half is sent from rank 0: what a policy draws - a diffusion's noise, by torch's generator or NumPy's - is
drawn in each process apart, and NumPy's is seeded by each from the system at its start; rank 1 computing its half of
its own draws would answer for other noise than rank 0's. Sent, both halves are of rank 0's inputs, whatever rank 1
drew; what it costs is timed in the trial with the rest.

Adapted from xdit-project/xDiT xfuser/model_executor/pipelines/base_pipeline.py (Apache-2.0), with its
pipeline_stable_diffusion_3.py: see THIRD_PARTY_NOTICES.md. Changed here: the split made around a model's call, not in
a pipeline's own loop, so a policy's model is split with no change to its code; the batch cut in half along its first
dimension, where xDiT hands each rank the negative or the positive prompt; the two outputs gathered back into the whole
batch's, where xDiT hands the two halves to the guidance.
"""
from __future__ import annotations

from typing import Any, Callable, Optional

from .fused import _ABSENT, Patch, uninstall

__all__ = ["WORLD", "group", "install", "uninstall", "batch_of", "census", "trial"]

WORLD = 2           # the processes the batch is cut between: its unconditioned half and its conditioned one


def group(backend: Optional[str] = None) -> tuple:
    """The group the two processes split the batch in: torch.distributed's own, made from torchrun's environment
    (RANK, WORLD_SIZE, MASTER_ADDR, MASTER_PORT) where the model made none - gloo for tensors on the CPU, NCCL for those
    on a GPU where there is one - and (its rank, its size). ValueError where it is not of two."""
    import torch
    import torch.distributed as dist

    if not dist.is_initialized():
        backend = backend or ("cpu:gloo,cuda:nccl" if torch.cuda.is_available() else "gloo")
        dist.init_process_group(backend=backend, init_method="env://")
    size = dist.get_world_size()
    if size != WORLD:
        raise ValueError(f"cfg_parallel cuts a batch between {WORLD} processes, and torch.distributed's group has "
                         f"{size}: start the server as {WORLD} (torchrun --nproc-per-node {WORLD}, or WORLD_SIZE "
                         f"{WORLD} across two machines)")
    return dist.group.WORLD, dist.get_rank(), size


def batch_of(args: tuple, kwargs: dict) -> Optional[int]:
    """The batch a call's tensors lead with - the first dimension of its first tensor with one - where it is even and
    of two or more; None otherwise: the call runs whole on both processes."""
    for value in _leaves((args, kwargs)):
        if _is_tensor(value) and value.dim() >= 1:
            n = int(value.shape[0])
            return n if n >= WORLD and n % WORLD == 0 else None
    return None


def install(inst: Any, paths: list[str], *, say: Callable[[str], Any] = print, group_of: Optional[Callable] = None
            ) -> list[Patch]:
    """Each torch module at `paths` (dotted from `inst`, a namespace of names as optimize() reads a policy) run on this
    process's half of each call's batch, the halves gathered back (the module's docstring); the patches, for
    uninstall(). A path that names no torch module, or one with a forward put in its place already, is left as it is
    and said. `group_of`: for tests, what group() gives."""
    from .cuda_graphs import resolve

    grp, rank, size = (group_of or group)()
    patches: list[Patch] = []
    for path in paths:
        try:
            holder, name = resolve(inst, path)
            module = holder[name] if isinstance(holder, dict) else getattr(holder, name)
        except (AttributeError, KeyError, TypeError):
            say(f"cfg_parallel: {path} is not in this model: not split")
            continue
        if not _is_module(module):
            say(f"cfg_parallel: {path} is not a torch module: not split")
            continue
        if "forward" in vars(module):
            say(f"cfg_parallel: {path} runs another forward already: not split")
            continue
        patches.append(Patch(module, "forward", _split(module.forward, grp, rank, size), _ABSENT, path))
    for patch in patches:
        setattr(patch.holder, patch.name, patch.value)
    return patches


def census(roots: dict, call: Callable[[], Any]) -> list[str]:
    """The module to split: of the torch modules reachable from `roots` (a namespace of names, as optimize() reads a
    policy), the one that took the most time in `call()` - one act of the policy - of those each of whose calls led
    with one even batch and answered for the same batch, and inside no other such module; [its path], or [] for none.
    `call()` runs with every module watched, and is run once."""
    import time

    from .cuda_graphs import modules_of

    found: dict = {}
    for name, root in roots.items():
        for sub, module in modules_of(root).items():
            found.setdefault(id(module), (f"{name}.{sub}" if sub else name, module))
    seen: dict = {}
    hooks = []

    def before(path: str):
        def hook(module, args, kwargs):
            entry = seen.setdefault(path, {"ms": 0.0, "ok": True, "open": []})
            n = batch_of(args, kwargs)
            entry["ok"] = entry["ok"] and n is not None
            entry["open"].append((n, time.perf_counter()))
        return hook

    def after(path: str):
        def hook(module, args, kwargs, output):
            entry = seen[path]
            n, started = entry["open"].pop()
            entry["ms"] += (time.perf_counter() - started) * 1000.0
            first = next((v for v in _leaves(output) if _is_tensor(v) and v.dim() >= 1), None)
            entry["ok"] = entry["ok"] and first is not None and int(first.shape[0]) == n
        return hook

    try:
        for path, module in found.values():
            hooks.append(module.register_forward_pre_hook(before(path), with_kwargs=True))
            hooks.append(module.register_forward_hook(after(path), with_kwargs=True))
        call()
    finally:
        for handle in hooks:
            handle.remove()
    kept = [path for path, entry in seen.items() if entry["ok"]]
    outer = [path for path in kept if not any(path.startswith(other + ".") for other in kept if other != path)]
    return sorted(outer, key=lambda path: -seen[path]["ms"])[:1]


def trial(policy: Any, call: Callable[[Any], Any], toggle: Callable[[list, bool], Any], examples: list, *,
          sizes: Optional[list] = None, limits: Optional[dict] = None, seed: int = 0,
          min_speedup: Optional[float] = None, rounds: int = 3, say: Callable[[str], Any] = print) -> dict:
    """cfg_parallel tried as optimize() tries a switch that changes the outputs, on rank 0 of two: `call(item)` the
    policy on one run's observation (or list of them) on every rank, rank 0's output back; `toggle(paths, on)` the split
    put in place on every rank, or taken out. The module census() finds is split; the outputs of every run of
    `examples` (optimize's runs, each seeded) held to eager mode's within `limits` (optimize's tolerance, a dict);
    then the act timed without the split and with it, in turns, `rounds` times on each timed run. Kept - left in place
    - where they pass and the act is `min_speedup` faster (optimize.MIN_SPEEDUP); taken out otherwise. The report, as
    optimize() reports a switch: {"on": [...], "switches": {"cfg_parallel": {"on": ..., ...}}}."""
    import importlib
    import statistics
    import time

    opt = importlib.import_module(".optimize", __package__)     # the module: the package names its function so

    min_speedup = opt.MIN_SPEEDUP if min_speedup is None else min_speedup
    runs = opt._runs(examples, sizes, seed)

    def played(run) -> Any:
        opt._seed_all(run.seed)
        return call(run.item)

    def off(why: str, **detail) -> dict:
        say(f"optimize: cfg_parallel off - {why}")
        return {"on": [], "switches": {"cfg_parallel": {"on": False, "why": why, **detail}}}

    if not limits:
        return off("it changes the outputs: give tolerance=, the largest difference you accept from eager mode's")
    kept = opt._states()
    try:
        paths = census(opt._namespace(policy), lambda: played(runs[0]))
        if not paths:
            return off("no module of the policy is called with one even batch and answers for it - the guidance's "
                       "two halves in one batch: nothing to cut between the two processes")
        eager = [played(run) for run in runs]
        toggle(paths, True)
        try:
            worst: dict = {}
            for i, (run, want) in enumerate(zip(runs, eager)):
                found = opt.differences(want, played(run))
                where = f"on run {i + 1} of {len(runs)}"
                if found is None:
                    toggle(paths, False)
                    return off(f"its outputs were not shaped as eager mode's {where}", modules=paths)
                for name, value in found.items():
                    worst[name] = min(worst.get(name, 1.0), value) if name == "cosine" else \
                        max(worst.get(name, 0.0), value)
                for name, limit in limits.items():
                    value = found[name]
                    if (value < limit) if name == "cosine" else (value > limit):
                        toggle(paths, False)
                        return off(f"its {name} from eager mode's was {value:.3g} {where}, past the {limit:g} of the "
                                   "tolerance", modules=paths, largest=opt._rounded(worst))
            times: dict = {False: [], True: []}
            for _ in range(rounds):
                for on in (False, True):
                    toggle(paths, on)
                    for run in (r for r in runs if r.timed):
                        started = time.perf_counter()
                        played(run)
                        times[on].append((time.perf_counter() - started) * 1000.0)
            before, after = statistics.median(times[False]), statistics.median(times[True])
        except Exception as exc:  # noqa: BLE001 - the policy refused the split: it is taken out, saying why
            toggle(paths, False)
            return off(f"the policy raised with it on: {type(exc).__name__}: {str(exc)[:160]}", modules=paths)
        faster = round(before / after, 2) if after > 0 else None
        act = f"act {before:.1f} → {after:.1f} ms"
        if faster is None or faster < min_speedup:
            toggle(paths, False)
            gained, needs = round(((faster or 0) - 1) * 100), round((min_speedup - 1) * 100)
            return off(f"{gained}% faster ({act}), under the {needs}% it needs" if gained > 0
                       else f"no faster with it ({act})", modules=paths, largest=opt._rounded(worst))
        largest = ", ".join(f"{name} {value:g}" for name, value in opt._rounded(worst).items())
        say(f"optimize: cfg_parallel on - {', '.join(paths)}, its batch cut between two processes: within the "
            f"tolerance on {len(runs)} runs (largest differences: {largest}); {act}")
        return {"on": ["cfg_parallel"], "act_ms": {"eager": round(before, 2), "optimized": round(after, 2)},
                "switches": {"cfg_parallel": {"on": True, "modules": paths, "speedup": faster,
                                              "largest": opt._rounded(worst), "checked": len(runs)}}}
    finally:
        opt._put_states(kept)


def _split(forward: Callable, grp: Any, rank: int, size: int) -> Callable:
    """`forward`, run on this rank's share of each call's batch, its outputs gathered back whole."""

    def run(*args, **kwargs):
        n = batch_of(args, kwargs)
        if n is None:
            return forward(*args, **kwargs)
        part = n // size
        args, kwargs = _map((args, kwargs), lambda t: _half(t, grp, rank, part) if _leads(t, n) else t)
        return _map(forward(*args, **kwargs), lambda t: _gathered(t, grp, size) if _leads(t, part) else t)

    run.__seq_cfg_parallel__ = True
    return run


def _half(tensor: Any, grp: Any, rank: int, part: int) -> Any:
    """This rank's half of one of a call's batched inputs: on rank 0 its first half, its second sent to rank 1; on rank
    1 that second half, as rank 0 sent it."""
    import torch
    import torch.distributed as dist

    if rank == 0:
        dist.send(tensor.narrow(0, part, part).contiguous(), dst=1, group=grp)
        return tensor.narrow(0, 0, part)
    got = torch.empty((part, *tensor.shape[1:]), dtype=tensor.dtype, device=tensor.device)
    dist.recv(got, src=0, group=grp)
    return got


def _gathered(tensor: Any, grp: Any, size: int) -> Any:
    """One output's halves from every process, in rank order, as one tensor along the batch."""
    import torch
    import torch.distributed as dist

    mine = tensor.contiguous()
    parts = [torch.empty_like(mine) for _ in range(size)]
    dist.all_gather(parts, mine, group=grp)
    return torch.cat(parts, dim=0)


def _leads(value: Any, n: int) -> bool:
    return _is_tensor(value) and value.dim() >= 1 and int(value.shape[0]) == n


def _is_tensor(value: Any) -> bool:
    import torch

    return isinstance(value, torch.Tensor)


def _is_module(value: Any) -> bool:
    import torch

    return isinstance(value, torch.nn.Module)


def _leaves(tree: Any) -> list:
    from torch.utils import _pytree

    return _pytree.tree_leaves(tree)


def _map(tree: Any, fn: Callable) -> Any:
    """`fn` on each leaf of `tree` (tuples, lists, dicts and the dataclasses torch's pytree knows, diffusers' outputs
    among them), the tree's shape kept."""
    from torch.utils import _pytree

    return _pytree.tree_map(fn, tree)
