from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor

from cortex.cognitive_substrate._shared import make_mlp


class PredictiveBox(nn.Module, ABC):
    """Abstract predictive/world-model box."""

    @abstractmethod
    def project_latent(self, pred_state: Tensor) -> Tensor:
        """Project predictive tower state into the latent used by dynamics."""

    @abstractmethod
    def rollout(
        self,
        z_btF: Tensor,
        action_head_actions_bt: Sequence[Tensor | None],
    ) -> "PredictiveRolloutOutputs":
        """Unroll action-conditioned latent predictions."""


@dataclass(frozen=True)
class PredictiveRolloutOutputs:
    latents_btHF: Tensor
    rewards_btH: Tensor
    values_btH: Tensor
    action_head_logits_btHA: tuple[Tensor, ...]


class DefaultPredictiveBox(PredictiveBox):
    """Default Muesli-style decoder-free predictive box."""

    def __init__(
        self,
        *,
        state_dim: int,
        latent_dim: int,
        hidden_dim: int,
        horizon: int,
        action_head_dims: Sequence[int],
        action_embed_dim: int | None = None,
    ) -> None:
        super().__init__()
        self.latent_dim = int(latent_dim)
        self.horizon = int(horizon)
        self.action_embed_dim = int(action_embed_dim or latent_dim)
        self.action_head_dims = tuple(int(head_dim) for head_dim in action_head_dims)

        self.latent_norm = nn.LayerNorm(state_dim)
        self.latent_proj = nn.Linear(state_dim, latent_dim)
        self.action_head_embeddings = nn.ModuleList(
            nn.Embedding(head_dim, self.action_embed_dim) for head_dim in self.action_head_dims
        )

        transition_in = latent_dim + len(self.action_head_dims) * self.action_embed_dim
        self.transition = make_mlp(transition_in, hidden_dim, latent_dim)
        self.reward_head = make_mlp(latent_dim, hidden_dim, 1)
        self.value_head = make_mlp(latent_dim, hidden_dim, 1)
        self.action_head_policy_layers = nn.ModuleList(
            make_mlp(latent_dim, hidden_dim, head_dim) for head_dim in self.action_head_dims
        )

    def project_latent(self, pred_state: Tensor) -> Tensor:
        return self.latent_proj(self.latent_norm(pred_state))

    def rollout(
        self,
        z_btF: Tensor,
        action_head_actions_bt: Sequence[Tensor | None],
    ) -> PredictiveRolloutOutputs:
        current = z_btF
        pred_latents: list[Tensor] = []
        pred_rewards: list[Tensor] = []
        pred_values: list[Tensor] = []
        pred_action_head_logits: list[list[Tensor]] = [[] for _ in self.action_head_dims]

        for step in range(self.horizon):
            transition_inputs = [current]
            for head_index, action_embedding in enumerate(self.action_head_embeddings):
                head_actions = action_head_actions_bt[head_index] if head_index < len(action_head_actions_bt) else None
                shifted_actions = shift_actions(head_actions, step) if head_actions is not None else None
                head_embed = current.new_zeros((*current.shape[:-1], self.action_embed_dim))
                if shifted_actions is not None:
                    head_embed = action_embedding(shifted_actions)
                transition_inputs.append(head_embed)
            transition_input = torch.cat(transition_inputs, dim=-1)
            current = current + self.transition(transition_input)
            pred_latents.append(current)
            pred_rewards.append(self.reward_head(current).squeeze(-1))
            pred_values.append(self.value_head(current).squeeze(-1))
            for head_index, policy_head in enumerate(self.action_head_policy_layers):
                pred_action_head_logits[head_index].append(policy_head(current))

        return PredictiveRolloutOutputs(
            latents_btHF=torch.stack(pred_latents, dim=2),
            rewards_btH=torch.stack(pred_rewards, dim=2),
            values_btH=torch.stack(pred_values, dim=2),
            action_head_logits_btHA=tuple(torch.stack(head_logits, dim=2) for head_logits in pred_action_head_logits),
        )


@dataclass(frozen=True)
class PredictiveObjectiveResult:
    total: Tensor
    latent_loss: Tensor
    reward_loss: Tensor
    value_loss: Tensor
    action_head_policy_losses: tuple[Tensor, ...]
    active_horizons: int


def shift_actions(actions_bt: Tensor | None, step: int) -> Tensor:
    if actions_bt is None:
        raise ValueError("actions_bt cannot be None when computing predictive rollouts")
    if step == 0:
        return actions_bt
    shifted = torch.zeros_like(actions_bt)
    shifted[:, :-step] = actions_bt[:, step:]
    return shifted


def future_valid_mask(boundary_bt: Tensor, steps_ahead: int) -> Tensor:
    if steps_ahead <= 0:
        raise ValueError("steps_ahead must be positive")
    batch_size, time_steps = boundary_bt.shape
    valid_steps = time_steps - steps_ahead
    if valid_steps <= 0:
        return torch.zeros((batch_size, 0), device=boundary_bt.device, dtype=torch.bool)

    valid = torch.ones((batch_size, valid_steps), device=boundary_bt.device, dtype=torch.bool)
    for offset in range(steps_ahead):
        valid &= ~boundary_bt[:, offset : offset + valid_steps]
    return valid


def masked_mean(values: Tensor, mask: Tensor) -> Tensor:
    if mask.numel() == 0 or not bool(mask.any()):
        return values.new_zeros(())
    weights = mask.to(device=values.device, dtype=values.dtype)
    return (values * weights).sum() / weights.sum().clamp_min(1.0)


def masked_mse(pred: Tensor, target: Tensor, mask: Tensor) -> Tensor:
    errors = F.mse_loss(pred, target, reduction="none")
    while errors.dim() > mask.dim():
        errors = errors.mean(dim=-1)
    return masked_mean(errors, mask)


def masked_kl_from_target_log_probs(pred_logits: Tensor, target_log_probs: Tensor, mask: Tensor) -> Tensor:
    target_log_probs = target_log_probs.detach()
    target_probs = target_log_probs.exp()
    pred_log_probs = F.log_softmax(pred_logits, dim=-1)
    kl = (target_probs * (target_log_probs - pred_log_probs)).sum(dim=-1)
    return masked_mean(kl, mask)


def compute_predictive_objective(
    *,
    z_btF: Tensor,
    pred_latents_btHF: Tensor,
    pred_rewards_btH: Tensor,
    pred_values_btH: Tensor,
    pred_action_head_logits_btHA: Sequence[Tensor],
    target_action_head_log_probs_btA: Sequence[Tensor],
    extrinsic_rewards_bt: Tensor,
    value_targets_bt: Tensor,
    boundary_bt: Tensor,
    latent_coef: float,
    reward_coef: float,
    value_coef: float,
    action_head_policy_coefs: Sequence[float],
) -> PredictiveObjectiveResult:
    _, time_steps = boundary_bt.shape
    total_loss = z_btF.new_zeros(())
    latent_meter = z_btF.new_zeros(())
    reward_meter = z_btF.new_zeros(())
    value_meter = z_btF.new_zeros(())
    action_head_policy_meters = [z_btF.new_zeros(()) for _ in pred_action_head_logits_btHA]
    active_horizons = 0

    for horizon_idx in range(pred_latents_btHF.shape[2]):
        steps_ahead = horizon_idx + 1
        if time_steps <= steps_ahead:
            break

        valid_mask = future_valid_mask(boundary_bt, steps_ahead=steps_ahead)
        if valid_mask.numel() == 0 or not bool(valid_mask.any()):
            continue

        pred_latent = pred_latents_btHF[:, : time_steps - steps_ahead, horizon_idx, :]
        target_latent = z_btF[:, steps_ahead:, :].detach()
        pred_latent = F.normalize(pred_latent, dim=-1)
        target_latent = F.normalize(target_latent, dim=-1)
        latent_loss = masked_mse(pred_latent, target_latent, valid_mask)

        pred_reward = pred_rewards_btH[:, : time_steps - steps_ahead, horizon_idx]
        target_reward = extrinsic_rewards_bt[:, steps_ahead - 1 : time_steps - 1].detach()
        reward_loss = masked_mse(pred_reward, target_reward, valid_mask)

        pred_value = pred_values_btH[:, : time_steps - steps_ahead, horizon_idx]
        target_value = value_targets_bt[:, steps_ahead:]
        value_loss = masked_mse(pred_value, target_value, valid_mask)

        step_total = (
            float(latent_coef) * latent_loss + float(reward_coef) * reward_loss + float(value_coef) * value_loss
        )
        for head_index, pred_head_logits_btHA in enumerate(pred_action_head_logits_btHA):
            if head_index >= len(target_action_head_log_probs_btA):
                break
            pred_head_logits = pred_head_logits_btHA[:, : time_steps - steps_ahead, horizon_idx, :]
            target_head_log_probs = target_action_head_log_probs_btA[head_index][:, steps_ahead:, :]
            head_policy_loss = masked_kl_from_target_log_probs(pred_head_logits, target_head_log_probs, valid_mask)
            policy_coef = (
                float(action_head_policy_coefs[head_index]) if head_index < len(action_head_policy_coefs) else 1.0
            )
            step_total = step_total + policy_coef * head_policy_loss
            action_head_policy_meters[head_index] = action_head_policy_meters[head_index] + head_policy_loss.detach()

        total_loss = total_loss + step_total
        latent_meter = latent_meter + latent_loss.detach()
        reward_meter = reward_meter + reward_loss.detach()
        value_meter = value_meter + value_loss.detach()
        active_horizons += 1

    if active_horizons == 0:
        return PredictiveObjectiveResult(
            total=total_loss,
            latent_loss=latent_meter,
            reward_loss=reward_meter,
            value_loss=value_meter,
            action_head_policy_losses=tuple(action_head_policy_meters),
            active_horizons=0,
        )

    inv_horizons = 1.0 / active_horizons
    return PredictiveObjectiveResult(
        total=total_loss * inv_horizons,
        latent_loss=latent_meter * inv_horizons,
        reward_loss=reward_meter * inv_horizons,
        value_loss=value_meter * inv_horizons,
        action_head_policy_losses=tuple(policy_loss * inv_horizons for policy_loss in action_head_policy_meters),
        active_horizons=active_horizons,
    )


__all__ = [
    "PredictiveBox",
    "PredictiveRolloutOutputs",
    "DefaultPredictiveBox",
    "PredictiveObjectiveResult",
    "shift_actions",
    "future_valid_mask",
    "masked_mean",
    "masked_mse",
    "masked_kl_from_target_log_probs",
    "compute_predictive_objective",
]
