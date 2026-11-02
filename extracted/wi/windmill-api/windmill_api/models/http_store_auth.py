from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.http_store_auth_type import HttpStoreAuthType
from ..types import UNSET, Unset

T = TypeVar("T", bound="HttpStoreAuth")


@_attrs_define
class HttpStoreAuth:
    """
    Attributes:
        type (HttpStoreAuthType):
        header_name (Union[Unset, str]): StaticHeader and BearerTokenFile (default Authorization)
        header_value (Union[Unset, str]): StaticHeader
        token_path (Union[Unset, str]): BearerTokenFile
        prefix (Union[Unset, str]): BearerTokenFile (default "Bearer ")
        cert_path (Union[Unset, str]): ClientCertificate, PEM certificate optionally followed by its chain
        key_path (Union[Unset, str]): ClientCertificate, PEM private key
        reload_interval_secs (Union[Unset, int]): BearerTokenFile (default 60) and ClientCertificate (default 300)
    """

    type: HttpStoreAuthType
    header_name: Union[Unset, str] = UNSET
    header_value: Union[Unset, str] = UNSET
    token_path: Union[Unset, str] = UNSET
    prefix: Union[Unset, str] = UNSET
    cert_path: Union[Unset, str] = UNSET
    key_path: Union[Unset, str] = UNSET
    reload_interval_secs: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        header_name = self.header_name
        header_value = self.header_value
        token_path = self.token_path
        prefix = self.prefix
        cert_path = self.cert_path
        key_path = self.key_path
        reload_interval_secs = self.reload_interval_secs

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
            }
        )
        if header_name is not UNSET:
            field_dict["header_name"] = header_name
        if header_value is not UNSET:
            field_dict["header_value"] = header_value
        if token_path is not UNSET:
            field_dict["token_path"] = token_path
        if prefix is not UNSET:
            field_dict["prefix"] = prefix
        if cert_path is not UNSET:
            field_dict["cert_path"] = cert_path
        if key_path is not UNSET:
            field_dict["key_path"] = key_path
        if reload_interval_secs is not UNSET:
            field_dict["reload_interval_secs"] = reload_interval_secs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        type = HttpStoreAuthType(d.pop("type"))

        header_name = d.pop("header_name", UNSET)

        header_value = d.pop("header_value", UNSET)

        token_path = d.pop("token_path", UNSET)

        prefix = d.pop("prefix", UNSET)

        cert_path = d.pop("cert_path", UNSET)

        key_path = d.pop("key_path", UNSET)

        reload_interval_secs = d.pop("reload_interval_secs", UNSET)

        http_store_auth = cls(
            type=type,
            header_name=header_name,
            header_value=header_value,
            token_path=token_path,
            prefix=prefix,
            cert_path=cert_path,
            key_path=key_path,
            reload_interval_secs=reload_interval_secs,
        )

        http_store_auth.additional_properties = d
        return http_store_auth

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
