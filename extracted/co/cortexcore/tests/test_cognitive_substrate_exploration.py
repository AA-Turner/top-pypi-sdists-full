from __future__ import annotations

import torch
from cortex.cognitive_substrate.exploration import (
    compute_successor_intrinsic_bonus,
    update_prev_predicted_successor_state_,
)


def test_successor_intrinsic_bonus_adds_count_and_delta() -> None:
    psi = torch.tensor([[1.0, -1.0], [2.0, 0.0]], dtype=torch.float32)
    prev_psi = torch.tensor([[0.0, 0.0], [1.0, 0.0]], dtype=torch.float32)
    prev_valid = torch.tensor([False, True])

    result = compute_successor_intrinsic_bonus(
        psi_bf=psi,
        prev_psi_bf=prev_psi,
        prev_valid_b=prev_valid,
        beta_count=0.5,
        epsilon=0.5,
        beta_delta=0.25,
        delta_clip=1.0,
    )

    count0 = 0.5 / (0.5 + 2.0)
    count1 = 0.5 / (0.5 + 2.0)
    delta1 = min(float(((psi[1] - prev_psi[1]) ** 2).sum().item()), 1.0)
    expected = torch.tensor([count0, count1 + 0.25 * delta1], dtype=torch.float32)
    torch.testing.assert_close(result.intrinsic_b, expected, rtol=0, atol=1e-6)


def test_successor_intrinsic_bonus_can_use_successor_prediction_error() -> None:
    psi = torch.tensor([[1.0, 0.0], [0.0, 2.0]], dtype=torch.float32)
    prev_psi = torch.zeros_like(psi)
    prev_valid = torch.tensor([False, False])
    prev_pred_psi = torch.tensor([[1.0, 0.0], [2.0, 0.0]], dtype=torch.float32)
    prev_pred_valid = torch.tensor([False, True])

    result = compute_successor_intrinsic_bonus(
        psi_bf=psi,
        prev_psi_bf=prev_psi,
        prev_valid_b=prev_valid,
        beta_count=0.5,
        epsilon=0.5,
        beta_delta=0.0,
        delta_clip=1.0,
        prev_pred_psi_bf=prev_pred_psi,
        prev_pred_psi_valid_b=prev_pred_valid,
        beta_successor_prediction=0.25,
        successor_prediction_clip=10.0,
    )

    expected = torch.tensor(
        [
            0.5 / (0.5 + 1.0),
            0.5 / (0.5 + 2.0) + 0.25,
        ],
        dtype=torch.float32,
    )
    torch.testing.assert_close(result.intrinsic_b, expected, rtol=0, atol=1e-6)


def test_update_prev_predicted_successor_state_resets_boundaries() -> None:
    prev_pred_psi = torch.full((3, 2), torch.nan, dtype=torch.float32)
    agent_ids = torch.tensor([0, 2], dtype=torch.long)
    pred_next_psi = torch.tensor([[3.0, 4.0], [0.0, 5.0]], dtype=torch.float32)
    boundary = torch.tensor([False, True])

    update_prev_predicted_successor_state_(
        prev_pred_psi_agentF=prev_pred_psi,
        agent_ids_b=agent_ids,
        pred_next_psi_bf=pred_next_psi,
        boundary_b=boundary,
    )

    torch.testing.assert_close(prev_pred_psi[0], torch.tensor([3.0, 4.0], dtype=torch.float32))
    assert torch.isnan(prev_pred_psi[2]).all()
