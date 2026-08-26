"""Blaxel - AI development platform SDK."""

from .core.common.autoload import autoload
from .core.common.env import env
from .core.common.settings import settings

__version__ = "0.4.4"
__commit__ = "e5118d575879f7816f0d1a66b28402a49cdc393f"
__sentry_dsn__ = "https://9711de13cd02b285ca4378c01de8dc30@o4508714045276160.ingest.us.sentry.io/4510461121462272"
__all__ = ["autoload", "settings", "env"]

autoload()
