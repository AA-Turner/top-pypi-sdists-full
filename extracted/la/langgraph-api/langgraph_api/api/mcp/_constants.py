MAX_ASSISTANTS = 1000
DEFAULT_PAGE_SIZE = 100
MAX_PAGE_OFFSET = 2**63 - 1
MAX_CURSOR_LENGTH = len(str(MAX_PAGE_OFFSET))

PAUSED_TOOL_MESSAGE = (
    "This tool paused to ask for human input, and this client can't answer it."
)
RUN_FAILED_MESSAGE = "The tool's run failed."
INVALID_CURSOR_MESSAGE = "Invalid cursor"
INTERNAL_ERROR_MESSAGE = "Internal server error"
UNRESUMABLE_PAUSE_MESSAGE = (
    "This tool paused to ask for human input, and this call can't be resumed."
)
ELICITATION_REQUIRED_MESSAGE = (
    "This tool asks for human input and needs {modes} elicitation."
)
INVALID_REQUEST_STATE = "Invalid or expired requestState"
UNASKABLE_INPUT_MESSAGE = "This tool needs input that can't be asked over MCP"
BREAKPOINT_MESSAGE = (
    "This tool stopped at a breakpoint (interrupt_before or interrupt_after), "
    "which can't be resumed over MCP."
)
PAUSED_CALL_TTL_MINUTES = 24 * 60
FINISHED_CALL_TTL_MINUTES = 10
