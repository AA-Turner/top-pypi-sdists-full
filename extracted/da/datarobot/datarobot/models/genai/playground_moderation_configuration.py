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

from typing import Any, Dict

import trafaret as t

from datarobot.enums import enum_to_list, ModerationGuardAction
from datarobot.models.api_object import APIObject
from datarobot.models.moderation.intervention import GuardInterventionCondition

moderation_configuration_without_id = t.Dict(
    {
        t.Key("guard_conditions"): t.List(
            t.Dict(
                {
                    t.Key("comparator"): t.String,
                    t.Key("comparand"): t.Or(t.Float, t.String, t.Bool, t.List(t.String)),
                }
            )
        ),
        t.Key("intervention"): t.Dict(
            {
                t.Key("action"): t.String,
                t.Key("message"): t.String,
            }
        ),
    }
).ignore_extra("*")

moderation_configuration_with_id = moderation_configuration_without_id + {"id": t.String}


intervention = t.Dict(
    {
        t.Key("action"): t.Enum(*enum_to_list(ModerationGuardAction)),
        t.Key("message"): t.String,
    }
).ignore_extra("*")


class Intervention(APIObject):
    """Intervention for playground moderation.

    Attributes
    ----------
    action : str
        The intervention strategy.
    message : str
        The intervention message to replace the prediction when a guard condition is satisfied.
    """

    _converter = intervention

    def __init__(self, action: str, message: str):
        self.action = action
        self.message = message

    def __repr__(self) -> str:
        return f"Playground Intervention(action={self.action}, message={self.message})"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action": self.action,
            "message": self.message,
        }


class ModerationConfigurationWithoutId(APIObject):
    """The moderation configuration for a metric in Playground.

    Attributes
    ----------
    guard_conditions : GuardInterventionCondition
        The guard conditions for the metric.
    intervention : Intervention
        The interventions for the guard.
    """

    _converter = moderation_configuration_without_id

    def __init__(self, guard_conditions: list[Dict[str, Any]], intervention: Dict[str, str]):
        self.guard_conditions = [
            GuardInterventionCondition.from_server_data(gc) for gc in guard_conditions
        ]
        self.intervention = Intervention.from_server_data(intervention)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "guard_conditions": [gc.to_dict() for gc in self.guard_conditions],
            "intervention": self.intervention.to_dict(),
        }
