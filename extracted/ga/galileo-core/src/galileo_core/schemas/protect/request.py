from datetime import timedelta
from functools import cached_property
from os import getenv
from typing import Dict, List, Optional, Set
from uuid import UUID

from pydantic import UUID4, ConfigDict, Field, field_validator, model_validator

from galileo_core.schemas.protect.payload import Payload
from galileo_core.schemas.protect.rule import Rule
from galileo_core.schemas.protect.ruleset import RulesetsMixin


class Request(RulesetsMixin):
    payload: Payload = Field(description="Payload to be processed.")
    project_name: Optional[str] = Field(default=None, description="Project name.", validate_default=True)
    project_id: Optional[UUID4] = Field(default=None, description="Project ID.", validate_default=True)
    stage_name: Optional[str] = Field(default=None, description="Stage name.", validate_default=True)
    stage_id: Optional[UUID4] = Field(default=None, description="Stage ID.", validate_default=True)
    stage_version: Optional[int] = Field(
        default=None,
        description="Stage version to use for the request, if it's a central stage with a previously registered version.",
        validate_default=True,
    )
    timeout: float = Field(
        default=timedelta(minutes=5).total_seconds(),
        description="Optional timeout for the guardrail execution in seconds. This is not the timeout for the request. If not set, a default timeout of 5 minutes will be used.",
    )
    metadata: Optional[Dict[str, str]] = Field(
        default=None,
        description="Optional additional metadata. This will be echoed back in the response.",
    )
    headers: Optional[Dict[str, str]] = Field(
        default=None,
        description="Optional additional HTTP headers that should be included in the response.",
    )

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("project_name", mode="before")
    def project_name_from_env(cls, value: Optional[str]) -> Optional[str]:
        env_value = getenv("GALILEO_PROJECT_NAME", getenv("GALILEO_PROJECT"))
        if value is None and env_value:
            value = env_value
        return value

    @field_validator("project_id", mode="before")
    def project_id_from_env(cls, value: Optional[UUID4]) -> Optional[UUID4]:
        env_value = getenv("GALILEO_PROJECT_ID")
        if value is None and env_value:
            value = UUID(env_value)
        return value

    @field_validator("stage_name", mode="before")
    def stage_name_from_env(cls, value: Optional[str]) -> Optional[str]:
        env_value = getenv("GALILEO_STAGE_NAME")
        if value is None and env_value:
            value = env_value
        return value

    @field_validator("stage_id", mode="before")
    def stage_id_from_env(cls, value: Optional[UUID4]) -> Optional[UUID4]:
        env_value = getenv("GALILEO_STAGE_ID")
        if value is None and env_value:
            value = UUID(env_value)
        return value

    @field_validator("stage_version", mode="before")
    def stage_version_from_env(cls, value: Optional[int]) -> Optional[int]:
        env_value = getenv("GALILEO_STAGE_VERSION")
        if value is None and env_value:
            value = int(env_value)
        return value

    @model_validator(mode="after")
    def validate_project_stage(self) -> "Request":
        """
        Validate that one of:
        1. stage_id
        2. stage_name and project_id
        3. stage_name and project_name
        are provided.

        Returns
        -------
        Request
            The request object.

        Raises
        ------
        ValueError
            If the validation fails.
        """
        if (self.stage_id) or (self.stage_name and self.project_id) or (self.stage_name and self.project_name):
            return self
        else:
            raise ValueError(
                "Either stage_id or stage_name and project_id or stage_name and project_name must be provided."
            )

    @cached_property
    def rules(self) -> List[Rule]:
        rules: List[Rule] = []
        for ruleset in self.rulesets:
            rules.extend(ruleset.rules)
        return rules

    @cached_property
    def metrics(self) -> Set[str]:
        metrics_to_compute = []
        for rule in self.rules:
            metrics_to_compute.append(rule.metric)
        return set(metrics_to_compute)

    @cached_property
    def timeout_ns(self) -> float:
        return self.timeout * 1e9
