from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor

from cortex.cognitive_substrate._shared import make_mlp


def _normalized_squared_error_mean(x_btF: Tensor, y_btF: Tensor, *, eps: float) -> Tensor:
    feature_dim = x_btF.shape[-1]
    x_sqnorm_bt = x_btF.pow(2).sum(dim=-1)
    y_sqnorm_bt = y_btF.pow(2).sum(dim=-1)
    x_inv_norm_bt = x_sqnorm_bt.clamp_min(float(eps) ** 2).rsqrt()
    y_inv_norm_bt = y_sqnorm_bt.clamp_min(float(eps) ** 2).rsqrt()
    cross_bt = (x_btF * y_btF).sum(dim=-1) * x_inv_norm_bt * y_inv_norm_bt
    sq_err_bt = (x_sqnorm_bt * x_inv_norm_bt.square() + y_sqnorm_bt * y_inv_norm_bt.square() - 2.0 * cross_bt) / float(
        feature_dim
    )
    return sq_err_bt.clamp_min(0.0)


class SuccessorBox(nn.Module, ABC):
    """Abstract successor-feature box."""

    @abstractmethod
    def forward(
        self,
        z: Tensor,
        sf_state: Tensor,
        *,
        couple_into_pred: bool,
    ) -> "SuccessorOutputs":
        """Return phi/psi/h outputs for the successor objective."""

    @abstractmethod
    def predict_next_psi(
        self,
        sf_state: Tensor,
        action_head_actions: Sequence[Tensor | None],
    ) -> Tensor:
        """Predict next-step successor features from state and action."""


@dataclass(frozen=True)
class SuccessorOutputs:
    phi: Tensor
    psi: Tensor
    h: Tensor
    reward_pred: Tensor


class DefaultSuccessorBox(SuccessorBox):
    """Default successor-feature box with GTD-style psi/h outputs."""

    def __init__(
        self,
        *,
        latent_dim: int,
        sf_state_dim: int,
        phi_dim: int,
        hidden_dim: int,
        action_head_dims: Sequence[int],
        action_embed_dim: int,
    ) -> None:
        super().__init__()
        self.phi_dim = int(phi_dim)
        self.sf_state_dim = int(sf_state_dim)
        self.action_embed_dim = int(action_embed_dim)
        self.action_head_dims = tuple(int(head_dim) for head_dim in action_head_dims)
        self._single_action_head = len(self.action_head_dims) == 1
        self.phi_head = make_mlp(latent_dim, hidden_dim, phi_dim)
        self.psi_head = make_mlp(sf_state_dim, hidden_dim, phi_dim)
        self.h_head = make_mlp(sf_state_dim, hidden_dim, phi_dim)
        self.reward_head = nn.Linear(phi_dim, 1)
        self.next_psi_action_embeddings = nn.ModuleList(
            nn.Embedding(head_dim, self.action_embed_dim) for head_dim in self.action_head_dims
        )
        transition_in = sf_state_dim + len(self.action_head_dims) * self.action_embed_dim
        self.next_psi_head = make_mlp(transition_in, hidden_dim, phi_dim)

    def forward(
        self,
        z: Tensor,
        sf_state: Tensor,
        *,
        couple_into_pred: bool,
    ) -> SuccessorOutputs:
        phi_input = z if couple_into_pred else z.detach()
        phi = self.phi_head(phi_input)
        psi = self.psi_head(sf_state)
        return SuccessorOutputs(
            phi=phi,
            psi=psi,
            h=self.h_head(sf_state),
            reward_pred=self.reward_head(phi).squeeze(-1),
        )

    def predict_next_psi(
        self,
        sf_state: Tensor,
        action_head_actions: Sequence[Tensor | None],
    ) -> Tensor:
        leading_shape = sf_state.shape[:-1]
        flat_sf = sf_state.reshape(-1, self.sf_state_dim)
        if self._single_action_head:
            head_actions = action_head_actions[0] if action_head_actions else None
            if head_actions is None:
                head_embed = flat_sf.new_zeros((flat_sf.shape[0], self.action_embed_dim))
            else:
                head_embed = self.next_psi_action_embeddings[0](
                    head_actions.to(device=flat_sf.device, dtype=torch.long).reshape(-1)
                )
            transition_input = torch.cat((flat_sf, head_embed), dim=-1)
        else:
            transition_inputs = [flat_sf]
            for head_index, action_embedding in enumerate(self.next_psi_action_embeddings):
                head_actions = action_head_actions[head_index] if head_index < len(action_head_actions) else None
                if head_actions is None:
                    head_embed = flat_sf.new_zeros((flat_sf.shape[0], self.action_embed_dim))
                else:
                    head_embed = action_embedding(head_actions.to(device=flat_sf.device, dtype=torch.long).reshape(-1))
                transition_inputs.append(head_embed)
            transition_input = torch.cat(transition_inputs, dim=-1)
        return self.next_psi_head(transition_input).reshape(*leading_shape, self.phi_dim)


@dataclass(frozen=True)
class SuccessorRewardPredictionResult:
    loss: Tensor


@dataclass(frozen=True)
class SuccessorPredictionResult:
    loss: Tensor


def compute_successor_reward_reconstruction_loss(
    *,
    reward_pred_bt: Tensor,
    extrinsic_rewards_bt: Tensor,
) -> SuccessorRewardPredictionResult:
    return SuccessorRewardPredictionResult(loss=F.mse_loss(reward_pred_bt, extrinsic_rewards_bt, reduction="mean"))


def compute_successor_prediction_loss(
    *,
    pred_next_psi_btF: Tensor,
    psi_btF: Tensor,
    resets_bt: Tensor,
) -> SuccessorPredictionResult:
    if psi_btF.dim() != 3:
        raise ValueError(f"Expected psi_btF with shape [B, T, F], got {tuple(psi_btF.shape)}")
    if pred_next_psi_btF.shape != psi_btF.shape:
        raise ValueError(
            "pred_next_psi_btF must have shape [B, T, F], got "
            f"{tuple(pred_next_psi_btF.shape)} for psi shape {tuple(psi_btF.shape)}"
        )
    if resets_bt.shape != psi_btF.shape[:2]:
        raise ValueError(
            f"resets_bt must have shape [B, T], got {tuple(resets_bt.shape)} for psi shape {tuple(psi_btF.shape)}"
        )
    if psi_btF.shape[1] < 2:
        return SuccessorPredictionResult(loss=psi_btF.new_zeros(()))

    valid_bt = (~resets_bt[:, :-1]).to(device=psi_btF.device, dtype=psi_btF.dtype)
    if not bool(valid_bt.any()):
        return SuccessorPredictionResult(loss=psi_btF.new_zeros(()))

    sq_err_bt = _normalized_squared_error_mean(
        pred_next_psi_btF[:, :-1, :],
        psi_btF[:, 1:, :].detach(),
        eps=1e-12,
    )
    loss = (sq_err_bt * valid_bt).sum() / valid_bt.sum().clamp_min(1.0)
    return SuccessorPredictionResult(loss=loss)


__all__ = [
    "SuccessorBox",
    "SuccessorOutputs",
    "DefaultSuccessorBox",
    "SuccessorPredictionResult",
    "SuccessorRewardPredictionResult",
    "compute_successor_prediction_loss",
    "compute_successor_reward_reconstruction_loss",
]
