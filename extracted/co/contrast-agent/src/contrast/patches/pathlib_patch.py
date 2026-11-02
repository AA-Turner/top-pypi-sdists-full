# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import builtins
import inspect
import io
import os
import sys

from contrast.agent.assess.utils import get_properties
from contrast.agent.policy import patch_manager
from contrast.agent.policy.applicator import (
    apply_module_patches,
    reverse_module_patches,
)
from contrast.agent.scope import pop_contrast_scope
from contrast.extensions import smart_setattr
from contrast.utils.decorators import fail_quietly
from contrast.utils.patch_utils import (
    register_module_patcher,
    repatch_module,
    unregister_module_patcher,
)


def property_getter(self):
    """This property makes pathlib.Path instances look like tracked strings"""
    # Getting the string representation could cause propagation to occur
    with pop_contrast_scope():
        string = str(self)

    return get_properties(string)


def create_adjusted_patch(patch):
    def adjusted_patch(path, *args, **kwargs):
        # We cast the path to str only for compatiblity with PY35. In all later
        # versions of Python, the underlying system functions accept pathlib.Path
        # objects as parameters, and so the cast is redundant. Strictly speaking, this
        # cast means that we don't need the cs__property attribute for any cases, but
        # it is good to have for future-proofing.
        return patch(str(path), *args, **kwargs)

    return staticmethod(adjusted_patch)


def is_wrapped_staticmethod(obj):
    return isinstance(obj, staticmethod) and hasattr(obj.__func__, "__wrapped__")


@fail_quietly("Failed to apply pathlib patches")
def patch_pathlib(pathlib_module):
    """
    Apply patches to the pathlib module

    We abuse the patch manager here to actually repatch a _class_.  This is necessary
    because pathlib stores references to a bunch of os module functions within an
    accessor class. Since pathlib is part of the standard library, this happens
    before our patching machinery is applied, which means the accessor retains
    references to the _original_ functions, and not our patched versions. We can't
    simply run repatch_module on pathlib itself because the references are in the
    class definition and not at module level. But if we explicitly repatch the
    _class_, everything works out just fine.

    Currently we would potentially miss cases where a custom accessor class was used
    (assuming the custom accessor was also defined before our patches applied). In
    theory, we could handle this by repatching the given accessor at the time each
    pathlib.Path is instantiated. However, given the fact that this functionality isn't
    even documented, I don't think it's worth pursuing right now.

    """
    # In order for pathlib patches to work, the os and io patches *must* be applied first
    # The best way to ensure that this occurs in the right order is by applying them
    # explicitly here before doing anything else.
    apply_module_patches(builtins)
    apply_module_patches(io)
    # Make sure builtin patches are applied to io module
    repatch_module(io)

    apply_module_patches(os)

    repatch_module(pathlib_module)

    # Using this property enables pathlib.Path instances to look like tracked strings
    # for the purposes of triggering vulnerabilities.
    pathprop = property(fget=property_getter)
    smart_setattr(pathlib_module.Path, "cs__properties", pathprop)

    # Overly-cautious safety check
    accessor_cls = getattr(pathlib_module, "_NormalAccessor", None)
    if accessor_cls is not None:
        for attr_name, attr in accessor_cls.__dict__.items():
            if not inspect.isroutine(attr):
                continue

            patch = patch_manager.get_patch(patch_manager.as_func(attr))

            if patch is None:
                continue

            # This does an end-run around the patch manager, but since it's a very
            # special case, we shouldn't be too concerned about reverse patching.
            smart_setattr(accessor_cls, attr_name, create_adjusted_patch(patch))

    # This is probably not necessary in most real-world environments but it
    # ensures that our instrumented `join` method is used in cases where the
    # flavours are initialized prior to our patch application.
    for name in ["_posix_flavour", "_windows_flavour"]:
        flavour = getattr(pathlib_module, name, None)
        if flavour is not None:
            smart_setattr(flavour, "join", flavour.sep.join)


def register_patches():
    register_module_patcher(patch_pathlib, "pathlib")


def reverse_patches():
    reverse_module_patches(os)
    reverse_module_patches(io)
    reverse_module_patches(builtins)

    unregister_module_patcher("pathlib")
    pathlib_module = sys.modules.get("pathlib")
    if not pathlib_module:
        return

    if hasattr(pathlib_module, "_NormalAccessor"):
        patch_manager.reverse_patches_by_owner(pathlib_module._NormalAccessor)

    delattr(pathlib_module.Path, "cs__properties")
