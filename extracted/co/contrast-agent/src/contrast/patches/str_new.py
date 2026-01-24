# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast.agent import scope
from contrast.agent.assess.policy import string_propagation
from contrast.agent.policy import patch_manager
from contrast.extensions import c_ext
from contrast.utils.decorators import fail_quietly
from contrast.utils.namespace import Namespace
from contrast.utils.object_utils import find_subclasses
from contrast.utils.patch_utils import build_and_apply_patch


class module(Namespace):
    patched_classes = []


def check_or_enter_scope(func):
    def wrapper(*args, **kwargs):
        if scope.in_contrast_or_propagation_scope():
            return
        with scope.contrast_scope(), scope.propagation_scope():
            func(*args, **kwargs)
            return

    return wrapper


@check_or_enter_scope
@fail_quietly("Failed to propagate string subclass __new__")
def propagate_str_cast(result, args, kwargs):
    string_propagation.propagate_unicode_cast(result, args[0], result, args[1:], kwargs)


@check_or_enter_scope
@fail_quietly("Failed to propagate bytes subclass __new__")
def propagate_bytes_cast(result, args, kwargs):
    string_propagation.propagate_bytes_cast(result, args[0], result, args[1:], kwargs)


@check_or_enter_scope
@fail_quietly("Failed to propagate bytearray subclass __init__")
def propagate_bytearray_init(instance, args, kwargs):
    """
    To make use of our generalized bytearray cast propagation machinery, we need to call
    `propagate_bytearray_cast` as though this were a __new__ patch. The calling
    semantics of __new__ differ from __init__, so we shuffle some things around
    accordingly.
    """
    target = instance
    result = instance
    self_obj = None
    string_propagation.propagate_bytearray_cast(target, result, self_obj, args, kwargs)


def build_cast_patch(orig_func, patch_policy, propagation_func):
    del patch_policy

    def __new__(*args, **kwargs):
        result = orig_func(*args, **kwargs)
        propagation_func(result, args, kwargs)
        return result

    # NOTE: builtin methods can't be wrapped
    return __new__


def build_bytearray_init_patch(orig_func, patch_policy):
    del patch_policy

    def __init__(self, *args, **kwargs) -> None:
        result = orig_func(self, *args, **kwargs)
        propagate_bytearray_init(self, args, kwargs)
        return result

    return __init__


def _is_immutable(cls) -> bool:
    """
    We currently don't have machinery for patching __init__ or __new__ on immutable
    types. This appears to be sufficiently rare and is not currently an issue.
    """
    flags = getattr(cls, "__flags__", None)
    if flags is None:
        return False

    if sys.version_info >= (3, 10):
        return bool(flags & c_ext.Py_TPFLAGS_IMMUTABLETYPE)
    return not (flags & c_ext.Py_TPFLAGS_HEAPTYPE)


@fail_quietly("Failed to apply patches for strtype subclasses")
def register_patches():
    """
    Applies patches to known subclasses of str, bytes, and bytearray

    Problem statement: the cast/new hook for subclasses of strtypes does not
    always work. This seems to be an issue with timing: subclasses that
    are defined *after* our extension hooks are applied do not appear to have
    a problem.

    However, even with the runner, our instrumentation is not necessarily going
    to be early enough to affect *all* subclasses that are defined.

    The solution is to use __subclasses__() to find any subclasses of strtypes
    that may already be defined at this point in time. We then explicitly apply
    propagation patches to the __new__ (or __init__) methods of these classes.
    """
    for cls in find_subclasses(str):
        if _is_immutable(cls):
            continue
        build_and_apply_patch(
            cls,
            "__new__",
            build_cast_patch,
            builder_args=(propagate_str_cast,),
        )
        module.patched_classes.append(cls)

    for cls in find_subclasses(bytes):
        if _is_immutable(cls):
            continue
        build_and_apply_patch(
            cls,
            "__new__",
            build_cast_patch,
            builder_args=(propagate_bytes_cast,),
        )
        module.patched_classes.append(cls)

    for cls in find_subclasses(bytearray):
        if _is_immutable(cls):
            continue
        build_and_apply_patch(
            cls,
            "__init__",
            build_bytearray_init_patch,
        )
        module.patched_classes.append(cls)


def reverse_patches():
    for cls in module.patched_classes:
        patch_manager.reverse_patches_by_owner(cls)

    module.patched_classes = []
