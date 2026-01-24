# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations

import re

from contrast_fireball import AssessEventType

from contrast.agent.assess.assess_exceptions import ContrastAssessException
from contrast.agent.assess.policy.trigger_actions import (
    fromstring_action,
    openai_action,
    pymongo_action,
    redos_action,
    ssrf_action,
    subprocess_action,
    unvalidated_redirect_action,
)
from contrast.agent.assess.policy.trigger_actions.default_action import DefaultAction
from contrast.agent.policy import constants
from contrast.agent.policy.policy_node import PolicyNode


class TriggerNode(PolicyNode):
    TRIGGER_ACTIONS: dict[str, DefaultAction] = {
        constants.TRIGGER_ACTION_DEFAULT: DefaultAction(),
        constants.TRIGGER_ACTION_REDOS: redos_action.RedosAction(),
        constants.TRIGGER_ACTION_SSRF: ssrf_action.SsrfAction(),
        constants.TRIGGER_ACTION_STARLETTE_REDIRECT: unvalidated_redirect_action.StarletteRedirectAction(),
        constants.TRIGGER_ACTION_FROMSTRING: fromstring_action.FromstringAction(),
        constants.TRIGGER_ACTION_SUBPROCESS: subprocess_action.SubprocessAction(),
        constants.TRIGGER_ACTION_OPENAI: openai_action.OpenAIAction(),
        constants.TRIGGER_ACTION_PYMONGO: pymongo_action.PyMongoAction(),
    }

    def __init__(
        self,
        module: str,
        class_name: str,
        instance_method: bool,
        method_name: str,
        source="",
        dataflow=True,
        good_value: str = "",
        bad_value: str = "",
        action=None,
        policy_patch=True,
        rule=None,
        protect_mode=False,
        unsafe_default=False,
    ):
        super().__init__(
            module,
            class_name,
            instance_method,
            method_name,
            source,
            target="",
            policy_patch=policy_patch,
        )

        self.dataflow = dataflow

        self.good_value = (
            re.compile(good_value, flags=re.IGNORECASE) if good_value else None
        )
        self.bad_value = (
            re.compile(bad_value, flags=re.IGNORECASE) if bad_value else None
        )
        self.action = action or constants.TRIGGER_ACTION_DEFAULT

        self.rule = rule

        self.protect_mode = protect_mode
        self.unsafe_default = unsafe_default

        self.validate()

    @property
    def node_type(self):
        return AssessEventType.METHOD

    @property
    def dataflow_rule(self):
        return self.dataflow

    def validate(self):
        super().validate()

        if not self.dataflow_rule:
            return

        if not (self.sources and len(self.sources) != 0):
            raise ContrastAssessException(
                f"Trigger {self.name} did not have a proper source. Unable to create."
            )

    def get_matching_sources(
        self, self_obj: object, ret: object, args: tuple, kwargs: dict[str, object]
    ) -> list[object]:
        sources = []

        for source in self.sources:
            if source == constants.OBJECT:
                sources.append(self_obj)
            elif source == constants.ALL_ARGS:
                sources.append(args)
            elif source == constants.ALL_KWARGS:
                sources.append(kwargs)
            elif source == constants.RETURN:
                sources.append(ret)
            elif isinstance(source, int) and len(args) > source:
                sources.append(args[source])
            elif kwargs and source in kwargs:
                sources.append(kwargs[source])
            elif (
                isinstance(source, str)  # only consider kwarg sources
                and self.unsafe_default
                and source not in sources
            ):
                # if the default argument for this source is unsafe and we landed
                # here, we should trigger a finding. To do so, we add `None`,
                # with the assumption that most triggers will use `None`
                # as a default, but this won't always be correct. We may add a
                # trigger that uses a boolean as a default.

                # TODO: PYT-1764 special machinery to know what the default really is
                sources.append(None)
        return sources

    def get_protect_sources(
        self, args: tuple, kwargs: dict[str, object]
    ) -> list[object]:
        self_obj = args[0] if self.instance_method else None
        args = args[1:] if self.instance_method else args
        return self.get_matching_sources(self_obj, None, args, kwargs)

    @property
    def trigger_action(self) -> DefaultAction | None:
        return self.TRIGGER_ACTIONS.get(self.action)
