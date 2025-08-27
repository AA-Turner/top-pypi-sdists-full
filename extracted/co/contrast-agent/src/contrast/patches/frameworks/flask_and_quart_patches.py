# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys
import functools

from contrast_fireball import DiscoveredRoute

import contrast
from contrast.agent import scope
from contrast.agent.middlewares.route_coverage import common
from contrast.agent.policy import patch_manager
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    unregister_module_patcher,
    wrap_and_watermark,
    register_module_patcher,
)
from contrast.utils.decorators import fail_quietly
from contrast.utils.safe_import import safe_import_list

from contrast.agent.assess.rules.config import (
    FlaskSessionAgeRule,
    FlaskSecureFlagRule,
    FlaskHttpOnlyRule,
)

from contrast_vendor import structlog as logging

FLASK_MODULE_NAME = "flask"
QUART_MODULE_NAME = "quart"

logger = logging.getLogger("contrast")


@functools.lru_cache(maxsize=1)
def _get_flask_app_type():
    return tuple(safe_import_list("flask.Flask"))


@functools.lru_cache(maxsize=1)
def _get_quart_app_type():
    return tuple(safe_import_list("quart.Quart"))


def build_flask_full_dispatch_request_patch(orig_func, patch_policy):
    del patch_policy

    def full_dispatch_request_patch(wrapped, instance, args, kwargs):
        do_first_request_analysis(instance, "flask")
        try:
            result = wrapped(*args, **kwargs)
        finally:
            do_flask_route_observation(instance)
        return result

    return wrap_and_watermark(orig_func, full_dispatch_request_patch)


def build_quart_full_dispatch_request_patch(orig_func, patch_policy):
    del patch_policy

    async def full_dispatch_request_patch(wrapped, instance, args, kwargs):
        do_first_request_analysis(instance, "quart")
        try:
            result = await wrapped(*args, **kwargs)
        finally:
            do_quart_route_observation(instance, *args, **kwargs)
        return result

    return wrap_and_watermark(orig_func, full_dispatch_request_patch)


@fail_quietly("Failed to run first-request analysis")
@scope.contrast_scope()
def do_first_request_analysis(app_instance, framework: str):
    from contrast.agent import agent_state

    if not agent_state.is_first_request():
        return

    common.handle_route_discovery(framework, discover_routes, (app_instance,))
    do_config_scanning(app_instance)


@fail_quietly("unable to perform Flask route observation")
@scope.contrast_scope()
def do_flask_route_observation(flask_instance):
    logger.debug("Performing Flask route observation")

    flask_ctx = None
    try:
        from flask.globals import request_ctx

        flask_ctx = request_ctx
    except ImportError:
        from flask.globals import _request_ctx_stack

        flask_ctx = _request_ctx_stack.top

    do_route_observation(flask_ctx, flask_instance)


@fail_quietly("unable to perform Quart route observation")
@scope.contrast_scope()
def do_quart_route_observation(quart_instance, *args, **kwargs):
    logger.debug("Performing Quart route observation")

    quart_ctx = args[0] if len(args) > 0 else kwargs.get("request_context")
    do_route_observation(quart_ctx, quart_instance)


@fail_quietly("unable to perform Flask/Quart route observation")
@scope.contrast_scope()
def do_route_observation(framework_ctx, app_instance):
    if (context := contrast.REQUEST_CONTEXT.get()) is None:
        logger.debug("not in request context - skipping route observation")
        return

    if not framework_ctx:
        logger.debug("WARNING: unable to get framework_ctx for route observation")
        return

    if not (rule := framework_ctx.request.url_rule):
        logger.debug("WARNING: unable to get url_rule for route observation")
        return

    endpoint = getattr(framework_ctx.request.url_rule, "endpoint", None)
    if (view_func := app_instance.view_functions.get(endpoint)) is None:
        logger.debug("did not find endpoint for route observation")
        return

    context.signature = common.build_signature(endpoint, view_func)
    context.path_template = rule.rule
    logger.debug(
        "Found view function",
        view_func=context.signature,
        path_template=context.path_template,
    )


def discover_routes(app) -> set[DiscoveredRoute]:
    """
    Returns all the routes registered to a Flask or Quart app
    """
    routes = set()

    for rule in list(app.url_map.iter_rules()):
        view_func = app.view_functions[rule.endpoint]
        signature = common.build_signature(rule.endpoint, view_func)
        methods = rule.methods or common.DEFAULT_ROUTE_METHODS
        path_template = rule.rule
        for method_type in methods:
            routes.add(
                DiscoveredRoute(
                    verb=method_type,
                    url=path_template,
                    signature=signature,
                    framework=("Quart" if type(app).__name__ == "Quart" else "Flask"),
                )
            )

    return routes


@fail_quietly("Failed to run config scanning rules")
def do_config_scanning(app_instance):
    logger.debug("Running config scanning rules")
    for rule in [FlaskSessionAgeRule, FlaskSecureFlagRule, FlaskHttpOnlyRule]:
        rule().apply(app_instance)


def patch_flask(flask_module):
    build_and_apply_patch(
        flask_module.Flask,
        "full_dispatch_request",
        build_flask_full_dispatch_request_patch,
    )


def patch_quart(quart_module):
    build_and_apply_patch(
        quart_module.Quart,
        "full_dispatch_request",
        build_quart_full_dispatch_request_patch,
    )


def register_patches():
    register_module_patcher(patch_flask, FLASK_MODULE_NAME)
    register_module_patcher(patch_quart, QUART_MODULE_NAME)


def reverse_patches():
    unregister_module_patcher(FLASK_MODULE_NAME)
    flask_module = sys.modules.get(FLASK_MODULE_NAME)
    if flask_module:
        patch_manager.reverse_patches_by_owner(flask_module.Flask)

    unregister_module_patcher(QUART_MODULE_NAME)
    quart_module = sys.modules.get(QUART_MODULE_NAME)
    if quart_module:
        patch_manager.reverse_patches_by_owner(quart_module.Quart)
