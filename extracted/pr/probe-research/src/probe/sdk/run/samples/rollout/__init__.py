"""rollout: one rollout's capture (`RolloutCapture`): its messages as sent, tool runs, and the files its own code
attaches with `attach_file` / `attach_text`, exported into the adapter's own generator part. DESIGN.md "Rollout
capture"."""

from .decoded import Decode, build_decoded_turns, make_decode
from .messages import REASONING_KEYS, build_turns, to_tool_call
from .rollout import ENVIRONMENT_SPAN, RolloutCapture, attach_file, attach_text, get_current_rollout
from .uploads import UPLOAD_QUEUE_TIMEOUT_S, UPLOAD_TIMEOUT_S, Attachment

__all__ = [
    "ENVIRONMENT_SPAN",
    "REASONING_KEYS",
    "UPLOAD_QUEUE_TIMEOUT_S",
    "UPLOAD_TIMEOUT_S",
    "Attachment",
    "Decode",
    "RolloutCapture",
    "attach_file",
    "attach_text",
    "build_decoded_turns",
    "build_turns",
    "get_current_rollout",
    "make_decode",
    "to_tool_call",
]
