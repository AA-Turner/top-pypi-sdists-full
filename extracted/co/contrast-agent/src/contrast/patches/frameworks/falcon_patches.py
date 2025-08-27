# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys
import contrast
from contrast.agent import scope
from contrast.agent.assess.policy.source_policy import apply_stream_source
from contrast.agent.policy import patch_manager
from contrast.agent.middlewares.route_coverage import common

from contrast.utils.patch_utils import (
    build_and_apply_patch,
    unregister_module_patcher,
    wrap_and_watermark,
    register_module_patcher,
)
from contrast.utils.decorators import fail_quietly
from contrast_vendor import structlog as logging


FALCON_MULTIPART_MIDDLEWARE_MODULE = "falcon_multipart.middleware"
FALCON_MULTIPART_MIDDLEWARE_CLASS = "MultipartMiddleware"
FALCON_MODULE = "falcon"
FALCON_ASGI_MODULE = "falcon.asgi"

logger = logging.getLogger("contrast")


def build_parse_patch(orig_method, _):
    def parse_patch(wrapped, instance, args, kwargs):
        """
        Deadzone for falcon_multipart.middleware.MultipartMiddleware.parse

        This method can cause an enormous amount of propagation to occur, which can
        cause requests to be extremely slow. This is because this middleware parses all
        of the multipart form data into memory on the request object. We deadzone this
        propagation in order to greatly improve performance. The parse_field method
        patch below ensures that we still track the relevant data.

        This method gets called before MultipartMiddleware.parse_field in
        MultipartMiddleware.process_request.
        """
        del instance

        with scope.contrast_scope():
            return wrapped(*args, **kwargs)

    return wrap_and_watermark(orig_method, parse_patch)


def build_parse_field_patch(orig_method, _):
    def parse_field_patch(wrapped, instance, args, kwargs):
        """
        Deadzone and source tracker for falcon_multipart.middleware.MultipartMiddleware

        First we deadzone the call to the original method in order to prevent
        unnecessary propagation and improve performance. Next, we create sources for
        the result so that we don't miss any input data.

        This method gets called after MultipartMiddleware.parse in
        MultipartMiddleware.process_request.
        """
        with scope.contrast_scope():
            result = wrapped(*args, **kwargs)

        apply_stream_source("parse_field", result, instance, result, args, kwargs)

        return result

    return wrap_and_watermark(orig_method, parse_field_patch)


def patch_falcon_multipart(module):
    middleware_cls = getattr(module, FALCON_MULTIPART_MIDDLEWARE_CLASS, None)
    if middleware_cls is None:
        return

    build_and_apply_patch(middleware_cls, "parse", build_parse_patch)
    build_and_apply_patch(middleware_cls, "parse_field", build_parse_field_patch)


def build_call_patch(orig_func, patch_policy):
    """
    Patch for falcon.App.__call__

    This is how we perform route discovery and observation for Falcon.
    """
    del patch_policy

    def call_patch(wrapped, instance, args, kwargs):
        do_falcon_first_request_analysis(instance)
        try:
            result = wrapped(*args, **kwargs)
        finally:
            do_falcon_routes_observation(instance, args)

        return result

    return wrap_and_watermark(orig_func, call_patch)


@fail_quietly("unable to perform Falcon first request analysis discovery")
@scope.contrast_scope()
def do_falcon_first_request_analysis(falcon_instance):
    from contrast.agent.middlewares.route_coverage.falcon_routes import (
        create_falcon_routes,
    )

    from contrast.agent import agent_state

    if not agent_state.is_first_request():
        return

    common.handle_route_discovery("falcon", create_falcon_routes, (falcon_instance,))
    do_config_scanning(logger, falcon_instance)


@fail_quietly("unable to perform Falcon route observation")
@scope.contrast_scope()
def do_falcon_routes_observation(falcon_app_instance, request_args):
    from contrast.agent.middlewares.route_coverage.falcon_routes import (
        get_falcon_signature_and_template,
    )

    context = contrast.REQUEST_CONTEXT.get()

    if context is None:
        return
    if getattr(falcon_app_instance, "_ASGI", False):
        request_path = request_args[0]["path"]
        request_method = request_args[0]["method"]
    else:
        request_path = request_args[0]["PATH_INFO"]
        request_method = request_args[0]["REQUEST_METHOD"]

    context.signature, context.path_template = get_falcon_signature_and_template(
        request_path,
        falcon_app_instance,
        request_method,
    )
    logger.debug(
        "Found Falcon view function",
        signature=context.signature,
        path_template=context.path_template,
    )


@fail_quietly("failed to apply Falcon config scanning rules")
def do_config_scanning(logger, falcon_app_instance):
    from contrast.agent.assess.rules.config.falcon_secure_flag_rule import (
        FalconSecureFlagRule,
    )

    logger.debug("applying falcon config scanning rules")

    for rule in [
        FalconSecureFlagRule(),
    ]:
        rule.apply(falcon_app_instance.resp_options)


def patch_falcon(falcon_module):
    # If the runner is in use, then CommonMiddlewarePatch has already
    # patched __call__ for foundational middleware operations. We want
    # both patches to be applied, so we force this one.
    build_and_apply_patch(falcon_module.App, "__call__", build_call_patch, force=True)


def patch_falcon_asgi(falcon_asgi_module):
    build_and_apply_patch(
        falcon_asgi_module.App, "__call__", build_call_patch, force=True
    )


def register_patches():
    register_module_patcher(patch_falcon, FALCON_MODULE)
    register_module_patcher(patch_falcon_asgi, FALCON_ASGI_MODULE)

    register_module_patcher(patch_falcon_multipart, FALCON_MULTIPART_MIDDLEWARE_MODULE)


def reverse_patches():
    unregister_module_patcher(FALCON_MODULE)
    if falcon_module := sys.modules.get(FALCON_MODULE):
        patch_manager.reverse_patches_by_owner(falcon_module.App)

    unregister_module_patcher(FALCON_ASGI_MODULE)
    if falcon_asgi_module := sys.modules.get(FALCON_ASGI_MODULE):
        patch_manager.reverse_patches_by_owner(falcon_asgi_module.app.App)
        patch_manager.reverse_patches_by_owner(falcon_asgi_module.App)
        patch_manager.reverse_patches_by_owner(falcon_asgi_module)

    unregister_module_patcher(FALCON_MULTIPART_MIDDLEWARE_MODULE)
    if (
        falcon_multipart_middleware_module := sys.modules.get(
            FALCON_MULTIPART_MIDDLEWARE_MODULE
        )
    ) and (
        middleware_cls := getattr(
            falcon_multipart_middleware_module, FALCON_MULTIPART_MIDDLEWARE_CLASS
        )
    ):
        patch_manager.reverse_patches_by_owner(middleware_cls)
