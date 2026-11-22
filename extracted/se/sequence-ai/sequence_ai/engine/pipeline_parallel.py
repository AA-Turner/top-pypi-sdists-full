# SPDX-FileCopyrightText: Copyright (c) 2026 General Sequences Company
# SPDX-License-Identifier: Apache-2.0
"""
A model's run of blocks - a transformer's layers - split into consecutive stages, one a process, each on a GPU of its
own or a machine of its own, and each call of the run passed through the stages in parts, so that they work at once:
parts of its batch, or, for a diffusion transformer, patches of its tokens.

    torchrun --nproc-per-node 2 my_server.py        # or one process on each of two machines: WORLD_SIZE 2
    from sequence_ai.engine import pipeline_parallel

    split = pipeline_parallel.install(policy_user, "model.blocks", form="patches", parts=2)    # in every process
    pipeline_parallel.begin()                       # at each act: its first call of the blocks runs whole
    pipeline_parallel.uninstall(split)              # the blocks' own forwards again

In one sentence: the processes' group (torch.distributed: made from torchrun's environment where the model made none)
→ the blocks at a path - a ModuleList or a Sequential its parent calls one after another, each on the one before's
output - cut into one stage a process, contiguous, each process's share as many blocks as its GPU runs in the time the
others run theirs (timed on each at the first call) → each call of the blocks, up to the last block, runs nothing: each
block gives back its input, and what it was called with is kept → at the last block the run goes through the stages
by PyTorch's pipelining, its GPipe schedule forward only: rank 0's input cut into parts, each part through rank 0's
blocks and on to rank 1's, so that rank 1 works on one part while rank 0 works on the next (a call in one part - each
act's first, in patches - goes through them in turn, by sends of its own) → the last stage's parts, joined, sent to
rank 0, which gives them back as the last block's output.

The two forms:
  "layers"   the parts are rows of the call's batch, along its first dimension: several robots' observations at once.
  "patches"  (a diffusion transformer's tokens, along the second dimension, adapted from PipeFusion) each patch's
             self-attention reads the other patches' keys and values as last computed - this call's for the patches
             before it, the previous call's (the diffusion's previous step) for those after - so a call of one
             observation is pipelined too. The first `warmup` calls of each act run whole, which computes them all.

WHY a switch that changes the outputs (optimize's tolerance): a part's matrix products are computed in another order
than the whole call's, by other kernels; and a patch's attention reads keys and values one step old.
WHY each block's call kept until the last: a block may be called with other arguments than the one before it (a
cross-attention's context on one block, none on the next), which only its parent's call of it says; at the last block
every block's are known, and each stage runs its blocks with their own.
WHY the blocks run only in their stages: each process holds the whole model, but computes its own share of the
blocks; the rest of the model - its embeddings, its head, a sampler's loop - runs in every process, and rank 0's answer
is the server's: no other process's values reach it but the blocks' outputs it is sent.
WHY the shares timed on each GPU: two GPUs of different makes run a block in different times, and the slowest stage
sets the pace of all.
WHY a stage that raises gives its next stage zeros and says so after the step: a process that stopped in the middle
of the schedule would leave the others waiting for its parts forever; so every process ends the step, and then every
process raises what any of them raised.

Adapted from xdit-project/xDiT xfuser/core/cache_manager/cache_manager.py (Apache-2.0), its update_and_get_kv_cache
and naive cache, with xfuser/model_executor/pipefusion/layout.py, its patches' token ranges: see
THIRD_PARTY_NOTICES.md. Changed here: each self-attention's keys and values kept at its call of
torch.nn.functional.scaled_dot_product_attention, for any block, where xDiT replaces each model's attention
processors; the stages run by PyTorch's own pipelining; a call's patches joined at the last stage and sent to rank 0,
where xDiT runs the scheduler's step on the last stage.
"""
from __future__ import annotations

import time
import weakref
from typing import Any, Callable, Optional

from .fused import _ABSENT, Patch
from .fused import uninstall as _uninstall_patches

__all__ = ["FORMS", "WARMUP", "Split", "group", "install", "uninstall", "begin", "stages_for", "census", "trial"]

FORMS = ("patches", "layers")   # what a call is cut into: its tokens' patches, its batch's rows
WARMUP = 1                      # the calls of each act run whole before its patches, as a diffusion's first step

_LIVE: "weakref.WeakSet" = weakref.WeakSet()     # the splits installed in this process, for begin()


def group(backend: Optional[str] = None) -> tuple:
    """The group the processes split the blocks in: torch.distributed's own, made from torchrun's environment (RANK,
    WORLD_SIZE, MASTER_ADDR, MASTER_PORT) where the model made none - gloo for tensors on the CPU, NCCL for those on a
    GPU where there is one - and (its rank, its size). ValueError where it is of one process."""
    import torch
    import torch.distributed as dist

    if not dist.is_initialized():
        backend = backend or ("cpu:gloo,cuda:nccl" if torch.cuda.is_available() else "gloo")
        dist.init_process_group(backend=backend, init_method="env://")
    size = dist.get_world_size()
    if size < 2:
        raise ValueError(f"pipeline_parallel splits a model's blocks between processes, and torch.distributed's group "
                         f"has {size}: start the server as 2 or more (torchrun --nproc-per-node 2, or WORLD_SIZE 2 "
                         "across two machines)")
    return dist.group.WORLD, dist.get_rank(), size


def stages_for(times: list) -> list:
    """How many blocks each process runs, in rank order: `times[r][i]`, block i's milliseconds on process r's GPU →
    the contiguous shares, a block or more each, whose slowest stage is as fast as any can be (of equal ones, the one
    with the fewest blocks in the first stages)."""
    size, n = len(times), len(times[0])
    if n < size:
        raise ValueError(f"{n} blocks cannot be cut into {size} stages of one block or more")
    sums = []
    for row in times:
        acc = [0.0]
        for value in row:
            acc.append(acc[-1] + float(value))
        sums.append(acc)
    worst = [[float("inf")] * (n + 1) for _ in range(size)]
    cut = [[0] * (n + 1) for _ in range(size)]
    for j in range(1, n + 1):
        worst[0][j] = sums[0][j]
    for r in range(1, size):
        for j in range(r + 1, n + 1):
            for k in range(r, j):                    # process r runs blocks k to j - 1
                slowest = max(worst[r - 1][k], sums[r][j] - sums[r][k])
                if slowest < worst[r][j]:
                    worst[r][j], cut[r][j] = slowest, k
    counts, j = [], n
    for r in range(size - 1, 0, -1):
        counts.append(j - cut[r][j])
        j = cut[r][j]
    counts.append(j)
    return counts[::-1]


class Split:
    """The blocks at one path of a model cut into stages, in this process (install()): `stages` the blocks of each
    process, in rank order - None until the first call times them; `ran` the calls run whole and in parts."""

    def __init__(self, path: str, blocks: list, grp: Any, rank: int, size: int, *, form: str, parts: int,
                 stages: Optional[list], slot: Any, out: Any, warmup: int) -> None:
        self.path, self.blocks, self.grp, self.rank, self.size = path, blocks, grp, rank, size
        self.form, self.parts, self.stages, self.slot, self.out, self.warmup = form, parts, stages, slot, out, warmup
        self.ran = {"whole": 0, "parts": 0}
        self._own = [block.forward for block in blocks]          # each block's own forward, called by its stage
        self._patches: list = []
        self._calls: dict = {}            # this pass: each block's (args, kwargs), as its parent called it
        self._next = 0                    # the block the parent calls next
        self._since = 0                   # the calls since the act began: the first `warmup` run whole
        self._schedules: dict = {}        # (parts, shapes ...) → this process's stage and its schedule
        self._kv: dict = {}               # the patches' keys and values: each self-attention of this stage's blocks
        self._kv_shape: Optional[tuple] = None   # the input they were computed for
        self._mine: dict = {}             # this pass, for the stage: each of its blocks' arguments, by part
        self._attend: dict = {}           # this part's place for the attention: whole, its patch, its tokens
        self._error: Optional[str] = None
        self._part = 0                    # the part this process's stage runs next, in this pass
        self._dim = 0                     # the dimension this pass cuts: 0 the batch, 1 the tokens
        _LIVE.add(self)

    def on(self) -> None:
        """Each block's forward replaced by its share of the pass (the module's docstring)."""
        if self._patches:
            return
        self._patches = [Patch(block, "forward", self._forward_of(i), _ABSENT, f"{self.path}.{i}")
                         for i, block in enumerate(self.blocks)]
        for patch in self._patches:
            setattr(patch.holder, patch.name, patch.value)

    def off(self) -> None:
        """Each block's own forward again; the stages and their schedules kept for on()."""
        _uninstall_patches(self._patches)
        self._patches, self._calls, self._next = [], {}, 0

    def begin(self) -> None:
        """A new act: its first `warmup` calls of the blocks run whole."""
        self._since = 0

    # ── the parent's calls ──────────────────────────────────────────────────────────────────────────────────────────
    def _forward_of(self, i: int) -> Callable:
        last = len(self.blocks) - 1

        def forward(*args, **kwargs):
            if self._next != i:
                expected = self._next
                self._calls, self._next = {}, 0
                raise RuntimeError(f"pipeline_parallel: {self.path}.{i} was called where {self.path}.{expected} was "
                                   "next: its parent does not call its blocks one after another, each once a pass")
            self._calls[i] = (args, kwargs)
            if i < last:
                self._next = i + 1
                return self._shaped(_slot_value(args, kwargs, self.slot))
            self._next = 0
            try:
                return self._shaped(self._pass())
            finally:
                self._calls = {}

        forward.__seq_pipeline_parallel__ = True
        return forward

    def _shaped(self, hidden: Any) -> Any:
        """`hidden` as the blocks give back their output: itself, or first in a tuple or a list of Nones."""
        if self.out is None:
            return hidden
        kind, length = self.out
        values = [hidden] + [None] * (int(length) - 1)
        return tuple(values) if kind == "tuple" else values

    # ── one pass of the blocks ──────────────────────────────────────────────────────────────────────────────────────
    def _pass(self) -> Any:
        import torch.distributed as dist

        args, kwargs = self._calls[0]
        hidden = _slot_value(args, kwargs, self.slot)
        if self.stages is None:
            self.stages = self._measure(hidden)
        lo = sum(self.stages[:self.rank])
        hi = lo + self.stages[self.rank]
        dim = 1 if self.form == "patches" else 0
        whole = self.form == "patches" and (self._since < self.warmup or tuple(hidden.shape) != self._kv_shape)
        self._since += 1
        parts = 1 if whole else _divisor(int(hidden.shape[dim]), self.parts)
        if parts < self.size:            # GPipe gives each stage a part at least: fewer go through as one
            parts = 1
        if whole:
            self._kv, self._kv_shape = {}, tuple(hidden.shape)
        self._mine = {j: self._parts_of(j, parts, dim, int(hidden.shape[0])) for j in range(lo, hi)}
        self._attend = {"patches": self.form == "patches", "whole": parts == 1,
                        "tokens": int(hidden.shape[1]) if hidden.dim() >= 2 else 0,
                        "length": int(hidden.shape[dim]) // parts if parts > 1 else 0}
        self._error, self._part, self._dim = None, 0, dim
        with _attention(self):
            if parts > 1:                # each stage at work on one part while the next works on the one before
                # the dimension cut leading, so that each part is one dense tensor, as every torch's stage checks it
                lead = hidden if dim == 0 else hidden.movedim(dim, 0).contiguous()
                schedule = self._schedule(lead, parts, lo, hi)
                out = schedule.step(lead) if self.rank == 0 else schedule.step()
                if out is not None and dim != 0:
                    out = out.movedim(0, dim)
            else:
                out = self._through(hidden)
        last = self.size - 1
        if self.rank == last and last != 0:
            dist.send(out.contiguous(), dst=0, group=self.grp)
        elif self.rank == 0:
            out = hidden.new_empty(hidden.shape)
            dist.recv(out, src=last, group=self.grp)
        else:
            out = hidden
        self._mine = {}
        self._raise_any()
        self.ran["whole" if parts == 1 else "parts"] += 1
        return out

    def _through(self, hidden: Any) -> Any:
        """The call whole through the stages in turn: each process's blocks on what the one before sent it, its output
        sent to the next. Nothing overlaps here, so no schedule is needed."""
        import torch.distributed as dist

        if self.rank > 0:
            got = hidden.new_empty(hidden.shape)
            dist.recv(got, src=self.rank - 1, group=self.grp)
            hidden = got
        hidden = self._run_stage(hidden)
        if self.rank < self.size - 1:
            dist.send(hidden.contiguous(), dst=self.rank + 1, group=self.grp)
        return hidden

    def _parts_of(self, j: int, parts: int, dim: int, batch: int) -> list:
        """Block j's arguments, its hidden among them as given, for each part: in the layers form each tensor leading
        with the batch cut as the hidden is; in the patches form, the same for every patch."""
        args, kwargs = self._calls[j]
        if parts == 1 or dim != 0:
            return [(args, kwargs)] * parts

        def cut(m: int):
            return _map((args, kwargs), lambda t: t.chunk(parts, 0)[m] if _leads(t, batch) else t)

        return [cut(m) for m in range(parts)]

    def _run_stage(self, hidden: Any, lead: bool = False) -> Any:
        """This process's blocks on its next part, each called as its parent called it, with the part for its hidden;
        `lead`: a part as the schedule cut it, its cut dimension leading, put back in place for the blocks and leading
        again in what is sent on.
        WHY the parts counted here: the GPipe schedule runs a stage's parts in order, and the part's place is not an
        argument every torch's pipelining passes on."""
        part, self._part = self._part, self._part + 1
        self._attend["part"], self._attend["calls"] = part, 0
        given, moved = hidden, lead and self._dim != 0
        try:
            if moved:
                hidden = hidden.movedim(0, self._dim).contiguous()
            for j in sorted(self._mine):
                args, kwargs = self._mine[j][part]
                args, kwargs = _with_slot(args, kwargs, self.slot, hidden)
                hidden = _first(self._own[j](*args, **kwargs))
            return hidden.movedim(self._dim, 0).contiguous() if moved else hidden
        except Exception as e:  # noqa: BLE001 - said after the step, by every process: none waits for this one
            if self._error is None:
                self._error = f"{type(e).__name__}: {str(e)[:300]}"
            return given.new_zeros(given.shape)

    def _raise_any(self) -> None:
        """What any process's stage raised this pass, raised in every process."""
        import torch.distributed as dist

        said: list = [None] * self.size
        dist.all_gather_object(said, self._error, group=self.grp)
        for rank, error in enumerate(said):
            if error is not None:
                raise RuntimeError(f"pipeline_parallel: rank {rank}'s stage of {self.path} raised: {error}")

    def _measure(self, hidden: Any) -> list:
        """Each block timed on this process's GPU - the pass run whole, twice, the faster kept - and the shares
        stages_for() gives every process's times."""
        import torch.distributed as dist

        mine: Optional[list] = None
        try:
            best = [float("inf")] * len(self.blocks)
            for _ in range(2):
                h = hidden
                for j in range(len(self.blocks)):
                    args, kwargs = _with_slot(*self._calls[j], self.slot, h)
                    _sync(h)
                    started = time.perf_counter()
                    h = _first(self._own[j](*args, **kwargs))
                    _sync(h)
                    best[j] = min(best[j], (time.perf_counter() - started) * 1000.0)
            mine = best
        except Exception as e:  # noqa: BLE001 - every process's word gathered first, then raised in all
            self._error = f"{type(e).__name__}: {str(e)[:300]}"
        every: list = [None] * self.size
        dist.all_gather_object(every, mine, group=self.grp)
        if any(times is None for times in every):
            self._raise_any()
        return stages_for(every)

    def _schedule(self, lead: Any, parts: int, lo: int, hi: int) -> Any:
        """This process's stage of the blocks lo to hi - 1 and its GPipe schedule for `parts` parts of `lead` - the
        call's hidden with the dimension it is cut along first - made once for each shape: the stage told the parts'
        shapes, so none is inferred."""
        import torch
        from torch.distributed.pipelining import PipelineStage, ScheduleGPipe
        from torch.distributed.pipelining.microbatch import TensorChunkSpec

        key = (parts, self._dim, lo, hi, tuple(lead.shape), lead.dtype, str(lead.device))
        if key not in self._schedules:
            example = torch.empty_like(lead.chunk(parts, 0)[0])
            stage = PipelineStage(_stage_module(self), self.rank, self.size, lead.device, input_args=(example,),
                                  output_args=torch.empty_like(example), group=self.grp)
            self._schedules[key] = ScheduleGPipe(stage, parts, args_chunk_spec=(TensorChunkSpec(0),),
                                                 output_merge_spec=TensorChunkSpec(0))
        return self._schedules[key]


def install(inst: Any, path: str, *, form: str = "layers", parts: int = 2, stages: Optional[list] = None,
            slot: Any = 0, out: Any = None, warmup: int = WARMUP, group_of: Optional[Callable] = None) -> Split:
    """The blocks at `path` (dotted from `inst`, a namespace of names as optimize() reads a policy) - a ModuleList or a
    Sequential its parent calls one after another - split between this group's processes, in every process alike
    (the module's docstring). `form`: "layers" or "patches"; `parts`: the most parts a call is cut into (a divisor of
    its batch, or of its tokens, at most this); `stages`: each process's blocks, timed at the first call where None;
    `slot`: the argument of each block's call that is the one before's output, its position or its keyword; `out`:
    how a block gives back its output - None for a tensor, ["tuple", n] or ["list", n] for one leading n values, the
    rest None. `group_of`: for tests, what group() gives. The split, put in place."""
    import torch

    from .cuda_graphs import resolve

    if form not in FORMS:
        raise ValueError(f"pipeline_parallel: form={form!r}: it is one of {', '.join(FORMS)}")
    grp, rank, size = (group_of or group)()
    holder, name = resolve(inst, path)
    container = holder[name] if isinstance(holder, dict) else getattr(holder, name)
    if not isinstance(container, (torch.nn.ModuleList, torch.nn.Sequential)):
        raise TypeError(f"pipeline_parallel: {path} is not a ModuleList or a Sequential of blocks")
    blocks = list(container)
    if len(blocks) < size:
        raise ValueError(f"pipeline_parallel: {path} holds {len(blocks)} blocks, fewer than the {size} processes")
    if any("forward" in vars(block) for block in blocks):
        raise ValueError(f"pipeline_parallel: a block of {path} runs another forward already")
    if stages is not None and (len(stages) != size or sum(stages) != len(blocks) or min(stages) < 1):
        raise ValueError(f"pipeline_parallel: stages={stages} do not cut {len(blocks)} blocks into {size} stages")
    split = Split(path, blocks, grp, rank, size, form=form, parts=int(parts), stages=stages, slot=slot, out=out,
                  warmup=int(warmup))
    split.on()
    return split


def uninstall(split: Split) -> None:
    """The split's blocks given their own forwards back."""
    split.off()


def begin() -> None:
    """A new act for every split in this process: its first `warmup` calls of the blocks run whole."""
    for split in list(_LIVE):
        split.begin()


def census(roots: dict, call: Callable[[], Any], size: int) -> Optional[dict]:
    """The run of blocks to split, as one act - `call()`, run once - shows it: of the ModuleLists and Sequentials of
    `size` blocks or more in the torch modules reachable from `roots` (a namespace of names, as optimize() reads a
    policy), the one whose passes took the most time, where each pass called its blocks one after another, each with
    the one before's output in the same argument, and each block gave back a tensor shaped as that input - or a tuple
    or a list leading with one, the rest None. {"path", "blocks", "slot", "out", "batch", "tokens", "attention"}, or
    None. "tokens": the second dimension of a 3-dimensional input, a transformer's [batch, tokens, width];
    "attention": the calls of torch.nn.functional.scaled_dot_product_attention in a pass over all its tokens - the
    self-attention a patch reads the others' keys and values in. MultiheadAttention's fused path is off for the call:
    its attention then goes through scaled_dot_product_attention, as it does in the patches."""
    import torch
    import torch.nn.functional as F

    from .cuda_graphs import modules_of

    runs: dict = {}
    for name, root in roots.items():
        for sub, top in modules_of(root).items():
            base = f"{name}.{sub}" if sub else name
            for inner, module in top.named_modules():
                if isinstance(module, (torch.nn.ModuleList, torch.nn.Sequential)) and len(module) >= max(2, size) \
                        and all(isinstance(block, torch.nn.Module) for block in module) and id(module) not in runs:
                    runs[id(module)] = {"path": f"{base}.{inner}" if inner else base, "blocks": list(module),
                                        "ok": True, "ms": 0.0, "next": 0, "slot": None, "out": "unset", "prev": None,
                                        "first": None, "batch": None, "tokens": None, "attention": 0, "open": False,
                                        "seen": [], "started": 0.0}
    if not runs:
        return None

    def before(run: dict, i: int):
        def hook(module, args, kwargs):
            if not run["ok"]:
                return
            if i == 0:
                if run["open"]:
                    run["ok"] = False
                    return
                _sync_any(args, kwargs)
                run.update(open=True, next=1, first=(args, kwargs), seen=[], started=time.perf_counter())
                return
            if not run["open"] or run["next"] != i:
                run["ok"] = False
                return
            slot = _slot_of(args, kwargs, run["prev"])
            if slot is None or run["slot"] not in (None, slot):
                run["ok"] = False
                return
            run["slot"] = slot
            if i == 1:
                hidden = _slot_value(*run["first"], slot) if _has_slot(*run["first"], slot) else None
                if not _is_tensor(hidden) or tuple(hidden.shape) != tuple(run["prev"].shape) or hidden.dim() < 2:
                    run["ok"] = False
                    return
                batch, tokens = int(hidden.shape[0]), int(hidden.shape[1]) if hidden.dim() == 3 else None
                if run["batch"] not in (None, batch) or run["tokens"] not in (None, tokens):
                    run["ok"] = False
                run["batch"], run["tokens"] = batch, tokens
            run["next"] = i + 1
        return hook

    def after(run: dict, i: int):
        def hook(module, args, kwargs, output):
            if not run["ok"]:
                return
            first, out = _output_of(output)
            if first is None or run["out"] not in ("unset", out):
                run["ok"] = False
                return
            run["out"] = out
            if i > 0:
                given = _slot_value(args, kwargs, run["slot"])
                if tuple(first.shape) != tuple(given.shape):
                    run["ok"] = False
                    return
            run["prev"] = first
            if i == len(run["blocks"]) - 1:
                _sync_any((first,), {})
                run["ms"] += (time.perf_counter() - run["started"]) * 1000.0
                tokens = run["tokens"]
                run["attention"] = max(run["attention"],
                                       sum(1 for q, k in run["seen"] if tokens is not None and q == k == tokens))
                run.update(open=False, next=0)
        return hook

    own_sdpa = F.scaled_dot_product_attention

    def watched(query, key, value, *args, **kwargs):
        for run in runs.values():
            if run["open"]:
                run["seen"].append((int(query.shape[-2]), int(key.shape[-2])))
        return own_sdpa(query, key, value, *args, **kwargs)

    hooks = []
    fast = _fastpath(False)
    F.scaled_dot_product_attention = watched
    try:
        for run in runs.values():
            for i, block in enumerate(run["blocks"]):
                hooks.append(block.register_forward_pre_hook(before(run, i), with_kwargs=True))
                hooks.append(block.register_forward_hook(after(run, i), with_kwargs=True))
        call()
    finally:
        F.scaled_dot_product_attention = own_sdpa
        _fastpath(fast)
        for handle in hooks:
            handle.remove()
    kept = [run for run in runs.values()
            if run["ok"] and not run["open"] and run["ms"] > 0 and run["slot"] is not None and run["out"] != "unset"]
    if not kept:
        return None
    best = max(kept, key=lambda run: run["ms"])
    return {"path": best["path"], "blocks": len(best["blocks"]), "slot": best["slot"], "out": best["out"],
            "batch": best["batch"], "tokens": best["tokens"], "attention": best["attention"]}


def trial(policy: Any, call: Callable[[Any], Any], toggle: Callable[[dict, bool], Any], examples: list, *, size: int,
          sizes: Optional[list] = None, limits: Optional[dict] = None, seed: int = 0,
          min_speedup: Optional[float] = None, rounds: int = 3, say: Callable[[str], Any] = print) -> dict:
    """pipeline_parallel tried as optimize() tries a switch that changes the outputs, on rank 0 of `size`:
    `call(item)` the policy on one run's observation (or list of them) on every rank, rank 0's output back;
    `toggle(spec, on)` the split put in place on every rank as `spec` says ({"path", "slot", "out", "form", "parts",
    "stages"}: install()'s), or taken out - giving back rank 0's Split. The run of blocks census() finds is tried in
    each form it can take - its tokens in patches, as many as processes and twice as many, and its batch in parts -
    each held to eager mode's outputs on every run of `examples` (optimize's runs, each seeded) within `limits`, then
    timed against eager mode in turns, `rounds` times; the fastest within the tolerance kept - left in place - where
    its acts are `min_speedup` faster (optimize.MIN_SPEEDUP), and none otherwise, each form's reason said. The report,
    as optimize() reports a switch: {"on": [...], "switches": {"pipeline_parallel": {"on": ..., ...}}}."""
    import importlib
    import statistics

    opt = importlib.import_module(".optimize", __package__)

    min_speedup = opt.MIN_SPEEDUP if min_speedup is None else min_speedup
    runs = opt._runs(examples, sizes, seed)

    def played(run) -> Any:
        opt._seed_all(run.seed)
        return call(run.item)

    def off(why: str, **detail) -> dict:
        say(f"optimize: pipeline_parallel off - {why}")
        return {"on": [], "switches": {"pipeline_parallel": {"on": False, "why": why, **detail}}}

    if not limits:
        return off("it changes the outputs: give tolerance=, the largest difference you accept from eager mode's")
    kept = opt._states()
    try:
        found = census(opt._namespace(policy), lambda: played(runs[0]), size)
        if found is None:
            return off(f"no run of blocks in the policy - a ModuleList or Sequential of {size} or more its model "
                       "calls one after another, each on the one before's output - to cut into stages")
        forms = _forms(found, size)
        if not forms:
            return off(f"{found['path']}'s calls lead with a batch of {found['batch']} and no tokens to cut into "
                       f"patches: nothing to pipeline", path=found["path"])
        eager = [played(run) for run in runs]
        tried = [_tried(dict(found, form=form, parts=parts, stages=None), runs, eager, played, toggle, limits,
                        rounds, opt, statistics) for form, parts in forms]
        passed = [one for one in tried if "why" not in one]
        best = max(passed, key=lambda one: one["speedup"] or 0.0) if passed else None
        if best is None or best["speedup"] is None or best["speedup"] < min_speedup:
            why = "; ".join(f"{_said_form(one['spec'])}, {one.get('why') or _slower(one, min_speedup)}"
                            for one in tried)
            return off(why, path=found["path"], tried=[{**_detail(one)} for one in tried])
        split = toggle(best["spec"], True)
        spec = best["spec"]
        stages = spec.get("stages") or (split.stages if split is not None else None)
        shares = f" of {', '.join(str(n) for n in stages)}" if stages else ""
        largest = ", ".join(f"{name} {value:g}" for name, value in best["largest"].items())
        say(f"optimize: pipeline_parallel on - {spec['path']}, its {found['blocks']} blocks in {size} stages{shares}, "
            f"{_said_form(spec)}: within the tolerance on {len(runs)} runs (largest differences: {largest}); "
            f"{best['act']}")
        return {"on": ["pipeline_parallel"], "act_ms": {"eager": best["before"], "optimized": best["after"]},
                "switches": {"pipeline_parallel": {"on": True, **_detail(best), "checked": len(runs)}}}
    finally:
        opt._put_states(kept)


def _tried(spec: dict, runs: list, eager: list, played: Callable, toggle: Callable, limits: dict, rounds: int, opt: Any,
           statistics: Any) -> dict:
    """One form of the split checked on every run and timed against eager mode; taken out after. {"spec", ...} with
    "why" where it did not pass."""
    try:
        split = toggle(spec, True)
        worst: dict = {}
        for i, (run, want) in enumerate(zip(runs, eager)):
            found = opt.differences(want, played(run))
            where = f"on run {i + 1} of {len(runs)}"
            if found is None:
                return {"spec": spec, "why": f"its outputs were not shaped as eager mode's {where}"}
            for name, value in found.items():
                worst[name] = min(worst.get(name, 1.0), value) if name == "cosine" else max(worst.get(name, 0.0), value)
            for name, limit in limits.items():
                value = found[name]
                if (value < limit) if name == "cosine" else (value > limit):
                    return {"spec": spec, "largest": opt._rounded(worst),
                            "why": f"its {name} from eager mode's was {value:.3g} {where}, past the {limit:g} of the "
                                   "tolerance"}
        if split is not None and split.stages is not None:
            spec["stages"] = list(split.stages)          # timed once: the timing's toggles cut it the same way
        times: dict = {False: [], True: []}
        for _ in range(rounds):
            for on in (False, True):
                toggle(spec, on)
                for run in (r for r in runs if r.timed):
                    started = time.perf_counter()
                    played(run)
                    times[on].append((time.perf_counter() - started) * 1000.0)
        before, after = statistics.median(times[False]), statistics.median(times[True])
    except Exception as exc:  # noqa: BLE001 - the policy refused the split: it is taken out, saying why
        return {"spec": spec, "why": f"the policy raised with it on: {type(exc).__name__}: {str(exc)[:200]}"}
    finally:
        try:
            toggle(spec, False)
        except Exception:  # noqa: BLE001 - a rank gone: the server's own failure says so
            pass
    return {"spec": spec, "largest": opt._rounded(worst), "before": round(before, 2), "after": round(after, 2),
            "speedup": round(before / after, 2) if after > 0 else None, "act": f"act {before:.1f} → {after:.1f} ms"}


def _forms(found: dict, size: int) -> list:
    """The forms the run found can be tried in: its tokens in patches - as many as processes, and twice as many -
    where it is a transformer's with a self-attention to share; its batch in parts, as many as processes or more and
    at most twice as many (a part for each stage at least, as GPipe gives them)."""
    forms = []
    tokens = found.get("tokens")
    if tokens and found.get("attention"):
        for parts in sorted({size, 2 * size}):
            if tokens % parts == 0 and tokens // parts >= 1:
                forms.append(("patches", parts))
    batch = found.get("batch") or 1
    parts = _divisor(batch, 2 * size)
    if parts >= size:
        forms.append(("layers", parts))
    return forms


def _said_form(spec: dict) -> str:
    if spec["form"] == "patches":
        return f"each call's tokens in {spec['parts']} patches"
    return f"each call's batch in up to {spec['parts']} parts"


def _slower(one: dict, min_speedup: float) -> str:
    gained, needs = round(((one.get("speedup") or 0) - 1) * 100), round((min_speedup - 1) * 100)
    return f"{gained}% faster ({one['act']}), under the {needs}% it needs" if gained > 0 \
        else f"no faster with it ({one['act']})"


def _detail(one: dict) -> dict:
    spec = one["spec"]
    detail = {"path": spec["path"], "form": spec["form"], "parts": spec["parts"], "stages": spec.get("stages")}
    for name in ("speedup", "largest", "why"):
        if name in one:
            detail[name] = one[name]
    return detail


class _Attention:
    """While a pass's step runs: torch.nn.functional.scaled_dot_product_attention replaced by one that keeps each
    self-attention's keys and values (a whole call) or reads them with this patch's in place (a patch), and
    MultiheadAttention's fused path off, so its attention goes through it. Nothing for the layers form."""

    def __init__(self, split: Split) -> None:
        self.split = split

    def __enter__(self):
        if not self.split._attend.get("patches"):
            return self
        import torch.nn.functional as F

        self.own, self.fast = F.scaled_dot_product_attention, _fastpath(False)
        F.scaled_dot_product_attention = self._sdpa
        return self

    def __exit__(self, *exc) -> None:
        if not self.split._attend.get("patches"):
            return
        import torch.nn.functional as F

        F.scaled_dot_product_attention = self.own
        _fastpath(self.fast)

    def _sdpa(self, query, key, value, *args, **kwargs):
        place, kv = self.split._attend, self.split._kv
        i = place["calls"]
        place["calls"] = i + 1
        n_q, n_k = int(query.shape[-2]), int(key.shape[-2])
        if place["whole"]:
            if n_q == n_k == place["tokens"]:
                kv[i] = (key.clone(), value.clone())
            return self.own(query, key, value, *args, **kwargs)
        kept = kv.get(i)
        length = place["length"]
        if kept is None or n_q != length or n_k != length:
            return self.own(query, key, value, *args, **kwargs)
        mask = args[0] if args else kwargs.get("attn_mask")
        causal = args[2] if len(args) > 2 else kwargs.get("is_causal", False)
        if mask is not None or causal:
            raise ValueError("a patch's self-attention is given a mask here, which keys and values shared with the "
                             "other patches cannot keep")
        keys, values = kept
        start = place["part"] * length
        keys.narrow(-2, start, length).copy_(key)
        values.narrow(-2, start, length).copy_(value)
        return self.own(query, keys, values, *args, **kwargs)


def _attention(split: Split) -> _Attention:
    return _Attention(split)


_STAGE: list = []


def _stage_module(split: Split) -> Any:
    """A torch module of the split's stage in this process, as PyTorch's pipelining wraps one: each part's call runs
    the split's own blocks (Split._run_stage)."""
    if not _STAGE:
        import torch

        class _Stage(torch.nn.Module):
            def __init__(self, owner: Split) -> None:
                super().__init__()
                self._owner = [owner]            # a list: not a submodule, so its blocks are not registered twice

            def forward(self, hidden):
                return self._owner[0]._run_stage(hidden, lead=True)

        _STAGE.append(_Stage)
    return _STAGE[0](split)


def _divisor(n: int, most: int) -> int:
    """The largest divisor of `n` that is `most` or less (1 for none above it)."""
    for parts in range(min(n, max(1, most)), 0, -1):
        if n % parts == 0:
            return parts
    return 1


def _fastpath(on: Optional[bool]) -> Optional[bool]:
    """MultiheadAttention's fused path set on or off where torch has the switch; what it was."""
    import torch

    mha = getattr(torch.backends, "mha", None)
    if mha is None or not hasattr(mha, "set_fastpath_enabled"):
        return None
    was = mha.get_fastpath_enabled()
    if on is not None:
        mha.set_fastpath_enabled(on)
    return was


def _sync(tensor: Any) -> None:
    import torch

    if _is_tensor(tensor) and tensor.is_cuda:
        torch.cuda.synchronize(tensor.device)


def _sync_any(args: tuple, kwargs: dict) -> None:
    for value in _leaves((args, kwargs)):
        if _is_tensor(value) and value.is_cuda:
            _sync(value)
            return


def _slot_of(args: tuple, kwargs: dict, previous: Any) -> Any:
    """Which argument of a block's call is the one before's output: its position, or its keyword; None for none."""
    for i, value in enumerate(args):
        if value is previous:
            return i
    for name, value in kwargs.items():
        if value is previous:
            return name
    return None


def _has_slot(args: tuple, kwargs: dict, slot: Any) -> bool:
    return (isinstance(slot, int) and slot < len(args)) or (isinstance(slot, str) and slot in kwargs)


def _slot_value(args: tuple, kwargs: dict, slot: Any) -> Any:
    return args[slot] if isinstance(slot, int) else kwargs[slot]


def _with_slot(args: tuple, kwargs: dict, slot: Any, value: Any) -> tuple:
    if isinstance(slot, int):
        return (*args[:slot], value, *args[slot + 1:]), kwargs
    return args, {**kwargs, slot: value}


def _output_of(output: Any) -> tuple:
    """A block's output as (its tensor, how it was given back: None, or [kind, length]); (None, None) for an output
    with other tensors in it than the first."""
    if _is_tensor(output):
        return output, None
    if isinstance(output, (tuple, list)) and output and _is_tensor(output[0]) \
            and all(value is None for value in output[1:]):
        return output[0], ["tuple" if isinstance(output, tuple) else "list", len(output)]
    return None, None


def _first(output: Any) -> Any:
    return output[0] if isinstance(output, (tuple, list)) else output


def _leads(value: Any, n: int) -> bool:
    return _is_tensor(value) and value.dim() >= 1 and int(value.shape[0]) == n


def _is_tensor(value: Any) -> bool:
    import torch

    return isinstance(value, torch.Tensor)


def _leaves(tree: Any) -> list:
    from torch.utils import _pytree

    return _pytree.tree_leaves(tree)


def _map(tree: Any, fn: Callable) -> Any:
    from torch.utils import _pytree

    return _pytree.tree_map(fn, tree)
