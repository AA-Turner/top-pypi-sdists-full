from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ManagedAgentsTriggerBinding")



@_attrs_define
class ManagedAgentsTriggerBinding:
    """ One wake rule: which provider events start a session, and the agent, environment, and vaults that session runs with.
    New rules are Slack-only; retired GitHub rules remain readable and may be disabled or deleted during migration.

        Example:
            {'agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'automation_kind': 'example', 'binding_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'capture_patch': True, 'channel_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'connection_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'enabled':
                True, 'environment_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'include_drafts': True, 'organization_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'owner_key': 'example', 'provider': 'example', 'publish_review': True,
                'repository': 'example', 'repository_id': 1, 'vault_ids': ['example'], 'wake_app_ids': ['example'],
                'wake_event': 'example'}

        Attributes:
            agent_id (str): Agent (UUID) a matching event starts a session for.
            binding_id (str): Identifier for this binding (UUID). Server-assigned; cite it when updating or deleting the
                binding.
            capture_patch (bool): Whether a matching run captures the agent's final working-tree patch as a session
                artifact.
            connection_id (str): Integration connection (UUID) whose verified events this binding routes.
            enabled (bool): Whether this binding is eligible to match. A disabled binding is retained but never wakes a
                session.
            environment_id (str): Environment (UUID) that session runs in.
            include_drafts (bool): Whether a draft pull request may trigger this binding. Draft events are skipped when
                false.
            organization_id (str): Organization that owns this binding. Resolved from the API key; never accepted from the
                caller.
            provider (str): Integration provider whose events this binding routed. New bindings support Slack; retired
                GitHub bindings remain readable for migration.
            publish_review (bool): Whether a matching run publishes its validated result back to the pull request as a
                GitHub review.
            wake_event (str): Slack selector: app_mention (explicit tags), message (exact channel; every post and reply
                wakes the agent), message_root (exact channel, internal or Slack Connect; every new top-level post starts an
                investigation at once and thread replies stay mention-only), or app_mention_ext_shared (explicit shared-only
                fallback with independent vault grants). Exact bindings take precedence over either fallback; a channel may have
                only one enabled exact binding while one of them is message_root. Retired GitHub values remain readable.
            automation_kind (str | Unset): Repository automation strategy this binding runs. pull_request_review is the only
                supported value; empty on a Slack binding.
            channel_id (str | Unset): Slack channel scope. app_mention may be exact or an internal-only fallback; message
                and message_root require an exact channel; app_mention_ext_shared requires empty scope and is a separate shared-
                only fallback. Always empty on a GitHub binding.
            owner_key (str | Unset): Caller-owned stable identity for a binding managed by code, so its owner can recognise
                the binding after the channel or wake event changes. Absent on a binding made by hand. At most 128 characters of
                letters, digits, '.', '_', ':', '/', and '-'. Not unique: the owning code refuses ambiguity itself.
            repository (str | Unset): Provider-normalized GitHub repository name this binding automates. Empty on a Slack
                binding.
            repository_id (int | Unset): Immutable GitHub repository id matched against the delivered event, so a repository
                rename or transfer cannot redirect the automation. Zero on a Slack binding.
            vault_ids (list[str] | Unset): Vaults (UUIDs) granted to the woken session.
            wake_app_ids (list[str] | Unset): Slack source app ids (A…) whose top-level posts may start a session. Empty
                means app-authored roots never start work. Legal only on an exact-channel message_root binding.
     """

    agent_id: str
    binding_id: str
    capture_patch: bool
    connection_id: str
    enabled: bool
    environment_id: str
    include_drafts: bool
    organization_id: str
    provider: str
    publish_review: bool
    wake_event: str
    automation_kind: str | Unset = UNSET
    channel_id: str | Unset = UNSET
    owner_key: str | Unset = UNSET
    repository: str | Unset = UNSET
    repository_id: int | Unset = UNSET
    vault_ids: list[str] | Unset = UNSET
    wake_app_ids: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        agent_id = self.agent_id

        binding_id = self.binding_id

        capture_patch = self.capture_patch

        connection_id = self.connection_id

        enabled = self.enabled

        environment_id = self.environment_id

        include_drafts = self.include_drafts

        organization_id = self.organization_id

        provider = self.provider

        publish_review = self.publish_review

        wake_event = self.wake_event

        automation_kind = self.automation_kind

        channel_id = self.channel_id

        owner_key = self.owner_key

        repository = self.repository

        repository_id = self.repository_id

        vault_ids: list[str] | Unset = UNSET
        if not isinstance(self.vault_ids, Unset):
            vault_ids = self.vault_ids



        wake_app_ids: list[str] | Unset = UNSET
        if not isinstance(self.wake_app_ids, Unset):
            wake_app_ids = self.wake_app_ids




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "agent_id": agent_id,
            "binding_id": binding_id,
            "capture_patch": capture_patch,
            "connection_id": connection_id,
            "enabled": enabled,
            "environment_id": environment_id,
            "include_drafts": include_drafts,
            "organization_id": organization_id,
            "provider": provider,
            "publish_review": publish_review,
            "wake_event": wake_event,
        })
        if automation_kind is not UNSET:
            field_dict["automation_kind"] = automation_kind
        if channel_id is not UNSET:
            field_dict["channel_id"] = channel_id
        if owner_key is not UNSET:
            field_dict["owner_key"] = owner_key
        if repository is not UNSET:
            field_dict["repository"] = repository
        if repository_id is not UNSET:
            field_dict["repository_id"] = repository_id
        if vault_ids is not UNSET:
            field_dict["vault_ids"] = vault_ids
        if wake_app_ids is not UNSET:
            field_dict["wake_app_ids"] = wake_app_ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        agent_id = d.pop("agent_id")

        binding_id = d.pop("binding_id")

        capture_patch = d.pop("capture_patch")

        connection_id = d.pop("connection_id")

        enabled = d.pop("enabled")

        environment_id = d.pop("environment_id")

        include_drafts = d.pop("include_drafts")

        organization_id = d.pop("organization_id")

        provider = d.pop("provider")

        publish_review = d.pop("publish_review")

        wake_event = d.pop("wake_event")

        automation_kind = d.pop("automation_kind", UNSET)

        channel_id = d.pop("channel_id", UNSET)

        owner_key = d.pop("owner_key", UNSET)

        repository = d.pop("repository", UNSET)

        repository_id = d.pop("repository_id", UNSET)

        vault_ids = cast(list[str], d.pop("vault_ids", UNSET))


        wake_app_ids = cast(list[str], d.pop("wake_app_ids", UNSET))


        managed_agents_trigger_binding = cls(
            agent_id=agent_id,
            binding_id=binding_id,
            capture_patch=capture_patch,
            connection_id=connection_id,
            enabled=enabled,
            environment_id=environment_id,
            include_drafts=include_drafts,
            organization_id=organization_id,
            provider=provider,
            publish_review=publish_review,
            wake_event=wake_event,
            automation_kind=automation_kind,
            channel_id=channel_id,
            owner_key=owner_key,
            repository=repository,
            repository_id=repository_id,
            vault_ids=vault_ids,
            wake_app_ids=wake_app_ids,
        )


        managed_agents_trigger_binding.additional_properties = d
        return managed_agents_trigger_binding

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
