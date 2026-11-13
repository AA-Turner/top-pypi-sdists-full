"""GOLD's per-sample divergence, same tokenizer (`gold_trainer.py:2762-3172`; spike S1): the same
`generalized_jsd_loss` wrap as GKD. Each micro-step trains the slice `_prepare_inputs` just returned, which the sample
recorder keyed (`last_calls`) right before `compute_loss`. The cross-tokenizer ULD / X-Token losses never call the
divergence: refused. Its per-writer `on_policy_loss` / `off_policy_loss` are rounded mixes no rollup rebuilds."""

from __future__ import annotations

from typing import Any

from ..declarations import GOLD_WRITER_KEYS
from .gkd import GkdLoss


class GoldLoss(GkdLoss):
    names = ("GOLDTrainer",)

    def find_unsupported(self) -> list[str]:
        trainer = self.trainer
        if getattr(trainer, "teacher_tokenizer", None) is not None and (
                getattr(trainer, "use_uld_loss", False) or getattr(trainer, "xtoken_loss_fn", None) is not None):
            return ["GOLD cross-tokenizer loss"]
        return []

    def find_unsent(self) -> list[str]:
        return list(GOLD_WRITER_KEYS)

    def _install_stamp(self) -> None:
        """Nothing to carry: the slice is keyed right before its loss call."""

    def _get_prefix(self, inputs: Any, split: str) -> str | None:
        return self._make_prefix(split)
