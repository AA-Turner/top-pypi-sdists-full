# -*- coding: utf-8 -*-
# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

"""
The sitecustomize.py file is automatically loaded by Python during interpreter
initialization. Our runner script ensures that it is on the PYTHONPATH which is
sufficient to make sure it is loaded.

See https://docs.python.org/3/library/site.html for additional details
"""

### This is the very first line of code we control in the app's python process ###

# We want to minimize the amount of code we run before we register the rewriter,
# because modules imported during that time won't be fully rewritten or patched.
# We attempt to repatch imported modules, but there still could be gaps.

import os
import sys

MIN_SUPPORTED_VERSION = (3, 10)
MAX_SUPPORTED_VERSION = (3, 15)
# We need to check the version_info because certain installation tools bypass
# pip and setuptools, so the version check in setup.py is skipped. For example,
# the agent operator and the universal agent bundle the agent distribution and
# prepend them to PYTHONPATH directly.


def _log(msg):
    import contrast_rewriter

    contrast_rewriter.log_stderr(msg, logger_name="contrast-loader")


def _log_env(key):
    _log("{}: {}".format(key, os.environ.get(key, "<not set>")))


def _init_contrast():
    # this function is called at the module-level
    if not (MIN_SUPPORTED_VERSION <= sys.version_info[:2] <= MAX_SUPPORTED_VERSION):
        return
    import contrast_rewriter

    _log("Initializing Contrast Python Agent")
    _log_env("CONTRAST_INSTALLATION_TOOL")
    _log("Platform: {}".format(sys.platform))
    _log("Python Version: {}".format(sys.version))
    _log("Python Executable: {}".format(sys.executable))
    _log("Command: {}".format(getattr(sys, "orig_argv", sys.argv)))
    _log_env("PYTHONPATH")
    _log_env("CONTRAST__ASSESS__ENABLE")

    if contrast_rewriter.is_startup_profiler_enabled():
        contrast_rewriter.start_profiler()

    assess_enabled_env_var = os.environ.get("CONTRAST__ASSESS__ENABLE")
    skip_rewriter = False
    if assess_enabled_env_var is not None:
        try:  # noqa: SIM105
            skip_rewriter = (
                contrast_rewriter.str_to_bool(assess_enabled_env_var) is False
            )
        except ValueError:
            pass
    if skip_rewriter:
        _log("Skipping rewriter")
    else:
        _log("Registering rewriter")
        # NOTE: The rewriter must be applied prior to importing the agent itself. Do not
        # import any unnecessary modules before registering the rewriter.
        contrast_rewriter.register()
        _log("Completed rewriter registration")

    if sys.version_info[:2] >= (3, 14):
        from concurrent import interpreters

        if interpreters.get_current().id != interpreters.get_main().id:
            _log(
                "ERROR: Contrast Agent does not support loading in subinterpreters. "
                "Contrast will not run in this subinterpreter."
            )
            return

    import contrast
    from contrast_vendor import structlog as logging

    logger = logging.getLogger("contrast")
    logger.info("Python Agent version: {}".format(contrast.__version__))

    from contrast import loader  # noqa: E402
    from contrast.loader import instrumentation  # noqa: E402

    logger.info("Applying early instrumentation")
    instrumentation.apply_early_instrumentation()

    loader.SITECUSTOMIZE_LOADED = True

    if contrast_rewriter.is_startup_profiler_enabled():
        contrast_rewriter.stop_profiler("end_sitecustomize")
        contrast_rewriter.start_profiler()


_init_contrast()

### Attempt to import the next sitecustomize.py file ###

loader_dir = os.path.dirname(__file__)
if loader_dir not in sys.path:
    # loader_dir will always be in sys.path when this sitecustomize is
    # being called by the Python interpreter site startup machinery.
    # If it's missing, we're being imported by some other module at
    # runtime, after the site machinery has already run. In that case,
    # don't attempt to import the next sitecustomize module because
    # that's not what an uninstrumented Python process would do.
    pass
else:
    # Unhook this sitecustomize from the import machinery.
    loader_syspath_index = sys.path.index(loader_dir)
    del sys.path[loader_syspath_index]
    this_sitecustomize = sys.modules["sitecustomize"]
    del sys.modules["sitecustomize"]

    # Attempt to import the next sitecustomize module.
    try:
        import sitecustomize  # noqa: F401
    except ImportError:
        # Only replace sitecustomize if the import fails. Otherwise,
        # an instrumented runner might assume its sitecustomize is in
        # place and raise errors if our sitecustomize were imported
        # instead.
        sys.modules["sitecustomize"] = this_sitecustomize
        sys.path.insert(loader_syspath_index, loader_dir)

    # Only catch the ImportError so that we don't swallow exceptions raised
    # by a buggy third-party sitecustomize implementation.
