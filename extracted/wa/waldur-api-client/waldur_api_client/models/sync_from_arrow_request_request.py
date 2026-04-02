from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SyncFromArrowRequestRequest")


@_attrs_define
class SyncFromArrowRequestRequest:
    """
    Attributes:
        settings_uuid (Union[Unset, UUID]):
    """

    settings_uuid: Union[Unset, UUID] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        settings_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.settings_uuid, Unset):
            settings_uuid = str(self.settings_uuid)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if settings_uuid is not UNSET:
            field_dict["settings_uuid"] = settings_uuid

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _settings_uuid = d.pop("settings_uuid", UNSET)
        settings_uuid: Union[Unset, UUID]
        if isinstance(_settings_uuid, Unset):
            settings_uuid = UNSET
        else:
            settings_uuid = UUID(_settings_uuid)

        sync_from_arrow_request_request = cls(
            settings_uuid=settings_uuid,
        )

        sync_from_arrow_request_request.additional_properties = d
        return sync_from_arrow_request_request

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
