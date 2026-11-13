"""What the TRL adapter says about its per-sample training metrics (`plan(training=...)`): how TRL computes its own
logged series of each per-sample key (so the server can rebuild it), and what it cannot capture, with why."""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

from probe.generated.samples import SampleSplit
from probe.generated.samples.points import Dtype, Grouping, Reducer, RollupSource
from probe.generated.samples.points.training import MAX_LOGGING_WINDOW, MAX_UNSUPPORTED_CHARS

#: Why the run's `eval/loss` is approximate (transformers' `evaluation_loop`).
EVAL_LOSS_APPROXIMATE = (
    "transformers repeats each eval batch's loss once per example and gathers it with gather_for_metrics, which cuts "
    "the last gathered batch to the dataset's remainder: batches weigh by size, and GRPO's repeated eval prompts lose "
    "real rows to the cut"
)

#: The `unsupported` key a whole-run stop is declared under: a pattern naming every key.
EVERY_KEY = "*"
#: What a key no reason names falls back to (a hook's own reasons come first, `LossHook.get_reasons`).
NOT_REBUILT = "the loss hook does not rebuild this; nothing per sample is sent"
PACKED_SFT, SFT_TENSOR_PARALLEL = "packed SFT", "SFT tensor parallel"
#: Paths whose rows are proven on GPUs (T3, 2 x A100 bf16 flash-attn: `~/plans/rl-trajectory-gaps/gpu/trl/RESULT.md`);
#: a path built but not named here declares its reason below and sends nothing.
GPU_PROVEN: frozenset[str] = frozenset({PACKED_SFT, SFT_TENSOR_PARALLEL})
# What the adapter cannot capture, by what (`TrainingPlan.unsupported`), and why. A run declares the ones it hits.
UNSUPPORTED: dict[str, str] = {
    PACKED_SFT: "packed and padding-free SFT rows are switched off in this build (`GPU_PROVEN`); nothing per sample is "
                "sent",
    "packed SFT (bfd_split)": "this packing strategy splits an example across packed rows, so a row's tokens do not "
                              "name one sample; use packing_strategy='bfd' or padding_free",
    "packed SFT (wrapped)": "this packing strategy drops example boundaries, so a row's tokens do not name one "
                            "sample; use packing_strategy='bfd' or padding_free",
    "SFT context parallel": "context parallelism cuts each example into pieces across ranks before the loss, so a "
                            "rank's rows would be partial examples; nothing per sample is sent",
    "SFT sequence parallel": "Ulysses sequence parallelism splits each example across ranks; per-sample rows need "
                             "each shard keyed to its example and sent as a fragment, which only a GPU run can show; "
                             "nothing per sample is sent",
    SFT_TENSOR_PARALLEL: "SFT tensor parallel rows are switched off in this build (`GPU_PROVEN`); nothing per sample "
                         "is sent",
    "SFT loss": "a loss_type other than nll or dft, a compute_loss_func, or label smoothing with loss_type='dft' or "
                "with packing or padding_free: the hook rebuilds nll, dft and unpacked nll + label smoothing only; "
                "nothing per sample is sent",
    "SFT without record_sft": "per-sample metrics name SFT examples, which are samples only with "
                              "track(record_sft=True)",
    "GOLD cross-tokenizer loss": "GOLD's cross-tokenizer ULD and X-Token losses align student and teacher tokens by "
                                 "byte offsets and never call generalized_jsd_loss; per-sample metrics are sent for "
                                 "same-tokenizer GOLD only",
    "eval metric_key_prefix": "more evaluate() metric_key_prefix values than the plan can declare rollups for; "
                              "passes past them send no per-sample rows",
}  # fmt: skip
#: Two `evaluate()` prefixes whose passes made loss calls, anywhere in the run (a dict of eval datasets, or a
#: `metric_key_prefix="test"` pass beside the default): a loss rollup folds every eval row of a step whatever its name.
EVAL_LOSSES = "eval loss under several metric_key_prefix values"
UNSUPPORTED[EVAL_LOSSES] = (
    "the server folds an eval loss rollup over every eval row of a step whatever its metric_key_prefix, so once two "
    "evaluate() prefixes have made loss calls (a dict of eval datasets, or a test pass beside the eval one) no eval "
    "loss is rebuilt; the rows, their loss bookkeeping and each prefix's other keys are still sent, and a loss rollup "
    "scoped to its own prefix needs a server change"
)
#: GOLD's per-writer losses: kept beside the loss it sends, never rebuilt.
GOLD_WRITER_KEYS = ("on_policy_loss", "off_policy_loss")
GOLD_WRITER_REASON = ("GOLD logs this as the mean of one writer's (student or dataset) micro-batch losses x GA, "
                      "rounded to 4 places (gold_trainer.py:3360-3362); rows carry no writer filter or rounding, so no "
                      "rollup rebuilds it")
UNSUPPORTED.update(dict.fromkeys(GOLD_WRITER_KEYS, GOLD_WRITER_REASON))
#: A trainer subclass that defines its own loss method (TRL's GMPOTrainer): `UNSUPPORTED` key and why.
OVERRIDE_SUFFIX = " overrides "
OVERRIDE_REASON = ("the loss hook rebuilds the TRL trainer's own {method}; this subclass computes its own loss, so "
                   "nothing per sample is sent")
#: Every name TRL computes per token and logs as a series, by trainer kind: the token-weighted ones.
GRPO_TOKEN_KEYS = ("entropy", "clip_ratio/low_mean", "clip_ratio/high_mean", "clip_ratio/region_mean")
SFT_TOKEN_KEYS = ("entropy", "mean_token_accuracy")
#: A row's own value of these is the row's clip mean; TRL's series takes each call's min or max over rows.
EXTREME_KEYS = {"clip_ratio/low_min": Reducer.MIN, "clip_ratio/high_max": Reducer.MAX}
#: transformers' default `metric_key_prefix`: eval rows log under `eval_<key>`, TRL's own eval names.
EVAL_KEY_PREFIX = "eval"
#: The `evaluate()` prefixes a run declares rollups for (`eval` and 8 more, a dict of eval datasets): each adds one
#: rollup per eval key, and a plan holds at most `MAX_POINT_METRICS`.
MAX_EVAL_PREFIXES = 9


def get_run_key(name: str) -> str:
    """The run's own series of a TRL log key under `report_to="probe"` (`train/loss`, `eval/loss`): the HF callback's
    `rewrite_logs` rule (`integrations/huggingface.py`, which needs transformers to import; the real test pins both)."""
    for prefix in ("eval_", "test_"):
        if name.startswith(prefix):
            return f"{prefix[:-1]}/{name[len(prefix):]}"
    return f"train/{name}"


def make_rollups(train_keys: Iterable[str], *, dtype: Dtype = Dtype.FP32, dtypes: Mapping[str, Dtype] | None = None,
                 has_policy_loss: bool = False, logging_window: int | None = None,
                 eval_prefixes: Sequence[str] = (EVAL_KEY_PREFIX,), extremes: Mapping[str, Reducer] = EXTREME_KEYS,
                 step_reducers: Mapping[str, Reducer] | None = None) -> dict[str, dict]:  # fmt: skip
    """How TRL computes each logged series, for the train keys and, per `evaluate()` prefix in ``eval_prefixes``,
    their `<prefix>_` twins, as grouping levels (finest first). `loss`: the sum of a process's returned (GA-scaled)
    micro-batch losses, the mean over processes (`trainer.py:2229-2234`); `eval_loss`: the mean of every process's
    batch losses; a token key: each call's token-weighted mean over every process (`global_masked_mean`), the mean
    over the step's calls; an ``extremes`` key: each call's min/max over every process's rows, then the step's
    ``step_reducers`` (TRL: the mean over calls; AsyncGRPO: min/max); `policy_loss`: each process's loss before the
    bonus, the mean over processes, then over calls. A train series pools every step since its last log
    (``logging_window``); `evaluate()` logs its own at once. Each key's tolerance is the loss tensors' ``dtype`` unless
    it is computed from others (``dtypes``, by train name: `entropy`). An eval key's series is the HF callback's name
    of `<prefix>_<key>`, the name TRL logs the loss under (diagnostics TRL logs as `eval_<key>` whatever the prefix,
    so a dict of eval datasets collides there; the rows' own series keep each dataset apart)."""
    rollups: dict[str, dict[str, Any]] = {}
    splits = [(SampleSplit.TRAIN, "")] + [(SampleSplit.EVAL, f"{prefix}_") for prefix in eval_prefixes]
    keys = list(dict.fromkeys(train_keys))
    for split, prefix in splits:
        is_train = split is SampleSplit.TRAIN
        found: dict[str, dict[str, Any]] = {"loss": {
            "source": RollupSource.CONTRIBUTION,
            "levels": make_levels((Grouping.RANK, Reducer.SUM), (Grouping.STEP, Reducer.MEAN)) if is_train
            else make_levels((Grouping.MICRO_BATCH, Reducer.SUM), (Grouping.STEP, Reducer.MEAN)),
        }}  # fmt: skip
        if not is_train:
            found["loss"]["approximate"] = EVAL_LOSS_APPROXIMATE
        for key in keys:
            step = (step_reducers or {}).get(key, Reducer.MEAN)
            found[key] = {"levels": make_levels((Grouping.CALL, extremes.get(key, Reducer.WEIGHTED_MEAN)),
                                                (Grouping.STEP, step))}  # fmt: skip
        if has_policy_loss:
            found["policy_loss"] = {"levels": make_levels(
                (Grouping.MICRO_BATCH, Reducer.SUM), (Grouping.CALL, Reducer.MEAN), (Grouping.STEP, Reducer.MEAN))}
        for key, rollup in found.items():
            if is_train and logging_window is not None:
                rollup["logging_window"] = logging_window
            rollups[f"{prefix}{key}"] = {"run_key": get_run_key(f"{prefix}{key}"), "split": split,
                                         "dtype": (dtypes or {}).get(key, dtype), **rollup}  # fmt: skip
    return rollups


def get_logging_window(args: Any) -> int:
    """How many steps each logged train point pools (transformers logs every `logging_steps`, a ratio of
    `max_steps` when below 1, averaging every step since its last log). Unknown before `train()` (an epoch
    strategy, a ratio of a length not yet counted): the contract's largest window, which the check reads from the
    previous logged point (the first point then reads unchecked, never unreconciled)."""
    strategy = getattr(getattr(args, "logging_strategy", "steps"), "value", getattr(args, "logging_strategy", "steps"))
    steps = getattr(args, "logging_steps", 1)
    if str(strategy) != "steps" or not isinstance(steps, (int, float)) or steps <= 0:
        return MAX_LOGGING_WINDOW
    if steps >= 1:
        return min(int(steps), MAX_LOGGING_WINDOW)
    max_steps = getattr(args, "max_steps", -1)
    return min(math.ceil(max_steps * steps), MAX_LOGGING_WINDOW) if isinstance(max_steps, int) and max_steps > 0 \
        else MAX_LOGGING_WINDOW


def make_levels(*levels: tuple[Grouping, Reducer]) -> list[dict[str, Any]]:
    return [{"by": by, "reducer": reducer} for by, reducer in levels]


def get_reason(what: str, reasons: Mapping[str, str] | None = None) -> str:
    """Why ``what`` (a hook's own reason in ``reasons``, an `UNSUPPORTED` key, or `<Class> overrides <method>`) is
    not captured."""
    if reasons and what in reasons:
        return reasons[what]
    if OVERRIDE_SUFFIX in what:
        return OVERRIDE_REASON.format(method=what.split(OVERRIDE_SUFFIX, 1)[1])
    return UNSUPPORTED.get(what, NOT_REBUILT)


def make_plan(*, rollups: Mapping[str, Mapping[str, Any]] | None = None, unsupported: Iterable[str] = (),
              stopped: Iterable[str] = (), reasons: Mapping[str, str] | None = None) -> dict:  # fmt: skip
    """A `TrainingPlan`: loss bookkeeping when rollups exist, and why each named thing is not captured (``reasons``:
    the hook's own words for what it names, before `UNSUPPORTED`'s). ``stopped``: what stopped capture for the whole
    run, declared under `*` too (the contract's pattern naming every key)."""
    plan: dict[str, Any] = {"sends_loss_bookkeeping": bool(rollups)}
    if rollups:
        plan["rollups"] = {key: dict(rollup) for key, rollup in rollups.items()}
    found = {what: get_reason(what, reasons) for what in unsupported}
    whole = "; ".join(f"{what}: {get_reason(what, reasons)}" for what in stopped)
    if whole:
        found[EVERY_KEY] = whole if len(whole) <= MAX_UNSUPPORTED_CHARS else f"{whole[:MAX_UNSUPPORTED_CHARS - 3]}..."
    if found:
        plan["unsupported"] = found
    return plan
