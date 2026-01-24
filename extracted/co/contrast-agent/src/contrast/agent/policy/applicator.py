# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import functools
import inspect
from inspect import iscoroutinefunction
from types import ModuleType


from contrast.utils.patch_utils import register_module_patcher
from contrast.agent.policy import patch_manager, registry
from contrast.agent.protect.policy import apply_protect_patch
from contrast.agent.assess.policy.patches import (
    build_assess_method,
    build_assess_method_legacy,
    build_assess_classmethod,
    build_assess_deadzone,
    build_assess_property_fget,
    apply_cached_property,
    build_assess_async_method,
    build_assess_async_deadzone,
)
from contrast.utils.patch_utils import repatch_module
from contrast.utils.safe_import import safe_import


from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


# Maintains a record of all patch locations that have been applied
PATCH_LOCATIONS = set()


@functools.lru_cache(maxsize=1)
def _get_werkzeug_cached_property():
    return safe_import("werkzeug.utils.cached_property")


def remove_patch_location(owner, name):
    """
    Remove patch located at owner (class or module) and name
    from patch locations.
    """
    if inspect.ismodule(owner):
        policy_patch_name = f"{owner.__name__}.{name}"
    elif inspect.isclass(owner):
        policy_patch_name = f"{owner.__module__}.{owner.__name__}.{name}"

    if policy_patch_name in PATCH_LOCATIONS:
        PATCH_LOCATIONS.remove(policy_patch_name)


def apply_assess_patch(patch_site, patch_policy):
    """
    Store the original method implementation under our custom "cs_assess_{name}" so we
    can call the old method from the new method in order to return the same result

    :param cls_or_module: Class or module to patch
    :param patch_policy: PatchLocationPolicy containing all policy nodes for this patch
    :param methods: methods in cls_or_module
    :param node_method: tuple of string and actual method
        ('get_raw_uri', <unbound method django.http.request.HttpRequest.get_raw_uri>)

    Static methods and class methods are implemented as descriptors. When one of these
    methods is called on the parent object, it uses the descriptor protocol, which
    means that the underlying function objects are not seen directly by the caller.

    In order to access the staticmethod/classmethod objects directly, they must be
    accessed via the parent object's __dict__ attribute.

    For example,

    class D:
        @staticmethod
        def sm():
            pass

    If I do this:
    D.sm will call __get__ under the hood to get the function definition (this is
    what's wrapped inside the staticmethod or classmethod obj in this case)

    If we do this:
    D.__dict__['sm'] we get the underlying staticmethod/classmethod object. This is
    required because we need to do a type check in order to replace the original obj
    with our own function of the correct type.

    This shows examples of C code re-written in python for the __get__ desc
    implementation for classmethod, staticmethod and function
    https://docs.python.org/2.7/howto/descriptor.html#functions-and-methods

    For additional details on PY3:
    https://docs.python.org/3/howto/descriptor.html#functions-and-methods
    """
    logger.debug("Applying assess patch to %s", patch_policy.name)

    method_name = patch_policy.method_name
    has_key = hasattr(patch_site, "__dict__") and method_name in patch_site.__dict__

    static_method = has_key and isinstance(
        patch_site.__dict__[method_name], staticmethod
    )
    class_method = has_key and isinstance(patch_site.__dict__[method_name], classmethod)

    old_method = _get_original_method(
        patch_policy, patch_site, method_name, static_method, class_method
    )

    werkzeug_cached_property = _get_werkzeug_cached_property()
    if werkzeug_cached_property is not None and isinstance(
        old_method, werkzeug_cached_property
    ):
        # return so that we don't prematurely run policy analysis.
        return apply_cached_property(patch_site, patch_policy, method_name, old_method)
    elif isinstance(old_method, property):
        fget = build_assess_property_fget(old_method, patch_policy)
        new_method = property(fget=fget, fset=old_method.fset, fdel=old_method.fdel)
    elif class_method:
        new_method = classmethod(build_assess_classmethod(old_method, patch_policy))
    elif static_method:
        new_method = staticmethod(build_assess_classmethod(old_method, patch_policy))
    elif iscoroutinefunction(old_method):
        new_method = (
            build_assess_async_deadzone(old_method, patch_policy)
            if patch_policy.is_deadzone
            else build_assess_async_method(old_method, patch_policy)
        )
    elif patch_policy.module in ("falcon.util.uri"):
        new_method = build_assess_method_legacy(old_method, patch_policy)
    else:
        # We only support deadzones for methods/functions right now.
        if patch_policy.is_deadzone and not patch_policy.deadzone_enabled:
            return False

        new_method = (
            build_assess_deadzone(old_method, patch_policy)
            if patch_policy.is_deadzone
            else build_assess_method(old_method, patch_policy)
        )

    # OPTIMIZATION: If we know this patch location is only one type (trigger,
    # propagation, source) and only one node, then we can assign that analysis code here
    # at patch-time and save time when patch is called. Most patches will benefit
    # from optimization as very few functions are more than one thing (example:
    # re.split is both a trigger for redos rule and a propagator).
    if len(patch_policy.all_nodes) == 1:
        patch_policy.assign_analysis_func()

    try:
        patch_manager.patch(patch_site, method_name, new_method)
        logger.debug("added patch to %s.%s", patch_site, method_name)
    except Exception as e:
        logger.debug(
            "unable to patch %s method of %s: %s", method_name, patch_site, str(e)
        )
        return False

    return True


def _get_original_method(
    patch_policy, patch_site, method_name, static_method, class_method
):
    # Need to make sure we get original static/class function
    if static_method or class_method:
        old_method = patch_site.__dict__[method_name]
    else:
        # get old function/property/method
        try:
            old_method = getattr(patch_site, patch_policy.method_name)
        except AttributeError:
            # Some python/framework versions or platforms will not have certain
            # methods/funcs defined so we skip them here. This isn't a failure
            # so logging is not necessary.
            return False

    return old_method


def apply_module_patches(module: ModuleType):
    """
    Apply patches to all methods and functions in a module as dictated by policy.

    This function might be called multiple times per module if multiple agent modes are
    enabled or in certain special cases (see direct references to this function). The
    global PATCH_LOCATIONS set ensures instrumentation is only actually applied once.
    """
    logger.debug("Applying module patches", module=module.__name__)

    _apply_v1_patches(module)
    _apply_v2_patches(module)

    # It's possible that the current module contains multiple references to the
    # function we replaced, but that only one of them is represented in policy. We do a
    # quick repatching pass over the current module here to make sure we cover all of
    # the references that may have been missed.
    repatch_module(module)

    # EDGE CASE PYT-1065: Werkzeug==0.16.x
    # This version of Werkzeug keeps a reference to the module in _real_module
    # which requires us to repatch functions in this second reference, too.
    if hasattr(module, "_real_module"):
        repatch_module(module._real_module)


def reverse_module_patches(module: ModuleType):
    """
    Reverse all patches applied to a module.
    """
    for patch_policy in registry.get_policy_by_module(module.__name__):
        if patch_policy.name in PATCH_LOCATIONS:
            PATCH_LOCATIONS.remove(patch_policy.name)
        if patch_policy.class_name:
            patch_manager.reverse_patches_by_owner(
                getattr(module, patch_policy.class_name)
            )

    patch_manager.reverse_patches_by_owner(module)


def _apply_v1_patches(module: ModuleType):
    module_policy = registry.get_policy_by_module(module.__name__)
    if module_policy is None:
        logger.debug("WARNING: No module policy found", module=module.__name__)
        return

    from contrast.agent import agent_state, patch_controller

    preinstrument = patch_controller.is_preinstrument_flag_set()

    for patch_policy in module_policy:
        if patch_policy.name in PATCH_LOCATIONS:
            continue

        # If the module has no policy nodes, or if none of the nodes are policy
        # patches, then there's nothing to do here.
        if not patch_policy.has_patches:
            continue

        # If nothing is on, there's nothing to do.
        if (
            not agent_state.module.protect_enabled
            and not agent_state.module.assess_enabled
            and not preinstrument
        ):
            continue

        # If only Protect is on and this isn't a protect patch, there's nothing to do.
        if (
            agent_state.module.protect_enabled
            and not agent_state.module.assess_enabled
            and not preinstrument
            and not patch_policy.is_protect_mode
        ):
            continue

        if patch_policy.class_name:
            patch_site = getattr(module, patch_policy.class_name, None)
            if patch_site is None:
                continue
        else:
            patch_site = module

        try:
            if (
                agent_state.module.protect_enabled or preinstrument
            ) and patch_policy.is_protect_mode:
                apply_protect_patch(patch_site, patch_policy)
        except Exception:
            logger.debug("Failed to apply protect patch for %s", patch_policy.name)

        try:
            if agent_state.module.assess_enabled or preinstrument:
                apply_assess_patch(patch_site, patch_policy)
        except Exception:
            logger.debug("Failed to apply assess patch for %s", patch_policy.name)

        PATCH_LOCATIONS.add(patch_policy.name)


@functools.cache
def _apply_v2_patches(module: ModuleType):
    from contrast.agent.policy import registry_v2

    patch_locations = {
        location
        for location in registry_v2.get_policy_locations()
        if location.module == module.__name__
    }
    if len(patch_locations) == 0:
        logger.debug("No v2 module policy found", module=module.__name__)
        return

    for location in patch_locations:
        patch_site = (
            module
            if location.class_name is None
            else getattr(module, location.class_name, None)
        )
        if patch_site is None:
            logger.debug(
                "Patch site not found", location=location, module=module.__name__
            )
            continue
        original_func = getattr(patch_site, location.method_name, None)
        if original_func is None:
            logger.debug(
                "Original function not found",
                method=location.method_name,
                module=module.__name__,
            )
            continue

        patch_manager.patch(
            patch_site,
            location.method_name,
            registry_v2.build_generic_contrast_wrapper(
                original_func, module_name=location.module
            ),
        )


def register_policy_patches(*, protect_mode: bool):
    """
    Use policy to register import hooks for each module that requires patches

    If protect_mode, patch only module patches with protect if trigger node has
    protect_mode: true.
    If not protect_mode, we will patch all module patches with assess.
    """
    from contrast.agent.policy import registry_v2

    modules_to_patch = set(registry.get_patch_policies(protect=protect_mode)) | {
        location.module for location in registry_v2.get_policy_locations()
    }

    for module_name in modules_to_patch:
        logger.debug("Registering import hook for %s", module_name)
        register_module_patcher(apply_module_patches, module_name)


def apply_patch_to_dynamic_property(class_to_patch, property_name, tags):
    """
    Take the property of a class we want to patch and:
        1. create a source node to store in policy
        2. patch the original property with our own code, including
            the policy instance with the new dynamic source.

    This means that the next time the cls.property is called,
    we will inject ourselves and run source policy.

    NOTE: adding the dynamic source to policy BEFORE patching is critical order,
    given that we have to patch with the policy instance that has this dynamic source.
    This could later be modified to not need this requirement.
    """
    module = class_to_patch.__module__
    class_name = class_to_patch.__name__

    patch_policy = registry.register_dynamic_source(
        module,
        class_name,
        property_name,
        tags,
        policy_patch=False,
    )

    orig_property = getattr(class_to_patch, property_name)

    def fset(cls_instance, value):
        # while good instinct would lead us to use setattr here instead of __dict__,
        # doing so does not work because we are in fact within a setter!
        cls_instance.__dict__[property_name] = value

    new_property = property(
        fget=build_assess_property_fget(orig_property, patch_policy),
        fset=fset,
        fdel=getattr(orig_property, "fdel", None),
    )

    patch_manager.patch(class_to_patch, property_name, new_property)

    return True
