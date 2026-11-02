from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AwsSecretsManagerSettings")


@_attrs_define
class AwsSecretsManagerSettings:
    """
    Attributes:
        region (str): AWS region (e.g., us-east-1)
        access_key_id (Union[Unset, str]): AWS Access Key ID (optional, uses default credential chain if not provided)
        secret_access_key (Union[Unset, str]): AWS Secret Access Key (optional)
        endpoint_url (Union[Unset, str]): Custom endpoint URL for testing (e.g., LocalStack)
        prefix (Union[Unset, str]): Prefix for secret names (e.g., windmill/)
    """

    region: str
    access_key_id: Union[Unset, str] = UNSET
    secret_access_key: Union[Unset, str] = UNSET
    endpoint_url: Union[Unset, str] = UNSET
    prefix: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        region = self.region
        access_key_id = self.access_key_id
        secret_access_key = self.secret_access_key
        endpoint_url = self.endpoint_url
        prefix = self.prefix

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "region": region,
            }
        )
        if access_key_id is not UNSET:
            field_dict["access_key_id"] = access_key_id
        if secret_access_key is not UNSET:
            field_dict["secret_access_key"] = secret_access_key
        if endpoint_url is not UNSET:
            field_dict["endpoint_url"] = endpoint_url
        if prefix is not UNSET:
            field_dict["prefix"] = prefix

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        region = d.pop("region")

        access_key_id = d.pop("access_key_id", UNSET)

        secret_access_key = d.pop("secret_access_key", UNSET)

        endpoint_url = d.pop("endpoint_url", UNSET)

        prefix = d.pop("prefix", UNSET)

        aws_secrets_manager_settings = cls(
            region=region,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            endpoint_url=endpoint_url,
            prefix=prefix,
        )

        aws_secrets_manager_settings.additional_properties = d
        return aws_secrets_manager_settings

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
