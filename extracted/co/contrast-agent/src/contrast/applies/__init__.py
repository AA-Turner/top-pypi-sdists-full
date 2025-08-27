# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import contrast
from contrast.agent import scope
from contrast.agent.settings import Settings


def apply_rule(patch_policy, orig_func, args, kwargs):
    context = contrast.REQUEST_CONTEXT.get()

    if (
        context is not None
        and context.protect_enabled
        and not scope.in_contrast_scope()
    ):
        for node in patch_policy.trigger_nodes:
            rule_name = node.rule.name
            rule = Settings().protect_rules.get(rule_name)
            if not rule or not rule.enabled:
                continue

            for source in node.get_protect_sources(args, kwargs):
                rule.protect(patch_policy, source, args, kwargs)

    return orig_func(*args, **kwargs)
