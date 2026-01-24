# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import _io
import os

from contrast import import_hook
from contrast.agent.assess.policy import string_propagation
from contrast.agent.policy import registry
from contrast.agent.policy.applicator import register_policy_patches
from contrast.agent.policy.rewriter import apply_rewrite_policy
from contrast.agent.settings import Settings
from contrast.extensions import c_ext
from contrast.patches import pure_python_string_patches
from contrast.patches import (
    register_assess_monkeypatches,
    register_common_monkeypatches,
)
from contrast.utils.configuration_utils import str_to_bool
from contrast.utils.namespace import Namespace
from contrast.utils.patch_utils import repatch_imported_modules
from contrast_rewriter import register as register_rewriter
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


class module(Namespace):
    assess_patches_enabled: bool = False


def is_preinstrument_flag_set() -> bool:
    """
    Special flag signaling that the agent should apply all instrumentation on startup
    regardless of which modes are enabled. This allows any mode to be enabled later
    without requiring an application restart.
    """
    try:
        return str_to_bool(os.environ.get("CONTRAST_PREINSTRUMENT"))
    except ValueError:
        return False


def _enable_pure_python_string_patches(string_types):
    """
    Enable string propagation hooks for individual string type methods

    This method uses policy to determine all of the string methods that need to be
    patched. Patches are applied in pure Python.
    """
    for strtype in string_types:
        for node in registry.get_string_method_nodes():
            method_name = node.method_name

            if method_name.lower() in ["cast", "concat"]:
                # these are applied directly in the C extension only
                continue

            real_method_name = (
                "format_map" if method_name == "formatmap" else method_name
            )

            if not hasattr(strtype, real_method_name):
                continue

            pure_python_string_patches.patch_strtype_method(strtype, real_method_name)
            logger.debug(
                "Applied pure Python patch for %s.%s", strtype.__name__, method_name
            )


def _enable_pure_python_stream_patches():
    pure_python_string_patches.patch_stream_method(_io._IOBase, "readline")
    pure_python_string_patches.patch_stream_method(_io._IOBase, "readlines")
    pure_python_string_patches.patch_stream_method(_io.BytesIO, "read")
    pure_python_string_patches.patch_stream_method(_io.BytesIO, "readline")
    pure_python_string_patches.patch_stream_method(_io.BytesIO, "readlines")
    pure_python_string_patches.patch_stream_method(_io.BytesIO, "read1")
    pure_python_string_patches.patch_stream_method(_io.StringIO, "read")
    pure_python_string_patches.patch_stream_method(_io.StringIO, "readline")


def enable_assess_patches():
    """
    Enables string patches.

    Has no effect if these patches are already enabled.
    """
    if module.assess_patches_enabled:
        return
    # NOTE: String propagator functions *must* be built before the extension
    # is initialized.
    string_propagation.build_string_propagator_functions()
    c_ext.initialize()
    pure_python_string_patches.enable_str_properties()
    c_ext.enable_c_patches()
    _enable_pure_python_string_patches([str, bytes, bytearray])
    _enable_pure_python_stream_patches()

    module.assess_patches_enabled = True


def disable_assess_patches():
    """
    Disables extension hooks and other string patches.

    Has no effect if these patches are not already enabled.

    This does not disable "pure python" strtype patches applied with set_attr_on_type.
    """
    if not module.assess_patches_enabled:
        return

    c_ext.disable_c_patches()

    module.assess_patches_enabled = False


def _enable_protect_patches():
    register_common_monkeypatches()

    logger.debug("adding protect policy")
    register_policy_patches(protect_mode=True)

    # This has no effect if the patches are not enabled
    disable_assess_patches()


def _enable_assess_patches():
    enable_assess_patches()

    # Policy-based rewrites need to be applied prior to any policy patches.
    # Policy patches can be layered on top of rewritten functions. So that
    # means we need to make sure that the "original" function called by the
    # policy patch is the *rewritten* one.
    # Pathlib rewrites must not be applied here. They are only stable when applied by
    # the runner. The exact reason for this is unknown, but it's related to repatching.
    # If this causes noticeable issues, use the runner. This will eventually be
    # mandatory anyway, and policy-based rewrites will be removed from here entirely.
    apply_rewrite_policy(rewrite_pathlib=False)

    logger.debug("enabled assess string patches")
    register_common_monkeypatches()
    register_assess_monkeypatches()

    logger.debug("adding assess policy")
    register_policy_patches(protect_mode=False)

    # This is included as a fallback so that we continue to support the case
    # where the runner is not used. If the rewriter has already been enabled by
    # the runner, this has no effect (other than to log a message).
    register_rewriter()


def enable_patches(*, preinstrument: bool):
    settings = Settings()

    if settings.is_analyze_libs_enabled() or preinstrument:
        import_hook.register_path_finder()

    from contrast.agent import agent_state

    if agent_state.module.protect_enabled or preinstrument:
        _enable_protect_patches()
    if agent_state.module.assess_enabled or preinstrument:
        _enable_assess_patches()
        import_hook.register_path_finder()
    if agent_state.module.observe_enabled or preinstrument:
        register_policy_patches(protect_mode=False)
        # register import hook to deadzone file-open-create action
        # reports for source files.
        import_hook.register_path_finder()

    logger.debug("revisiting imported modules to apply patches")
    repatch_imported_modules()
