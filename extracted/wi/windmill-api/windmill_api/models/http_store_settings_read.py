from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.http_store_settings_read_value_encoding import HttpStoreSettingsReadValueEncoding
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.http_store_settings_read_query import HttpStoreSettingsReadQuery


T = TypeVar("T", bound="HttpStoreSettingsRead")


@_attrs_define
class HttpStoreSettingsRead:
    """
    Attributes:
        path (str): Path template appended to base_url. {workspace} and {path} must each appear here or in a query
            value.
        query (Union[Unset, HttpStoreSettingsReadQuery]): Query parameters; values may use {workspace} and {path}
        value_pointer (Union[Unset, str]): JSON pointer to the value in the response; empty means the whole body
        value_encoding (Union[Unset, HttpStoreSettingsReadValueEncoding]):
    """

    path: str
    query: Union[Unset, "HttpStoreSettingsReadQuery"] = UNSET
    value_pointer: Union[Unset, str] = UNSET
    value_encoding: Union[Unset, HttpStoreSettingsReadValueEncoding] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        query: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.query, Unset):
            query = self.query.to_dict()

        value_pointer = self.value_pointer
        value_encoding: Union[Unset, str] = UNSET
        if not isinstance(self.value_encoding, Unset):
            value_encoding = self.value_encoding.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
            }
        )
        if query is not UNSET:
            field_dict["query"] = query
        if value_pointer is not UNSET:
            field_dict["value_pointer"] = value_pointer
        if value_encoding is not UNSET:
            field_dict["value_encoding"] = value_encoding

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.http_store_settings_read_query import HttpStoreSettingsReadQuery

        d = src_dict.copy()
        path = d.pop("path")

        _query = d.pop("query", UNSET)
        query: Union[Unset, HttpStoreSettingsReadQuery]
        if isinstance(_query, Unset):
            query = UNSET
        else:
            query = HttpStoreSettingsReadQuery.from_dict(_query)

        value_pointer = d.pop("value_pointer", UNSET)

        _value_encoding = d.pop("value_encoding", UNSET)
        value_encoding: Union[Unset, HttpStoreSettingsReadValueEncoding]
        if isinstance(_value_encoding, Unset):
            value_encoding = UNSET
        else:
            value_encoding = HttpStoreSettingsReadValueEncoding(_value_encoding)

        http_store_settings_read = cls(
            path=path,
            query=query,
            value_pointer=value_pointer,
            value_encoding=value_encoding,
        )

        http_store_settings_read.additional_properties = d
        return http_store_settings_read

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
