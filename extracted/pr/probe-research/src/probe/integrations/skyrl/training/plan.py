"""What the SkyRL adapter declares about its per-sample metrics (`plan(training=...)`): it sends loss bookkeeping;
how SkyRL builds its own series of each per-sample key (S0 amendment A1 `update_mean`: each row weighted by its share
of the update's number, then the plain mean over the step's updates) and in what precision; every path S0 did not
prove, with why (losses: derived from `SUPPORTED_LOSSES`). Why: DESIGN.md "Per-sample training metrics"."""

from __future__ import annotations

from typing import Any

from probe.generated.samples import SampleSplit
from probe.generated.samples.points import Dtype, Grouping, Reducer, RollupSource

#: [update: sum, step: mean]: SkyRL sums `*_loss` keys over micro-batches and ranks and averages the rest
#: (`worker_utils.py:77-147`); the row's weight already says which, so one rule covers both (A1).
UPDATE_MEAN = [{"by": Grouping.UPDATE, "reducer": Reducer.SUM}, {"by": Grouping.STEP, "reducer": Reducer.MEAN}]
#: `eval/<data source>/avg_score` and `mean_positive_reward`: plain means over the pass's trajectories.
EVAL_LEVELS = [{"by": Grouping.STEP, "reducer": Reducer.WEIGHTED_MEAN}]
#: The policy loss, entropy, KL and loss metrics all come out of `_forward_backward_micro`'s
#: `torch.autocast(dtype=torch.bfloat16, device_type="cuda")` (`worker.py:1157`), which SkyRL turns on with no
#: setting: bf16 on every GPU run (a CPU run computes fp32 and passes the wider bound too).
AUTOCAST_DTYPE = Dtype.BF16

#: The policy losses proven per sample (S0: regular, dppo; rl-trajectory-gaps T2 / T7: the rest): each reduces once
#: through `reduce_loss` and is positively homogeneous in the pre-scaled advantages (`ppo_utils.py:564-1066`).
#: clip_cov's row is its share GIVEN the micro-batch's own random token draw (`torch.randperm` over the batch's
#: covariance picks): recomputed alone with that draw it matches (T7); without it, it cannot.
SUPPORTED_LOSSES = frozenset({"regular", "dppo", "dual_clip", "gspo", "sapo", "cispo", "rollout_is", "reinforce",
                              "clip_cov"})  # fmt: skip
#: Why each loss SkyRL ships outside `SUPPORTED_LOSSES` sends no rows (any other: not proven).
LOSS_REASONS = {
    "kl_cov": "kl_cov adds kl_cov.ppo_kl_coef x |log ratio|, which the advantage does not scale, to the tokens it "
              "picks by batch covariance (`ppo_utils.py:1068-1121`), so a row's loss with its own advantages cannot "
              "be read back from the reduced tensor: 63% off when one row is recomputed alone",
    "cross_entropy": "cross_entropy is SkyRL's SFT objective: no advantages, no KL or entropy terms, its own status "
                     "keys (`worker.py:1195-1250`); record SFT examples instead",
    "importance_sampling": "importance_sampling (Tinker's loss) sums inline without `reduce_loss` "
                           "(`ppo_utils.py:1162-1210`): no reduction to observe",
}  # fmt: skip
#: The Megatron configurations a GPU proof ran (rl-trajectory-gaps T12 and T15, D19; `gpu/p2/skyrl/RESULT.md`,
#: `gpu/p2/dp/RESULT.md`): (tensor, pipeline) parallel sizes, each at data parallel 1 or 2 and no more
#: (`MEGATRON_PROVEN_DATA_PARALLEL`, `megatron.get_megatron_reason`). Each with
#: context parallel 1, expert parallel 1, no virtual pipeline, sample-based micro-batches, no packing, the plain LM head,
#: a text-only model, no router replay and no sample-support replay. Only these send rows (D18 proven boundary).
MEGATRON_PROVEN = frozenset({(1, 1), (2, 1), (1, 2)})
#: The largest data-parallel size any proven layout ran at (T12: DP 2 at TP 1 / PP 1; T15, 4 x A100: TP 2 x DP 2 and
#: PP 2 x DP 2).
MEGATRON_PROVEN_DATA_PARALLEL = 2
MEGATRON_REASON = ("SkyRL's Megatron worker sends rows only for the GPU-proven configurations (tensor parallel 2 or "
                   "pipeline parallel 2 at data parallel 1 or 2, or data parallel 2 alone; context and expert "
                   "parallel 1, no virtual pipeline, sample-based micro-batches, no packing, the plain LM head, a "
                   "text-only model, no router replay, no sample-support replay); any other trains without per-sample "
                   "training metrics")  # fmt: skip
#: Why a Megatron run outside `MEGATRON_PROVEN` sends no rows, by what it set (`megatron.get_megatron_reason`).
MEGATRON_REASONS = {
    "parallel": "SkyRL's Megatron worker at tensor parallel {tp} x pipeline parallel {pp} x data parallel {dp} was not "
                "proven per sample (only TP 2 or PP 2 at data parallel 1 or 2, and data parallel 2 alone, were): no "
                "rows are sent",
    "context_parallel": "SkyRL's Megatron worker under context parallelism splits each row across ranks before the "
                        "loss: not proven per sample, no rows are sent",
    "expert_parallel": "SkyRL's Megatron worker under expert parallelism was not proven per sample: no rows are sent",
    "virtual_pipeline": "SkyRL's Megatron worker under a virtual (interleaved) pipeline was not proven per sample: no "
                        "rows are sent",
    "packing": "SkyRL's Megatron worker with remove_microbatch_padding packs rows and computes entropy without the "
               "per-row mean Probe reads (`megatron_model_wrapper.py:1101`): no rows are sent",
    "token_batching": "SkyRL's Megatron worker with max_tokens_per_microbatch pads micro-batches to one size and adds "
                      "padding micro-batches: not proven per sample, no rows are sent",
    "fused_lm_head": "SkyRL's Megatron worker with fused_lm_head_logprob computes entropy inside the fused op, not "
                     "through the per-row mean Probe reads: no rows are sent",
    "sample_support": "SkyRL's Megatron worker with sample-support replay computes entropy over the sampler's support "
                      "(`megatron_model_wrapper.py:1088`): not proven per sample, no rows are sent",
    "mtp": "SkyRL's Megatron worker with multi-token prediction adds a draft loss to each micro-batch: not proven per "
           "sample, no rows are sent",
    "vlm": "SkyRL's Megatron worker on a vision-language model feeds image inputs through the vision tower before "
           "the loss: not proven per sample, no rows are sent",
    "router_replay": "SkyRL's Megatron worker with moe_enable_routing_replay replays the rollout's expert routing: not "
                     "proven per sample, no rows are sent",
}  # fmt: skip
MEGATRON_CRITIC_REASON = ("SkyRL's Megatron critic computes its loss inside Megatron's schedule, never through "
                          "`_forward_backward_micro`, the call Probe watches: its rows are not sent (the policy's are, "
                          "for the proven configurations)")  # fmt: skip
#: Paths and keys with no rows, with why. Packing (`remove_microbatch_padding`) and Ulysses sequence parallelism are
#: GPU-proven (rl-trajectory-gaps T3; the critic's T12): one process per data-parallel rank records. The fully async
#: trainer stamps its rows through the same batch conversion (rl-trajectory-gaps T12, D21).
UNSUPPORTED = {
    "policy_loss_type": f"policy losses other than {', '.join(sorted(SUPPORTED_LOSSES))} send no rows",
    **{f"policy_loss_type={name}": f"{reason}: no rows are sent" for name, reason in LOSS_REASONS.items()},
    "megatron": MEGATRON_REASON,
    "megatron_critic": MEGATRON_CRITIC_REASON,
    # Batch statistics and inline fractions, not per-sample sums through a reducer the hook observes.
    "policy/loss_metrics/is_ratio_std": "a batch standard deviation, not a per-sample sum",
    "policy/loss_metrics/is_ratio_max": "a batch extreme, not a per-sample sum",
    "policy/loss_metrics/is_ratio_min": "a batch extreme, not a per-sample sum",
    "policy/loss_metrics/*_clip_high_ratio": "an inline batch fraction of the off-policy correction, not observed",
    "policy/loss_metrics/outlier_seq_*": "an inline batch fraction of the off-policy correction, not observed",
    "policy/loss_metrics/token_mask_ratio": "an inline batch fraction of the off-policy correction, not observed",
    "policy/loss_metrics/*_sequence_mask_*": "an inline batch fraction of the off-policy correction, not observed",
    "policy/loss_metrics/cispo/ratio_max": "a micro-batch extreme, not a per-sample sum",
    "policy/loss_metrics/cispo/ratio_min": "a micro-batch extreme, not a per-sample sum",
    "policy/score_centering/*": "inline micro-batch diagnostics of score centering, not per-sample sums",
    "policy/rollout_train_logprobs_abs_diff_*": "the trainer's forward-pass diagnostics (`trainer.py:1509-1511`), "
                                                "outside any update",
}  # fmt: skip
#: Losses whose `clip_ratio` is a constant 0.0 (no clipping): it has no rows.
CONSTANT_CLIP_RATIO_LOSSES = frozenset({"sapo", "reinforce"})
#: clip_cov's rows are sent, with this caveat on its path (it names no key).
CLIP_COV_CAVEAT = ("each row is the sample's share given the micro-batch's random token draw; alone with a fresh draw "
                   "it differs up to 0.5%")  # fmt: skip


def get_loss_reason(loss: str) -> str | None:
    """Why ``loss`` sends no rows; None when it is supported."""
    if loss in SUPPORTED_LOSSES:
        return None
    return LOSS_REASONS.get(loss, f"policy loss {loss!r} was not proven per sample")


def build_training_plan(policy_loss_type: str | None = None) -> dict[str, Any]:
    """The declaration (`policy/` is how SkyRL's driver names a policy worker's metrics, `trainer.py:1617-1660`)."""
    rollups: dict[str, Any] = {key: {"levels": UPDATE_MEAN, "dtype": AUTOCAST_DTYPE} for key in (
        "policy/policy_loss", "policy/policy_entropy", "policy/policy_kl", "policy/loss_metrics/*")}  # fmt: skip
    rollups["policy/final_loss"] = {"source": RollupSource.CONTRIBUTION, "levels": UPDATE_MEAN, "dtype": AUTOCAST_DTYPE}
    rollups["eval/*"] = {"split": SampleSplit.EVAL, "levels": EVAL_LEVELS}
    unsupported = dict(UNSUPPORTED)
    if str(policy_loss_type) in CONSTANT_CLIP_RATIO_LOSSES:
        unsupported["policy/loss_metrics/clip_ratio"] = f"{policy_loss_type} does not clip: a constant 0.0, no rows"
    if str(policy_loss_type) == "clip_cov":
        unsupported["policy_loss_type=clip_cov"] = CLIP_COV_CAVEAT
    return {"sends_loss_bookkeeping": True, "rollups": rollups, "unsupported": unsupported}


def get_unsupported_keys(policy_loss_type: str | None) -> tuple[str, ...]:
    """The plan's unsupported key patterns (`policy/...`, never a path entry) for ``policy_loss_type``: a loss metric
    matching one is never value-matched to a row (`loss.summarize_micro_call`)."""
    return tuple(key for key in build_training_plan(policy_loss_type)["unsupported"] if "/" in key)
