# ruff: noqa

import warnings
warnings.warn("""
################################
###       ! WARNING !        ###
###    DEPRECATION NOTICE    ###
################################

You have imported `openapi_client` package provided by VESSL SDK/CLI.

This package will be DEPRECATED in future releases,
and programs relying on it will become broken.

We strongly recommend that you find and remove imports to `openapi_client`,
and instead use VESSL SDK functions for such purpose.
This package is for internal use; please do not use this directly.
""")
del warnings

from vessl.openapi_client import *