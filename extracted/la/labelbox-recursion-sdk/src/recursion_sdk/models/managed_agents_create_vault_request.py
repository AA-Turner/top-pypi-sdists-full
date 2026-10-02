from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_create_vault_request_metadata import ManagedAgentsCreateVaultRequestMetadata





T = TypeVar("T", bound="ManagedAgentsCreateVaultRequest")



@_attrs_define
class ManagedAgentsCreateVaultRequest:
    """ Request body for creating a vault: the container that credentials are added to and that sessions are granted.
    Creating a vault stores no secret material of its own.

        Example:
            {'display_name': 'example-name', 'idempotency_key': 'example', 'metadata': {'key': 'example'}}

        Attributes:
            display_name (str): Operator-facing label for the vault, shown wherever grants are reviewed. Required.
            idempotency_key (str | Unset): Optional retry key scoped to the authenticated organization. Reusing it with
                different creation details is a conflict.
            metadata (ManagedAgentsCreateVaultRequestMetadata | Unset): Free-form caller-owned JSON stored with the vault
                and returned on reads. Not interpreted by the service; never put secret material here.
     """

    display_name: str
    idempotency_key: str | Unset = UNSET
    metadata: ManagedAgentsCreateVaultRequestMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_create_vault_request_metadata import ManagedAgentsCreateVaultRequestMetadata # noqa: PLC0415
        display_name = self.display_name

        idempotency_key = self.idempotency_key

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "display_name": display_name,
        })
        if idempotency_key is not UNSET:
            field_dict["idempotency_key"] = idempotency_key
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_create_vault_request_metadata import ManagedAgentsCreateVaultRequestMetadata # noqa: PLC0415
        d = dict(src_dict)
        display_name = d.pop("display_name")

        idempotency_key = d.pop("idempotency_key", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsCreateVaultRequestMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsCreateVaultRequestMetadata.from_dict(_metadata)




        managed_agents_create_vault_request = cls(
            display_name=display_name,
            idempotency_key=idempotency_key,
            metadata=metadata,
        )


        managed_agents_create_vault_request.additional_properties = d
        return managed_agents_create_vault_request

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
