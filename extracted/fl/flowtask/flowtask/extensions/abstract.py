"""BaseExtension is a Helper to build Pluggable extensions for FlowTask."""
import sys
from typing import Optional
from collections.abc import Callable
from abc import ABC
from navconfig.logging import logging
from navigator.types import WebApp
from ..exceptions import TaskException

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec
P = ParamSpec("P")


class ExtensionError(TaskException):
    """Useful for raise errors from Extensions."""


class BaseExtension(ABC):
    """BaseExtension.

    Description: Base Class for all FlowTask Extensions.
    """

    app: WebApp

    # Signal for any startup method on application.
    on_startup: Optional[Callable] = None

    # Signal for any shutdown process (will registered into App).
    on_shutdown: Optional[Callable] = None

    # Signal for any cleanup process (will registered into App).
    on_cleanup: Optional[Callable] = None

    # adding custom middlewares to app (if needed)
    middleware: Optional[Callable] = None

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        ### added config support
        self._args = args
        self._kwargs = kwargs
        ## name of the extension:
        self.__name__: str = self.__class__.__name__
        ### logging
        self.logger = logging.getLogger(f"FlowTask.ext.{self.__name__}")

    def setup(self, app: WebApp) -> WebApp:
        if hasattr(app, "get_app"):  # migrate to BaseApplication (on types)
            self.app = app.get_app()
        elif isinstance(app, WebApp):
            self.app = app  # register the app into the Extension
        else:
            raise TypeError(f"Invalid type for aiohttp Application: {app}:{type(app)}")
        self.logger.debug(f":::: FlowTask Extension {self.__name__} Loaded ::::")
        # add a middleware to the app
        if callable(self.middleware):
            try:
                mdl = self.app.middlewares
                # add the middleware
                mdl.append(self.middleware)
            except Exception as err:
                self.logger.exception(
                    f"Error loading Extension Middleware {self.__name__} init: {err!s}"
                )
                raise ExtensionError(
                    f"Error loading Extension Middleware {self.__name__} init: {err!s}"
                ) from err

        # adding signals for startup and shutdown:
        # startup operations over extension backend
        if callable(self.on_startup):
            self.app.on_startup.append(self.on_startup)
        # cleanup operations over extension backend
        if callable(self.on_shutdown):
            self.app.on_shutdown.append(self.on_shutdown)
        # cleanup operations over extension backend
        if callable(self.on_cleanup):
            self.app.on_cleanup.append(self.on_cleanup)
        return self.app
