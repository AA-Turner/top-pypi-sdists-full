#
# Copyright 2024-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from typing import Any, Dict, Optional

import trafaret as t
from trafaret import String

from datarobot.enums import (
    ModerationGuardAction,
    ModerationGuardConditionLogic,
    ModerationGuardConditionOperator,
)
from datarobot.models.api_object import APIObject


class GuardInterventionCondition(APIObject):
    """Defines a condition for intervention."""

    _converter = t.Dict(
        {
            t.Key("comparator"): t.Enum(*[e.value for e in ModerationGuardConditionOperator]),
            t.Key("comparand"): t.Or(
                t.Float(),
                t.String(),
                t.Bool(),
                t.List(
                    t.String(),
                ),
            ),
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(self: GuardInterventionCondition, **kwargs: Any) -> None:
        self._set_values(**kwargs)

    def __repr__(self) -> str:
        return "{}(comparator={!r}, comparand={!r})".format(
            self.__class__.__name__,
            self.comparator,
            self.comparand,
        )

    def _set_values(
        self: GuardInterventionCondition,
        comparator: ModerationGuardConditionOperator,
        comparand: Any,
    ) -> None:
        self.comparator = ModerationGuardConditionOperator(comparator)
        self.comparand = comparand

    def to_dict(self) -> Dict[str, str]:
        return {
            "comparator": self.comparator.value,
            "comparand": self.comparand,
        }


class GuardInterventionForTemplate(APIObject):
    """
    Defines the intervention conditions and actions a guard can take.
    Configuration schema differs slightly from template because changes were requested after
    templates were baked in.
    """

    _converter = t.Dict(
        {
            t.Key("action"): t.Enum(*[e.value for e in ModerationGuardAction]),
            t.Key("conditions"): t.List(GuardInterventionCondition.schema),
            t.Key("modify_message"): t.String(allow_blank=True),
            t.Key("allowed_actions"): t.List(t.Enum(*[e.value for e in ModerationGuardAction])),
            t.Key("condition_logic", optional=True): t.Enum(
                *[e.value for e in ModerationGuardConditionLogic]
            ),
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(self: GuardInterventionForTemplate, **kwargs: Any) -> None:
        self._set_values(**kwargs)

    def __repr__(self) -> str:
        return "{}(action={!r})".format(
            self.__class__.__name__,
            self.action,
        )

    def _set_values(
        self: GuardInterventionForTemplate,
        action: ModerationGuardAction | str,
        conditions: list[GuardInterventionCondition | str],
        modify_message: str,
        allowed_actions: list[ModerationGuardAction | str],
        condition_logic: Optional[
            ModerationGuardConditionLogic
        ] = ModerationGuardConditionLogic.ANY,
    ) -> None:
        """
        Initialize an intervention object based on values from init or server data.
        """
        # from_server_data() may not convert inner objects
        c_obj = [
            (
                x
                if isinstance(x, GuardInterventionCondition)
                else GuardInterventionCondition(**x)  # type: ignore[arg-type]
            )
            for x in conditions
        ]
        a_list = [ModerationGuardAction(x) for x in allowed_actions]
        self.action = ModerationGuardAction(action)
        self.conditions = c_obj
        self.modify_message = modify_message
        self.allowed_actions = a_list
        self.condition_logic = ModerationGuardConditionLogic(condition_logic)  # type: ignore[arg-type]

    def to_dict(self: GuardInterventionForTemplate) -> Dict[str, str]:
        return {
            "action": self.action.value,
            "conditions": [x.to_dict() for x in self.conditions],  # type: ignore[dict-item]
            "modifyMessage": self.modify_message,
            "allowedActions": [x.value for x in self.allowed_actions],  # type: ignore[dict-item]
            "conditionLogic": self.condition_logic.value,
        }

    @classmethod
    def ensure_object(
        cls, maybe_dict: Dict[str, str] | GuardInterventionForTemplate
    ) -> GuardInterventionForTemplate:
        """intervention may arrive as an object, or as a dict. Return an object."""
        if isinstance(maybe_dict, GuardInterventionForTemplate):
            return maybe_dict
        elif isinstance(maybe_dict, dict):
            return GuardInterventionForTemplate(**maybe_dict)
        else:
            raise ValueError("Expected GuardInterventionForTemplate object or dictionary")


class GuardInterventionForConfiguration(APIObject):
    """
    Defines the intervention conditions and actions a guard can take.
    Configuration schema differs slightly from template because changes were requested after
    templates were baked in.
    """

    _converter = t.Dict(
        {
            t.Key("action"): t.Enum(*[e.value for e in ModerationGuardAction]),
            t.Key("conditions"): t.List(GuardInterventionCondition.schema),
            t.Key("message"): String(allow_blank=True),
            t.Key("allowed_actions"): t.List(t.Enum(*[e.value for e in ModerationGuardAction])),
            t.Key("condition_logic", optional=True): t.Enum(
                *[e.value for e in ModerationGuardConditionLogic]
            ),
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(self: GuardInterventionForConfiguration, **kwargs: Any) -> None:
        self._set_values(**kwargs)

    def __repr__(self) -> str:
        return "{}(action={!r})".format(
            self.__class__.__name__,
            self.action,
        )

    def _set_values(
        self: GuardInterventionForConfiguration,
        action: ModerationGuardAction | str,
        conditions: list[GuardInterventionCondition | str],
        message: str,
        allowed_actions: list[ModerationGuardAction | str],
        condition_logic: Optional[
            ModerationGuardConditionLogic
        ] = ModerationGuardConditionLogic.ANY,
    ) -> None:
        """
        Initialize an intervention object based on values from init or server data.
        """
        # from_server_data() may not convert inner objects
        c_obj = [
            (
                x
                if isinstance(x, GuardInterventionCondition)
                else GuardInterventionCondition(**x)  # type: ignore[arg-type]
            )
            for x in conditions
        ]
        a_list = [ModerationGuardAction(x) for x in allowed_actions]
        self.action = ModerationGuardAction(action)
        self.conditions = c_obj
        self.message = message
        self.allowed_actions = a_list
        self.condition_logic = ModerationGuardConditionLogic(condition_logic)  # type: ignore[arg-type]

    def to_dict(self: GuardInterventionForConfiguration) -> Dict[str, str]:
        return {
            "action": self.action.value,
            "conditions": [x.to_dict() for x in self.conditions],  # type: ignore[dict-item]
            "message": self.message,
            "allowedActions": [x.value for x in self.allowed_actions],  # type: ignore[dict-item]
            "conditionLogic": self.condition_logic.value,
        }

    @classmethod
    def ensure_object(
        cls, maybe_dict: Dict[str, str] | GuardInterventionForConfiguration
    ) -> GuardInterventionForConfiguration:
        """intervention may arrive as an object, or as a dict. Return an object."""
        if isinstance(maybe_dict, GuardInterventionForConfiguration):
            return maybe_dict
        elif isinstance(maybe_dict, dict):
            return GuardInterventionForConfiguration(**maybe_dict)
        else:
            raise ValueError("Expected GuardInterventionForConfiguration object or dictionary")
