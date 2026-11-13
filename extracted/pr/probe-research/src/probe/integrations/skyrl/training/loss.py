"""One SkyRL `_forward_backward_micro` call seen from inside: while it runs, `ppo_utils.reduce_loss` (the policy
loss's masked sum), the worker's `masked_mean` (entropy, KL) and `ppo_utils.masked_mean` (clip ratio and the other
loss metrics) are observed: each module's own function runs, its output is returned untouched, and the recording is
guarded. Each row's share comes from autograd of that same reduction on a detached float64 copy (N4). SkyRL pre-scales
advantages by the loss reduction (`ppo_utils.py:1219-1287`), so a row's own policy loss is its token mean divided by
that scale. The row ids, scales, every column and every scalar reach the host in one copy (`copy_to_host`). Line refs
are `NovaSky-AI/SkyRL@d87004689e3a`. Why: DESIGN.md "Per-sample training metrics"."""

from __future__ import annotations

import inspect
import sys
from fnmatch import fnmatchcase
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from probe.generated.samples.points import Dtype, hash_mask
from probe.sdk.run.samples.points import MicroBatchCapture, RowCapture, Share, copy_to_host, to_float

POLICY_LOSSES_MODULE = "skyrl.backends.skyrl_train.utils.ppo_utils"
#: The off-policy correction's own `masked_mean` (`is_ratio_mean`, `off_policy_correction_utils.py:449`).
OFF_POLICY_MODULE = "skyrl.backends.skyrl_train.utils.off_policy_correction_utils"
WORKER_MODULE = "skyrl.backends.skyrl_train.workers.worker"
#: The columns the driver adds (`driver.py`), copied into `Experience.info` by the batch iterator wrap.
ROW_FIELD = "probe_row"
SCALE_FIELD = "probe_adv_scale"
#: SkyRL's per-micro-batch status keys, as its driver logs them (`policy/` prefix, `trainer.py:1617-1660`).
POLICY_LOSS = "policy/policy_loss"
ENTROPY = "policy/policy_entropy"
KL = "policy/policy_kl"
LOSS_METRICS_PREFIX = "loss_metrics/"
MATCH_TOLERANCE = 1e-6


@dataclass
class Reduction:
    values: Any
    mask: Any
    #: The module's own function that ran (re-run on the copy).
    reduce: Callable[..., Any]


@dataclass
class MeanCall:
    where: str
    #: The caller's local name for the values (`entropy_BS`, `kl_loss`).
    name: str | None
    values: Any
    mask: Any
    dim: Any
    output: Any
    reduce: Callable[..., Any]


@dataclass
class MicroCalls:
    reductions: list[Reduction] = field(default_factory=list)
    means: list[MeanCall] = field(default_factory=list)
    #: Calls Probe could not record (a new argument SkyRL added): the micro-batch is not captured.
    failures: int = 0


class ReductionWatch:
    """SkyRL's `reduce_loss` and both `masked_mean`s, observed in the modules that call them between `start` and
    `stop`."""

    def __init__(self) -> None:
        self.calls = MicroCalls()
        self._saved: list[tuple[Any, str, Any]] = []

    def start(self) -> MicroCalls:
        losses_module, worker = sys.modules[POLICY_LOSSES_MODULE], sys.modules[WORKER_MODULE]
        self._patch(losses_module, "reduce_loss", lambda real: _make_reduce_watch(real, self.calls))
        self._patch(worker, "masked_mean", lambda real: _make_mean_watch(real, "worker", self.calls))
        self._patch(losses_module, "masked_mean", lambda real: _make_mean_watch(real, "ppo_utils", self.calls))
        if (off_policy := sys.modules.get(OFF_POLICY_MODULE)) is not None:  # `is_ratio_mean`
            self._patch(off_policy, "masked_mean", lambda real: _make_mean_watch(real, "ppo_utils", self.calls))
        return self.calls

    def stop(self) -> None:
        while self._saved:
            module, name, value = self._saved.pop()
            setattr(module, name, value)

    def _patch(self, module: Any, name: str, make: Callable[[Any], Any]) -> None:
        real = getattr(module, name, None)
        if callable(real):
            self._saved.append((module, name, real))
            setattr(module, name, make(real))


def _get_signature(real: Callable[..., Any]) -> inspect.Signature | None:
    try:
        return inspect.signature(real)
    except (TypeError, ValueError):
        return None


def _make_reduce_watch(real: Callable[..., Any], calls: MicroCalls) -> Callable[..., Any]:
    signature = _get_signature(real)

    def watch_reduce_loss(*args: Any, **kwargs: Any) -> Any:
        output = real(*args, **kwargs)
        try:
            loss, mask = list(signature.bind(*args, **kwargs).arguments.values())[:2]  # type: ignore[union-attr]
            calls.reductions.append(Reduction(loss.detach(), None if mask is None else mask.detach(), real))
        except Exception:  # noqa: BLE001 -- never reaches training: this micro-batch is not captured
            calls.failures += 1
        return output

    return watch_reduce_loss


def _make_mean_watch(real: Callable[..., Any], where: str, calls: MicroCalls) -> Callable[..., Any]:
    signature = _get_signature(real)

    def watch_masked_mean(*args: Any, **kwargs: Any) -> Any:
        output = real(*args, **kwargs)
        try:
            bound = signature.bind(*args, **kwargs)  # type: ignore[union-attr]
            bound.apply_defaults()
            tensor, mask, dim = list(bound.arguments.values())[:3]
            calls.means.append(MeanCall(where, _get_caller_name(sys._getframe(1), tensor), tensor.detach(),
                                        None if mask is None else mask.detach(), dim, output.detach(), real))  # fmt: skip
        except Exception:  # noqa: BLE001 -- never reaches training
            calls.failures += 1
        return output

    return watch_masked_mean


def summarize_micro_call(calls: MicroCalls, *, rows: Any, scales: Any, status: Mapping[str, Any], micro_weight: float,
                         ranks: int, kl_coef: float, entropy_coef: float,
                         unsupported: tuple[str, ...] = ()) -> MicroBatchCapture | None:  # fmt: skip
    """The micro-batch's rows. ``rows`` / ``scales``: the `probe_row` / `probe_adv_scale` tensors (scales may be
    None); ``status``: what the call returned (`final_loss`, `loss_metrics/*`); ``micro_weight``: SkyRL's
    `microbatch_weight`; ``unsupported``: the plan's unsupported key patterns, whose loss metrics are never matched
    by value (`plan.get_unsupported_keys`). None when it was not the one policy-loss reduction the hook pins, or a call was not
    recorded."""
    import torch

    if len(calls.reductions) != 1 or calls.failures:
        return None
    reduction = calls.reductions[0]
    mask = reduction.mask.to(torch.float64)
    tokens = mask.sum(-1)
    zeros = torch.zeros_like(tokens)
    entropy = next((c for c in calls.means if c.where == "worker" and c.name == "entropy_BS"), None)
    kl = next((c for c in calls.means if c.where == "worker" and c.name == "kl_loss"), None)
    contribution_pg = get_row_shares(lambda x: reduction.reduce(x, reduction.mask), reduction.values)
    contribution_kl = get_row_shares(lambda x: kl.reduce(x, kl.mask, -1).mean(), kl.values) if kl else zeros
    contribution_entropy = get_row_shares(lambda x: entropy.reduce(x, entropy.mask), entropy.values) if entropy \
        else zeros  # fmt: skip
    columns = [rows, zeros if scales is None else scales, tokens, (reduction.values.to(torch.float64) * mask).sum(-1),
               contribution_pg, contribution_kl * kl_coef * micro_weight / ranks,
               -contribution_entropy * entropy_coef * micro_weight / ranks]  # fmt: skip
    named = [(key, call) for key, call in ((ENTROPY, entropy), (KL, kl)) if call is not None]
    named_start = len(columns)
    # Off-policy correction: each mean's OWN mask (the policy loss's mask is the corrected one; entropy, KL
    # and clip ratio average over the uncorrected `loss_mask`): its row sum, then its row token count.
    for _, call in named:
        own = get_own_mask(call, mask)
        columns += [(call.values.to(torch.float64) * own).sum(-1), own.sum(-1)]
    # Every whole-micro-batch `ppo_utils.masked_mean` is a candidate loss metric: its row sums ride the copy.
    candidates = [c for c in calls.means if c.where == "ppo_utils" and c.dim is None and tuple(c.values.shape) ==
                  tuple(mask.shape)]  # fmt: skip
    candidate_start = len(columns)
    for c in candidates:
        own = get_own_mask(c, mask)
        columns += [(c.values.to(torch.float64) * own).sum(-1), own.sum(-1)]
    wanted = {str(name): value for name, value in status.items() if str(name).startswith(LOSS_METRICS_PREFIX)
              and _is_number(value) and not any(fnmatchcase(f"policy/{name}", key) for key in unsupported)}  # fmt: skip
    scalars = [*(c.output.float().mean() for c in candidates), *wanted.values()]
    host = copy_to_host(columns, (mask > 0), scalars)
    matched = _match_loss_metrics(dict(zip(wanted, host.scalars[len(candidates):], strict=True)),
                                  host.scalars[: len(candidates)])  # fmt: skip
    named_columns = [(key, named_start + 2 * offset) for offset, (key, _) in enumerate(named)]
    named_columns += [(f"policy/{name}", candidate_start + 2 * index) for name, index in matched.items()]
    batch_rows = len(host.rows)
    batch_tokens = {column: sum(row[column + 1] for row in host.rows) for _, column in named_columns}
    captured = []
    for stats, row_flags in zip(host.rows, host.flags, strict=True):
        row_id, scale, count, policy_sum, pg, kl_c, entropy_c = stats[:7]
        scale = scale if scales is not None else None
        values: dict[str, float | None] = {}
        bases: dict[str, tuple[float, Share]] = {}
        if scale:  # the row's own loss with its raw advantages: SkyRL's policy losses are homogeneous in them
            values[POLICY_LOSS] = policy_sum / scale / count if count else None
            bases[POLICY_LOSS] = (scale * count, Share.TOTAL)
        for key, column in named_columns:
            own_count, tokens = stats[column + 1], batch_tokens[column]
            values[key] = stats[column] / own_count if own_count else None
            share = 1.0 / batch_rows if key == KL else (own_count / tokens if tokens else 0.0)
            bases[key] = (share, Share.CALL_MEAN)  # KL is a mean over rows (`worker.py:1267-1273`)
        terms = {POLICY_LOSS: pg, KL: kl_c, ENTROPY: entropy_c}
        terms = {key: value for key, value in terms.items() if key == POLICY_LOSS or value}
        captured.append(RowCapture(
            row=int(row_id), token_count=int(round(count)), mask_sha256=hash_mask(row_flags),
            loss_sum=policy_sum / scale if scale else None, normalizer=1.0 / scale if scale else None,
            contribution=pg + kl_c + entropy_c, contribution_terms=terms, values=values, bases=bases,
        ))  # fmt: skip
    tensors = (reduction.values, *(call.values for call in calls.means))
    dtype = Dtype.BF16 if any(t.dtype == torch.bfloat16 for t in tensors) else \
        Dtype.FP16 if any(t.dtype == torch.float16 for t in tensors) else Dtype.FP32  # fmt: skip
    return MicroBatchCapture(rows=captured, reported_loss=to_float(status.get("final_loss")), dtype=dtype)


def get_own_mask(call: MeanCall, fallback: Any) -> Any:
    """The mask a `masked_mean` call averaged over, as float64 (None: every token)."""
    import torch

    if call.mask is None:
        return torch.ones_like(fallback, dtype=torch.float64)
    return call.mask.to(torch.float64).expand_as(call.values) if call.mask.shape != call.values.shape else \
        call.mask.to(torch.float64)


def get_row_shares(reduction: Any, matrix: Any) -> Any:
    """Each row's share of ``reduction(matrix)``: the gradient times the values, summed over the row (exact for a
    reduction linear in the matrix)."""
    import torch

    copy = matrix.detach().to(torch.float64).clone().requires_grad_(True)
    with torch.enable_grad():
        (gradient,) = torch.autograd.grad(reduction(copy), copy)
    return (gradient * copy.detach()).sum(-1)


def _match_loss_metrics(wanted: Mapping[str, float | None], outputs: list[float | None]) -> dict[str, int]:
    """Each `loss_metrics/*` the policy loss returned (`clip_ratio`, ...) matched, in order, to the
    `ppo_utils.masked_mean` over this micro-batch that produced it (same value): its index among the candidates."""
    remaining = list(range(len(outputs)))
    matched: dict[str, int] = {}
    for name, want in wanted.items():
        if want is None:
            continue
        for position, index in enumerate(remaining):
            output = outputs[index]
            if output is not None and abs(output - want) <= MATCH_TOLERANCE * max(1.0, abs(want)):
                matched[name] = index
                del remaining[position]
                break
    return matched


def _is_number(value: Any) -> bool:
    """A Python number or a one-element tensor (SkyRL `.item()`s most; `copy_to_host` takes either)."""
    if isinstance(value, bool):
        return False
    return isinstance(value, (int, float)) or (hasattr(value, "numel") and value.numel() == 1)


def _get_caller_name(frame: Any, value: Any) -> str | None:
    names = [name for name, local in frame.f_locals.items() if local is value]
    return names[0] if names else None
