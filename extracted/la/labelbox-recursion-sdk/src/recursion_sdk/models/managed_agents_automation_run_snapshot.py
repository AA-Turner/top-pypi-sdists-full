from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef





T = TypeVar("T", bound="ManagedAgentsAutomationRunSnapshot")



@_attrs_define
class ManagedAgentsAutomationRunSnapshot:
    """ The automation's configuration frozen at the instant a run fired.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'credential_refs': [{'credential_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'vault_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}], 'cron': 'example', 'environment_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'initial_message_digest': 'example', 'schedule_version': 1, 'timezone':
                'example', 'vault_ids': ['example']}

        Attributes:
            agent_id (str): Agent the run started, as configured when it fired.
            environment_id (str): Environment the run's session was provisioned in.
            agent_version_id (str | Unset): Concrete agent version the run used, so a later re-pin cannot change what this
                run did.
            credential_refs (list[ManagedAgentsVaultCredentialRef] | Unset): Explicit credential grants the run's session
                was given.
            cron (str | Unset): Cron expression in force at firing time, for a scheduled run.
            initial_message_digest (str | Unset): Digest of the initial message in force at firing time. A digest rather
                than the text, because messages can be long and the question this answers is only whether it changed.
            schedule_version (int | Unset): Configuration revision of the trigger this run fired from.
            timezone (str | Unset): Timezone in force at firing time, for a scheduled run.
            vault_ids (list[str] | Unset): Vaults the run's session was granted.
     """

    agent_id: str
    environment_id: str
    agent_version_id: str | Unset = UNSET
    credential_refs: list[ManagedAgentsVaultCredentialRef] | Unset = UNSET
    cron: str | Unset = UNSET
    initial_message_digest: str | Unset = UNSET
    schedule_version: int | Unset = UNSET
    timezone: str | Unset = UNSET
    vault_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef # noqa: PLC0415
        agent_id = self.agent_id

        environment_id = self.environment_id

        agent_version_id = self.agent_version_id

        credential_refs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.credential_refs, Unset):
            credential_refs = []
            for credential_refs_item_data in self.credential_refs:
                credential_refs_item = credential_refs_item_data.to_dict()
                credential_refs.append(credential_refs_item)



        cron = self.cron

        initial_message_digest = self.initial_message_digest

        schedule_version = self.schedule_version

        timezone = self.timezone

        vault_ids: list[str] | Unset = UNSET
        if not isinstance(self.vault_ids, Unset):
            vault_ids = self.vault_ids




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "agent_id": agent_id,
            "environment_id": environment_id,
        })
        if agent_version_id is not UNSET:
            field_dict["agent_version_id"] = agent_version_id
        if credential_refs is not UNSET:
            field_dict["credential_refs"] = credential_refs
        if cron is not UNSET:
            field_dict["cron"] = cron
        if initial_message_digest is not UNSET:
            field_dict["initial_message_digest"] = initial_message_digest
        if schedule_version is not UNSET:
            field_dict["schedule_version"] = schedule_version
        if timezone is not UNSET:
            field_dict["timezone"] = timezone
        if vault_ids is not UNSET:
            field_dict["vault_ids"] = vault_ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_vault_credential_ref import ManagedAgentsVaultCredentialRef # noqa: PLC0415
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        environment_id = d.pop("environment_id")

        agent_version_id = d.pop("agent_version_id", UNSET)

        _credential_refs = d.pop("credential_refs", UNSET)
        credential_refs: list[ManagedAgentsVaultCredentialRef] | Unset = UNSET
        if _credential_refs is not UNSET:
            credential_refs = []
            for credential_refs_item_data in _credential_refs:
                credential_refs_item = ManagedAgentsVaultCredentialRef.from_dict(credential_refs_item_data)



                credential_refs.append(credential_refs_item)


        cron = d.pop("cron", UNSET)

        initial_message_digest = d.pop("initial_message_digest", UNSET)

        schedule_version = d.pop("schedule_version", UNSET)

        timezone = d.pop("timezone", UNSET)

        vault_ids = cast(list[str], d.pop("vault_ids", UNSET))


        managed_agents_automation_run_snapshot = cls(
            agent_id=agent_id,
            environment_id=environment_id,
            agent_version_id=agent_version_id,
            credential_refs=credential_refs,
            cron=cron,
            initial_message_digest=initial_message_digest,
            schedule_version=schedule_version,
            timezone=timezone,
            vault_ids=vault_ids,
        )


        managed_agents_automation_run_snapshot.additional_properties = d
        return managed_agents_automation_run_snapshot

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
