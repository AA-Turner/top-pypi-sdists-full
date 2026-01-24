# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import importlib
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
    temp_name = "__contrast_temp." + module.__name__
    spec = importlib.util.spec_from_file_location(temp_name, module.__file__)

    module = importlib.util.module_from_spec(spec)
    # Add the unrewritten module to sys.modules so that relative imports
    # can be resolved when exec'ing the rewritten module.
    sys.modules[temp_name] = module
    ContrastRewriteLoader(temp_name, module.__file__).exec_module(module)

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
            'Failed to rewrite functions in module "%s": module not loaded', module_name
        )
        return

    logger.debug("Applying rewriter policy to module: %s", module_name)

    rewritten_module = load_and_rewrite_module(module)
    sys.modules[rewritten_module.__name__] = rewritten_module

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
    if rewrite_pathlib and sys.version_info[:2] > (3, 10):
        rewrite_module_functions("pathlib")

    repatch_imported_modules()

    policy_rewriter_state.enabled = True


def reverse_rewrite_policy():
    for module in REWRITE_MODULES:
        reverse_module_patches_by_name(module)

    policy_rewriter_state.enabled = False
