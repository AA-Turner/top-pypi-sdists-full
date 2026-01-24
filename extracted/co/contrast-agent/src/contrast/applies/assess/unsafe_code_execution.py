# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy import registry
from contrast.agent.assess.policy import trigger_policy
from contrast.utils.decorators import fail_quietly


@fail_quietly("Error running unsafe code execution assess rule")
def apply_rule(module_name, method_name, result, args, kwargs):
    trigger_rule = registry.get_triggers_by_rule("unsafe-code-execution")

    trigger_nodes = trigger_rule.find_trigger_nodes(module_name, method_name)

    trigger_policy.apply(trigger_rule, trigger_nodes, result, args, kwargs)
