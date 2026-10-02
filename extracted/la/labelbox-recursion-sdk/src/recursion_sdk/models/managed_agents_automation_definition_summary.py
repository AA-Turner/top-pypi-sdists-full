from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_automation_definition_summary_status import ManagedAgentsAutomationDefinitionSummaryStatus
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="ManagedAgentsAutomationDefinitionSummary")



@_attrs_define
class ManagedAgentsAutomationDefinitionSummary:
    """ Compact canonical automation representation without prompts, defaults, or trigger configuration.

        Example:
            {'agentId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agentVersionId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'automationId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'createdAt': '2026-02-18T09:30:00Z', 'displayName':
                'example', 'environmentId': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'revision': 1, 'status': 'paused',
                'updatedAt': '2026-02-18T09:30:00Z'}

        Attributes:
            agent_id (UUID): Managed agent selected by this automation.
            agent_version_id (UUID): Immutable agent version pinned for runs.
            automation_id (UUID): Stable canonical automation identifier.
            created_at (datetime.datetime): Time the automation was created.
            display_name (str): Human-readable automation name.
            environment_id (UUID): Execution environment selected for sessions.
            revision (int): Monotonic aggregate revision.
            status (ManagedAgentsAutomationDefinitionSummaryStatus): Current lifecycle state.
            updated_at (datetime.datetime): Time the aggregate was last changed.
     """

    agent_id: UUID
    agent_version_id: UUID
    automation_id: UUID
    created_at: datetime.datetime
    display_name: str
    environment_id: UUID
    revision: int
    status: ManagedAgentsAutomationDefinitionSummaryStatus
    updated_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        agent_id = str(self.agent_id)

        agent_version_id = str(self.agent_version_id)

        automation_id = str(self.automation_id)

        created_at = self.created_at.isoformat()

        display_name = self.display_name

        environment_id = str(self.environment_id)

        revision = self.revision

        status = self.status.value

        updated_at = self.updated_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "agentId": agent_id,
            "agentVersionId": agent_version_id,
            "automationId": automation_id,
            "createdAt": created_at,
            "displayName": display_name,
            "environmentId": environment_id,
            "revision": revision,
            "status": status,
            "updatedAt": updated_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = UUID(d.pop("agentId"))




        agent_version_id = UUID(d.pop("agentVersionId"))




        automation_id = UUID(d.pop("automationId"))




        created_at = datetime.datetime.fromisoformat(d.pop("createdAt"))




        display_name = d.pop("displayName")

        environment_id = UUID(d.pop("environmentId"))




        revision = d.pop("revision")

        status = ManagedAgentsAutomationDefinitionSummaryStatus(d.pop("status"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updatedAt"))




        managed_agents_automation_definition_summary = cls(
            agent_id=agent_id,
            agent_version_id=agent_version_id,
            automation_id=automation_id,
            created_at=created_at,
            display_name=display_name,
            environment_id=environment_id,
            revision=revision,
            status=status,
            updated_at=updated_at,
        )

        return managed_agents_automation_definition_summary

