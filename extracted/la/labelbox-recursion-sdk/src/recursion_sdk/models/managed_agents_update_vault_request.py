from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_update_vault_request_metadata import ManagedAgentsUpdateVaultRequestMetadata





T = TypeVar("T", bound="ManagedAgentsUpdateVaultRequest")



@_attrs_define
class ManagedAgentsUpdateVaultRequest:
    """ Request body for updating a vault's label or metadata. Every field is optional; omitted fields keep their current
    value.

        Example:
            {'display_name': 'example-name', 'metadata': {'key': 'example'}}

        Attributes:
            display_name (str | Unset): Replacement operator-facing label. Omit to keep the current one.
            metadata (ManagedAgentsUpdateVaultRequestMetadata | Unset): Replacement free-form caller-owned JSON. Sent as a
                whole object, not merged; omit to keep the current value.
     """

    display_name: str | Unset = UNSET
    metadata: ManagedAgentsUpdateVaultRequestMetadata | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_update_vault_request_metadata import ManagedAgentsUpdateVaultRequestMetadata # noqa: PLC0415
        display_name = self.display_name

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if display_name is not UNSET:
            field_dict["display_name"] = display_name
        if metadata is not UNSET:
            field_dict["metadata"] = metadata

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_update_vault_request_metadata import ManagedAgentsUpdateVaultRequestMetadata # noqa: PLC0415
        d = dict(src_dict)
        display_name = d.pop("display_name", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsUpdateVaultRequestMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsUpdateVaultRequestMetadata.from_dict(_metadata)




        managed_agents_update_vault_request = cls(
            display_name=display_name,
            metadata=metadata,
        )


        managed_agents_update_vault_request.additional_properties = d
        return managed_agents_update_vault_request

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
