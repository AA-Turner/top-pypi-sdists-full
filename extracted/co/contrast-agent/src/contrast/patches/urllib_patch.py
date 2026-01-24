# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast.agent.policy.applicator import (
    apply_module_patches,
    reverse_module_patches,
)
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    register_module_patcher,
    unregister_module_patcher,
    wrap_and_watermark,
)

import urllib.parse as urllib

MODULE_NAME = "urllib.parse"


def build_urlencode_patch(orig_func, _):
    def urlencode_patch(wrapped, _, args, kwargs):
        """
        Patch for urllib.urlencode / urllib.parse.urlencode.

        This is needed because of the unfortunate way urllib calls on
        `quote_via` as a kwarg.
        See https://github.com/python/cpython/blob/master/Lib/urllib/parse.py#L909

        Because of this behavior, the `quote_via` func is not our patched
        `quote_via` defined in policy.
        By patching `urlencode`, we intercept its call and instead of allowing
        it to use the default kwarg for `quote_via`, we pass our own
        patched `quote_via` in order to prevent false positive XSS findings.
        """
        # quote_plus MUST already be patched by policy in order
        # to pass in the patched func to urlencode
        kwargs.setdefault("quote_via", urllib.quote_plus)
        return wrapped(*args, **kwargs)

    return wrap_and_watermark(orig_func, urlencode_patch)


def patch_urllib(urllib_module):
    # We ask policy to go ahead and do all urllib patches here (even though policy
    # patches will happen later on) because we MUST have some urllib policy patches
    # already applied for these non-policy patches to work.
    # This would not be necessary if in _enable_patches policy patches were applied
    # first.
    apply_module_patches(urllib_module)

    build_and_apply_patch(urllib_module, "urlencode", build_urlencode_patch, force=True)


def register_patches():
    register_module_patcher(patch_urllib, MODULE_NAME)


def reverse_patches():
    unregister_module_patcher(MODULE_NAME)
    urllib_module = sys.modules.get(MODULE_NAME)
    if not urllib_module:  # pragma: no cover
        return

    reverse_module_patches(urllib_module)
