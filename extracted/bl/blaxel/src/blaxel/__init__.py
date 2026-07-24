"""Blaxel - AI development platform SDK."""

from .core.common.autoload import autoload
from .core.common.env import env
from .core.common.settings import settings

__version__ = "0.3.4"
__commit__ = "f3eaace5feb46939c2d49b4c75994be7bbfb1287"
__sentry_dsn__ = "https://9711de13cd02b285ca4378c01de8dc30@o4508714045276160.ingest.us.sentry.io/4510461121462272"
__all__ = ["autoload", "settings", "env"]

autoload()
