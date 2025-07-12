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

from typing import Any, Dict, List, Optional

import trafaret as t

from datarobot.enums import ModerationGuardModelTargetType
from datarobot.models.api_object import APIObject


class GuardModelInfo(APIObject):
    """
    Model information for moderation templates and configurations.
    Omitted optional values are stored and presented as:
    * []  (for class names)
    * None  (all others)
    """

    _converter = t.Dict(
        {
            t.Key("input_column_name"): t.String(),
            t.Key("output_column_name"): t.String(),
            t.Key("target_type"): t.Enum(*[e.value for e in ModerationGuardModelTargetType]),
            t.Key("replacement_text_column_name", optional=True): t.String(allow_blank=True),
            t.Key("class_names", optional=True): t.List(t.String()),
            t.Key("model_id", optional=True): t.String(allow_blank=True),
            t.Key("model_name", optional=True): t.String(allow_blank=True),
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(self: GuardModelInfo, **kwargs: Any) -> None:
        self._set_values(**kwargs)

    def __repr__(self) -> str:
        return "{}(target_type={!r})".format(
            self.__class__.__name__,
            self.target_type,
        )

    def _set_values(
        self: GuardModelInfo,
        input_column_name: str,
        output_column_name: str,
        target_type: ModerationGuardModelTargetType,
        replacement_text_column_name: Optional[str] = None,
        class_names: Optional[list[str]] = None,
        model_id: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> None:
        """
        Initialize a model information object based on values from init or server data.

        Parameters
        ----------
        input_column_name : str
            The name of the input column.
        output_column_name : str
            The name of the output column.
        target_type : ModerationGuardModelTargetType
            The target type of the model.
        replacement_text_column_name : Optional[str]
            The name of the replacement text column.
        class_names : list[str], optional
            The class names of the model.
        model_id : Optional[str]
            The ID of the model.
        model_name : Optional[str]
            The name of the model.
        """
        self.input_column_name = input_column_name
        self.output_column_name = output_column_name
        self.target_type = ModerationGuardModelTargetType(target_type)
        self.replacement_text_column_name = replacement_text_column_name
        self.class_names = class_names or []
        self.model_id = model_id
        self.model_name = model_name

    def to_dict(self: GuardModelInfo) -> Dict[str, str | List[str] | Optional[str]]:
        """
        Convert the model information object to a dictionary.
        """
        response = {
            "inputColumnName": self.input_column_name,
            "outputColumnName": self.output_column_name,
            "targetType": self.target_type.value,
            "classNames": self.class_names or [],
            "modelId": self.model_id,
            "modelName": self.model_name,
            "replacementTextColumnName": self.replacement_text_column_name,
        }
        return response

    @classmethod
    def ensure_object(cls, maybe_dict: Dict[str, str] | GuardModelInfo) -> GuardModelInfo:
        """intervention may arrive as an object, or as a dict. Return an object."""
        if isinstance(maybe_dict, GuardModelInfo):
            return maybe_dict
        elif isinstance(maybe_dict, dict):
            return GuardModelInfo(**maybe_dict)
        else:
            raise ValueError("Expected GuardModelInfo object or dictionary")
