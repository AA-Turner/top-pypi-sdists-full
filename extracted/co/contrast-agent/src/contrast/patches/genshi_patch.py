# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Instrumentation for genshi globals function. Essentially what happens here is when
genshi calls the builtin eval function to eval the template code (and perform var lookup)
a custom mechanism is used in the genshi eval.py file. As a result we needed to patch
globals in order to inject our contrast__operator for modulo string operations.
"""

from contrast.utils.patch_utils import (
    build_and_apply_patch,
    wrap_and_watermark,
    register_module_patcher,
)
from contrast_rewriter import PropagationRewriter, add_dependency_to_globals


GENSHI_TEMPALTE_ENGINE_EVAL_MODULE = "genshi.template.eval"


def build_genshi_eval_globals_patch(orig_func, _, rule_applicator):
    del rule_applicator

    def genshi_eval_globals_patch(wrapped, instance, args, kwargs):
        if len(args) > 0 and isinstance(args[0], dict):
            for mod in PropagationRewriter.all_possible_injected_modules:
                add_dependency_to_globals(args[0], mod)

        return orig_func(args)

    return wrap_and_watermark(orig_func, genshi_eval_globals_patch)


def patch_genshi_globals(genshi_eval_module):
    build_and_apply_patch(
        genshi_eval_module.LookupBase,
        "globals",
        build_genshi_eval_globals_patch,
        (None,),
    )


def register_patches():
    register_module_patcher(patch_genshi_globals, GENSHI_TEMPALTE_ENGINE_EVAL_MODULE)
