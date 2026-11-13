"""What the verl adapter declares about its per-sample metrics (`plan(training=...)`): it sends loss bookkeeping;
how verl builds its own series of each per-sample key, so the trainer check can rebuild it (S0 amendment A1:
`update_mean`, each row weighted by its share of the update's number, then the plain mean over the step's updates);
and every path no spike proved, with why; the critic's own declaration (D4). Why: DESIGN.md "Per-sample training metrics"."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from probe.generated.samples import SampleSplit
from probe.generated.samples.points import Dtype, Grouping, LossRole, Reducer, RollupSource

#: verl's per-micro-batch keys the hook logs per sample (`losses.py:56-180`, vanilla `core_algos.py:1286-1375`).
VALUE_KEYS = ("actor/pg_loss", "actor/entropy_loss", "actor/kl_loss", "actor/pg_clipfrac", "actor/ppo_kl",
              "actor/pg_clipfrac_lower")  # fmt: skip
#: Terms verl reduces in the autocast dtype (the engine's entropy, S0: bf16 `agg_loss` sums it in bf16).
AUTOCAST_KEYS = frozenset({"actor/entropy_loss"})
#: [update: sum, step: mean]: the row's weight is its share of its update's number (A1).
UPDATE_MEAN = [{"by": Grouping.UPDATE, "reducer": Reducer.SUM}, {"by": Grouping.STEP, "reducer": Reducer.MEAN}]
#: `actor/loss`: per rank the micro-batches' losses summed, averaged over ranks (`engine_workers.py:229-234`),
#: then over the step's updates.
LOSS_LEVELS = [{"by": Grouping.RANK, "reducer": Reducer.SUM}, {"by": Grouping.UPDATE, "reducer": Reducer.MEAN},
               {"by": Grouping.STEP, "reducer": Reducer.MEAN}]  # fmt: skip
#: A validation series is the plain mean over the prompts with n responses of each prompt's mean, i.e. over rows.
EVAL_LEVELS = [{"by": Grouping.STEP, "reducer": Reducer.WEIGHTED_MEAN}]
#: `actor/entropy`: one pass a step, no update; the step's rows pooled by their weights.
ENTROPY_LEVELS = [{"by": Grouping.STEP, "reducer": Reducer.WEIGHTED_MEAN}]

#: Every `policy_loss.loss_mode` in verl's `POLICY_LOSS_REGISTRY` at the pin, with None when the T2 spike proved its
#: rows (D16 a/b/c, `rl-trajectory-gaps/spike/verl/RESULT.md`), else why it sends none. The one list: the supported
#: set and the declarations both come from it. A mode not listed (a newer verl's) sends nothing either.
LOSS_MODES: dict[str, str | None] = {
    "vanilla": None, "dppo_tv": None, "dppo_kl": None, "gspo": None, "sapo": None, "gpg": None, "kl_cov": None,
    "geo_mean": None, "dro": None, "cispo": None, "bypass_mode": None,
    "clip_cov": "clip_cov zeroes a random draw (torch.randperm) of high-covariance tokens over the whole micro-batch, "
                "so a sample cannot be recomputed on its own; its rows rebuild verl's series exactly and training is "
                "unchanged, but per-sample metrics stay off until that check passes",
}  # fmt: skip
SUPPORTED_LOSS_MODES = frozenset(mode for mode, reason in LOSS_MODES.items() if reason is None)
#: `actor/entropy` (the driver's old-log-prob pass) is folded the way `fit()` folds it (`ray_trainer.py:1588-1593`)
#: only under these `loss_agg_mode`s: each row's token mean, weighted by its tokens (token-mean) or 1 per row with a
#: trained token (seq-mean-token-mean). `loss_scale_factor` only scales seq-mean-token-sum-norm (`core_algos.py:1189`).
ENTROPY_MODES = frozenset({"token-mean", "seq-mean-token-mean"})
ENTROPY_KEY = "actor/entropy"

#: Why the Megatron engine stays off (`rl-trajectory-gaps/gpu/verl/RESULT.md` V3). The actor's `use_remove_padding`,
#: Ulysses, LoRA (with and without remove_padding) and bf16 paths are GPU-proven there and send rows.
MEGATRON_REASON = ("its GPU proof could not run (verl's prebuilt Megatron libraries, transformer-engine 2.20.2, need "
                   "Ubuntu 24.04 / glibc 2.38), so whether the row ids reach Megatron's loss is unproven")
UNSUPPORTED = {
    "trainer.use_v1": "the V1 trainer passes TransferQueue keys (KVBatchMeta) to the workers, and score centering "
                      "runs only there; neither has been run with Probe, so a V1 step sends no per-sample training "
                      "metrics (hook: RayPPOTrainerV1._update_actor, v1/trainer_base.py:1840)",
    "score_centering": "score centering runs only in the V1 trainer, which has not been run with Probe "
                       "(score_centering.py:353 feeds pg_losses, core_algos.py:2396)",
    "fully_async": "the fully async trainer's steps are parameter versions fed by a separate rollouter; it has not "
                   "been run with Probe, so it sends no per-sample training metrics "
                   "(hook: FullyAsyncTrainer.fit_step, fully_async_trainer.py:536)",
    "distillation": "verl's distillation computes its per-token top-k loss inside the engine's logits processor; it "
                    "has not been run with Probe, so a distillation step sends no per-sample training metrics "
                    "(hook: agg_loss(loss_mat=distillation_losses), trainer/distillation/losses.py:333)",
    "megatron": f"the Megatron engine sends no rows: {MEGATRON_REASON}",
    **{f"policy_loss.loss_mode={mode}": reason for mode, reason in LOSS_MODES.items() if reason is not None},
    ENTROPY_KEY: "the driver's old-log-prob entropy is sent per sample only under loss_agg_mode token-mean or "
                 "seq-mean-token-mean, and not in bypass mode (algorithm.rollout_correction.bypass_mode: verl runs "
                 "no old-log-prob pass)",
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


def build_training_plan(config: Any) -> dict[str, Any]:
    """The declaration for this run's config. bf16 autocast (verl's default) makes the entropy term bf16."""
    actor = _get(_get(config, "actor_rollout_ref"), "actor")
    autocast = get_autocast_dtype(_get(actor, "fsdp_config"))
    rollups: dict[str, Any] = {
        key: {"levels": UPDATE_MEAN, "dtype": autocast if key in AUTOCAST_KEYS else Dtype.FP32} for key in VALUE_KEYS
    }
    rollups["actor/loss"] = {"source": RollupSource.CONTRIBUTION, "levels": LOSS_LEVELS, "dtype": autocast}
    unsupported = dict(UNSUPPORTED)
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
        return {"sends_loss_bookkeeping": False, "rollups": {},
                "unsupported": {**{key: reason for key in CRITIC_KEYS}, **CRITIC_UNSUPPORTED}}  # fmt: skip
    autocast = get_autocast_dtype(engine_config)
    rollups: dict[str, Any] = {key: {"role": LossRole.CRITIC, "levels": UPDATE_MEAN, "dtype": autocast}
                               for key in CRITIC_VALUE_KEYS}  # fmt: skip
    rollups["critic/loss"] = {"role": LossRole.CRITIC, "source": RollupSource.CONTRIBUTION, "levels": LOSS_LEVELS,
                              "dtype": autocast}  # fmt: skip
    return {"sends_loss_bookkeeping": True, "rollups": rollups, "unsupported": {**CRITIC_UNSUPPORTED, **CRITIC_WARMUP}}


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
    if target is None:
        return None
    if isinstance(target, Mapping):
        return target.get(name)
    try:
        return getattr(target, name, None)
    except Exception:  # noqa: BLE001 -- an OmegaConf interpolation that cannot resolve here
        return None
