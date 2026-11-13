"""`probe.samples`: what a rollout's own code calls (`attach_file`, `attach_text`, `current_rollout`: the files and
span on the exact sample, D10) and who wrote an SFT example (`generated_by(run=..., version=...)`, RL plan §6.2)."""

from .sdk.run.samples.refs import generated_by, parse_generated_by
from .sdk.run.samples.rollout import attach_file, attach_text
from .sdk.run.samples.rollout import get_current_rollout as current_rollout

__all__ = ["attach_file", "attach_text", "current_rollout", "generated_by", "parse_generated_by"]
