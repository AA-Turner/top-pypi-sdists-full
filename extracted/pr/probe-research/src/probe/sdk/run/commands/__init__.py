"""commands: a running script takes the run kinds it registered (agentic W&B W17); `probe.commands.sync()` is where
every rank of a multi-process script takes them together."""

from .sync import sync

__all__ = ["sync"]
