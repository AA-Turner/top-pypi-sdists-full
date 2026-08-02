# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import functools
from enum import Enum

import attrs

from geneva.config import ConfigBase


class TqdmMode(Enum):
    AUTO = "auto"
    SLACK = "slack"
    RICH = "rich"
    STD = "std"
    NOTEBOOK = "notebook"

    @staticmethod
    def from_str(s: str) -> "TqdmMode":
        return TqdmMode(s)


@attrs.define
class TqdmSlackConfig(ConfigBase):
    token: str | None = attrs.field(default=None)
    channel: str | None = attrs.field(default=None)
    mininterval: float | None = attrs.field(
        default=None, converter=attrs.converters.optional(float)
    )

    @classmethod
    def name(cls) -> str:
        return "slack"


@attrs.define
class TqdmConfig(ConfigBase):
    slack_config: TqdmSlackConfig | None = attrs.field(default=None)

    mode: TqdmMode = attrs.field(default=TqdmMode.AUTO, converter=TqdmMode.from_str)

    @classmethod
    def name(cls) -> str:
        return "tqdm"


_tqdm_config = TqdmConfig.get()
if _tqdm_config.mode == TqdmMode.AUTO:
    from tqdm.auto import tqdm
elif _tqdm_config.mode == TqdmMode.RICH:
    from tqdm.rich import tqdm
elif _tqdm_config.mode == TqdmMode.STD:
    from tqdm.std import tqdm
elif _tqdm_config.mode == TqdmMode.NOTEBOOK:
    from tqdm.notebook import tqdm
elif _tqdm_config.mode == TqdmMode.SLACK:
    from tqdm.contrib.slack import tqdm

    if (config := _tqdm_config.slack_config) is not None:
        args = {
            **({"token": config.token} if config.token is not None else {}),
            **({"channel": config.channel} if config.channel is not None else {}),
            **(
                {"mininterval": config.mininterval}
                if config.mininterval is not None
                else {}
            ),
        }
        tqdm = functools.partial(tqdm, **args)
else:
    raise ValueError(f"Unknown tqdm mode: {_tqdm_config.mode}")


# ANSI color codes for progress bar styling
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright foreground colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"


def supports_color() -> bool:
    # tqdm notebook module doesn't support ANSI colors in progress bar descriptions
    # use ANSI formatting for TTY environments only
    return tqdm.__module__ in {"tqdm.std", "tqdm.asyncio", "tqdm.rich"}


def fmt(text: str, color: str, bold: bool = False) -> str:
    """Apply ANSI color formatting to text."""
    if not supports_color():
        return text
    prefix = (Colors.BOLD if bold else "") + color
    return f"{prefix}{text}{Colors.RESET}"


def fmt_status_badge(status: str) -> str:
    """Format a status as a colorized badge."""
    if not status:
        return ""
    status = status.lower()
    state_color = {
        "running": Colors.BRIGHT_GREEN,
        "pending": Colors.BRIGHT_YELLOW,
        "failed": Colors.BRIGHT_RED,
        "suspended": Colors.YELLOW,
        "nodes-provisioning": Colors.BRIGHT_YELLOW,
        "pods-creating": Colors.BRIGHT_YELLOW,
        "cluster-cold": Colors.GREEN,
        "cluster-warm": Colors.BRIGHT_GREEN,
    }.get(status, Colors.CYAN)
    return fmt(f"{status}", state_color, bold=True)


def fmt_numeric(val: int | None, total: int | None = None) -> str:
    val = val or 0
    total = total or 0

    try:
        if total:
            col = Colors.BRIGHT_RED if val < total else Colors.BRIGHT_GREEN
        else:
            col = Colors.BRIGHT_RED if val == 0 else Colors.BRIGHT_GREEN
        return fmt(str(val), col)
    except Exception:
        return Colors.BRIGHT_GREEN


def fmt_pending(val: int | None) -> str:
    val = val or 0
    color = Colors.BRIGHT_YELLOW if val > 0 else Colors.BRIGHT_GREEN
    return fmt(str(val), color)


__all__ = ["tqdm"]
