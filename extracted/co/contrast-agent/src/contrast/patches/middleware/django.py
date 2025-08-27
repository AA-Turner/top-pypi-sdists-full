# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import sys

import contrast
from contrast.agent import scope
from contrast.agent.policy import patch_manager
from contrast.utils.decorators import fail_loudly, fail_quietly
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    unregister_module_patcher,
    wrap_and_watermark,
    register_module_patcher,
)
from contrast.agent.middlewares.route_coverage import common

from contrast_vendor import structlog as logging

DJANGO_WSGI_NAME = "django.core.wsgi"
DJANGO_ASGI_NAME = "django.core.asgi"


@fail_quietly("failed to apply django config scanning rules")
def do_config_scanning(logger):
    # Lazy import for django
    from django.conf import settings as app_settings
    from contrast.agent.assess.rules.config import (
        DjangoHttpOnlyRule,
        DjangoSecureFlagRule,
        DjangoSessionAgeRule,
    )

    logger.debug("applying django config scanning rules")
    app_config_module_name = os.environ.get("DJANGO_SETTINGS_MODULE")
    if not app_config_module_name:
        logger.warning("unable to find django settings for config scanning")
        return

    app_config_module = sys.modules.get(app_config_module_name)
    if not app_config_module:
        logger.warning("django settings module not loaded; can't scan config")
        return

    for rule in [DjangoSessionAgeRule, DjangoSecureFlagRule, DjangoHttpOnlyRule]:
        rule().apply(app_settings, app_config_module)


@fail_quietly("failed to run django first request analysis")
@scope.contrast_scope()
def django_first_request(sender, **kwargs):
    from django.core import signals
    from contrast.agent.middlewares.route_coverage.django_routes import (
        create_django_routes,
    )

    del sender, kwargs

    logger = logging.getLogger("contrast")
    logger.debug("called django first request signal")

    do_config_scanning(logger)
    common.handle_route_discovery("django", create_django_routes, ())

    # the signal is no longer needed after the first request
    logger.debug("disconnecting django first request signal (first request started)")
    signals.request_started.disconnect(
        django_first_request, dispatch_uid="contrast_first_request"
    )


def _extract_path(signal_kwargs):
    """Extract path based on wsgi environ vs asgi scope"""
    # Handles the wsgi case
    environ = signal_kwargs.get("environ")
    if environ is not None:
        return environ.get("PATH_INFO", "")

    # Handles the asgi case
    scope = signal_kwargs.get("scope")
    if scope is not None:
        return scope.get("path", "")

    return ""


@fail_quietly("failed to run django request analysis")
@scope.contrast_scope()
def django_every_request(sender, **kwargs):
    """
    Django signal handler that performs route observation

    We expect the `environ` kwarg (for wsgi) or the `scope` kwarg (for asgi) to
    be present and not None. If these conditions do not hold, they will be
    handled by `fail_quietly`.
    """
    # Lazy import for django
    from contrast.agent.middlewares.route_coverage.django_routes import (
        build_django_signature,
        get_matched_resolver,
    )

    del sender

    logger = logging.getLogger("contrast")
    logger.debug("performing django route observation")

    context = contrast.REQUEST_CONTEXT.get()
    if context is None:
        logger.debug("not in request context - skipping route observation")
        return

    request_path = _extract_path(kwargs)
    resolved = get_matched_resolver(request_path)
    if resolved is None:
        logger.debug("did not find django view function for route observation")
        return

    context.signature = build_django_signature(resolved)
    if resolved.route is not None:
        context.path_template = resolved.route
    logger.debug(
        "Observed route",
        signature=context.signature,
        path_template=context.path_template,
    )


@fail_quietly("Failed to retrieve django application name from settings")
def get_app_name() -> str:
    # Lazy import for django
    from django.conf import settings

    application = getattr(
        settings,
        "WSGI_APPLICATION",
        "",
    ) or getattr(
        settings,
        "ASGI_APPLICATION",
        "",
    )

    return application.split(".")[0]


@fail_loudly("Failed to initialize Django-specific instrumentation")
def initialize_django():
    from contrast.agent.agent_state import set_application_name

    # Lazy import for django
    from django.core import signals

    logger = logging.getLogger("contrast")

    # TODO: PYT-2852 Revisit application name detection
    set_application_name(get_app_name())

    logger.debug("Connecting django signals")
    signals.request_started.connect(
        django_every_request, dispatch_uid="contrast_every_request"
    )
    # This signal runs on the first request only
    # Runs at the end of the first request to make sure we gather all registered routes
    signals.request_started.connect(
        django_first_request, dispatch_uid="contrast_first_request"
    )


def disconnect_django():
    from django.core import signals

    signals.request_started.disconnect(
        django_every_request, dispatch_uid="contrast_every_request"
    )
    signals.request_started.disconnect(
        django_first_request, dispatch_uid="contrast_first_request"
    )


def build_get_wsgi_app_patch(orig_func, _):
    def get_wsgi_application(wrapped, _, args, kwargs):
        # Avoids circular import
        from contrast.agent.agent_state import automatic_middleware
        from contrast.wsgi import ContrastMiddleware

        # This call needs to occur before middleware initialization
        initialize_django()

        with automatic_middleware():
            return ContrastMiddleware(wrapped(*args, **kwargs), framework_name="django")

    return wrap_and_watermark(orig_func, get_wsgi_application)


def build_get_asgi_app_patch(orig_func, _):
    def get_asgi_application(wrapped, _, args, kwargs):
        # Avoids circular import
        from contrast.agent.agent_state import automatic_middleware
        from contrast.asgi import ContrastMiddleware

        # This call needs to occur before middleware initialization
        initialize_django()

        with automatic_middleware():
            return ContrastMiddleware(wrapped(*args, **kwargs), framework_name="django")

    return wrap_and_watermark(orig_func, get_asgi_application)


def patch_django_wsgi(module):
    # XXX: It may be better to hook django.core.handlers.base.BaseHandler.__init__
    # It's possible that this will be more general solution for other servers
    build_and_apply_patch(module, "get_wsgi_application", build_get_wsgi_app_patch)


def patch_django_asgi(module):
    build_and_apply_patch(module, "get_asgi_application", build_get_asgi_app_patch)


def register_patches():
    register_module_patcher(patch_django_wsgi, DJANGO_WSGI_NAME)
    register_module_patcher(patch_django_asgi, DJANGO_ASGI_NAME)


def reverse_patches():  # pragma: no cover
    unregister_module_patcher(DJANGO_WSGI_NAME)
    unregister_module_patcher(DJANGO_ASGI_NAME)
    patch_manager.reverse_module_patches_by_name(DJANGO_WSGI_NAME)
    patch_manager.reverse_module_patches_by_name(DJANGO_ASGI_NAME)
