"""Blaxel - AI development platform SDK."""

from .core.common.autoload import autoload
from .core.common.env import env
from .core.common.settings import settings

__version__ = "0.3.1"
__commit__ = "f04af247028eda18f66638c2f88dfbaed82b0804"
__sentry_dsn__ = "https://9711de13cd02b285ca4378c01de8dc30@o4508714045276160.ingest.us.sentry.io/4510461121462272"
__all__ = ["autoload", "settings", "env"]

autoload()
