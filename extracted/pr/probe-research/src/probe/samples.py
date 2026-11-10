"""Compatibility import for ``probe.sdk.run.samples``: ``import probe.samples`` then
``probe.samples.generated_by(run=..., version=...)`` names who wrote an SFT example (RL plan §6.2)."""

from .sdk.run.samples.refs import generated_by, parse_generated_by

__all__ = ["generated_by", "parse_generated_by"]
