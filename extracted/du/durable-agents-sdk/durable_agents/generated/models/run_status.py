from enum import Enum

class RunStatus(str, Enum):
    Queued = "queued",
    Running = "running",
    Paused = "paused",
    Success = "success",
    Error = "error",
    Timeout = "timeout",
    Skipped = "skipped",
    Cancelled = "cancelled",

