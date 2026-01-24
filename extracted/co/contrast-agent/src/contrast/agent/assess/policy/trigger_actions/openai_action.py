# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.policy.trigger_actions.default_action import DefaultAction


class OpenAIAction(DefaultAction):
    """
    This is currently no different from the DefaultAction, but that might not always be
    the case. This is ready to go if necessary in the future.
    """

    # for now, keep this True - might change if we modify `extract_source` logic
    unwind_source = True

    def extract_source(  # pylint: disable=useless-parent-delegation
        self, source, args, kwargs
    ):
        """
        The openai API requires a "role" for each prompt message. Currently, we've
        determined that all role types are vulnerable to prompt-injection. If this
        changes in the future, more complicated logic here may be necessary.
        """
        return super().extract_source(source, args, kwargs)
