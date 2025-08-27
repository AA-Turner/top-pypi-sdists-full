# Copyright © 2025 Contrast Security, Inc.
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

import sys
import os

MIN_SUPPORTED_VERSION = (3, 9)
MAX_SUPPORTED_VERSION = (3, 14) if os.environ.get("CONTRAST_ALLOW_PY314") else (3, 13)
# We need to check the version_info because certain installation tools bypass
# pip and setuptools, so the version check in setup.py is skipped. For example,
# the agent operator and the universal agent bundle the agent distribution and
# prepend them to PYTHONPATH directly.
if MIN_SUPPORTED_VERSION <= sys.version_info[:2] <= MAX_SUPPORTED_VERSION:
    import contrast_rewriter

    # NOTE: This must be applied prior to importing the agent itself. Do not import any
    # other modules before registering the rewriter.
    contrast_rewriter.register()

    from contrast import loader  # noqa: E402
    from contrast.loader import instrumentation  # noqa: E402

    instrumentation.apply_early_instrumentation()

    loader.SITECUSTOMIZE_LOADED = True


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
