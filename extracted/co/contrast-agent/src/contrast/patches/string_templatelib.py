# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Implements patches for the templatelib module
"""

from __future__ import annotations

import operator
import sys
from collections.abc import Iterable
from itertools import groupby

from contrast.agent.policy import patch_manager
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    register_module_patcher,
    unregister_module_patcher,
)
from contrast_vendor import structlog as logging
from contrast_vendor import wrapt

logger = logging.getLogger("contrast")


def propagate_to_template(args: Iterable) -> Iterable:
    """
    Given the arguments to Template.__init__, propagate tags from tracked strings into the
    Template instance being created.
    """
    args = [arg for arg in args if arg is not None]
    new_args = []
    for is_strs, group in groupby(args, lambda x: isinstance(x, str)):
        if is_strs:
            joined_str = ""
            for str_part in group:
                joined_str = operator.add(joined_str, str_part)
            new_args.append(joined_str)
        else:
            new_args.extend(group)

    return new_args


if sys.version_info[:2] < (3, 14):

    def build_template_hook(original_attr, patch_policy):
        return original_attr
else:

    class TemplateProxy(wrapt.ObjectProxy):
        def __call__(*args):
            def _unpack_self(self, *args):
                return self, args

            self, args = _unpack_self(*args)

            new_args = propagate_to_template(args)
            return self.__wrapped__(*new_args)

    def build_template_hook(original_attr, patch_policy):
        return TemplateProxy(original_attr)


def patch_string_module(string_module):
    if sys.version_info[:2] < (3, 14):
        return
    build_and_apply_patch(string_module.templatelib, "Template", build_template_hook)


def register_patches():
    register_module_patcher(patch_string_module, "string")


def reverse_patches():
    unregister_module_patcher("strings.templatelib")
    templatelib_module = sys.modules.get("strings.templatelib")
    if not templatelib_module:
        return

    patch_manager.reverse_patches_by_owner(templatelib_module)
