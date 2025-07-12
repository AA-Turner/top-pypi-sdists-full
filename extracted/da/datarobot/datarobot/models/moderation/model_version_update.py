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
from typing import Dict, List

from datarobot.models.api_object import APIObject
from datarobot.models.moderation.configuration import ModerationConfiguration
from datarobot.models.moderation.overall import OverallModerationConfig
from datarobot.utils import to_api


class ModelVersionUpdate(APIObject):
    """
    Implements the operation provided by "Save Configuration" in moderation UI.
    All guard configurations and overall config is saved to a new custom model version.
    """

    _path = "guardConfigurations/toNewCustomModelVersion/"

    @classmethod
    def new_custom_model_version_with_config(
        cls,
        custom_model_id: str,
        overall_config: OverallModerationConfig,
        configs: List[ModerationConfiguration],
    ) -> str:
        """
        Create a new custom model version with the provided moderation configuration
        Parameters
        ----------
        custom_model_id
        overall_config
        configs

        Returns
        -------
        ID of the new custom model version.

        """
        # API payload is a subset of guard configuration fields
        # unroll the list comprehension to make mypy happy
        fields_to_drop = ["id", "createdAt", "creatorId", "entityId", "entityType"]
        fields_to_drop_if_empty = [
            "openaiApiKey",
            "openaiApiBase",
            "openaiDeploymentId",
            "openaiCredential",
            "errorMessage",
        ]
        config_data: List[Dict[str, str]] = []
        # mypy really hates to_api(), so several suppressions are needed here
        for config in configs:
            config_dict = to_api(config)
            for f in fields_to_drop:
                config_dict.pop(f, None)  # type: ignore [union-attr, call-arg, arg-type]
            for f in fields_to_drop_if_empty:
                if not config_dict.get(f):  # type: ignore [union-attr]
                    config_dict.pop(f, None)  # type: ignore [union-attr, call-arg, arg-type]
            config_data.append(config_dict)  # type: ignore [arg-type]
        # and a subset of overall configuration fields.
        payload = {
            "customModelId": custom_model_id,
            "overallConfig": {
                "timeoutSec": overall_config.timeout_sec,
                "timeoutAction": overall_config.timeout_action.value,
            },
            "data": config_data,
        }
        response = cls._client.post(
            cls._path,
            data=payload,
        )
        custom_model_version_id: str = response.json().get("customModelVersionId")
        return custom_model_version_id
