"""One call of verl's `ppo_loss` seen from inside: while it runs, every `agg_loss` and `masked_mean` it calls is
observed (each module's own function runs, its output is returned untouched, and the recording is guarded), then each
reduction is re-run by that same function on a detached float64 copy and autograd gives each row's exact share of it
(N4). The row ids, every column and every scalar reach the host in one copy (`copy_to_host`). Line refs are
`verl-project/verl@b17218ba58a6`. Why: DESIGN.md "Per-sample training metrics"."""

from __future__ import annotations

import inspect
import sys
from collections.abc import Callable, Collection, Mapping
from dataclasses import dataclass, field
from typing import Any

from probe.generated.samples.points import ContributionSource, Dtype, hash_mask
from probe.sdk.run.samples.points import MicroBatchCapture, RowCapture, Share, copy_to_host, get_lowest_dtype

from .plan import DECLARED_KEYS

#: `ppo_loss`'s terms by the local name the reduced matrix has in its caller (`losses.py:56-180`,
#: `core_algos.py:1286-1375`): the key verl logs it under and how it enters `policy_loss`.
TERMS = {
    "pg_losses": "actor/pg_loss",
    "entropy": "actor/entropy_loss",
    "kld": "actor/kl_loss",
    "clipped_vf_losses": "critic/vf_loss",  # the critic's `compute_value_loss` (`core_algos.py:2174`, D4)
    "distillation_losses": "actor/distillation/loss",  # `distillation_loss`'s own `agg_loss` (`losses.py:333`)
    "distillation_pg_losses": "actor/distillation/loss",  # under `use_policy_gradient` (`DISTILLATION_PG_TERM`)
}
#: `use_policy_gradient`: the distillation term is a policy loss over `-distillation_losses` (`losses.py:309-327`),
#: reduced as a second `pg_losses`; one reduced inside `distillation_loss` is named this (T2c).
DISTILLATION_PG_TERM = "distillation_pg_losses"
#: Where `distillation_loss` lives; a call whose stack passes through it is the distillation's own.
DISTILLATION_MODULE = "verl.trainer.distillation.losses"
#: How many frames up from a reduction `distillation_loss` can sit (it calls the policy loss, which reduces).
DISTILLATION_DEPTH = 8
#: A term verl logs scaled: `vf_loss = 0.5 * agg_loss(clipped_vf_losses)` (`core_algos.py:2175`). Its coefficient
#: carries the 0.5 into the contribution; its logged value carries it here.
VALUE_SCALES = {"critic/vf_loss": 0.5}
#: verl modules whose `agg_loss` / `masked_mean` the loss reaches through a module global.
AGG_LOSS_MODULES = ("verl.trainer.ppo.core_algos", "verl.workers.utils.losses", DISTILLATION_MODULE)
MASKED_MEAN_MODULE = "verl.utils.torch_functional"
#: Values match a returned metric within this (they are the same float32 computation).
MATCH_TOLERANCE = 1e-6
#: The row-id column the driver adds (`driver.stamp_update_batch`).
ROW_FIELD = "probe_row"
CRITIC_PREFIX = "critic/"


@dataclass
class AggCall:
    name: str | None
    arguments: dict[str, Any]
    #: The module's own `agg_loss` that ran (re-run on the copy).
    reduce: Callable[..., Any]


@dataclass
class LossCalls:
    """What one loss call reduced."""

    aggregations: list[AggCall] = field(default_factory=list)
    #: (values, mask, output) of each `masked_mean` over the whole micro-batch, detached, still on the device.
    means: list[tuple[Any, Any, Any]] = field(default_factory=list)
    #: Calls Probe could not record (a new argument verl added): the micro-batch is not captured.
    failures: int = 0


class ReductionWatch:
    """verl's `agg_loss` and `masked_mean`, observed in the modules that call them between `start` and `stop`."""

    def __init__(self) -> None:
        self.calls = LossCalls()
        self._saved: list[tuple[Any, str, Any]] = []

    def start(self) -> LossCalls:
        for name in AGG_LOSS_MODULES:
            self._patch(sys.modules.get(name), "agg_loss", _make_agg_watch)
        self._patch(sys.modules.get(MASKED_MEAN_MODULE), "masked_mean", _make_mean_watch)
        return self.calls

    def stop(self) -> None:
        while self._saved:
            module, name, value = self._saved.pop()
            setattr(module, name, value)

    def _patch(self, module: Any, name: str, make: Callable[[Any, LossCalls], Any]) -> None:
        real = getattr(module, name, None) if module is not None else None
        if callable(real):
            self._saved.append((module, name, real))
            setattr(module, name, make(real, self.calls))


def _make_agg_watch(real: Callable[..., Any], calls: LossCalls) -> Callable[..., Any]:
    try:
        signature: inspect.Signature | None = inspect.signature(real)
    except (TypeError, ValueError):
        signature = None

    def watch_agg_loss(*args: Any, **kwargs: Any) -> Any:
        output = real(*args, **kwargs)
        try:
            bound = signature.bind(*args, **kwargs)  # type: ignore[union-attr]
            bound.apply_defaults()
            arguments = dict(bound.arguments)
            calls.aggregations.append(AggCall(_get_caller_name(sys._getframe(1), arguments.get("loss_mat")),
                                              arguments, real))  # fmt: skip
        except Exception:  # noqa: BLE001 -- never reaches training: this micro-batch is not captured
            calls.failures += 1
        return output

    return watch_agg_loss


def _make_mean_watch(real: Callable[..., Any], calls: LossCalls) -> Callable[..., Any]:
    def watch_masked_mean(*args: Any, **kwargs: Any) -> Any:
        output = real(*args, **kwargs)
        try:
            # A whole micro-batch's mean; the distillation policy loss's own (`distillation/*`) are never candidates.
            if len(args) == 2 and not kwargs and getattr(output, "ndim", 1) == 0 \
                    and not _is_inside_distillation(sys._getframe(1)):
                calls.means.append((args[0].detach(), args[1].detach(), output.detach()))
        except Exception:  # noqa: BLE001 -- never reaches training
            calls.failures += 1
        return output

    return watch_masked_mean


def summarize_loss_call(calls: LossCalls, *, rows: Any, coefficients: Mapping[str, float], metrics: Mapping[str, Any],
                        loss: Any, prefix: str = "actor/", mask: Any = None,
                        declared: Collection[str] = DECLARED_KEYS) -> MicroBatchCapture | None:  # fmt: skip
    """The micro-batch's rows from one `ppo_loss` (or the critic's `value_loss`) call. ``rows``: the `probe_row`
    tensor; ``coefficients``: how each term key enters the loss; ``metrics``: what it returned (a `Metric`'s
    aggregation says how verl folds each key; the critic's bare floats fold as means); ``loss``: what it returned;
    ``prefix``: the role's metric names; ``mask``: the micro-batch's padded response mask, for a loss whose every
    term may bypass `agg_loss` (geo_mean at verl's defaults: no entropy, no KL term), so its rows are built with no
    term and the caller adds the rebuilt one; ``declared``: the keys the plan declares per sample, the only MEAN metrics
    matched to a watched mean. None when the call reduced no known term (and no ``mask`` was given) or a reduction was
    not recorded."""
    import torch

    terms = [call for call in calls.aggregations if call.name in TERMS and TERMS[call.name] in coefficients]
    if calls.failures or (not terms and mask is None):
        return None
    mask = (terms[0].arguments["loss_mask"] if terms else mask).detach().to(torch.float64)
    tokens = mask.sum(-1)
    columns = [rows, tokens]
    shares: list[tuple[str, int, int]] = []  # key, its column of row sums, its gradient-mass column
    contributions = []
    dtypes = set()
    loss_sum = torch.zeros_like(tokens)
    pg_mass = torch.zeros_like(tokens)
    for call in terms:
        key = TERMS[call.name]
        matrix = call.arguments["loss_mat"]
        dtypes.add(_to_dtype(matrix.dtype))
        copy = matrix.detach().to(torch.float64).clone().requires_grad_(True)
        with torch.enable_grad():
            reduced = call.reduce(**{**call.arguments, "loss_mat": copy})
            (gradient,) = torch.autograd.grad(reduced, copy)
        values = copy.detach() * mask
        coefficient = float(coefficients[key])
        shares.append((key, len(columns), len(columns) + 1))
        columns += [values.sum(-1), gradient.sum(-1)]
        contributions.append((key, coefficient * (gradient * copy.detach()).sum(-1)))
        loss_sum = loss_sum + coefficient * values.sum(-1)
        if call.name == "pg_losses":
            pg_mass = gradient.sum(-1)
    # Every whole-micro-batch mean is a candidate for a MEAN metric: its row sums ride the copy, matched after it.
    means = [mean for mean in calls.means if tuple(mean[0].shape) == tuple(mask.shape)]
    mean_start = len(columns)
    columns += [(values.to(torch.float64) * mean_mask.to(torch.float64)).sum(-1) for values, mean_mask, _ in means]
    contribution_start = len(columns)
    columns += [part for _, part in contributions]
    columns += [loss_sum, pg_mass]
    wanted = {name: _get_first_value(metric) for name, metric in metrics.items() if name.startswith(prefix)
              and name in declared and name not in coefficients
              and _get_aggregation(metric, prefix) is Share.CALL_MEAN}  # fmt: skip
    arguments = terms[0].arguments if terms else {}
    mode = str(arguments.get("loss_agg_mode") or "")
    normalizer = arguments.get("global_batch_size") if mode.startswith("seq-mean") else arguments.get("batch_num_tokens")
    scalars = [loss, arguments.get("dp_size"), normalizer, *(output for *_, output in means), *wanted.values()]
    host = copy_to_host(columns, (mask > 0), scalars)
    reported, dp_size, normalizer_number = host.scalars[:3]
    found_means = host.scalars[3: 3 + len(means)]
    matched = _match_means(dict(zip(wanted, host.scalars[3 + len(means):], strict=True)), found_means)
    mean_columns = [(name, mean_start + index) for name, index in matched.items()]
    width = len(columns)
    batch_tokens = sum(row[1] for row in host.rows)
    scale = dp_size or 1.0
    aggregations = {key: _get_aggregation(metrics.get(_get_metric_name(key))) or Share.RANK_MEAN for key, *_ in shares}
    value_scales = {key: VALUE_SCALES.get(key, 1.0) for key, *_ in shares}
    captured = []
    for stats, row_flags in zip(host.rows, host.flags, strict=True):
        count = stats[1]
        values: dict[str, float | None] = {}
        bases: dict[str, tuple[float, Share]] = {}
        for key, sum_column, mass_column in shares:
            values[key] = value_scales[key] * stats[sum_column] / count if count else None
            bases[key] = (stats[mass_column], aggregations[key])
        for key, column in mean_columns:
            values[key] = stats[column] / count if count else None
            bases[key] = (count / batch_tokens if batch_tokens else 0.0, Share.CALL_MEAN)
        terms_out = {key: stats[contribution_start + offset] for offset, (key, _) in enumerate(contributions)}
        mass = stats[width - 1]
        captured.append(RowCapture(
            row=int(stats[0]), token_count=int(round(count)), mask_sha256=hash_mask(row_flags),
            loss_sum=stats[width - 2], contribution=sum(terms_out.values()), contribution_terms=terms_out,
            normalizer=scale * count / mass if count and mass else None, values=values, bases=bases,
        ))  # fmt: skip
    return MicroBatchCapture(rows=captured, reported_loss=reported, scale=scale, normalizer=normalizer_number,
                             dtype=get_lowest_dtype(dtypes) or Dtype.FP32)  # fmt: skip


def _match_means(wanted: Mapping[str, float | None], outputs: list[float | None]) -> dict[str, int]:
    """Each declared MEAN metric the loss returned (`actor/pg_clipfrac`, `actor/ppo_kl`, ...) matched, in order, to
    the whole-micro-batch `masked_mean` that produced it (same value): its index among the candidates. By value, so
    ``wanted`` holds declared keys only: a mean no watch sees (score centering's head mass, exactly 1.0 with a complete
    support) would take another mean's rows when the values tie (T2c: rebuilt 0.125 vs verl's 0.916)."""
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


def _get_caller_name(frame: Any, value: Any) -> str | None:
    """The caller's local name for ``value`` (a term name in `TERMS` first); a `pg_losses` reduced inside verl's
    `distillation_loss` is the distillation term (`DISTILLATION_PG_TERM`)."""
    names = [name for name, local in frame.f_locals.items() if local is value]
    name = next((name for name in names if name in TERMS), names[0] if names else None)
    return DISTILLATION_PG_TERM if name == "pg_losses" and _is_inside_distillation(frame) else name


def _is_inside_distillation(frame: Any) -> bool:
    """Whether ``frame`` runs inside verl's `distillation_loss` (within `DISTILLATION_DEPTH` frames)."""
    for _ in range(DISTILLATION_DEPTH):
        if frame is None:
            return False
        if frame.f_code.co_name == "distillation_loss" and frame.f_globals.get("__name__") == DISTILLATION_MODULE:
            return True
        frame = frame.f_back
    return False


def _get_metric_name(key: str) -> str:
    """verl returns `kl_loss` and `distillation/loss` without the prefix its driver adds (`rename_dict(...,
    "actor/")`)."""
    return {"actor/kl_loss": "kl_loss", "actor/distillation/loss": "distillation/loss"}.get(key, key)


def _get_aggregation(metric: Any, prefix: str = "actor/") -> Share | None:
    """verl's `Metric.aggregation`: SUM folds as a mean over ranks of the micro-batch sums, MEAN as the mean over
    (micro-batch, rank). None: not a `Metric` (`kl_coef`), except the critic's bare floats, which verl's
    `reduce_metrics` folds as a mean (`critic/vf_clipfrac`)."""
    if prefix == CRITIC_PREFIX and isinstance(metric, float):
        return Share.CALL_MEAN
    aggregation = getattr(getattr(metric, "aggregation", None), "value", None)
    if aggregation == "sum":
        return Share.RANK_MEAN
    return Share.CALL_MEAN if aggregation == "mean" else None


def _get_first_value(metric: Any) -> Any:
    """A `Metric`'s first value: a float (verl `.item()`s it) or, on another version, a tensor `copy_to_host` takes."""
    values = getattr(metric, "values", None)
    value = values[0] if isinstance(values, (list, tuple)) and values else getattr(metric, "value", metric)
    return value if not isinstance(value, bool) and (isinstance(value, (int, float)) or hasattr(value, "numel")) else None


def _to_dtype(dtype: Any) -> Dtype:
    return {"torch.bfloat16": Dtype.BF16, "torch.float16": Dtype.FP16}.get(str(dtype), Dtype.FP32)


def read_geo_mean_fields(data: Any) -> Any:
    """The padded fields geo_mean's pg term reads (`ppo_loss`'s own select, `losses.py:96-101`); its response mask is
    the micro-batch's when no `agg_loss` term was seen."""
    names = ["response_mask", "old_log_probs", "advantages"]
    if "rollout_is_weights" in data.keys():
        names.append("rollout_is_weights")
    return data.select(*names).to_padded_tensor()


def add_geo_mean_pg(captured: MicroBatchCapture, config: Any, data: Any, model_output: Any, fields: Any) -> None:
    """geo_mean reduces its pg term with a plain `torch.mean` over the micro-batch's rows (`core_algos.py:2000`), never
    `agg_loss`, so no watch sees it: each row's `pg_losses` is rebuilt from the loss's own inputs with verl's formula
    (`:1970-1997`, rollout IS weights folded to a sequence weight by their geometric mean, as verl does) and its share
    `pg_i / rows` added (source `probe_reducer`, the T2 spike's shard and alone checks). ``fields``:
    `read_geo_mean_fields(data)`. Raises when the rows do not match: the caller drops the micro-batch."""
    import torch
    from verl.workers.utils.padding import no_padding_2_padding

    log_prob = no_padding_2_padding(model_output["log_probs"], data).detach()
    mask = fields["response_mask"].to(bool)
    old, advantages = fields["old_log_probs"], fields["advantages"]
    clip = config.clip_ratio
    low = config.clip_ratio_low if config.clip_ratio_low is not None else clip
    high = config.clip_ratio_high if config.clip_ratio_high is not None else clip
    with torch.no_grad():
        log_ratio = log_prob - old
        sign = torch.sign(advantages)
        clamped = torch.clamp(log_ratio, -low, high)
        smaller = sign * torch.min(sign * log_ratio, sign * clamped)
        count = mask.sum(dim=-1)
        ratio = torch.exp((smaller * mask).sum(dim=-1) / (count + 1e-8))
        advantage = (advantages * mask).sum(dim=-1) / (count + 1e-8)
        pg_losses = -advantage * ratio
        if "rollout_is_weights" in fields.keys():
            weights = fields["rollout_is_weights"]
            pg_losses = pg_losses * torch.exp((torch.log(weights + 1e-10) * mask).sum(dim=-1) / (count + 1e-8))
        pg_losses = pg_losses.double().tolist()
    rows = len(pg_losses)
    if rows != len(captured.rows):
        raise ValueError(f"geo_mean rebuilt {rows} rows for a micro-batch of {len(captured.rows)}")
    for row, value in zip(captured.rows, pg_losses, strict=True):
        row.contribution += value / rows
        row.contribution_terms["actor/pg_loss"] = value / rows
        row.values["actor/pg_loss"] = value if row.token_count else None
        row.bases["actor/pg_loss"] = (1.0 / rows, Share.RANK_MEAN)
    captured.source = ContributionSource.PROBE_REDUCER
