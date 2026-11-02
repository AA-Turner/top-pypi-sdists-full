# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.policy.policy_node import PolicyNode


class DeadZoneNode(PolicyNode):
    def __init__(
        self,
        module,
        class_name,
        method_name,
        instance_method=True,
        config_option=None,
        policy_patch=True,
    ):
        super().__init__(
            module=module,
            class_name=class_name,
            method_name=method_name,
            instance_method=instance_method,
            policy_patch=policy_patch,
        )
        self.config_option = config_option
