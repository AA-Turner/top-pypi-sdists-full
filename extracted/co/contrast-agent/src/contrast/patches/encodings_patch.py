# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import sys

from contrast.agent.assess.policy.patches import build_assess_method
from contrast.agent.policy import patch_manager, registry
from contrast.utils.patch_utils import (
    register_module_patcher,
    unregister_module_patcher,
)


CODEC_MODULES_TO_PATCH = [
    "encodings.ascii",
    "encodings.latin_1",
    "encodings.raw_unicode_escape",
    "encodings.unicode_escape",
    "encodings.unicode_internal",
]


def build_codec_patch(module, method_name):
    module_name = module.__name__

    orig_method = getattr(module.Codec, method_name)
    patch_policy = registry.get_policy_by_name(f"{module_name}.Codec.{method_name}")

    return build_assess_method(orig_method, patch_policy)


def patch_codec_module(module):
    patch_manager.patch(module.Codec, "encode", build_codec_patch(module, "encode"))
    patch_manager.patch(module.Codec, "decode", build_codec_patch(module, "decode"))

    import encodings

    # Clear the encodings cache so that our patches are seen
    encodings._cache.clear()


def register_patches():
    for module in CODEC_MODULES_TO_PATCH:
        register_module_patcher(patch_codec_module, module)


def reverse_patches():
    for name in CODEC_MODULES_TO_PATCH:
        unregister_module_patcher(name)
        module = sys.modules.get(name)
        if module is not None:
            patch_manager.reverse_patches_by_owner(module.Codec)
