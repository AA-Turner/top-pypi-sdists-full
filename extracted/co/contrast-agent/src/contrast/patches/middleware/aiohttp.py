# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from collections.abc import Iterable
from types import ModuleType

from contrast.agent.policy import patch_manager
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    unregister_module_patcher,
    wrap_and_watermark,
    register_module_patcher,
)
from contrast.utils.decorators import fail_quietly

from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

AIOHTTP_WEB_MODULE = "aiohttp.web"


def build__init__patch(orig_func, patch_policy):
    """
    Patch for aiohttp.web.Application.__init__

    This performs automatic middleware installation for aiohttp.
    """
    del patch_policy

    def __init__patch(wrapped, instance, args, kwargs) -> None:
        del instance

        add_middleware_to_kwargs(kwargs)
        return wrapped(*args, **kwargs)

    return wrap_and_watermark(orig_func, __init__patch)


@fail_quietly()
def add_middleware_to_kwargs(kwargs) -> None:
    """
    To actually auto-instrument aiohttp, we need to forcefully add our middleware to
    the `middlewares` kwarg passed in to aiohttp.web.Application.__init__. This kwarg
    expects an iterable of initialized aiohttp-style middlewares.

    This function simply accepts the constructor's original kwargs dict and injects our
    AioHttpMiddleware into the `middlewares` kwarg.
    """
    from contrast.aiohttp.middleware import AioHttpMiddleware
    from contrast.agent.agent_state import automatic_middleware

    contrast_middleware: AioHttpMiddleware
    with automatic_middleware():
        contrast_middleware = AioHttpMiddleware()

    middlewares: Iterable = kwargs.get("middlewares")
    if not middlewares:
        kwargs["middlewares"] = [contrast_middleware]
    elif isinstance(middlewares, list):
        middlewares.append(contrast_middleware)
    else:
        logger.error(
            "Cannot automatically install ContrastMiddleware - "
            "aiohttp's middlewares list had an unexpected type. "
            "See Contrast's documentation for installing the middleware manually."
        )


def patch_aiohttp_autoinstrumentation(aiohttp_web_module: ModuleType) -> None:
    build_and_apply_patch(
        aiohttp_web_module.Application, "__init__", build__init__patch
    )


def register_patches() -> None:
    register_module_patcher(patch_aiohttp_autoinstrumentation, AIOHTTP_WEB_MODULE)


def reverse_patches() -> None:
    unregister_module_patcher(AIOHTTP_WEB_MODULE)
    patch_manager.reverse_class_patches_by_name(AIOHTTP_WEB_MODULE, "Application")
