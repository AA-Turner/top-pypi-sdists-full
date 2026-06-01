"""Shared ABC-level configuration for framework integrations.

Every `<Framework>Config` dataclass (LangGraphConfig today, CrewAIConfig and
others tomorrow) inherits from `FrameworkConfigBase`. Fields defined here
are wire-contract knobs that apply to every framework — adding one here
delivers it to all integrations for free.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class FrameworkConfigBase:
    """Base for every framework's static config dataclass.

    Subclasses are free to add their own fields; they MUST keep
    `zero_retention` reachable (i.e. don't shadow it).
    """

    zero_retention: bool = False
