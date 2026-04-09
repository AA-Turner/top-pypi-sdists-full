# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import importlib
import importlib.machinery
import importlib.util
import inspect
import sys
from types import FunctionType, ModuleType

from contrast.agent.policy import patch_manager
from contrast.agent.policy.patch_manager import reverse_module_patches_by_name
from contrast.utils.decorators import fail_quietly
from contrast.utils.namespace import Namespace
from contrast.utils.patch_utils import repatch_imported_modules
from contrast_rewriter import ContrastRewriteLoader
from contrast_vendor import structlog as logging

# NOTE: it feels like overkill to store this in the policy registry right now,
# but we can always change this later if necessary.
REWRITE_MODULES = [
    "posixpath",
    "urllib.parse",
    # Also pathlib, conditionally. See references.
]

MODULE_REWRITE_SKIP_NAMES = [
    "__all__",
    "__name__",
    "__package__",
    "__module__",
    "__spec__",
    "__name__",
    "__builtins__",
    "__dict__",
    "__file__",
]

logger = logging.getLogger("contrast")


class policy_rewriter_state(Namespace):
    enabled: bool = False


CONTRAST_TEMP_NAMESPACE = "__contrast_temp"


def load_and_rewrite_module(module: ModuleType) -> ModuleType:
    """
    Returns a rewritten version of the given module

    (Note about frozen modules:)

    Frozen modules are modules whose bytecode is built into the interpreter
    itself for performance reasons. All of the modules required at interpreter
    startup are frozen in newer versions of Python (i.e. >= 3.10+).

    Frozen modules do not have access to the source code of module members such
    as functions. This means that calls toinspect.getsource(<frozen-module-name>.<member-name>)
    will fail. Since we need the source in order to perform rewrites, we need a
    non-frozen version of the module. We can achieve this by loading the module
    again and returning the new module object.
    """
    module_name = module.__name__

    # 1. Create a pseudo namespace for the rewritten modules to live in. This allows programs to
    # "import __contrast_temp". Later at 2, this will allow "import __contrast_temp.MODULE_NAME"
    # to access the rewritten modules. It's unlikely that programs would do this directly, but
    # dynamically accessing the __module__ attribute of a rewritten function or class could lead
    # to a scenario where a program needs to access __contrast_temp. See PYT-4052 as an example.
    if CONTRAST_TEMP_NAMESPACE not in sys.modules:
        temp_pkg = ModuleType(CONTRAST_TEMP_NAMESPACE)
        # Mark the temporary module as a namespace package so that
        # imports like "__contrast_temp.MODULE_NAME" work with the
        # standard import machinery.
        temp_pkg.__path__ = []
        temp_pkg.__package__ = CONTRAST_TEMP_NAMESPACE
        temp_spec = importlib.machinery.ModuleSpec(
            name=CONTRAST_TEMP_NAMESPACE,
            loader=None,
            is_package=True,
        )
        temp_spec.submodule_search_locations = temp_pkg.__path__
        temp_pkg.__spec__ = temp_spec
        sys.modules[CONTRAST_TEMP_NAMESPACE] = temp_pkg

    temp_module_name = f"{CONTRAST_TEMP_NAMESPACE}.{module_name}"
    spec = importlib.util.spec_from_file_location(temp_module_name, module.__file__)

    module = importlib.util.module_from_spec(spec)
    # 2. Add the unrewritten module to the __contrast_temp namespace so that 'import __contrast_temp.MODULE_NAME'
    # succeeds. After the RewriteLoader exec's the module, future access will also receive rewritten members.
    top_level_module_name, _sep, *_rest = module_name.partition(".")
    top_level_module = sys.modules[top_level_module_name]
    sys.modules[CONTRAST_TEMP_NAMESPACE].__dict__[top_level_module_name] = (
        top_level_module
    )

    # 3. Add the unrewritten module to sys.modules so that relative imports
    # can be resolved when exec'ing the rewritten module.
    sys.modules[temp_module_name] = module
    ContrastRewriteLoader(temp_module_name, module.__file__).exec_module(module)

    return module


@fail_quietly("Failed rewrite and patch function")
def rewrite_and_patch_function(
    module: ModuleType,
    name: str,
    function: FunctionType,
    new_module: ModuleType,
):
    # Some functions may already be patched by other policy, in which case we do not
    # want to rewrite them
    if patch_manager.is_patched(function):
        logger.debug("Skipping rewrite of already patched function: %s", name)
        return

    new_func = getattr(new_module, name)
    if new_func is None:
        logger.debug("No new function for %s. Skipping patch", name)
        return

    patch_manager.patch(module, name, new_func)


@fail_quietly("Failed to rewrite functions for module")
def rewrite_module_functions(module_name: str):
    module = sys.modules.get(module_name, None)
    if module is None:
        logger.debug(
            'Skipping rewriter policy for module "%s": module not loaded', module_name
        )
        return

    logger.debug("Applying rewriter policy to module: %s", module_name)

    rewritten_module = load_and_rewrite_module(module)

    for name, member in inspect.getmembers(module):
        # If the unfrozen module doesn't have a function that is found in the
        # original module, it's probably the case that the function was added
        # by us (e.g. a function added by some other policy node).
        # (This check shouldn't really be necessary anymore)
        if not hasattr(rewritten_module, name):
            continue

        if name in MODULE_REWRITE_SKIP_NAMES:
            continue

        if patch_manager.is_patched(member):
            continue

        new_member = getattr(rewritten_module, name)
        if new_member is None:
            logger.debug("No new member for %s. Skipping patch", name)
            continue

        # This would apply to any member that was imported from another module
        if new_member is member:
            continue

        patch_manager.patch(module, name, new_member)


def apply_rewrite_policy(*, rewrite_pathlib: bool = True):
    """
    Applies "policy-based rewrites" to modules that require instrumentation but are
    loaded before we can apply the rewriter. This machinery is policy-based because it
    is generic and applied identically to a list of modules we have listed.

    The strategy here is to load a copy of each module (which applies our rewriter) and
    then replace any attributes from the original, un-rewritten module with the
    corresponding attributes from the copy.

    It is the caller's responsibility to check any relevant agent configuration. Calling
    this function will always apply policy-based rewrites.
    """
    if policy_rewriter_state.enabled:
        logger.debug("Policy-based rewrites are already enabled")
        return

    for module in REWRITE_MODULES:
        rewrite_module_functions(module)

    # Rewriting pathlib is problematic within the unit testing setting since
    # pytest relies heavily on pathlib and our patches wreak havoc. We enable
    # it by default but allow unit tests to disable it as necessary.
    if rewrite_pathlib:
        orig_path = getattr(sys.modules.get("pathlib", None), "Path", None)
        as_file = getattr(sys.modules.get("importlib.resources", None), "as_file", None)
        as_file_for_path = (
            as_file.dispatch(orig_path) if as_file and orig_path else None
        )

        rewrite_module_functions("pathlib")

        if as_file and as_file_for_path:
            # register the rewritten __contrast_temp.pathlib.Path to call
            # the original as_file dispatch for pathlib.Path (PYT-4028)
            import pathlib as rewritten_pathlib

            as_file.register(rewritten_pathlib.Path)(as_file_for_path)

    repatch_imported_modules()

    policy_rewriter_state.enabled = True


def reverse_rewrite_policy():
    for module in REWRITE_MODULES:
        reverse_module_patches_by_name(module)

    policy_rewriter_state.enabled = False
