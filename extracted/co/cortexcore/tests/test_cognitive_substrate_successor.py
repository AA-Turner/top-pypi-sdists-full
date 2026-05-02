from __future__ import annotations

import torch
from cortex.cognitive_substrate.successor import compute_successor_prediction_loss


def test_successor_prediction_loss_is_zero_on_exact_normalized_target() -> None:
    psi_btF = torch.tensor(
        [
            [[3.0, 4.0], [0.0, 5.0], [8.0, 6.0]],
        ],
        dtype=torch.float32,
    )
    pred_next_psi_btF = torch.zeros_like(psi_btF)
    pred_next_psi_btF[:, :-1, :] = psi_btF[:, 1:, :]
    resets_bt = torch.tensor([[False, False, False]])

    result = compute_successor_prediction_loss(
        pred_next_psi_btF=pred_next_psi_btF,
        psi_btF=psi_btF,
        resets_bt=resets_bt,
    )

    torch.testing.assert_close(result.loss, torch.zeros((), dtype=torch.float32), rtol=0, atol=1e-6)


def test_successor_prediction_loss_masks_episode_boundaries() -> None:
    psi_btF = torch.tensor(
        [
            [[1.0, 0.0], [0.0, 1.0], [1.0, 0.0]],
        ],
        dtype=torch.float32,
    )
    pred_next_psi_btF = torch.zeros((1, 3, 2), dtype=torch.float32)
    resets_bt = torch.tensor([[False, True, False]])

    result = compute_successor_prediction_loss(
        pred_next_psi_btF=pred_next_psi_btF,
        psi_btF=psi_btF,
        resets_bt=resets_bt,
    )

    expected = torch.tensor(0.5, dtype=torch.float32)
    torch.testing.assert_close(result.loss, expected, rtol=0, atol=1e-6)
