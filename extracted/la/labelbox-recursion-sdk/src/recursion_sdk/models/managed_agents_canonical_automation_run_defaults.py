from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_automation_definition_credential_ref import ManagedAgentsAutomationDefinitionCredentialRef
  from ..models.managed_agents_automation_definition_memory_store import ManagedAgentsAutomationDefinitionMemoryStore
  from ..models.managed_agents_automation_definition_resource import ManagedAgentsAutomationDefinitionResource
  from ..models.managed_agents_canonical_automation_run_defaults_metadata_type_0 import ManagedAgentsCanonicalAutomationRunDefaultsMetadataType0





T = TypeVar("T", bound="ManagedAgentsCanonicalAutomationRunDefaults")



@_attrs_define
class ManagedAgentsCanonicalAutomationRunDefaults:
    """ Session metadata, credential grants, files and memory applied to every trigger and manual admission.

        Example:
            {'credentialRefs': [{'credentialId': 'example', 'vaultId': 'example'}], 'memoryStores': [{'access': 'read_only',
                'instructions': 'example', 'memoryStoreId': 'example'}], 'metadata': {'key': 'example'}, 'resources':
                [{'fileId': 'example', 'mountPath': 'example'}], 'vaultIds': ['example']}

        Attributes:
            metadata (ManagedAgentsCanonicalAutomationRunDefaultsMetadataType0 | None): String metadata copied to every
                admitted session.
            credential_refs (list[ManagedAgentsAutomationDefinitionCredentialRef] | Unset): Exact credential selection
                within vaultIds. Requires explicit vaultIds. Omit to grant all items in the selected vaults.
            memory_stores (list[ManagedAgentsAutomationDefinitionMemoryStore] | Unset): Additional memory stores attached at
                session start, alongside the agent memory store.
            resources (list[ManagedAgentsAutomationDefinitionResource] | Unset): Files resolved and mounted when each
                session starts.
            vault_ids (list[str] | Unset): Vaults available to each session. Omit to inherit the pinned agent defaults; an
                empty list grants no vault access.
     """

    metadata: ManagedAgentsCanonicalAutomationRunDefaultsMetadataType0 | None
    credential_refs: list[ManagedAgentsAutomationDefinitionCredentialRef] | Unset = UNSET
    memory_stores: list[ManagedAgentsAutomationDefinitionMemoryStore] | Unset = UNSET
    resources: list[ManagedAgentsAutomationDefinitionResource] | Unset = UNSET
    vault_ids: list[str] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_automation_definition_credential_ref import ManagedAgentsAutomationDefinitionCredentialRef # noqa: PLC0415
        from ..models.managed_agents_automation_definition_memory_store import ManagedAgentsAutomationDefinitionMemoryStore # noqa: PLC0415
        from ..models.managed_agents_automation_definition_resource import ManagedAgentsAutomationDefinitionResource # noqa: PLC0415
        from ..models.managed_agents_canonical_automation_run_defaults_metadata_type_0 import ManagedAgentsCanonicalAutomationRunDefaultsMetadataType0 # noqa: PLC0415
        metadata: dict[str, Any] | None
        if isinstance(self.metadata, ManagedAgentsCanonicalAutomationRunDefaultsMetadataType0):
            metadata = self.metadata.to_dict()
        else:
            metadata = self.metadata

        credential_refs: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.credential_refs, Unset):
            credential_refs = []
            for credential_refs_item_data in self.credential_refs:
                credential_refs_item = credential_refs_item_data.to_dict()
                credential_refs.append(credential_refs_item)



        memory_stores: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.memory_stores, Unset):
            memory_stores = []
            for memory_stores_item_data in self.memory_stores:
                memory_stores_item = memory_stores_item_data.to_dict()
                memory_stores.append(memory_stores_item)



        resources: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.resources, Unset):
            resources = []
            for resources_item_data in self.resources:
                resources_item = resources_item_data.to_dict()
                resources.append(resources_item)



        vault_ids: list[str] | Unset = UNSET
        if not isinstance(self.vault_ids, Unset):
            vault_ids = self.vault_ids




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "metadata": metadata,
        })
        if credential_refs is not UNSET:
            field_dict["credentialRefs"] = credential_refs
        if memory_stores is not UNSET:
            field_dict["memoryStores"] = memory_stores
        if resources is not UNSET:
            field_dict["resources"] = resources
        if vault_ids is not UNSET:
            field_dict["vaultIds"] = vault_ids

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_automation_definition_credential_ref import ManagedAgentsAutomationDefinitionCredentialRef # noqa: PLC0415
        from ..models.managed_agents_automation_definition_memory_store import ManagedAgentsAutomationDefinitionMemoryStore # noqa: PLC0415
        from ..models.managed_agents_automation_definition_resource import ManagedAgentsAutomationDefinitionResource # noqa: PLC0415
        from ..models.managed_agents_canonical_automation_run_defaults_metadata_type_0 import ManagedAgentsCanonicalAutomationRunDefaultsMetadataType0 # noqa: PLC0415
        d = dict(src_dict)
        def _parse_metadata(data: object) -> ManagedAgentsCanonicalAutomationRunDefaultsMetadataType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                metadata_type_0 = ManagedAgentsCanonicalAutomationRunDefaultsMetadataType0.from_dict(data)



                return metadata_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ManagedAgentsCanonicalAutomationRunDefaultsMetadataType0 | None, data)

        metadata = _parse_metadata(d.pop("metadata"))


        _credential_refs = d.pop("credentialRefs", UNSET)
        credential_refs: list[ManagedAgentsAutomationDefinitionCredentialRef] | Unset = UNSET
        if _credential_refs is not UNSET:
            credential_refs = []
            for credential_refs_item_data in _credential_refs:
                credential_refs_item = ManagedAgentsAutomationDefinitionCredentialRef.from_dict(credential_refs_item_data)



                credential_refs.append(credential_refs_item)


        _memory_stores = d.pop("memoryStores", UNSET)
        memory_stores: list[ManagedAgentsAutomationDefinitionMemoryStore] | Unset = UNSET
        if _memory_stores is not UNSET:
            memory_stores = []
            for memory_stores_item_data in _memory_stores:
                memory_stores_item = ManagedAgentsAutomationDefinitionMemoryStore.from_dict(memory_stores_item_data)



                memory_stores.append(memory_stores_item)


        _resources = d.pop("resources", UNSET)
        resources: list[ManagedAgentsAutomationDefinitionResource] | Unset = UNSET
        if _resources is not UNSET:
            resources = []
            for resources_item_data in _resources:
                resources_item = ManagedAgentsAutomationDefinitionResource.from_dict(resources_item_data)



                resources.append(resources_item)


        vault_ids = cast(list[str], d.pop("vaultIds", UNSET))


        managed_agents_canonical_automation_run_defaults = cls(
            metadata=metadata,
            credential_refs=credential_refs,
            memory_stores=memory_stores,
            resources=resources,
            vault_ids=vault_ids,
        )

        return managed_agents_canonical_automation_run_defaults

