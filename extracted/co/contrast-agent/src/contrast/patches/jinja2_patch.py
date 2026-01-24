# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys
from contrast.utils.decorators import fail_quietly
from contrast.utils.object_utils import get_name
from contrast.utils.patch_utils import (
    register_module_patcher,
    unregister_module_patcher,
)

original_concat_fns = {}


@fail_quietly()
def _patch_concat_fn(owner):
    """
    This is essentially a custom repatch. Jinja2 has several reexports of a `concat`
    function, which is set to `"".join`. If any module containing this function is
    loaded before our string patches are applied, we miss the patch on this attribute.
    Normally, repatching solves this problem; however repatching here doesn't work for
    multiple reasons:
    - `"".join` is already bound. We don't currently have machinery for repatching bound
      functions.
    - Repatching only covers module-level attributes, but in some instances, this is a
      class attribute

    The simplest solution is to overwrite these references with `"".join` again, after
    string patches have been applied.

    There are many reexports / aliases for `concat`, and these change across different
    versions of Jinja2. We currently only have fixes for those that appear to be
    critical for dataflow, but it's not impossible that we'll have to add more in the
    future.
    """
    if (original_concat := getattr(owner, "concat", None)) is None:
        return

    assert hasattr("".join, "__wrapped__"), (
        "string patches must be applied before jinja concat patches"
    )
    owner_name = get_name(owner)
    assert owner_name not in original_concat_fns
    if not (original_concat.__self__ == "" and original_concat.__name__ == "join"):
        raise RuntimeError(
            f"Unexpected value for {owner_name}.concat - skipping patch ({original_concat})"
        )

    owner.concat = "".join
    original_concat_fns[owner_name] = original_concat


def _reverse_patch_concat_fn(owner):
    if not hasattr(owner, "concat"):
        return

    owner_name = get_name(owner)
    original_concat = original_concat_fns.pop(owner_name, None)
    assert original_concat is not None
    owner.concat = original_concat


def patch_jinja2_environment(jinja2_environment_module):
    _patch_concat_fn(jinja2_environment_module)
    _patch_concat_fn(jinja2_environment_module.Environment)


def patch_jinja2_utils(jinja2_utils_module):
    _patch_concat_fn(jinja2_utils_module)


JINJA2_ENVIRONMENT_MODULE_NAME = "jinja2.environment"
JINJA2_UTILS_MODULE_NAME = "jinja2.utils"


def register_patches():
    register_module_patcher(patch_jinja2_environment, JINJA2_ENVIRONMENT_MODULE_NAME)
    register_module_patcher(patch_jinja2_utils, JINJA2_UTILS_MODULE_NAME)


def reverse_patches():
    unregister_module_patcher(JINJA2_ENVIRONMENT_MODULE_NAME)
    unregister_module_patcher(JINJA2_UTILS_MODULE_NAME)
    if (
        jinja2_environment_module := sys.modules.get(JINJA2_ENVIRONMENT_MODULE_NAME)
    ) is not None:
        _reverse_patch_concat_fn(jinja2_environment_module)
        _reverse_patch_concat_fn(jinja2_environment_module.Environment)
    if (jinja2_utils_module := sys.modules.get(JINJA2_UTILS_MODULE_NAME)) is not None:
        _reverse_patch_concat_fn(jinja2_utils_module)
