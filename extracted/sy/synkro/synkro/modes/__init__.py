"""Mode configurations for different dataset types."""

from synkro.modes.config import ModeConfig, get_mode_config
from synkro.modes.conversation import CONVERSATION_CONFIG, INSTRUCTION_CONFIG
from synkro.modes.tool_call import TOOL_CALL_CONFIG

__all__ = [
    "ModeConfig",
    "get_mode_config",
    "CONVERSATION_CONFIG",
    "INSTRUCTION_CONFIG",
    "TOOL_CALL_CONFIG",
]
