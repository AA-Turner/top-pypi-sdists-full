"""Agent telemetry event names and ambient context allowlists."""

from mistralai.vibe.sdk.observability import COMMON_CONTEXT_KEYS

NEW_SESSION_EVENT = "vibe.new_session"
REQUEST_SENT_EVENT = "vibe.request_sent"
TOOL_CALL_FINISHED_EVENT = "vibe.tool_call_finished"

EVENT_CONTEXT_KEYS: dict[str, tuple[str, ...]] = {
    NEW_SESSION_EVENT: (*COMMON_CONTEXT_KEYS, "nb_skills", "nb_mcp_servers"),
    REQUEST_SENT_EVENT: (*COMMON_CONTEXT_KEYS, "run_mode", "task_id"),
    TOOL_CALL_FINISHED_EVENT: (*COMMON_CONTEXT_KEYS, "task_id"),
}
