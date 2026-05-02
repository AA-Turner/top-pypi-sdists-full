"""Cognitive substrate boxes and box-aligned objective helpers."""

from cortex.cognitive_substrate.decision import (
    DecisionBox,
    DecisionOutputs,
    DefaultDecisionBox,
)
from cortex.cognitive_substrate.exploration import (
    IntrinsicRewardResult,
    compute_successor_intrinsic_bonus,
    successor_intrinsic_reward,
    update_prev_predicted_successor_state_,
    update_prev_successor_state_,
)
from cortex.cognitive_substrate.predictive import (
    DefaultPredictiveBox,
    PredictiveBox,
    PredictiveObjectiveResult,
    PredictiveRolloutOutputs,
    compute_predictive_objective,
    future_valid_mask,
    masked_kl_from_target_log_probs,
    masked_mean,
    masked_mse,
    shift_actions,
)
from cortex.cognitive_substrate.successor import (
    DefaultSuccessorBox,
    SuccessorBox,
    SuccessorOutputs,
    SuccessorPredictionResult,
    SuccessorRewardPredictionResult,
    compute_successor_prediction_loss,
    compute_successor_reward_reconstruction_loss,
)

__all__ = [
    "DecisionBox",
    "DecisionOutputs",
    "PredictiveBox",
    "PredictiveRolloutOutputs",
    "SuccessorBox",
    "SuccessorOutputs",
    "DefaultDecisionBox",
    "DefaultPredictiveBox",
    "DefaultSuccessorBox",
    "PredictiveObjectiveResult",
    "SuccessorPredictionResult",
    "SuccessorRewardPredictionResult",
    "IntrinsicRewardResult",
    "compute_predictive_objective",
    "shift_actions",
    "future_valid_mask",
    "masked_mean",
    "masked_mse",
    "masked_kl_from_target_log_probs",
    "compute_successor_prediction_loss",
    "compute_successor_reward_reconstruction_loss",
    "successor_intrinsic_reward",
    "compute_successor_intrinsic_bonus",
    "update_prev_successor_state_",
    "update_prev_predicted_successor_state_",
]
