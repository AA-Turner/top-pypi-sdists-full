"""Blaxel - AI development platform SDK."""

from .core.common.autoload import autoload
from .core.common.env import env
from .core.common.settings import settings

__version__ = "0.4.28"
__commit__ = "3df3ac639671faedf63724c3c232ad263a9108f9"
__sentry_dsn__ = "https://9711de13cd02b285ca4378c01de8dc30@o4508714045276160.ingest.us.sentry.io/4510461121462272"
__posthog_key__ = ""
__all__ = ["autoload", "settings", "env"]

autoload()
