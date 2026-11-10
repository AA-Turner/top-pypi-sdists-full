"""ART (OpenPipe Agent Reinforcement Trainer) on Probe: `track(model)` records metrics, trajectories as samples,
weight versions and checkpoints, with no W&B. DESIGN.md. Imports nothing from ART: it works on the objects given."""

from .art import ArtTracker, get_rewind_step, track

__all__ = ["ArtTracker", "get_rewind_step", "track"]
