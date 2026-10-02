from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_vault import ManagedAgentsVault





T = TypeVar("T", bound="ManagedAgentsVaultListResponse")



@_attrs_define
class ManagedAgentsVaultListResponse:
    """ Response body of GET /v1/vaults. A vault is the grantable unit of credential access: the vault_ids passed when
    starting a session decide which credentials that session may use. This lists the containers only; use GET
    /v1/vaults/{vault_id}/credentials for contents.

        Example:
            {'vaults': [{'created_at': '2026-02-18T09:30:00Z', 'credential_count': 1, 'display_name': 'example-name',
                'metadata': {'key': 'example'}, 'organization_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'updated_at':
                '2026-02-18T09:30:00Z', 'vault_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d'}]}

        Attributes:
            vaults (list[ManagedAgentsVault] | None): Every vault in the caller's organization, newest first. Null rather
                than an empty array when the organization has no vaults. Soft-deleted vaults are omitted.
     """

    vaults: list[ManagedAgentsVault] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_vault import ManagedAgentsVault # noqa: PLC0415
        vaults: list[dict[str, Any]] | None
        if isinstance(self.vaults, list):
            vaults = []
            for vaults_type_0_item_data in self.vaults:
                vaults_type_0_item = vaults_type_0_item_data.to_dict()
                vaults.append(vaults_type_0_item)


        else:
            vaults = self.vaults


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "vaults": vaults,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_vault import ManagedAgentsVault # noqa: PLC0415
        d = dict(src_dict)
        def _parse_vaults(data: object) -> list[ManagedAgentsVault] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                vaults_type_0 = []
                _vaults_type_0 = data
                for vaults_type_0_item_data in (_vaults_type_0):
                    vaults_type_0_item = ManagedAgentsVault.from_dict(vaults_type_0_item_data)



                    vaults_type_0.append(vaults_type_0_item)

                return vaults_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsVault] | None, data)

        vaults = _parse_vaults(d.pop("vaults"))


        managed_agents_vault_list_response = cls(
            vaults=vaults,
        )


        managed_agents_vault_list_response.additional_properties = d
        return managed_agents_vault_list_response

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
