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

from datarobot.models.api_object import APIObject


class GuardNemoInfo(APIObject):
    """Details of a NeMo Guardrails moderation guard."""

    _converter = t.Dict(
        {
            t.Key("main_config"): t.String(),
            t.Key("rails_config"): t.String(),
            t.Key("blocked_terms"): t.String(),
            t.Key("llm_prompts"): t.String(),
            t.Key("actions"): t.String(),
        }
    ).ignore_extra("*")

    schema = _converter

    def __init__(self, **kwargs: Any) -> None:
        self._set_values(**kwargs)

    def __repr__(self) -> str:
        return "NeMo guardrails; see details"

    def _set_values(
        self: GuardNemoInfo,
        main_config: str = "",
        rails_config: str = "",
        blocked_terms: str = "",
        llm_prompts: str = "",
        actions: str = "",
    ) -> None:
        """
        Initialize a NeMo guardrails object based on values from init or server data.
        """
        self.main_config = main_config
        self.rails_config = rails_config
        self.blocked_terms = blocked_terms
        self.llm_prompts = llm_prompts
        self.actions = actions

    def to_dict(self: GuardNemoInfo) -> Dict[str, str]:
        return {
            "mainConfig": self.main_config,
            "railsConfig": self.rails_config,
            "blockedTerms": self.blocked_terms,
            "llmPrompts": self.llm_prompts,
            "actions": self.actions,
        }
