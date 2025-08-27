# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

import contrast
from contrast.agent import scope
from contrast.agent.policy.applicator import (
    apply_module_patches,
    reverse_module_patches,
)
from contrast.agent.middlewares.route_coverage import common
from contrast.agent.policy import patch_manager
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    unregister_module_patcher,
    wrap_and_watermark,
    register_module_patcher,
)
from contrast.utils.decorators import fail_quietly
from contrast_fireball import DiscoveredRoute

from contrast_vendor import structlog as logging

MODULE_NAME = "bottle"
DEFAULT_BOTTLE_ROUTE_METHODS = common.DEFAULT_ROUTE_METHODS + ("PUT", "PATCH", "DELETE")

logger = logging.getLogger("contrast")


def build_prepare_patch(orig_func, patch_policy, bottle_module):
    del patch_policy

    def prepare_patch(wrapped, instance, args, kwargs):
        """
        Patch for bottle.SimpleTemplate.prepare.

        This is needed because of the unfortunate way bottle calls on
        `html_escape` as a kwarg in the prepare definition in SimpleTemplate.
        See https://github.com/bottlepy/bottle/blob/master/bottle.py#L3952

        Because of this behavior, the `html_escape` func is not our patched
        `html_escape` defined in policy.
        By patching prepare, we intercept its call and instead of allowing
        it to use the default kwarg for `html_escape`, we pass our own
        patched `html_escape` in order to prevent false positive XSS findings.
        """
        del instance

        # html_escape MUST already be patched by policy in order
        # to pass in the patched func to prepare
        kwargs.setdefault("escape_func", bottle_module.html_escape)
        return wrapped(*args, **kwargs)

    return wrap_and_watermark(orig_func, prepare_patch)


def build_call_patch(orig_func, patch_policy):
    """
    Patch for bottle.Bottle.__call__

    This is how we perform route discovery for Bottle. Many different patches could
    probably work here, since we really just need a reference to the Bottle instance
    after all routes have been registered.
    """
    del patch_policy

    def call_patch(wrapped, instance, args, kwargs):
        do_bottle_route_discovery(instance)
        return wrapped(*args, **kwargs)

    return wrap_and_watermark(orig_func, call_patch)


@fail_quietly("unable to perform Bottle route discovery")
@scope.contrast_scope()
def do_bottle_route_discovery(bottle_instance):
    from contrast.agent import agent_state

    if not agent_state.is_first_request():
        return

    common.handle_route_discovery("bottle", create_bottle_routes, (bottle_instance,))


def create_bottle_routes(app) -> set[DiscoveredRoute]:
    """
    Returns all the routes registered to a Bottle app.
    """
    return {
        DiscoveredRoute(
            verb=method_type,
            url=route.rule,
            signature=common.build_signature(route.rule, route.callback),
            framework="Bottle",
        )
        for route in app.routes
        for method_type in DEFAULT_BOTTLE_ROUTE_METHODS
    }


def build_match_patch(orig_func, patch_policy):
    """
    Patch for bottle.Router.match()

    This sets up request context with all necessary info for current route observation
    """
    del patch_policy

    def match_patch(wrapped, instance, args, kwargs):
        del instance

        result = wrapped(*args, **kwargs)
        do_bottle_route_observation(*result)
        return result

    return wrap_and_watermark(orig_func, match_patch)


@fail_quietly("unable to perform bottle route coverage in Bottle match patch")
@scope.contrast_scope()
def do_bottle_route_observation(route, url_args):
    context = contrast.REQUEST_CONTEXT.get()
    if context is None:
        return

    context.signature = common.build_signature(route.rule, route.callback)
    context.path_template = route.rule
    logger.debug(
        "Found Bottle view function",
        signature=context.signature,
        path_template=context.path_template,
    )


def patch_bottle(bottle_module):
    # We ask policy to go ahead and do all bottle patches here (even though policy
    # patches will happen later on) because we MUST have some bottle policy patches
    # already applied for these non-policy patches to work.
    # This would not be necessary if in _enable_patches policy_patches were applied
    # first.
    apply_module_patches(bottle_module)

    build_and_apply_patch(
        bottle_module.SimpleTemplate,
        "prepare",
        build_prepare_patch,
        builder_args=(bottle_module,),
    )
    # If the runner is in use, then CommonMiddlewarePatch has already
    # patched __call__ for foundational middleware operations. We want
    # both patches to be applied, so we force this one.
    build_and_apply_patch(
        bottle_module.Bottle, "__call__", build_call_patch, force=True
    )
    build_and_apply_patch(bottle_module.Router, "match", build_match_patch)


def register_patches():
    register_module_patcher(patch_bottle, MODULE_NAME)


def reverse_patches():
    unregister_module_patcher(MODULE_NAME)
    bottle_module = sys.modules.get(MODULE_NAME)
    if not bottle_module:
        return

    reverse_module_patches(bottle_module)
    patch_manager.reverse_patches_by_owner(bottle_module.SimpleTemplate)
    patch_manager.reverse_patches_by_owner(bottle_module.Bottle)
    patch_manager.reverse_patches_by_owner(bottle_module.Router)
