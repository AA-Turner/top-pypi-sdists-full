# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from collections import OrderedDict
import functools
import inspect
import sys
from types import ModuleType
from typing import Callable

from contrast.utils.decorators import fail_quietly
from contrast.utils.libraries import get_module_distribution_metadata
from contrast.utils.stdlib_modules import is_stdlib_module
from contrast_vendor import wrapt

from contrast.agent.policy import patch_manager
from contrast.utils.object_utils import get_name

from contrast_vendor.wrapt import function_wrapper
from contrast_vendor import structlog as logging

from contrast.utils.string_utils import ensure_string
from contrast_vendor.wrapt import importer
from contrast_vendor.wrapt.importer import register_post_import_hook
import contextlib

logger = logging.getLogger("contrast")


def add_watermark(func):
    """
    Adds a "secret" attribute to patched function for debugging purposes.

    Do not rely on the existence of this attribute in agent source code.
    """
    with contextlib.suppress(Exception):
        func.__contrast__ = True
    return func


def wrap_and_watermark(orig_func, wrapper):
    # NOTE: adding a watermark here doesn't make a ton of sense anymore since
    # 1. The function wrapper always has a __wrapped__ attribute, which is a good watermark itself
    # 2. We can't apply the watermark to the wrapped function because in that
    # case it actually gets applied to the underlying object (which we don't want).
    return function_wrapper(add_watermark(wrapper))(orig_func)


def pack_self(instance: object | None, args: tuple) -> tuple:
    """Combines the instance and args into a single tuple. If instance is None, returns args."""
    return args if instance is None else (instance,) + args


def get_arg(args, kwargs, idx, kw=None, default=None):
    if kw and kw in kwargs:
        return kwargs[kw]

    if len(args) <= idx:
        return default

    return args[idx]


def set_arg(
    value: object, args, kwargs, idx, kw=None
) -> tuple[tuple, dict[str, object]]:
    """
    Set the value in the args or kwargs at the given index or keyword.

    If a value is not present in args or kwargs, it will be added as a kwarg.
    """
    if (kw and kw in kwargs) or idx >= len(args):
        kwargs[kw] = value
    else:
        mut_args = list(args)
        mut_args[idx] = value
        args = tuple(mut_args)
    return args, kwargs


def build_and_apply_patch(
    owner,
    attr_name,
    patch_builder,
    builder_args=None,
    owner_name=None,
    force=False,
):
    """
    Builds new patch using given builder and applies it to specified patch location

    :param owner: Module or class where patch will be applied
    :param loc_name: Fully specified name of module or class where patch will apply
    :param attr_name: Name of the method that is being patched/replaced
    :param patch_builder: Callback function used to build new patch
    :param builder_args: A tuple of positional args to be passed to `patch_builder`

    The `patch_builder` function must take at least two arguments:
        1. A pointer to the original function
        2. The patch policy associated with this patch (may be `None`)
    The `patch_builder` may accept additional positional arguments that are passed to
    this function as a tuple via `builder_args`.

    The `patch_builder` function must return a function that matches the argument
    signature of the original function. The returned function must call the original
    function and return the result.

    Not all patches will have policy. Some patch locations are used solely to apply
    proxies or do library analysis, and so no policy exists for those locations.
    Callers can indicate this by passing "" or None for `loc_name`, in which case no
    patch policy will be retrieved.
    """
    original_func = getattr(owner, attr_name)

    # In most cases, we don't want to patch a function that has already been patched.
    # Sometimes we do, though, so we have a `force` flag to allow it.
    # An examples of when we might want to force a patch is applying automatic
    # CommonMiddlewarePatch with route coverage patches.
    if patch_manager.is_patched(original_func) and not force:
        return

    from contrast.agent.policy import registry

    loc_name = owner_name if owner_name is not None else get_name(owner)

    patch_policy = (
        registry.get_policy_by_name(f"{loc_name}.{attr_name}") if loc_name else None
    )

    patch = patch_builder(original_func, patch_policy, *(builder_args or ()))

    patch_manager.patch(owner, attr_name, patch)

    func = add_watermark(patch_manager.as_func(getattr(owner, attr_name)))
    if hasattr(func, "__name__") and not isinstance(func, wrapt.FunctionWrapper):
        func.__name__ = ensure_string(attr_name)


THIRD_PARTY_SUPPORTED_VERSIONS = {
    "aiohttp": ((3, 7), (3, 10)),
    "aiohttp_session": ((2, 0), (2, 12)),
    "beaker": ((1, 0), (1, 13)),
    "bottle": ((0, 13), (0, 13)),
    "bottle_session": ((1, 0), (1, 0)),
    "cgi": ((2, 6), (2, 6)),
    "Crypto": ((3,), (3,)),  # pycryptodome
    "Cryptodome": ((3,), (3,)),  # pycryptodome
    "django": (
        (2, 2),
        (5, 2),
    ),  # official Django minimum support is 3.2, but the official DRF minimum version uses Django 2.2
    "enumfields": ((2, 0), (2, 1)),  # django-enumfields
    "falcon": ((3, 0), (4, 0)),
    "falcon_multipart": ((0, 1), (0, 2)),
    "fastapi": ((0, 71), (0, 116)),
    "flask": ((1, 1), (3, 1)),
    "genshi": ((0, 7), (0, 7)),
    "graphene": ((3, 4), (3, 4)),
    "httpx": ((0,), (0,)),
    "jinja2": ((2, 10), (3, 1)),  # min version required by our min version of flask
    "loguru": ((0, 7), (0, 7)),
    "lxml": ((4, 1), (5, 4)),
    "markupsafe": ((1, 0), (2, 1)),
    "mod_wsgi": ((4, 1), (5, 0)),
    "mysql": ((8, 0), (9, 4)),  # mysql-connector-python
    "openai": ((0, 27), (0, 28)),
    "pymysql": ((1, 0), (1, 1)),
    "psycopg2": ((2, 0), (2, 9)),
    "pymongo": ((4, 0), (4, 8)),
    "pyramid": ((1, 10), (2, 0)),
    "_pytest": (
        (0,),
        (100,),
    ),  # this is only used for our own unit tests, so we can make it broad.
    "quart": ((0, 15), (0, 20)),
    "requests": ((2, 4), (2, 32)),
    "rest_framework": ((3, 12), (3, 16)),  # drf
    "simplejson": ((3, 17), (3, 20)),
    "sqlalchemy": ((1,), (2,)),
    "starlette": (
        (0, 17),
        (0, 47),
    ),  # fastapi==0.71.0 requires starlette==0.17.1, fastapi==0.116.1 requires starlette<0.48.0
    "starlette_authlib": ((0, 1), (0, 3)),
    "urllib3": ((1, 25), (2, 3)),
    "webob": ((1, 8), (1, 9)),
    "werkzeug": ((1, 0), (3, 1)),  # flask==1.1.* resolved to Werkzeug==1.0.1
    "yaml": ((5, 1), (6, 0)),  # PyYAML
}

ModulePatcher = Callable[[ModuleType], None]


def register_module_patcher(patcher: ModulePatcher, module_name: str):
    """
    Register a patcher that will be called with the module object when the named module is imported.

    If the named module has already been imported, the patcher is called immediately.
    """
    is_contrast_module = module_name.startswith(("contrast.", "contrast_vendor."))
    if (
        not is_stdlib_module(module_name)
        and not is_contrast_module
        and not is_versioned_patch(patcher)
    ):
        top_level_module = module_name.split(".")[0]
        if constraint := THIRD_PARTY_SUPPORTED_VERSIONS.get(top_level_module):
            patcher = versioned_patch(*constraint)(patcher)
        else:
            raise ValueError(
                f"Patch for non-stdlib module {module_name} must have a version_constraint"
            )

    register_post_import_hook(
        patcher,
        module_name,
    )


def unregister_module_patcher(module_name: str):
    """
    Unregister a patcher that was registered with `register_module_patcher`.
    """
    with importer._post_import_hooks_lock:
        importer._post_import_hooks.pop(module_name, None)


def is_versioned_patch(patch: object) -> bool:
    return hasattr(patch, "__version_constraint__")


def versioned_patch(
    min: tuple | None = None, max: tuple | None = None
) -> Callable[[ModulePatcher], ModulePatcher]:
    """
    Decorator to restrict patch application to a specific version range.
    """
    if min is None and max is None:
        raise ValueError("Version range must be specified")

    if min and max and len(min) != len(max):
        raise ValueError("Version ranges must be the same length")

    def _versioned_patch_builder(patcher: ModulePatcher):
        @fail_quietly("Failed to apply versioned patch")
        def _versioned_patch(module: ModuleType):
            if dist_meta := get_module_distribution_metadata(module):
                version = dist_meta["Version"]
                version_info = tuple(int(v) for v in version.split(".")[:3])
                if min and version_info[: len(min)] < min:
                    # version is too low
                    return
                if max and version_info[: len(max)] > max:
                    # version is too high
                    return
                # version is just right
                patcher(module)
            else:
                raise ValueError(f"Failed to get distribution metadata for {module}")

        _versioned_patch.__version_constraint__ = (min, max)
        return _versioned_patch

    return _versioned_patch_builder


def get_loaded_modules(use_for_patching=False):
    """
    Retrieves and filters all loaded modules

    The parameter `use_for_patching` indicates that this function is being
    called to enable patching. In this case the modules are sorted to
    provide deterministic behavior, and .so modules are filtered out.
    Without `use_for_patching`, a simple, unsorted dict is returned.

    NOTE: This method gets called multiple times during the course of agent
    initialization. Ideally it would be called only once for PERF optimization,
    but because sys.modules is global to all threads, we can't guarantee its contents
    will be the same and that a race condition won't happen which would add modules
    across different threads.

    :return: dict of name and module as value
    """
    if not use_for_patching:
        # Have to make a copy of sys.modules in order to avoid RuntimeError: dictionary changed size during iteration
        return {k: v for k, v in dict(sys.modules).items() if inspect.ismodule(v)}

    filtered = OrderedDict()
    filtered.update(
        {
            name: module
            for name, module in sorted(sys.modules.items())
            if inspect.ismodule(module) and not is_so_module(module)
        }
    )

    return filtered


def is_so_module(module):
    """
    Return True if module is an .so file, such as
    ".../readline.cpython-38-darwin.so"

    :param module: python module object
    :return: bool
    """
    if not hasattr(module, "__file__") or module.__file__ is None:
        return False

    return module.__file__.endswith(".so")


def is_patchable(obj):
    if inspect.ismodule(obj):
        return False
    if inspect.isclass(obj):
        return True
    if type(obj) is functools.partial:
        return True

    # cython methods look like unpatchable builtins, but they can be patched normally
    # an example of this is lxml.etree.fromstring
    # for additional info, see https://groups.google.com/forum/#!topic/cython-users/v5dXFOu-DNc
    is_unpatchable_builtin_method = inspect.ismethoddescriptor(
        obj
    ) and not obj.__class__.__name__.startswith("cython")

    return inspect.isroutine(obj) and not is_unpatchable_builtin_method


@fail_quietly("Unable to repatch single module")
def repatch_module(module):
    """Repatch a single module. See docstring for repatch_imported_modules"""

    module_attrs = list(vars(module).items())

    for attr_name, attr in module_attrs:
        try:
            if not is_patchable(attr):
                continue
        except Exception as e:
            if (
                module.__name__.startswith("django")
                and type(e).__name__ == "ImproperlyConfigured"
            ):
                # Django gives ImproperlyConfigured if present in the env but unused.
                # This is not an issue, but can lead to noisy logging.
                continue
            logger.debug(
                "exception occurred while checking whether to patch %s in %s",
                attr_name,
                module.__name__,
                exc_info=e,
            )
            continue
        if type(attr) is functools.partial and (
            orig_patch := patch_manager.get_patch(attr.func)
        ):
            patch = functools.partial(orig_patch, *attr.args, **attr.keywords)
        else:
            patch = patch_manager.get_outer_patch(patch_manager.as_func(attr))

        if patch:
            logger.debug("applying repatch to %s in %s", attr_name, module.__name__)
            patch_manager.patch(module, attr_name, patch)


@fail_quietly("Unable to patch previously imported modules")
def repatch_imported_modules():
    """
    Applies patches to modules that were already imported prior to agent startup

    Here's the problem: our patches don't get applied until after our
    middleware class is initialized. At this point it's likely that most (or
    all) application modules will have already been imported.

    If we patch the function `foo.bar.baz`, and an application module that was
    loaded prior to our patches imports it as `from foo.bar import baz`, then
    our patch will have no effect within that application module. This is
    because the application module has a reference to the *original* function,
    and that reference remains unchanged even after we apply a patch to the
    `foo.bar` module.

    On the other hand, if the application imports it as `from foo import bar`
    and uses it as `bar.baz()`, then our patches will work just fine. In this
    case, the application module has a reference to the *module itself*, which
    is where we apply our patch. This means that when the application calls
    `bar.baz()`, it will be calling the updated (patched) function.

    Incidentally, if the application imports as `from foo.bar import baz`, but
    this module is not loaded until *after* our patches have been applied, our
    patch will be effective. However, we have no control over the order of
    imports in an application.

    This function is designed to remedy the former case in order to make sure
    that our patches are effective regardless of how they are imported or the
    order in which they are imported by the application.

    Prior to calling this function, we make a record of every function that
    gets patched. After all patches are applied, this function iterates
    through all imported modules, which includes all modules that may have been
    imported before our patches were applied. We look for any instances of the
    original functions that need to be patched, and we replace them with the
    patches in those modules.
    """
    for module in get_loaded_modules(use_for_patching=True).values():
        repatch_module(module)
