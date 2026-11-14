"""What the verl adapter declares about its per-sample metrics (`plan(training=...)`): it sends loss bookkeeping;
how verl builds its own series of each per-sample key, so the trainer check can rebuild it (S0 amendment A1:
`update_mean`, each row weighted by its share of the update's number, then the plain mean over the step's updates);
and every path no spike proved, with why; the critic's own declaration (D4). Why: DESIGN.md "Per-sample training metrics"."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from probe.generated.samples import SampleSplit
from probe.generated.samples.points import Dtype, Grouping, LossRole, Reducer, RollupSource

#: verl's per-micro-batch keys the hook logs per sample (`losses.py:56-180`, vanilla `core_algos.py:1286-1375`;
#: score centering's `actor/sc_correction`, `core_algos.py:2415`; distillation's term, `distillation/losses.py:263`).
VALUE_KEYS = ("actor/pg_loss", "actor/entropy_loss", "actor/kl_loss", "actor/pg_clipfrac", "actor/ppo_kl",
              "actor/pg_clipfrac_lower", "actor/sc_correction", "actor/distillation/loss")  # fmt: skip
#: Terms verl reduces in the autocast dtype (the engine's entropy, S0: bf16 `agg_loss` sums it in bf16); the score
#: centering and distillation keys too until a GPU run proves them fp32 (only CPU fp32 ran, T2c).
AUTOCAST_KEYS = frozenset({"actor/entropy_loss", "actor/sc_correction", "actor/distillation/loss"})
#: [update: sum, step: mean]: the row's weight is its share of its update's number (A1).
UPDATE_MEAN = [{"by": Grouping.UPDATE, "reducer": Reducer.SUM}, {"by": Grouping.STEP, "reducer": Reducer.MEAN}]
#: `actor/loss`: per rank the micro-batches' losses summed, averaged over ranks (`engine_workers.py:229-234`),
#: then over the step's updates.
LOSS_LEVELS = [{"by": Grouping.RANK, "reducer": Reducer.SUM}, {"by": Grouping.UPDATE, "reducer": Reducer.MEAN},
               {"by": Grouping.STEP, "reducer": Reducer.MEAN}]  # fmt: skip
#: A validation series is the plain mean over the prompts with n responses of each prompt's mean, i.e. over rows.
EVAL_LEVELS = [{"by": Grouping.STEP, "reducer": Reducer.WEIGHTED_MEAN}]
#: `actor/entropy`: one pass a step (fully async: one a mini-step, each weighted by its pass), no update; the step's rows
#: pooled by their weights.
ENTROPY_LEVELS = [{"by": Grouping.STEP, "reducer": Reducer.WEIGHTED_MEAN}]

#: Every `policy_loss.loss_mode` in verl's `POLICY_LOSS_REGISTRY` at the pin, with None when a spike proved its rows
#: (D16 a/b/c, `rl-trajectory-gaps/spike/verl/RESULT.md`; clip_cov: T11's replay, `gpu/p2/verl/RESULT.md`), else why it
#: sends none. Spike letters (also in `verl_d16.py` and the reports): a = shard and series rebuild, b = one row alone
#: (PLAN D16(a)), c = training bitwise unchanged (PLAN D16(b)). The one list: the supported set and the declarations
#: both come from it. A mode not listed (a newer verl's) sends nothing either.
LOSS_MODES: dict[str, str | None] = {
    "vanilla": None, "dppo_tv": None, "dppo_kl": None, "gspo": None, "sapo": None, "gpg": None, "kl_cov": None,
    "geo_mean": None, "dro": None, "cispo": None, "bypass_mode": None, "clip_cov": None,
}  # fmt: skip
#: clip_cov zeroes the loss of a random draw (`torch.randperm`, `core_algos.py:1823`) of tokens its micro-batch's
#: covariance picks: a row is the sample's share GIVEN that draw. Recomputed alone with the draw kept it matches its
#: row; with a fresh draw it does not. Said on the path (it names no key: every key is sent).
CLIP_COV_CAVEAT = ("rows are sent; each row is the sample's share given its micro-batch's random token draw "
                   "(torch.randperm over the micro-batch's covariance picks); recomputed alone with a fresh draw it "
                   "differs")  # fmt: skip
SUPPORTED_LOSS_MODES = frozenset(mode for mode, reason in LOSS_MODES.items() if reason is None)
#: `actor/entropy` (the driver's old-log-prob pass) is folded the way `fit()` folds it (`ray_trainer.py:1588-1593`)
#: only under these `loss_agg_mode`s: each row's token mean, weighted by its tokens (token-mean) or 1 per row with a
#: trained token (seq-mean-token-mean). `loss_scale_factor` only scales seq-mean-token-sum-norm (`core_algos.py:1189`).
ENTROPY_MODES = frozenset({"token-mean", "seq-mean-token-mean"})
ENTROPY_KEY = "actor/entropy"

#: The Megatron engine's configurations a GPU proof ran (D18 proven boundary, `rl-trajectory-gaps/gpu/p2/verl/
#: RESULT.md` and `gpu/p2/dp/RESULT.md`), by role: (tensor, pipeline) parallel sizes -> the largest data-parallel size
#: that layout ran at (T11: data parallel 1, every report `ranks_expected: 1`; T15, 4 x A100: the actor and the critic
#: at TP 2 x DP 2 and PP 2 x DP 2), each at context parallel 1, bf16, a dense model (no experts, no MTP), no expert or
#: virtual pipeline parallelism, Megatron-FSDP, LoRA or per-token loss, verl's default packed (THD) inputs. Read from
#: the worker's engine and its config at run time; every other Megatron configuration, and any gated value that cannot
#: be read, keeps a named reason (`get_megatron_reason`).
MEGATRON_PROVEN: dict[str, dict[tuple[int, int], int]] = {"actor": {(2, 1): 2, (1, 2): 2},
                                                         "critic": {(2, 1): 2, (1, 2): 2}}  # fmt: skip
MEGATRON_REASON = ("only the configurations its GPU proof ran send rows (tensor x pipeline x data parallel sizes per "
                   "role, context parallel 1, bf16, a dense model without MTP, no expert or virtual "
                   "pipeline parallelism, Megatron-FSDP, LoRA or per-token loss, packed inputs); any other, or one "
                   "whose config cannot be read, sends none")  # fmt: skip
#: The `McoreEngineConfig` fields the gate reads (`workers/config/engine.py:98-110`, `:182-206`). A field the config
#: does not carry is refused by name (D18: a missing value fails closed); None is accepted only where verl's own
#: default is None (`MEGATRON_NONE_DEFAULTS`, `:184`, `:186`).
MEGATRON_ENGINE_FIELDS = ("tensor_model_parallel_size", "pipeline_model_parallel_size", "context_parallel_size",
                          "dynamic_context_parallel", "expert_model_parallel_size", "expert_tensor_parallel_size",
                          "virtual_pipeline_model_parallel_size", "use_megatron_fsdp", "use_remove_padding", "dtype",
                          "override_transformer_config")  # fmt: skip
MEGATRON_NONE_DEFAULTS = frozenset({"expert_tensor_parallel_size", "virtual_pipeline_model_parallel_size"})
#: The `HFModelConfig` fields it reads (`workers/config/model.py:122-146`): Megatron's LoRA (`lora.rank`,
#: `megatron_peft.py:23`), FSDP's `lora_rank`, the HF config (its experts) and MTP.
MEGATRON_MODEL_FIELDS = ("lora", "lora_rank", "hf_config", "mtp")
#: The HF config fields that count a model's experts (verl's own list, `delta_weight_transfer.py:110`).
EXPERT_FIELDS = ("num_experts", "moe_num_experts", "n_routed_experts", "num_local_experts")
#: What `_read` returns for a field the config does not carry (distinct from a field set to None).
MISSING = object()
#: What a gated field that cannot be read says after its name.
UNREAD = "could not be read, and a value that cannot be read is never taken as one the GPU proof ran"
#: verl's distillation `loss_mode`s at the pin (`distillation/losses.py:343`, `:444`): k3, forward_kl_topk and
#: forward_kl_topk_tail ran (T2c, D16 a/b/c); the other estimators are the same function as k3 (`kl_penalty` picks
#: the per-token formula), so their term reaches the same `agg_loss`. A mode not listed (a newer verl's) sends nothing.
DISTILLATION_MODES = frozenset({"kl", "k1", "abs", "mse", "k2", "low_var_kl", "k3", "forward_kl_topk",
                                "forward_kl_topk_tail"})  # fmt: skip
#: `use_policy_gradient`: the policy loss the distillation term is reduced by; only vanilla ran inside it (T2c).
DISTILLATION_POLICY_MODES = frozenset({"vanilla"})
UNSUPPORTED = {
    "megatron": f"the Megatron engine: {MEGATRON_REASON}",
    **{f"policy_loss.loss_mode={mode}": reason for mode, reason in LOSS_MODES.items() if reason is not None},
    "distillation.distillation_loss.policy_loss_mode": "under use_policy_gradient only the vanilla policy loss has "
                                                       "been run with Probe inside verl's distillation loss; another "
                                                       "mode sends no per-sample training metrics",
    ENTROPY_KEY: "the driver's old-log-prob entropy is sent per sample only under loss_agg_mode token-mean or "
                 "seq-mean-token-mean, and not in bypass mode (algorithm.rollout_correction.bypass_mode: verl runs "
                 "no old-log-prob pass)",
}  # fmt: skip
#: Score centering's metrics no per-sample term carries (T2c, D6), by verl's logged name.
SCORE_CENTERING_UNSENT = {
    **dict.fromkeys(("actor/sc_sampler_head_mass", "actor/sc_train_head_mass"),
                    "verl's ppo_loss computes these score-centering masses with the masked_mean it imports by name "
                    "(workers/utils/losses.py:23, :157), which the loss watch does not see"),
    **dict.fromkeys(("actor/sc_support_aligned", "actor/sc_sampler_tail_mass", "actor/sc_support_unknown"),
                    "verl reduces these score-centering fractions straight from its model-output dict "
                    "(workers/utils/losses.py:144-155), not under a per-sample term"),
}  # fmt: skip
#: Distillation's diagnostics (T2c, D6), by verl's logged name (`rename_dict(..., "actor/")`).
DISTILLATION_UNSENT = {
    **{f"actor/distillation/{name}": "verl computes these distillation diagnostics with a plain mean, min or max over "
                                     "the micro-batch's masked tokens (trainer/distillation/losses.py:111-122, "
                                     ":396-434, :477), not through a reduction the loss watch sees"
       for name in ("abs_loss", "loss_min", "loss_max", "student_mass", "student_mass_min", "student_mass_max",
                    "teacher_mass", "teacher_mass_min", "teacher_mass_max", "overlap_ratio",
                    "overlap_token_advantage", "topk_loss", "tail_loss", "teacher_tail_mass", "student_tail_mass")},
    **{f"actor/distillation/{name}": "verl renames the distillation policy loss's metrics to distillation/* "
                                     "(trainer/distillation/losses.py:327); per-sample values are sent for "
                                     "distillation/loss only"
       for name in ("pg_clipfrac", "ppo_kl", "pg_clipfrac_lower")},
}  # fmt: skip
#: The fully async trainer's mini-steps verl never logs (rows sent, nothing of verl's to rebuild; T2c finding 3).
FULLY_ASYNC_UNLOGGED = {
    "fully_async.unlogged_mini_steps": "verl's fully async trainer logs a mini-step's actor metrics at the next weight "
                                       "sync's log (fully_async_trainer.py:601-604), so the mini-steps after the "
                                       "run's last sync log (at least its last mini-step) are logged only by fit()'s "
                                       "final flush, which logs them only when the run ends on a sync and "
                                       "current_param_version % trainer.test_freq != 0 (never under the default "
                                       "test_freq=-1, :529-531); their rows are sent at the step verl would log "
                                       "them at, with no verl value there to rebuild",
}  # fmt: skip
#: The critic's per-micro-batch keys (`value_loss`, `workers/utils/losses.py:187`; D4): verl's own names.
CRITIC_VALUE_KEYS = ("critic/vf_loss", "critic/vf_clipfrac")
CRITIC_UNSUPPORTED = {
    "critic/vpred_mean": "verl's value_loss computes vpred_mean with a masked_mean the loss watch does not see",
}
#: A warmup step (`trainer.critic_warmup > global_steps`, `ray_trainer.py:1684`) trains the critic alone: the driver
#: stamps nothing then, so the step sends no critic rows and no `actor/entropy` rows while verl logs both.
CRITIC_WARMUP = {
    "trainer.critic_warmup": "a critic warmup step (trainer.critic_warmup > global_steps) sends no per-sample critic "
                             "rows and no actor/entropy rows, though verl logs critic/* and actor/entropy there",
}  # fmt: skip
#: A critic's path the hook does not support names only the critic's keys (D4: never `*`, never the actor's).
CRITIC_KEYS = (*CRITIC_VALUE_KEYS, "critic/loss")
#: Every key the plans declare a per-sample value for: only these are matched to a watched mean (T2c finding 1).
DECLARED_KEYS = frozenset((*VALUE_KEYS, *CRITIC_VALUE_KEYS))


def build_training_plan(config: Any, unsupported_here: Mapping[str, str] | None = None) -> dict[str, Any]:
    """The declaration for this run's config. bf16 autocast (verl's default) makes the entropy term bf16.
    ``unsupported_here``: what this trainer family adds (`TrainerFamily.get_unsupported`)."""
    actor = _get(_get(config, "actor_rollout_ref"), "actor")
    autocast = get_autocast_dtype(_get(actor, "fsdp_config"))
    rollups: dict[str, Any] = {
        key: {"levels": UPDATE_MEAN, "dtype": autocast if key in AUTOCAST_KEYS else Dtype.FP32} for key in VALUE_KEYS
    }
    rollups["actor/loss"] = {"source": RollupSource.CONTRIBUTION, "levels": LOSS_LEVELS, "dtype": autocast}
    unsupported = {**UNSUPPORTED, **SCORE_CENTERING_UNSENT, **DISTILLATION_UNSENT, **(unsupported_here or {})}
    policy_loss = _get(actor, "policy_loss")
    if str(_get(policy_loss, "loss_mode") or "vanilla") == "clip_cov":
        unsupported["policy_loss.loss_mode=clip_cov"] = CLIP_COV_CAVEAT
    if has_entropy_rows(config):
        rollups[ENTROPY_KEY] = {"levels": ENTROPY_LEVELS, "dtype": autocast}
        del unsupported[ENTROPY_KEY]
    for section in ("val-core", "val-aux"):
        rollups[f"{section}/*"] = {"split": SampleSplit.EVAL, "levels": EVAL_LEVELS}
    return {"sends_loss_bookkeeping": True, "rollups": rollups, "unsupported": unsupported}


def build_critic_plan(engine_config: Any, reason: str | None = None) -> dict[str, Any]:
    """The critic producer's own declaration (D4): only the critic's keys, each `role: critic`; ``reason``: why this
    critic's path sends nothing, said for its keys alone (never `*`)."""
    if reason is not None:
        return {"sends_loss_bookkeeping": False, "rollups": {}, "unsupported": build_critic_unsupported(reason)}
    autocast = get_autocast_dtype(engine_config)
    rollups: dict[str, Any] = {key: {"role": LossRole.CRITIC, "levels": UPDATE_MEAN, "dtype": autocast}
                               for key in CRITIC_VALUE_KEYS}  # fmt: skip
    rollups["critic/loss"] = {"role": LossRole.CRITIC, "source": RollupSource.CONTRIBUTION, "levels": LOSS_LEVELS,
                              "dtype": autocast}  # fmt: skip
    return {"sends_loss_bookkeeping": True, "rollups": rollups, "unsupported": {**CRITIC_UNSUPPORTED, **CRITIC_WARMUP}}


def build_critic_unsupported(reason: str) -> dict[str, str]:
    """Every critic key, unsent for ``reason`` (D4: only the critic's own keys, never `*`)."""
    return {**dict.fromkeys(CRITIC_KEYS, reason), **CRITIC_UNSUPPORTED}


def get_megatron_reason(engine_config: Any, model_config: Any, role: str, data_parallel_size: int | None) -> str | None:
    """Why this Megatron worker sends no rows (None: a configuration `MEGATRON_PROVEN` names). ``engine_config``: the
    worker's `McoreEngineConfig`; ``model_config``: its `HFModelConfig`; ``role``: "actor" or "critic";
    ``data_parallel_size``: the engine's own (`get_data_parallel_size`), None when it could not be read."""
    engine = {name: _read(engine_config, name) for name in MEGATRON_ENGINE_FIELDS}
    for name, value in engine.items():
        if value is MISSING or (value is None and name not in MEGATRON_NONE_DEFAULTS):
            return f"the engine config's {name} {UNREAD}"
    if model_config is None:
        return f"the worker's model config (LoRA, experts, MTP) {UNREAD}"
    model = {name: _read(model_config, name) for name in MEGATRON_MODEL_FIELDS}
    for name, value in model.items():
        if value is MISSING or value is None:
            return f"the model config's {name} {UNREAD}"
    mtp = _read(model["mtp"], "enable")
    if mtp is MISSING or mtp is None:
        return f"the model config's mtp.enable {UNREAD}"
    context = int(engine["context_parallel_size"])
    if context > 1 or engine["dynamic_context_parallel"]:
        return (f"context parallel (context_parallel_size={context}) has not been run with Probe: verl splits each "
                "sequence across the context-parallel ranks and switches Megatron to a per-token loss there")
    expert, expert_tensor = int(engine["expert_model_parallel_size"]), int(engine["expert_tensor_parallel_size"] or 1)
    if expert > 1 or expert_tensor > 1:
        return (f"expert parallelism (expert_model_parallel_size={expert}, expert_tensor_parallel_size="
                f"{expert_tensor}) has not been run with Probe")
    experts = count_experts(model["hf_config"])
    if experts > 0:
        return f"a mixture-of-experts model ({experts} experts in its HF config) has not been run with Probe"
    virtual = int(engine["virtual_pipeline_model_parallel_size"] or 1)
    if virtual > 1:
        return f"virtual pipeline parallelism (virtual_pipeline_model_parallel_size={virtual}) has not been run with Probe"
    if engine["use_megatron_fsdp"]:
        return "Megatron-FSDP (use_megatron_fsdp) has not been run with Probe"
    if not engine["use_remove_padding"]:
        return "padded (BSHD) inputs (use_remove_padding=False) have not been run with Probe"
    if str(engine["dtype"]) != "bfloat16":
        return f"dtype={engine['dtype']} has not been run with Probe on Megatron (the GPU proof ran bfloat16)"
    if _get(engine["override_transformer_config"], "calculate_per_token_loss"):
        return ("a per-token loss (override_transformer_config.calculate_per_token_loss) has not been run with Probe: "
                "Megatron's finalize_model_grads then divides every gradient by the step's token count")
    if int(_get(model["lora"], "rank") or 0) > 0 or int(model["lora_rank"]) > 0:
        return "LoRA (model.lora.rank > 0) has not been run with Probe"
    if mtp:
        return "multi-token prediction (model.mtp.enable) has not been run with Probe on Megatron"
    if data_parallel_size is None:
        return f"the engine's data-parallel size {UNREAD}"
    tensor, pipeline = int(engine["tensor_model_parallel_size"]), int(engine["pipeline_model_parallel_size"])
    proven = MEGATRON_PROVEN.get(role, {})
    if (tensor, pipeline) not in proven:
        ran = ", ".join(f"TP {t} x PP {p}" for t, p in sorted(proven)) or "none"
        return (f"the {role} at tensor_model_parallel_size={tensor}, pipeline_model_parallel_size={pipeline} has not "
                f"been run with Probe (proven for the {role}: {ran})")
    largest = proven[(tensor, pipeline)]
    if data_parallel_size > largest:
        return (f"the {role} at TP {tensor} x PP {pipeline} with data parallel {data_parallel_size} has not been run "
                f"with Probe (its GPU proof ran data parallel up to {largest})")
    return None


def count_experts(hf_config: Any) -> int:
    """How many experts the HF config (or its text config) names: 0 for a dense model, which names none."""
    configs = [hf_config]
    get_text_config = getattr(hf_config, "get_text_config", None)
    if callable(get_text_config):
        configs.append(get_text_config())
    for config in configs:
        for name in EXPERT_FIELDS:
            value = _get(config, name)
            if isinstance(value, (list, tuple)):
                value = value[0] if value else 0
            if value and int(value) > 0:
                return int(value)
    return 0


def has_entropy_rows(config: Any) -> bool:
    """Whether the driver's `actor/entropy` comes from an old-log-prob pass (none in bypass mode, `ray_trainer.py:
    1574-1576`) and folds as the per-sample rows rebuild it (`ENTROPY_MODES`). ``config``: the trainer's whole config."""
    correction = _get(_get(config, "algorithm"), "rollout_correction")
    if _get(correction, "bypass_mode"):
        return False
    actor = _get(_get(config, "actor_rollout_ref"), "actor")
    return str(_get(actor, "loss_agg_mode") or "token-mean") in ENTROPY_MODES


def get_autocast_dtype(fsdp_config: Any) -> Dtype:
    precision = _get(_get(fsdp_config, "mixed_precision"), "param_dtype")
    return Dtype.FP32 if str(precision or "bf16").lower() in ("fp32", "float32", "torch.float32") else Dtype.BF16


def _get(target: Any, name: str) -> Any:
    value = _read(target, name)
    return None if value is MISSING else value


def _read(target: Any, name: str) -> Any:
    if target is None or target is MISSING:
        return MISSING
    if isinstance(target, Mapping):
        return target.get(name, MISSING)
    try:
        return getattr(target, name, MISSING)
    except Exception:  # noqa: BLE001 -- an OmegaConf interpolation that cannot resolve here
        return MISSING
