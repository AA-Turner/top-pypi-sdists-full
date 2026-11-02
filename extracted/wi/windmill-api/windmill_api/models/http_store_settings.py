from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.http_store_settings_path_encoding import HttpStoreSettingsPathEncoding
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.http_store_settings_auth import HttpStoreSettingsAuth
    from ..models.http_store_settings_extra_headers import HttpStoreSettingsExtraHeaders
    from ..models.http_store_settings_read import HttpStoreSettingsRead


T = TypeVar("T", bound="HttpStoreSettings")


@_attrs_define
class HttpStoreSettings:
    """Read-only secret backend for any secret store with an HTTP API. A secret variable saved with an empty value
    references the store key derived from its workspace and path.

        Attributes:
            base_url (str): Scheme, host and optional path prefix of the store
            read (HttpStoreSettingsRead):
            auth (HttpStoreSettingsAuth):
            path_encoding (Union[Unset, HttpStoreSettingsPathEncoding]): How a variable path becomes a store key (default
                url)
            extra_headers (Union[Unset, HttpStoreSettingsExtraHeaders]):
            ca_bundle_path (Union[Unset, str]): PEM bundle of additional CA certificates trusted for the store
            timeout_secs (Union[Unset, int]):
            skip_ssl_verify (Union[Unset, bool]):
    """

    base_url: str
    read: "HttpStoreSettingsRead"
    auth: "HttpStoreSettingsAuth"
    path_encoding: Union[Unset, HttpStoreSettingsPathEncoding] = UNSET
    extra_headers: Union[Unset, "HttpStoreSettingsExtraHeaders"] = UNSET
    ca_bundle_path: Union[Unset, str] = UNSET
    timeout_secs: Union[Unset, int] = UNSET
    skip_ssl_verify: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        base_url = self.base_url
        read = self.read.to_dict()

        auth = self.auth.to_dict()

        path_encoding: Union[Unset, str] = UNSET
        if not isinstance(self.path_encoding, Unset):
            path_encoding = self.path_encoding.value

        extra_headers: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.extra_headers, Unset):
            extra_headers = self.extra_headers.to_dict()

        ca_bundle_path = self.ca_bundle_path
        timeout_secs = self.timeout_secs
        skip_ssl_verify = self.skip_ssl_verify

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "base_url": base_url,
                "read": read,
                "auth": auth,
            }
        )
        if path_encoding is not UNSET:
            field_dict["path_encoding"] = path_encoding
        if extra_headers is not UNSET:
            field_dict["extra_headers"] = extra_headers
        if ca_bundle_path is not UNSET:
            field_dict["ca_bundle_path"] = ca_bundle_path
        if timeout_secs is not UNSET:
            field_dict["timeout_secs"] = timeout_secs
        if skip_ssl_verify is not UNSET:
            field_dict["skip_ssl_verify"] = skip_ssl_verify

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.http_store_settings_auth import HttpStoreSettingsAuth
        from ..models.http_store_settings_extra_headers import HttpStoreSettingsExtraHeaders
        from ..models.http_store_settings_read import HttpStoreSettingsRead

        d = src_dict.copy()
        base_url = d.pop("base_url")

        read = HttpStoreSettingsRead.from_dict(d.pop("read"))

        auth = HttpStoreSettingsAuth.from_dict(d.pop("auth"))

        _path_encoding = d.pop("path_encoding", UNSET)
        path_encoding: Union[Unset, HttpStoreSettingsPathEncoding]
        if isinstance(_path_encoding, Unset):
            path_encoding = UNSET
        else:
            path_encoding = HttpStoreSettingsPathEncoding(_path_encoding)

        _extra_headers = d.pop("extra_headers", UNSET)
        extra_headers: Union[Unset, HttpStoreSettingsExtraHeaders]
        if isinstance(_extra_headers, Unset):
            extra_headers = UNSET
        else:
            extra_headers = HttpStoreSettingsExtraHeaders.from_dict(_extra_headers)

        ca_bundle_path = d.pop("ca_bundle_path", UNSET)

        timeout_secs = d.pop("timeout_secs", UNSET)

        skip_ssl_verify = d.pop("skip_ssl_verify", UNSET)

        http_store_settings = cls(
            base_url=base_url,
            read=read,
            auth=auth,
            path_encoding=path_encoding,
            extra_headers=extra_headers,
            ca_bundle_path=ca_bundle_path,
            timeout_secs=timeout_secs,
            skip_ssl_verify=skip_ssl_verify,
        )

        http_store_settings.additional_properties = d
        return http_store_settings

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
