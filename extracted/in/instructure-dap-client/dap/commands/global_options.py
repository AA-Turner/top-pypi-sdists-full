import asyncclick as click
import os
from typing import Any, Optional

from .. import ui


class GlobalOptions:
    loglevel: str
    logfile: str
    logformat: str
    log_to_console: bool
    base_url: str
    client_id: str
    client_secret: str
    tracking: Optional[bool]
    interactive: bool
    console_theme: ui.ConsoleTheme

    def __init__(self, **kwargs: Any) -> None:
        for name in kwargs:
            setattr(self, name, kwargs[name])


pass_global_options = click.make_pass_decorator(GlobalOptions, ensure=True)


DAP_API_URL_DEFAULT = "https://api-gateway.instructure.com"
DAP_TRACKING_TRUE_VALUES = ("true", "1", "yes", "on")
DAP_TRACKING_FALSE_VALUES = ("false", "0", "no", "off")


def dap_tracking_valid_values() -> str:
    return ", ".join(DAP_TRACKING_TRUE_VALUES + DAP_TRACKING_FALSE_VALUES)


def read_dap_tracking_env_var() -> bool:
    tracking_str = os.getenv("DAP_TRACKING")
    if tracking_str is None:
        # default to tracking enabled if the environment variable is not set
        # this is to ensure that the library works out of the box with tracking enabled
        # unless explicitly disabled by the user
        return True
    else:
        if tracking_str.lower() in DAP_TRACKING_TRUE_VALUES:
            return True
        if tracking_str.lower() in DAP_TRACKING_FALSE_VALUES:
            return False
    raise ValueError(
        "Invalid value for DAP_TRACKING environment variable. "
        f"Expected values are: {dap_tracking_valid_values()}."
    )
