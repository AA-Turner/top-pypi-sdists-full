from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="MigrateSecretsToDatabaseJsonBody")


@_attrs_define
class MigrateSecretsToDatabaseJsonBody:
    """
    Attributes:
        address (str): HashiCorp Vault server address (e.g., https://vault.company.com:8200)
        mount_path (str): KV v2 secrets engine mount path (e.g., windmill)
        kv_secret_path_prefix (Union[Unset, str]): Optional path prefix inserted between the KV data/metadata segment
            and the workspace id (e.g., "apps/windmill"). When set, secrets are stored at
            `<mount>/data/<prefix>/<workspace>/<secret>`, allowing a Vault policy scoped to exactly
            `<mount>/data/<prefix>/*`.
        jwt_role (Union[Unset, str]): Vault JWT auth role name for Windmill (optional, if not provided token auth is
            used)
        jwt_mount_path (Union[Unset, str]): Mount path for the JWT auth method in Vault (optional, defaults to "jwt").
            Set this when the JWT auth method is mounted at a non-default path, e.g. via `vault auth enable -path=<mount>
            jwt`.
        namespace (Union[Unset, str]): Vault Enterprise namespace (optional)
        token (Union[Unset, str]): Static Vault token for testing/development (optional, if provided this is used
            instead of JWT authentication)
        skip_ssl_verify (Union[Unset, bool]): Skip TLS certificate verification when connecting to Vault. Only use for
            self-signed certificates in development environments.
    """

    address: str
    mount_path: str
    kv_secret_path_prefix: Union[Unset, str] = UNSET
    jwt_role: Union[Unset, str] = UNSET
    jwt_mount_path: Union[Unset, str] = UNSET
    namespace: Union[Unset, str] = UNSET
    token: Union[Unset, str] = UNSET
    skip_ssl_verify: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        address = self.address
        mount_path = self.mount_path
        kv_secret_path_prefix = self.kv_secret_path_prefix
        jwt_role = self.jwt_role
        jwt_mount_path = self.jwt_mount_path
        namespace = self.namespace
        token = self.token
        skip_ssl_verify = self.skip_ssl_verify

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "address": address,
                "mount_path": mount_path,
            }
        )
        if kv_secret_path_prefix is not UNSET:
            field_dict["kv_secret_path_prefix"] = kv_secret_path_prefix
        if jwt_role is not UNSET:
            field_dict["jwt_role"] = jwt_role
        if jwt_mount_path is not UNSET:
            field_dict["jwt_mount_path"] = jwt_mount_path
        if namespace is not UNSET:
            field_dict["namespace"] = namespace
        if token is not UNSET:
            field_dict["token"] = token
        if skip_ssl_verify is not UNSET:
            field_dict["skip_ssl_verify"] = skip_ssl_verify

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        address = d.pop("address")

        mount_path = d.pop("mount_path")

        kv_secret_path_prefix = d.pop("kv_secret_path_prefix", UNSET)

        jwt_role = d.pop("jwt_role", UNSET)

        jwt_mount_path = d.pop("jwt_mount_path", UNSET)

        namespace = d.pop("namespace", UNSET)

        token = d.pop("token", UNSET)

        skip_ssl_verify = d.pop("skip_ssl_verify", UNSET)

        migrate_secrets_to_database_json_body = cls(
            address=address,
            mount_path=mount_path,
            kv_secret_path_prefix=kv_secret_path_prefix,
            jwt_role=jwt_role,
            jwt_mount_path=jwt_mount_path,
            namespace=namespace,
            token=token,
            skip_ssl_verify=skip_ssl_verify,
        )

        migrate_secrets_to_database_json_body.additional_properties = d
        return migrate_secrets_to_database_json_body

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
