from enum import Enum

class DataSourceStatus(str, Enum):
    Active = "active",
    Running = "running",
    Paused = "paused",
    Syncing = "syncing",
    Limited = "limited",
    Quota_limited = "quota_limited",
    Finished = "finished",
    Error = "error",
    Needs_reauth = "needs_reauth",

