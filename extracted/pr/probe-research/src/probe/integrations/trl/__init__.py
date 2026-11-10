"""TRL on Probe: `track(trainer)` records a TRL trainer's samples (GRPO, RLOO, AsyncGRPO, distillation, opt-in SFT)
beside the metrics `report_to="probe"` records. DESIGN.md. Imports nothing from TRL or transformers: it works on the
trainer it is given."""

from .runs import get_rewind_step, read_resume_step
from .trl import TrlTracker, track

__all__ = ["TrlTracker", "get_rewind_step", "read_resume_step", "track"]
