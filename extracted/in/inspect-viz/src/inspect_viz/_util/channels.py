from inspect_viz._core.data import Data

LOG_VIEWER_COLUMN = "log_viewer"
LOG_VIEWER_CHANNEL_LABEL = "Log Viewer"


def resolve_log_viewer_channel(data: Data, channels: dict[str, str]) -> None:
    if LOG_VIEWER_COLUMN in data.columns:
        channels[LOG_VIEWER_CHANNEL_LABEL] = LOG_VIEWER_COLUMN
