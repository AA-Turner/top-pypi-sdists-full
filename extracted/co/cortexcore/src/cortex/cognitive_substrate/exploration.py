from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor


@dataclass(frozen=True)
class IntrinsicRewardResult:
    intrinsic_b: Tensor


def _normalized_squared_error_mean(x_bf: Tensor, y_bf: Tensor, *, eps: float) -> Tensor:
    feature_dim = x_bf.shape[-1]
    x_sqnorm_b = x_bf.pow(2).sum(dim=-1)
    y_sqnorm_b = y_bf.pow(2).sum(dim=-1)
    x_inv_norm_b = x_sqnorm_b.clamp_min(float(eps) ** 2).rsqrt()
    y_inv_norm_b = y_sqnorm_b.clamp_min(float(eps) ** 2).rsqrt()
    cross_b = (x_bf * y_bf).sum(dim=-1) * x_inv_norm_b * y_inv_norm_b
    sq_err_b = (x_sqnorm_b * x_inv_norm_b.square() + y_sqnorm_b * y_inv_norm_b.square() - 2.0 * cross_b) / float(
        feature_dim
    )
    return sq_err_b.clamp_min(0.0)


def successor_intrinsic_reward(
    *,
    psi_bf: Tensor,
    prev_psi_bf: Tensor,
    prev_valid_b: Tensor,
    beta_count: float,
    epsilon: float,
    beta_delta: float,
    delta_clip: float,
    prev_pred_psi_bf: Tensor | None = None,
    prev_pred_psi_valid_b: Tensor | None = None,
    beta_successor_prediction: float = 0.0,
    successor_prediction_clip: float = 1.0,
) -> Tensor:
    psi_safe_bf = torch.nan_to_num(psi_bf)
    prev_psi_safe_bf = torch.nan_to_num(prev_psi_bf)
    intrinsic_bonus = float(beta_count) / (float(epsilon) + psi_safe_bf.abs().sum(dim=-1))
    if float(beta_delta) > 0:
        delta_bonus = (psi_safe_bf - prev_psi_safe_bf).pow(2).sum(dim=-1)
        delta_bonus = delta_bonus.clamp(min=0.0, max=float(delta_clip))
        delta_bonus = delta_bonus * prev_valid_b.to(device=delta_bonus.device, dtype=delta_bonus.dtype)
        intrinsic_bonus = intrinsic_bonus + float(beta_delta) * delta_bonus

    if float(beta_successor_prediction) > 0:
        if prev_pred_psi_bf is None or prev_pred_psi_valid_b is None:
            raise ValueError("beta_successor_prediction > 0 requires prev_pred_psi_bf and prev_pred_psi_valid_b")
        prediction_bonus = _normalized_squared_error_mean(
            torch.nan_to_num(prev_pred_psi_bf),
            psi_safe_bf,
            eps=1e-6,
        )
        prediction_bonus = prediction_bonus.clamp(min=0.0, max=float(successor_prediction_clip))
        prediction_bonus = prediction_bonus * prev_pred_psi_valid_b.to(
            device=prediction_bonus.device,
            dtype=prediction_bonus.dtype,
        )
        intrinsic_bonus = intrinsic_bonus + float(beta_successor_prediction) * prediction_bonus

    return torch.nan_to_num(intrinsic_bonus, nan=0.0, posinf=0.0, neginf=0.0)


def compute_successor_intrinsic_bonus(
    *,
    psi_bf: Tensor,
    prev_psi_bf: Tensor,
    prev_valid_b: Tensor,
    beta_count: float,
    epsilon: float,
    beta_delta: float,
    delta_clip: float,
    prev_pred_psi_bf: Tensor | None = None,
    prev_pred_psi_valid_b: Tensor | None = None,
    beta_successor_prediction: float = 0.0,
    successor_prediction_clip: float = 1.0,
) -> IntrinsicRewardResult:
    return IntrinsicRewardResult(
        intrinsic_b=successor_intrinsic_reward(
            psi_bf=psi_bf,
            prev_psi_bf=prev_psi_bf,
            prev_valid_b=prev_valid_b,
            beta_count=beta_count,
            epsilon=epsilon,
            beta_delta=beta_delta,
            delta_clip=delta_clip,
            prev_pred_psi_bf=prev_pred_psi_bf,
            prev_pred_psi_valid_b=prev_pred_psi_valid_b,
            beta_successor_prediction=beta_successor_prediction,
            successor_prediction_clip=successor_prediction_clip,
        )
    )


def update_prev_successor_state_(
    *,
    prev_psi_agentF: Tensor,
    agent_ids_b: Tensor,
    psi_bf: Tensor,
    boundary_b: Tensor,
) -> None:
    with torch.no_grad():
        prev_psi_agentF[agent_ids_b] = psi_bf
        if bool(boundary_b.any()):
            prev_psi_agentF[agent_ids_b[boundary_b]] = torch.nan


def update_prev_predicted_successor_state_(
    *,
    prev_pred_psi_agentF: Tensor,
    agent_ids_b: Tensor,
    pred_next_psi_bf: Tensor,
    boundary_b: Tensor,
) -> None:
    with torch.no_grad():
        prev_pred_psi_agentF[agent_ids_b] = pred_next_psi_bf
        if bool(boundary_b.any()):
            prev_pred_psi_agentF[agent_ids_b[boundary_b]] = torch.nan


__all__ = [
    "IntrinsicRewardResult",
    "successor_intrinsic_reward",
    "compute_successor_intrinsic_bonus",
    "update_prev_successor_state_",
    "update_prev_predicted_successor_state_",
]
