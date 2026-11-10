"""Commands on a live sample: cancel, retry, watch. Each is a row of the shared `commands` table (`records/command.py`,
served from rl-next W33); its ask body is `CommandAsk`. DESIGN.md "Live"."""

from __future__ import annotations

from ...command import CommandKind

#: The kinds asked of one sample (`POST .../samples/live/{attempt}/<kind>`), in route order.
SAMPLE_COMMAND_KINDS = (CommandKind.CANCEL, CommandKind.RETRY, CommandKind.WATCH)
