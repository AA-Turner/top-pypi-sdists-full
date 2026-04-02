from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GoogleCalendar")


@_attrs_define
class GoogleCalendar:
    """
    Attributes:
        backend_id (Union[None, Unset, str]):
        public (Union[Unset, bool]):
        http_link (Union[Unset, str]):
    """

    backend_id: Union[None, Unset, str] = UNSET
    public: Union[Unset, bool] = UNSET
    http_link: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        backend_id: Union[None, Unset, str]
        if isinstance(self.backend_id, Unset):
            backend_id = UNSET
        else:
            backend_id = self.backend_id

        public = self.public

        http_link = self.http_link

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if public is not UNSET:
            field_dict["public"] = public
        if http_link is not UNSET:
            field_dict["http_link"] = http_link

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_backend_id(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        backend_id = _parse_backend_id(d.pop("backend_id", UNSET))

        public = d.pop("public", UNSET)

        http_link = d.pop("http_link", UNSET)

        google_calendar = cls(
            backend_id=backend_id,
            public=public,
            http_link=http_link,
        )

        google_calendar.additional_properties = d
        return google_calendar

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
