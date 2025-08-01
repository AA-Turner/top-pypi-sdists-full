# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.policy.trigger_actions.default_action import DefaultAction
from contrast.utils.patch_utils import get_arg


class FromstringAction(DefaultAction):
    """
    Custom trigger action that implements XXE fromstring rule logic.

    For lxml.etree.fromstring(), if the parser has resolve_entities disabled, then
    `fromstring` is not vulnerable to XXE.
    """

    def is_violated(
        self, source, required_tags, disallowed_tags, orig_args=None, orig_kwargs=None
    ) -> bool:
        if not super().is_violated(source, required_tags, disallowed_tags):
            return False

        from lxml import etree

        parser = get_arg(orig_args, orig_kwargs, 1, "parser", None)
        if parser is not None and not isinstance(parser, etree.XMLParser):
            return False
        return not (
            hasattr(parser, "resolve_entities") and parser.resolve_entities is False
        )
