"""One call of Miles' `loss_function` turned into rows: each reduction `watch.py` saw is re-reduced by Miles' own
reducer on a detached float64 copy and autograd gives each row's exact share (N4: the reducer is pure, no collective);
names come from `names.py`. Policy, value (the critic) and SFT losses; score centering through the policy path.
Everything read on the host goes in one copy per micro-batch (`copy_to_host`). Line refs are
`radixark/miles@bb18e6ab7811`. Why: DESIGN.md "Per-sample training metrics"."""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from probe.generated.samples.points import Dtype, hash_mask
from probe.sdk.run.samples.points import MicroBatchCapture, RowCapture, Share, copy_to_host, get_lowest_dtype, keep_finite

from ..samples.mapping import hash_tokens
from .names import ENTROPY, ESS, LOSS, OPSM_CLIPFRAC, get_unreduced, match_by_order, match_by_value
from .plan import LossType
from .update import RankFacts
from .watch import LossCalls

#: The reduction whose input ESS is taken from.
PPO_KL = "ppo_kl"
#: Columns per reduction in the stats table: row summand, row share; then (no context parallel) the ESS sums.
_PER_CALL = 2
_PER_CALL_ESS = 4


@dataclass
class LossCallCapture:
    """One captured `loss_function` call: its rows (row ids from ``first_row``), each row's identity (rollout index,
    token digest) and Miles' names the call sends."""

    micro_batch: MicroBatchCapture
    identities: list[tuple[Any, str]]
    names: set[str]


@dataclass
class PendingSummary:
    """One loss call's device-side tables, read on the host only once the update ended (D13: a host copy inside
    `loss_function` stalls the step until the forward finishes, ~60 ms a step on GPU)."""

    columns: list[Any]
    flat: Any
    scalars: list[Any]
    lengths: list[int]
    #: Per row: (mask length, token length) inside its flat run.
    sizes: list[tuple[int, int]]
    reduction_dtypes: list[Any]
    log_keys: list[str]
    args: Any
    facts: RankFacts
    sample_indices: list[Any]
    scaling: tuple
    has_ess: bool
    has_cp_ess: bool
    has_opsm: bool
    extra: int

    @property
    def rows(self) -> int:
        return len(self.sizes)


def summarize_loss_call(calls: LossCalls, *, args: Any, batch: Mapping[str, Any], result: Any, facts: RankFacts,
                        micro_batch_count: int, sample_indices: list[Any], first_row: int) -> LossCallCapture | None:  # fmt: skip
    """The micro-batch's rows from one `loss_function` call, at once (`start_summary` then `finish_summary`)."""
    pending = start_summary(calls, args=args, batch=batch, result=result, facts=facts,
                            micro_batch_count=micro_batch_count, sample_indices=sample_indices)  # fmt: skip
    return None if pending is None else finish_summary(pending, first_row)


def start_summary(calls: LossCalls, *, args: Any, batch: Mapping[str, Any], result: Any, facts: RankFacts,
                  micro_batch_count: int, sample_indices: list[Any]) -> PendingSummary | None:  # fmt: skip
    """Inside `loss_function`: the device-side work only (no host copy, no sync). None when the call reduced nothing
    or its rows do not line up with the stamp (`result` = its `(loss, normalizer, log)`)."""
    import torch
    from miles.backends.training_utils.data.context_parallel import get_local_response_loss_masks

    loss, _normalizer, log = result
    local_masks = get_local_response_loss_masks(batch["total_lengths"], batch["response_lengths"],
                                                batch["loss_masks"], args.qkv_format, batch.get("max_seq_lens"))  # fmt: skip
    rows = len(local_masks)
    if not calls.reductions or rows != len(sample_indices):
        return None
    # PaddedRows (torchtitan without dynamic shapes) reduces `[T]` logit rows: its own row-to-sample map, and no ESS
    has_padded = any(call.row_ids is not None for call in calls.reductions)
    has_ess = facts.cp_size == 1 and not has_padded
    device = calls.reductions[0].values.device
    row_ids = torch.cat([torch.full((int(mask.numel()),), row, device=device, dtype=torch.long)
                         for row, mask in enumerate(local_masks)])  # a fill on the device, no host copy  # fmt: skip
    local = torch.cat([mask.reshape(-1) for mask in local_masks]).to(device=device, dtype=torch.float64)
    columns = [torch.stack([mask.to(device=device, dtype=torch.float64).sum() for mask in batch["loss_masks"]]),
               _add_by_row(local, row_ids, rows)]  # fmt: skip
    for call in calls.reductions:
        leaf = call.values.to(torch.float64).clone().requires_grad_(True)
        with torch.enable_grad():
            (gradient,) = torch.autograd.grad(call.reducer(leaf), leaf)
        ids = row_ids if call.row_ids is None else call.row_ids
        columns += [_add_by_row(gradient * leaf.detach(), ids, rows), _add_by_row(gradient, ids, rows)]
        if has_ess:  # each reduction's ESS sums, picked on the host once ppo_kl is named (no second copy)
            weights = _get_importance_weights(call.values) * local
            columns += [_add_by_row(weights, row_ids, rows), _add_by_row(weights * weights, row_ids, rows)]
    extra = len(columns)
    # Context parallel: Miles' own all-reduced whole-sample ESS sums, sent from fragment 0 only (Miles zeroes the
    # other fragments' share, `math_utils.py:83-84`); the hook copies them and runs no collective (D15).
    has_cp_ess = facts.cp_size > 1 and facts.cp == 0 and calls.ess_sums is not None \
        and int(calls.ess_sums.shape[0]) == rows  # fmt: skip
    if has_cp_ess:
        columns += [calls.ess_sums[:, 0].to(torch.float64), calls.ess_sums[:, 1].to(torch.float64)]
    # OPSM's per-sample masked fraction (weight 1: Miles sums it); without context parallel only (`plan.OPSM_UNDER_CP`).
    has_opsm = facts.cp_size == 1 and calls.opsm_mask is not None and int(calls.opsm_mask.numel()) == int(row_ids.numel())
    if has_opsm:
        columns.append(_add_by_row(1.0 - calls.opsm_mask.to(device=device, dtype=torch.float64), row_ids, rows))
    masks = [mask.reshape(-1) for mask in batch["loss_masks"]]
    tokens = [t.reshape(-1) for t in batch["unconcat_tokens"]]
    flat, lengths = build_flat_rows(masks, tokens, device)
    values = log["values"].detach().reshape(-1)  # [the sample or token count, then each key's value]
    # read after the update ends: copied on the device now (no sync), so Miles' later in-place work never shows
    named = values[1:].clone()
    scalars = [_keep(call.output) for call in calls.reductions] + list(named.unbind()) + [_keep(loss)]
    return PendingSummary(
        columns=columns, flat=flat, scalars=scalars, lengths=lengths,
        sizes=[(int(m.numel()), int(t.numel())) for m, t in zip(masks, tokens, strict=True)],
        reduction_dtypes=[call.values.dtype for call in calls.reductions], log_keys=list(log["keys"]), args=args,
        facts=facts, sample_indices=sample_indices, scaling=_get_scaling(args, facts, micro_batch_count),
        has_ess=has_ess, has_cp_ess=has_cp_ess, has_opsm=has_opsm, extra=extra,
    )  # fmt: skip


def finish_summary(pending: PendingSummary, first_row: int) -> LossCallCapture:
    """After the update: the one host copy, the names and each row (row ids from ``first_row``)."""
    args, facts, rows, extra = pending.args, pending.facts, pending.rows, pending.extra
    has_ess, has_cp_ess, has_opsm = pending.has_ess, pending.has_cp_ess, pending.has_opsm
    sample_indices = pending.sample_indices
    host = copy_to_host(pending.columns, pending.flat, pending.scalars, lengths=pending.lengths)  # the one copy
    count = len(pending.reduction_dtypes)
    outputs, named_values, reported = host.scalars[:count], host.scalars[count:-1], host.scalars[-1]
    per_call = _PER_CALL_ESS if has_ess else _PER_CALL
    loss_type = getattr(args, "loss_type", LossType.POLICY_LOSS)
    named_log = dict(zip(pending.log_keys, named_values, strict=True))
    names = match_by_order(outputs, named_log, args) if loss_type == LossType.POLICY_LOSS else None
    if names is None:
        names = match_by_value(outputs, named_log, host.rows, per_call, get_unreduced(args))
    is_sft = loss_type == LossType.SFT_LOSS and count == 1  # `loss = -sum_of_sample_mean(log_probs)` (`losses.py:458`)
    if is_sft:
        names = {}
    is_value = loss_type == LossType.VALUE_LOSS and LossType.VALUE_LOSS in names  # the critic's loss is its value loss
    scale, factor, normalizer = pending.scaling
    has_loss = bool(_build_loss(dict.fromkeys(names, (0.0, 0.0)), args)) or is_sft or is_value
    has_row_ess = has_ess and PPO_KL in names
    captured, identities = [], []
    for row in range(rows):
        stats_row, flags = host.rows[row], host.flags[row]
        mask_length, token_length = pending.sizes[row]
        full, local_count = stats_row[0], stats_row[1]
        summands = {name: (stats_row[2 + per_call * j], stats_row[3 + per_call * j]) for name, j in names.items()}
        summands.update(_build_loss(summands, args))
        if is_sft:
            summands[LOSS] = (-stats_row[2], stats_row[3])
        row_values, bases = {}, {}
        for name, (summand, mass) in summands.items():
            if mass > 0 and math.isfinite(summand / mass):
                row_values[facts.get_key(name)], bases[facts.get_key(name)] = summand / mass, (mass, Share.TOTAL)
        ess_sums = None
        if has_row_ess:
            ess_sums = stats_row[4 + per_call * names[PPO_KL]], stats_row[5 + per_call * names[PPO_KL]], local_count
        elif has_cp_ess:
            ess_sums = stats_row[extra], stats_row[extra + 1], full
        ess = _get_ess(*ess_sums) if ess_sums is not None and full > 0 else None
        if ess is not None:
            row_values[facts.get_key(ESS)] = ess
            bases[facts.get_key(ESS)] = (full if facts.is_per_token else 1.0, Share.TOTAL)
        if has_opsm:
            row_values[facts.get_key(OPSM_CLIPFRAC)] = stats_row[extra + (2 if has_cp_ess else 0)] / max(full, 1.0)
            bases[facts.get_key(OPSM_CLIPFRAC)] = (1.0, Share.TOTAL)
        loss_summand, loss_mass = summands.get(LossType.VALUE_LOSS if is_value else LOSS, (0.0, 0.0))
        token_ids = [int(value) for value in flags[mask_length:mask_length + token_length]]
        identities.append((sample_indices[row], hash_tokens(token_ids)))
        captured.append(RowCapture(  # an unrebuildable loss leaves loss_sum and contribution unset, never 0
            row=first_row + row, token_count=int(round(local_count)), mask_sha256=hash_mask(flags[:mask_length]),
            loss_sum=(loss_summand / loss_mass * local_count if loss_mass > 0 else 0.0) if has_loss else None,
            contribution=loss_summand * factor if has_loss and factor is not None else None,
            contribution_terms={}, normalizer=None if normalizer is None else normalizer(full),
            values=row_values, bases=bases,
        ))  # fmt: skip
    sent = set(names) | ({LOSS} if has_loss and not is_value else set()) | \
        ({ESS} if has_row_ess or has_cp_ess else set()) | ({OPSM_CLIPFRAC} if has_opsm else set())  # fmt: skip
    reduced = [0] if is_sft else names.values()
    dtype = get_lowest_dtype(_to_dtype(pending.reduction_dtypes[j]) for j in reduced) or Dtype.FP32
    micro_batch = MicroBatchCapture(
        rows=captured, reported_loss=None if facts.cp_size > 1 else keep_finite(reported), dtype=dtype, scale=scale,
        normalizer=facts.step_tokens if facts.is_per_token and not facts.is_megatron else None,
    )  # fmt: skip
    return LossCallCapture(micro_batch=micro_batch, identities=identities, names=sent)


def build_flat_rows(masks: list[Any], tokens: list[Any], device: Any) -> tuple[Any, list[int]]:
    """Each row's mask flags then its token ids, concatenated flat (never padded to the longest row: a mixed-length
    micro-batch would copy rows x longest values), and each row's own length for `copy_to_host`."""
    import torch

    parts = [torch.cat([m.to(device=device, dtype=torch.float64), t.to(device=device, dtype=torch.float64)])
             for m, t in zip(masks, tokens, strict=True)]  # fmt: skip
    return torch.cat(parts), [int(m.numel()) + int(t.numel()) for m, t in zip(masks, tokens, strict=True)]


def _add_by_row(values: Any, row_ids: Any, rows: int) -> Any:
    """Per-row sums; an id of ``rows`` (a padded row no sample owns) is dropped."""
    import torch

    added = torch.zeros(rows + 1, dtype=torch.float64, device=values.device)
    return added.index_add_(0, row_ids, values.reshape(-1).to(torch.float64))[:rows]


def _get_importance_weights(ppo_kl: Any) -> Any:
    """Miles' importance weight exp(-ppo_kl), clamped as Miles clamps it (`math_utils.py:21-33`)."""
    import torch

    try:
        from miles.backends.training_utils.loss.hub.math_utils import _safe_exp_neg_ppo_kl

        return _safe_exp_neg_ppo_kl(ppo_kl).to(torch.float64)
    except Exception:  # noqa: BLE001 -- an older layout: Miles' own clamp, by hand
        return torch.exp(-torch.nan_to_num(ppo_kl.to(torch.float64), nan=0.0).clamp(-20.0, 20.0))


def _get_ess(sum_weights: float, sum_squares: float, count: float) -> float | None:
    """Miles' per-sample ESS ratio (`math_utils.py:36-81`): sum(w)^2 / (tokens x sum(w^2)); None when not finite."""
    ess = sum_weights * sum_weights / (max(count, 1.0) * max(sum_squares, 1e-8))
    return ess if math.isfinite(ess) else None


def _build_loss(summands: Mapping[str, tuple[float, float]], args: Any) -> dict[str, tuple[float, float]]:
    """`loss` per row from its terms, as `policy_loss_function` builds it; {} when a term it needs is unmatched."""
    if "pg_loss" not in summands:
        return {}
    summand, mass = summands["pg_loss"]
    terms = []
    if getattr(args, "entropy_coef", 0) != 0:
        terms.append((ENTROPY, -float(args.entropy_coef)))
    if getattr(args, "use_kl_loss", False) and getattr(args, "kl_loss_coef", 0) != 0:
        terms.append(("kl_loss", float(args.kl_loss_coef)))
    for name, coefficient in terms:
        if name not in summands:
            return {}
        summand += coefficient * summands[name][0]
    return {LOSS: (summand, mass)}


def _get_scaling(args: Any, place: RankFacts, micro_batch_count: int) -> tuple:
    """How `loss_function` turned the summed reductions into the loss it returned (`objective.py:240-262`): the scale,
    the factor a row's summand is multiplied by (None: known only after the update) and its row normalizer."""
    from miles.backends.training_utils.parallel import get_parallel_state

    state = get_parallel_state()
    if not place.is_per_token:
        rollouts = float(place.rollouts or 1.0)
        if place.is_megatron:
            ulysses = bool(getattr(args, "true_on_policy_mode", False) and getattr(state, "is_ulysses_cp", False))
            scale = float(micro_batch_count * (state.intra_dp.size if ulysses else state.intra_dp_cp.size))
        else:
            scale = float(state.intra_dp.size)
        return scale, scale / rollouts, lambda full: rollouts * max(full, 1.0)
    if place.is_megatron:
        return float(state.cp.size), None, None
    scale = float(state.intra_dp.size)
    tokens = float(place.step_tokens or 1.0)
    return scale, scale / tokens, lambda full: tokens


def _keep(value: Any) -> Any:
    return value.detach().clone() if hasattr(value, "detach") else value


def _to_dtype(dtype: Any) -> Dtype:
    return {"torch.bfloat16": Dtype.BF16, "torch.float16": Dtype.FP16}.get(str(dtype), Dtype.FP32)
