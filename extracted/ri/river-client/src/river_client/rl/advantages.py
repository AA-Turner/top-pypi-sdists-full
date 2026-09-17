"""Advantage estimators and explicit normalization of River's sum loss."""

from dataclasses import dataclass

import numpy as np

from .config import Truncation


@dataclass(frozen=True)
class GroupCentered:
    standardize: bool | str = False
    eps: float = 1e-8

    def __post_init__(self):
        if self.standardize not in (False, True, "batch"):
            raise ValueError("standardize must be False, True (group), or batch")
        if self.eps <= 0 or not np.isfinite(self.eps):
            raise ValueError("eps must be finite and positive")

    def __call__(self, rewards, *, min_members):
        batch = [r for group in rewards for r in group if r is not None]
        result = []
        for group in rewards:
            local = [r for r in group if r is not None]
            baseline = local if len(local) >= min_members else batch
            mean = float(np.mean(baseline)) if baseline else 0.0
            scale = (
                max(float(np.std(baseline)), self.eps)
                if baseline and self.standardize is True
                else 1.0
            )
            result.append([0.0 if r is None else (r - mean) / scale for r in group])
        if self.standardize == "batch":
            raw = [
                a
                for group, values in zip(result, rewards, strict=True)
                for a, r in zip(group, values, strict=True)
                if r is not None
            ]
            scale = max(float(np.std(raw)), self.eps) if len(raw) > 1 else 1.0
            result = [[a / scale for a in group] for group in result]
        return result


@dataclass(frozen=True)
class Batchwise:
    standardize: bool = False
    eps: float = 1e-8

    def __post_init__(self):
        if self.eps <= 0 or not np.isfinite(self.eps):
            raise ValueError("eps must be finite and positive")

    def __call__(self, rewards, *, min_members):
        # A single baseline across every finished member, including carried tails.
        flat = [r for group in rewards for r in group if r is not None]
        mean = float(np.mean(flat)) if flat else 0.0
        scale = max(float(np.std(flat)), self.eps) if flat and self.standardize else 1.0
        return [
            [0.0 if r is None else (r - mean) / scale for r in group]
            for group in rewards
        ]


def reward_values(groups, truncation):
    rewards = []
    for group in groups:
        values = []
        for traj in group:
            if not traj.done or traj.reward is None or not np.isfinite(traj.reward):
                raise ValueError(
                    "only completed, scored trajectories can enter training"
                )
            policy = truncation.policy(traj.truncated)
            values.append(
                None
                if policy == "drop_and_exclude_from_baseline"
                else 0.0
                if policy == "zero_reward"
                else traj.reward
            )
        rewards.append(values)
    return rewards


def build_batch(
    groups,
    *,
    estimator,
    normalize,
    truncation: Truncation,
    min_members,
    current_step,
    max_staleness,
    defer_normalization=False,
    advantages=None,
):
    if normalize not in {"token", "sequence", "batch", "sum"}:
        raise ValueError(
            "normalize must be explicitly 'token', 'sequence', 'batch', or 'sum'"
        )
    rewards = reward_values(groups, truncation)
    if advantages is None:
        advantages = estimator(rewards, min_members=min_members)
    records, ages, stale, total = [], [], 0, 0
    for group, group_advantages in zip(groups, advantages, strict=True):
        for traj, advantage in zip(group, group_advantages, strict=True):
            for span in traj.spans:
                if span.kind == "generated":
                    age = current_step - span.policy_step
                    if age < 0:
                        raise ValueError(
                            "sample policy step is ahead of trainer weights"
                        )
                    ages.append(age)
                    total += len(span)
                    if max_staleness is not None and age > max_staleness:
                        stale += len(span)
            if truncation.policy(traj.truncated) in {
                "drop",
                "drop_and_exclude_from_baseline",
            }:
                continue
            data = traj.to_data(
                advantage, current_step=current_step, max_staleness=max_staleness
            )
            masks = traj.to_data(
                1.0, current_step=current_step, max_staleness=max_staleness
            )
            n_tokens = sum(sum(d["advantages"]) for d in masks)
            if n_tokens:
                records.append((data, n_tokens))
    token_count = sum(count for data, count in records)
    for data, count in records:
        denominator = (
            1
            if normalize == "sum" or (defer_normalization and normalize != "sequence")
            else token_count
            if normalize == "token"
            else (1 if defer_normalization else len(records)) * count
            if normalize == "sequence"
            else len(records)
        )
        for datum in data:
            datum["advantages"] = [a / denominator for a in datum["advantages"]]
    data = [d for datums, count in records for d in datums if any(d["advantages"])]
    flat_rewards = [t.reward for group in groups for t in group]
    flat = [t for group in groups for t in group]
    metrics = {
        "reward/mean": float(np.mean(flat_rewards)) if flat_rewards else 0.0,
        "reward/std": float(np.std(flat_rewards)) if flat_rewards else 0.0,
        "reward/zero_variance_group_frac": sum(not any(a) for a in advantages)
        / max(1, len(groups)),
        "staleness/span_age_p50": float(np.percentile(ages, 50)) if ages else 0.0,
        "staleness/span_age_p99": float(np.percentile(ages, 99)) if ages else 0.0,
        "staleness/frac_masked": stale / max(1, total),
        "train/generated_tokens": float(total),
        "train/active_tokens": float(token_count),
        "train/active_sequences": float(len(records)),
        "train/datums": float(len(data)),
        "length/generated_p50": float(
            np.percentile([t.generated_tokens for t in flat], 50)
        )
        if flat
        else 0.0,
        "length/generated_p99": float(
            np.percentile([t.generated_tokens for t in flat], 99)
        )
        if flat
        else 0.0,
    }
    for cause in {t.truncated for t in flat if t.truncated}:
        metrics[f"truncated/{cause}"] = sum(t.truncated == cause for t in flat) / len(
            flat
        )
    for key in {key for t in flat for key in t.metrics}:
        metrics[f"rollout/{key}"] = sum(t.metrics.get(key, 0) for t in flat)
    return data, metrics


def decouple_ppo(data, proximal_logprobs, *, max_importance_weight: float):
    """Exact reduction to River PPO with A' = A * pi_prox / pi_behavior.

    See AReaL's decoupled objective: https://areal-ai.io/docs/en/algorithms/async.html
    Positive scaling commutes with PPO's min, preserving both advantage signs.
    The declared cap is a truncated importance-sampling correction.
    """
    if not np.isfinite(max_importance_weight) or max_importance_weight <= 0:
        raise ValueError("max_importance_weight must be finite and positive")
    if proximal_logprobs is None or len(proximal_logprobs) != len(data):
        raise ValueError("forward did not return one proximal logprob row per datum")
    output, ratios = [], []
    for datum, row in zip(data, proximal_logprobs, strict=True):
        old = np.asarray(datum["old_logprobs"], dtype=np.float64)
        adv = np.asarray(datum["advantages"], dtype=np.float64)
        prox = np.asarray(row, dtype=np.float64)
        # River predicts n-1 tokens; some forward transports retain a trailing
        # masked position. Both forms have the same prediction alignment.
        if prox.shape == (len(old) - 1,):
            prox = np.concatenate((prox, [0.0]))
        if prox.shape != old.shape or not np.all(np.isfinite(prox[adv != 0])):
            raise ValueError(
                "proximal logprobs do not align with generated prediction positions"
            )
        mask = adv != 0
        ratio = np.exp(
            np.minimum(prox[mask] - old[mask], np.log(max_importance_weight))
        )
        ratios.extend(ratio.tolist())
        adv[mask] *= ratio
        new_old = old.copy()
        new_old[mask] = prox[mask]
        output.append(
            {**datum, "old_logprobs": new_old.tolist(), "advantages": adv.tolist()}
        )
    return output, {
        "loss/behavior_importance_mean": float(np.mean(ratios)) if ratios else 0.0,
        "loss/behavior_importance_capped_frac": sum(
            r >= max_importance_weight for r in ratios
        )
        / max(1, len(ratios)),
    }


def accumulation_scale(
    groups, *, estimator, truncation, min_members, normalize, metrics
):
    """Finalize positive global factors after all rewards and lengths are known."""
    scale = 1.0
    if isinstance(estimator, GroupCentered) and estimator.standardize == "batch":
        rewards = reward_values(groups, truncation)
        raw = GroupCentered(eps=estimator.eps)(rewards, min_members=min_members)
        values = [
            a
            for group, rs in zip(raw, rewards, strict=True)
            for a, reward in zip(group, rs, strict=True)
            if reward is not None
        ]
        if len(values) > 1:
            scale /= max(float(np.std(values)), estimator.eps)
    if normalize == "token":
        scale /= max(1, metrics["train/active_tokens"])
    elif normalize in {"sequence", "batch"}:
        scale /= max(1, metrics["train/active_sequences"])
    return scale
