# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
import inspect
from enum import Enum, auto
from contextlib import contextmanager
from contextvars import ContextVar

from contrast.agent.policy import patch_manager
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    add_watermark,
    wrap_and_watermark,
    register_module_patcher,
)
from contrast.utils.namespace import Namespace
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class module(Namespace):
    called_with_middleware: ContextVar = ContextVar(
        "called_with_middleware", default=False
    )
    middleware = None


class AppInterfaceType(Enum):
    WSGI = auto()
    ASGI = auto()
    AUTO_DETECT = auto()


@contextmanager
def called_with_middleware():
    """
    We patch `__call__` on the application object and call our middleware from within
    that patch. This contextmanager provides a mechanism to avoid infinite recursion
    when the middleware in turn calls the original application.
    """
    try:
        module.called_with_middleware.set(True)
        yield
    finally:
        module.called_with_middleware.set(False)


def _is_asgi(app_interface: AppInterfaceType, app_call_func) -> bool:
    """
    Determine if we should consider this application to be an ASGI app.

    If an `app_interface` has been explicitly requested, use that. Otherwise,
    automatically determine the interface by inspection.
    """
    return (
        inspect.iscoroutinefunction(app_call_func)
        if app_interface == AppInterfaceType.AUTO_DETECT
        else app_interface == AppInterfaceType.ASGI
    )


def build__init__patch(
    orig_func, patch_policy, framework_name: str, app_interface: AppInterfaceType
):
    """
    Generic patch for __init__ method of various application classes

    This initializes the contrast middleware and saves it to this module
    """
    del patch_policy

    def __init__patch(wrapped, instance, args, kwargs) -> None:
        from contrast.agent.agent_state import automatic_middleware
        from contrast.wsgi.middleware import WSGIMiddleware
        from contrast.asgi.middleware import ASGIMiddleware

        result = wrapped(*args, **kwargs)

        is_asgi = _is_asgi(app_interface, instance.__call__)
        logger.info(f"Application interface: {'ASGI' if is_asgi else 'WSGI'}")

        with automatic_middleware():
            module.middleware = (ASGIMiddleware if is_asgi else WSGIMiddleware)(
                instance, framework_name=framework_name
            )

        return result

    return wrap_and_watermark(orig_func, __init__patch)


def build__call__patch(orig_func, patch_policy, app_interface: AppInterfaceType):
    """
    Generic patch for automatically instrumenting a WSGI/ASGI app's __call__ method.

    This patch calls the middleware, which must have been initialized in the `__init__`
    patch. This patch builder is also responsible for determining if we need to supply
    an async __call__ patch (ASGI) or sync (WSGI).

    ----------------------- NOTE -----------------------

    This patch does not make use of wrapt function wrappers. This is because `uvicorn`
    assumes that if the "application object" can be used like this

    ```
    application_object = application_object()
    ```

    without raising a TypeError, then the application object must have actually been an
    application factory. This is extremely unfortunate for us, because it means that the
    signature of our __call__ patch needs to match the original call (we can't accept
    *args, **kwargs and just pass them through).

    We can't even raise a TypeError manually, because in the async case, the TypeError
    wouldn't be raised until the coroutine is awaited. Uvicorn calls the app as though
    it were a synchronous function without actually checking.
    """
    del patch_policy

    async def __call__patch_asgi(self, scope, receive, send):
        if module.called_with_middleware.get():
            return await orig_func(self, scope, receive, send)

        with called_with_middleware():
            return await module.middleware(scope, receive, send)

    def __call__patch_wsgi(self, environ, start_response):
        if module.called_with_middleware.get():
            return orig_func(self, environ, start_response)

        with called_with_middleware():
            return module.middleware(environ, start_response)

    patch = (
        __call__patch_asgi if _is_asgi(app_interface, orig_func) else __call__patch_wsgi
    )
    return add_watermark(patch)


class CommonMiddlewarePatch:
    """
    Class that implements generic application patches for a variety of frameworks

    We expect that this class can potentially be used in any framework where
    the __init__ method of the framework's application class will be used for
    automatic instrumentation.

    :param module_name: Name of the module that owns the application class
    :param framework_name: Name of the framework (defaults to `module_name`)
    :param application_class_name: Name of the application class to be hooked (defaults to capitalized `framework_name`)
    """

    def __init__(
        self,
        module_name: str,
        *,
        application_class_name: str | None = None,
        framework_name: str | None = None,
        app_interface: AppInterfaceType = AppInterfaceType.WSGI,
    ):
        self.module_name = module_name
        self.framework_name = framework_name or module_name
        self.application_class_name = (
            application_class_name or self.framework_name.capitalize()
        )
        self.app_interface = app_interface

    @property
    def __name__(self):
        return f"{__name__.rpartition('.')[0]}.{self.module_name}"

    def register_patches(self):
        """
        Registers post-import hook for the __init__ method of the application class
        """

        def patch_application(module):
            app_class = getattr(module, self.application_class_name)
            build_and_apply_patch(
                app_class,
                "__init__",
                build__init__patch,
                builder_args=(
                    self.framework_name,
                    self.app_interface,
                ),
            )
            build_and_apply_patch(
                app_class,
                "__call__",
                build__call__patch,
                builder_args=(self.app_interface,),
            )

        register_module_patcher(patch_application, self.module_name)

    def reverse_patches(self):
        """
        Reverses patches for the __init__ method of the application class
        """
        patch_manager.reverse_class_patches_by_name(
            self.module_name,
            self.application_class_name,
        )
