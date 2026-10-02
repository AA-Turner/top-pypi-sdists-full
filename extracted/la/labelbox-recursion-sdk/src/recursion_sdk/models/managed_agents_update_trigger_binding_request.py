from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsUpdateTriggerBindingRequest")



@_attrs_define
class ManagedAgentsUpdateTriggerBindingRequest:
    """ Partial update of one trigger binding. Only the properties present in the request change; an omitted property keeps
    its stored value, so an explicit false or empty list is distinguishable from an omission. The merged binding is
    revalidated as a whole, which is what keeps a single-field edit from bypassing a provider or tenancy invariant.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'channel_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'enabled': True, 'environment_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'owner_key': 'example', 'vault_ids': ['example'], 'wake_app_ids':
                ['example'], 'wake_event': 'example'}

        Attributes:
            agent_id (None | str | Unset): Replacement agent (UUID) a matching event starts a session for.
            channel_id (None | str | Unset): Replacement Slack channel scope. Empty makes app_mention an internal-only
                fallback; message and message_root require an exact channel; app_mention_ext_shared requires empty scope and
                independently opts into shared channels.
            connection_id (None | str | Unset): Replacement integration connection (UUID) whose events the binding routes.
            enabled (bool | None | Unset): Arm or disarm the binding. Sending false on its own is the one update that skips
                revalidating the binding's references, so a rule pointing at a deleted agent can still be disabled.
            environment_id (None | str | Unset): Replacement environment (UUID) that session runs in.
            owner_key (None | str | Unset): Replacement caller-owned stable identity for a binding managed by code. An
                omitted property keeps the stored value; an explicit empty string clears it, returning the binding to hand-
                managed. At most 128 characters of letters, digits, '.', '_', ':', '/', and '-'.
            vault_ids (list[str] | None | Unset): Replacement vault (UUID) list. An empty list clears every grant.
            wake_app_ids (list[str] | None | Unset): Replacement Slack source app id list. An empty list restores the
                default that app-authored roots never start work. Legal only on an exact-channel message_root binding; a PATCH
                that moves the binding off message_root clears a stored list instead of rejecting the change.
            wake_event (None | str | Unset): Replacement provider event selector, validated against the binding's provider.
                Switching an exact app_mention binding to message_root turns on proactive root investigations for that channel
                with the same agent, environment, and vaults; switching back is the rollback.
     """

    agent_id: None | str | Unset = UNSET
    channel_id: None | str | Unset = UNSET
    connection_id: None | str | Unset = UNSET
    enabled: bool | None | Unset = UNSET
    environment_id: None | str | Unset = UNSET
    owner_key: None | str | Unset = UNSET
    vault_ids: list[str] | None | Unset = UNSET
    wake_app_ids: list[str] | None | Unset = UNSET
    wake_event: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        agent_id: None | str | Unset
        if isinstance(self.agent_id, Unset):
            agent_id = UNSET
        else:
            agent_id = self.agent_id

        channel_id: None | str | Unset
        if isinstance(self.channel_id, Unset):
            channel_id = UNSET
        else:
            channel_id = self.channel_id

        connection_id: None | str | Unset
        if isinstance(self.connection_id, Unset):
            connection_id = UNSET
        else:
            connection_id = self.connection_id

        enabled: bool | None | Unset
        if isinstance(self.enabled, Unset):
            enabled = UNSET
        else:
            enabled = self.enabled

        environment_id: None | str | Unset
        if isinstance(self.environment_id, Unset):
            environment_id = UNSET
        else:
            environment_id = self.environment_id

        owner_key: None | str | Unset
        if isinstance(self.owner_key, Unset):
            owner_key = UNSET
        else:
            owner_key = self.owner_key

        vault_ids: list[str] | None | Unset
        if isinstance(self.vault_ids, Unset):
            vault_ids = UNSET
        elif isinstance(self.vault_ids, list):
            vault_ids = self.vault_ids


        else:
            vault_ids = self.vault_ids

        wake_app_ids: list[str] | None | Unset
        if isinstance(self.wake_app_ids, Unset):
            wake_app_ids = UNSET
        elif isinstance(self.wake_app_ids, list):
            wake_app_ids = self.wake_app_ids


        else:
            wake_app_ids = self.wake_app_ids

        wake_event: None | str | Unset
        if isinstance(self.wake_event, Unset):
            wake_event = UNSET
        else:
            wake_event = self.wake_event


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if agent_id is not UNSET:
            field_dict["agent_id"] = agent_id
        if channel_id is not UNSET:
            field_dict["channel_id"] = channel_id
        if connection_id is not UNSET:
            field_dict["connection_id"] = connection_id
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if environment_id is not UNSET:
            field_dict["environment_id"] = environment_id
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
        def _parse_agent_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        agent_id = _parse_agent_id(d.pop("agent_id", UNSET))


        def _parse_channel_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        channel_id = _parse_channel_id(d.pop("channel_id", UNSET))


        def _parse_connection_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        connection_id = _parse_connection_id(d.pop("connection_id", UNSET))


        def _parse_enabled(data: object) -> bool | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(bool | None | Unset, data)

        enabled = _parse_enabled(d.pop("enabled", UNSET))


        def _parse_environment_id(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        environment_id = _parse_environment_id(d.pop("environment_id", UNSET))


        def _parse_owner_key(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        owner_key = _parse_owner_key(d.pop("owner_key", UNSET))


        def _parse_vault_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                vault_ids_type_1 = cast(list[str], data)

                return vault_ids_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        vault_ids = _parse_vault_ids(d.pop("vault_ids", UNSET))


        def _parse_wake_app_ids(data: object) -> list[str] | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                wake_app_ids_type_1 = cast(list[str], data)

                return wake_app_ids_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[str] | None | Unset, data)

        wake_app_ids = _parse_wake_app_ids(d.pop("wake_app_ids", UNSET))


        def _parse_wake_event(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        wake_event = _parse_wake_event(d.pop("wake_event", UNSET))


        managed_agents_update_trigger_binding_request = cls(
            agent_id=agent_id,
            channel_id=channel_id,
            connection_id=connection_id,
            enabled=enabled,
            environment_id=environment_id,
            owner_key=owner_key,
            vault_ids=vault_ids,
            wake_app_ids=wake_app_ids,
            wake_event=wake_event,
        )


        managed_agents_update_trigger_binding_request.additional_properties = d
        return managed_agents_update_trigger_binding_request

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
