from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MigrateSecretsToVaultJsonBody")


@_attrs_define
class MigrateSecretsToVaultJsonBody:
    """
    Attributes:
        address (str): HashiCorp Vault server address (e.g., https://vault.company.com:8200)
        mount_path (str): KV v2 secrets engine mount path (e.g., windmill)
        jwt_role (Union[Unset, str]): Vault JWT auth role name for Windmill (optional, if not provided token auth is
            used)
        namespace (Union[Unset, str]): Vault Enterprise namespace (optional)
        token (Union[Unset, str]): Static Vault token for testing/development (optional, if provided this is used
            instead of JWT authentication)
    """

    address: str
    mount_path: str
    jwt_role: Union[Unset, str] = UNSET
    namespace: Union[Unset, str] = UNSET
    token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address = self.address
        mount_path = self.mount_path
        jwt_role = self.jwt_role
        namespace = self.namespace
        token = self.token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address": address,
                "mount_path": mount_path,
            }
        )
        if jwt_role is not UNSET:
            field_dict["jwt_role"] = jwt_role
        if namespace is not UNSET:
            field_dict["namespace"] = namespace
        if token is not UNSET:
            field_dict["token"] = token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address = d.pop("address")

        mount_path = d.pop("mount_path")

        jwt_role = d.pop("jwt_role", UNSET)

        namespace = d.pop("namespace", UNSET)

        token = d.pop("token", UNSET)

        migrate_secrets_to_vault_json_body = cls(
            address=address,
            mount_path=mount_path,
            jwt_role=jwt_role,
            namespace=namespace,
            token=token,
        )

        migrate_secrets_to_vault_json_body.additional_properties = d
        return migrate_secrets_to_vault_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
