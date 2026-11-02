from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AzureKeyVaultSettings")


@_attrs_define
class AzureKeyVaultSettings:
    """
    Attributes:
        vault_url (str): Azure Key Vault URL (e.g., https://myvault.vault.azure.net)
        tenant_id (str): Azure AD tenant ID
        client_id (str): Azure AD application (client) ID
        client_secret (Union[Unset, str]): Azure AD client secret. Optional — when omitted, the integration falls back
            to Azure Workload Identity Federation, exchanging the Kubernetes-projected service-account JWT at
            AZURE_FEDERATED_TOKEN_FILE for an access token (no long-lived secret stored).
        token (Union[Unset, str]): Static Bearer token for testing/development (optional, if provided this is used
            instead of OAuth2 authentication)
    """

    vault_url: str
    tenant_id: str
    client_id: str
    client_secret: Union[Unset, str] = UNSET
    token: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        vault_url = self.vault_url
        tenant_id = self.tenant_id
        client_id = self.client_id
        client_secret = self.client_secret
        token = self.token

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "vault_url": vault_url,
                "tenant_id": tenant_id,
                "client_id": client_id,
            }
        )
        if client_secret is not UNSET:
            field_dict["client_secret"] = client_secret
        if token is not UNSET:
            field_dict["token"] = token

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        vault_url = d.pop("vault_url")

        tenant_id = d.pop("tenant_id")

        client_id = d.pop("client_id")

        client_secret = d.pop("client_secret", UNSET)

        token = d.pop("token", UNSET)

        azure_key_vault_settings = cls(
            vault_url=vault_url,
            tenant_id=tenant_id,
            client_id=client_id,
            client_secret=client_secret,
            token=token,
        )

        azure_key_vault_settings.additional_properties = d
        return azure_key_vault_settings

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
