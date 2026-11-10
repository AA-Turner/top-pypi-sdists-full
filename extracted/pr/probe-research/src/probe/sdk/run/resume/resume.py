"""ResumeMixin: a run relaunched from a checkpoint by `probe run resume` (agentic W&B C.2) knows where that checkpoint
is (`run.resume_checkpoint`) and the settings asked for this attempt (`run.resume_overrides`). The trainer applies
them AFTER loading the checkpoint (an optimizer's state brings the old learning rate back), and only then are they
recorded on `run.config`: `run.confirm_resume_overrides()` (the HF Trainer and Lightning integrations call it).
Why: DESIGN.md."""

from __future__ import annotations

import json
import os
from typing import Any

#: What `probe run resume` exports to the command it runs (and `--print` prints).
RESUME_CHECKPOINT_ENV = "PROBE_RESUME_CHECKPOINT"
CONFIG_SET_ENV = "PROBE_CONFIG_SET"


def read_resume_env(run_id: str | None = None) -> tuple[str | None, dict[str, Any]]:
    """The resume checkpoint and overrides `probe run resume` exported; nothing when they name another run than
    ``run_id`` (an inherited environment) or there are none. Without ``run_id``: whatever run `PROBE_RUN_ID` names
    (a rank that opened no run of its own)."""
    named = os.environ.get("PROBE_RUN_ID", "").strip()
    if not named or (run_id is not None and named != str(run_id)):
        return None, {}
    checkpoint = os.environ.get(RESUME_CHECKPOINT_ENV, "").strip() or None
    try:
        overrides = json.loads(os.environ.get(CONFIG_SET_ENV, "") or "{}")
    except json.JSONDecodeError:
        overrides = {}
    return checkpoint, overrides if isinstance(overrides, dict) else {}


class ResumeMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    id: str

    @property
    def resume_checkpoint(self) -> str | None:
        """The checkpoint `probe run resume` relaunched this run from (a local path), else None. Load it before
        training: HF `trainer.train(resume_from_checkpoint=run.resume_checkpoint)`, Lightning `ckpt_path=`."""
        return read_resume_env(self.id)[0]

    @property
    def resume_overrides(self) -> dict[str, Any]:
        """The settings asked for this attempt (`probe run resume --config lr=1e-4`), to apply after the checkpoint
        is loaded; empty when none. Not on `run.config` until `confirm_resume_overrides`."""
        return dict(read_resume_env(self.id)[1])

    def confirm_resume_overrides(self, applied: dict[str, Any] | None = None) -> dict[str, Any]:
        """Say the overrides took effect (after the checkpoint loaded): records them on `run.config`, so the run's
        config history shows them applied. ``applied``: what was applied, when not all of them. Returns it."""
        values = self.resume_overrides if applied is None else dict(applied)
        if values and not getattr(self, "_is_resume_confirmed", False):
            # Asked for by a person (`probe run resume --config`): a change, never a surprise to warn about.
            self.update_config(values, allow_val_change=True)
            self._is_resume_confirmed = True
        return values


__all__ = ["CONFIG_SET_ENV", "RESUME_CHECKPOINT_ENV", "ResumeMixin", "read_resume_env"]
