"""verl on Probe (RL plan §6.5): launch with `python -m probe.integrations.verl.launch -- python3 -m
verl.trainer.main_ppo ... trainer.logger="['console','probe']"`. `setup_worker` is the Ray setup hook the launcher
installs; `register()` teaches verl's `Tracking` the `probe` backend in this process. DESIGN.md. Nothing here
imports verl until it runs."""

from __future__ import annotations

from .runs import get_rewind_step, read_resume_step
from .tracking import register, setup_worker

__all__ = ["get_rewind_step", "read_resume_step", "register", "setup_worker"]
