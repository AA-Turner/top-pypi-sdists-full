from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsCreateTriggerBindingRequest")



@_attrs_define
class ManagedAgentsCreateTriggerBindingRequest:
    """ Request body creating a Slack wake rule: the connection and event to match, and the agent, environment, and vaults a
    match runs with. Every referenced object must belong to the calling organization; GitHub events use provider-neutral
    automations instead.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'channel_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'enabled': True, 'environment_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'owner_key': 'example', 'vault_ids': ['example'], 'wake_app_ids':
                ['example'], 'wake_event': 'example'}

        Attributes:
            agent_id (str): Agent (UUID) a matching event starts a session for, as returned by listAgents.
            connection_id (str): The integration connection whose events this binding routes.
            environment_id (str): Environment (UUID) that session runs in, as returned by listEnvironments.
            channel_id (str | Unset): Scope the binding to one channel; omit to match every channel.
            enabled (bool | Unset): Whether the binding may match events. Defaults to false, which stores the rule without
                arming it.
            owner_key (str | Unset): Optional caller-owned stable identity for a binding managed by code, so its owner can
                recognise the binding after the channel or wake event changes. Omit for a binding made by hand. At most 128
                characters of letters, digits, '.', '_', ':', '/', and '-'. Not unique: the owning code refuses ambiguity
                itself.
            vault_ids (list[str] | Unset): Vaults (UUIDs) to grant the woken session.
            wake_app_ids (list[str] | Unset): Slack source app ids (A…) whose top-level posts may start a session. Empty
                means app-authored roots never start work. Legal only on an exact-channel message_root binding.
            wake_event (str | Unset): Slack selector: app_mention (exact channel or internal-only fallback), message (exact
                channel required; every post and reply wakes the agent), message_root (exact channel required, internal or Slack
                Connect; each new top-level post starts an investigation immediately and replies stay mention-only), or
                app_mention_ext_shared (empty channel required; opt-in shared-only fallback). Exact bindings take precedence;
                creating an enabled message_root binding is rejected while another enabled exact binding exists on the channel,
                and vice versa.
     """

    agent_id: str
    connection_id: str
    environment_id: str
    channel_id: str | Unset = UNSET
    enabled: bool | Unset = UNSET
    owner_key: str | Unset = UNSET
    vault_ids: list[str] | Unset = UNSET
    wake_app_ids: list[str] | Unset = UNSET
    wake_event: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        connection_id = self.connection_id

        environment_id = self.environment_id

        channel_id = self.channel_id

        enabled = self.enabled

        owner_key = self.owner_key

        vault_ids: list[str] | Unset = UNSET
        if not isinstance(self.vault_ids, Unset):
            vault_ids = self.vault_ids



        wake_app_ids: list[str] | Unset = UNSET
        if not isinstance(self.wake_app_ids, Unset):
            wake_app_ids = self.wake_app_ids



        wake_event = self.wake_event


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "agent_id": agent_id,
            "connection_id": connection_id,
            "environment_id": environment_id,
        })
        if channel_id is not UNSET:
            field_dict["channel_id"] = channel_id
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if owner_key is not UNSET:
            field_dict["owner_key"] = owner_key
        if vault_ids is not UNSET:
            field_dict["vault_ids"] = vault_ids
        if wake_app_ids is not UNSET:
            field_dict["wake_app_ids"] = wake_app_ids
        if wake_event is not UNSET:
            field_dict["wake_event"] = wake_event

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        connection_id = d.pop("connection_id")

        environment_id = d.pop("environment_id")

        channel_id = d.pop("channel_id", UNSET)

        enabled = d.pop("enabled", UNSET)

        owner_key = d.pop("owner_key", UNSET)

        vault_ids = cast(list[str], d.pop("vault_ids", UNSET))


        wake_app_ids = cast(list[str], d.pop("wake_app_ids", UNSET))


        wake_event = d.pop("wake_event", UNSET)

        managed_agents_create_trigger_binding_request = cls(
            agent_id=agent_id,
            connection_id=connection_id,
            environment_id=environment_id,
            channel_id=channel_id,
            enabled=enabled,
            owner_key=owner_key,
            vault_ids=vault_ids,
            wake_app_ids=wake_app_ids,
            wake_event=wake_event,
        )


        managed_agents_create_trigger_binding_request.additional_properties = d
        return managed_agents_create_trigger_binding_request

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
