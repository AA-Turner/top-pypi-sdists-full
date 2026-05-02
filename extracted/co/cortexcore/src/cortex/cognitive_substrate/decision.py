from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Sequence

import torch.nn as nn
from torch import Tensor

from cortex.cognitive_substrate._shared import make_mlp


class DecisionBox(nn.Module, ABC):
    """Abstract decision/evaluation box."""

    @abstractmethod
    def forward(self, rl_state: Tensor) -> "DecisionOutputs":
        """Return action-head logits and value estimates."""


@dataclass(frozen=True)
class DecisionOutputs:
    action_head_logits: tuple[Tensor, ...]
    values: Tensor
    h_values: Tensor


class DefaultDecisionBox(DecisionBox):
    """Default RL box for action selection and evaluation."""

    def __init__(
        self,
        *,
        state_dim: int,
        actor_hidden: int,
        critic_hidden: int,
        action_head_dims: Sequence[int],
    ) -> None:
        super().__init__()
        self.actor_body = make_mlp(state_dim, actor_hidden, actor_hidden)
        self.value_body = make_mlp(state_dim, critic_hidden, 1)
        self.h_value_body = make_mlp(state_dim, critic_hidden, 1)
        self.action_head_layers = nn.ModuleList(nn.Linear(actor_hidden, head_dim) for head_dim in action_head_dims)

    def forward(self, rl_state: Tensor) -> DecisionOutputs:
        actor_hidden = self.actor_body(rl_state)
        return DecisionOutputs(
            action_head_logits=tuple(head(actor_hidden) for head in self.action_head_layers),
            values=self.value_body(rl_state).squeeze(-1),
            h_values=self.h_value_body(rl_state).squeeze(-1),
        )


__all__ = [
    "DecisionBox",
    "DecisionOutputs",
    "DefaultDecisionBox",
]
