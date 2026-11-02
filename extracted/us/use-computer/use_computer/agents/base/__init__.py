"""Public base-agent surface for CUA agents."""

from use_computer.agents.base.actions import _annotate_click, execute_action
from use_computer.agents.base.agent import BaseCUAAgent
from use_computer.agents.base.desktop import (
    DesktopProfile,
    OpenAIComputerEnvironment,
    desktop_profile,
)
from use_computer.agents.base.prompts import build_system_prompt, load_prompt
from use_computer.agents.base.sandbox import ComputerSandbox
from use_computer.agents.base.screenshots import (
    scale_screenshot_for_model,
    screenshot_cap_for_model,
)
from use_computer.agents.base.trajectory import write_trajectory

__all__ = [
    "BaseCUAAgent",
    "ComputerSandbox",
    "DesktopProfile",
    "OpenAIComputerEnvironment",
    "_annotate_click",
    "build_system_prompt",
    "desktop_profile",
    "execute_action",
    "load_prompt",
    "scale_screenshot_for_model",
    "screenshot_cap_for_model",
    "write_trajectory",
]
