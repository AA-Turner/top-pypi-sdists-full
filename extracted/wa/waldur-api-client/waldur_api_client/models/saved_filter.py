import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.saved_filter_filter_params import SavedFilterFilterParams


T = TypeVar("T", bound="SavedFilter")


@_attrs_define
class SavedFilter:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        filter_params (Union[Unset, SavedFilterFilterParams]): Saved filter parameters as JSON.
        is_shared (Union[Unset, bool]): If True, visible to all staff/support users.
    """

    url: str
    uuid: UUID
    name: str
    created: datetime.datetime
    modified: datetime.datetime
    filter_params: Union[Unset, "SavedFilterFilterParams"] = UNSET
    is_shared: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        filter_params: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.filter_params, Unset):
            filter_params = self.filter_params.to_dict()

        is_shared = self.is_shared

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "created": created,
                "modified": modified,
            }
        )
        if filter_params is not UNSET:
            field_dict["filter_params"] = filter_params
        if is_shared is not UNSET:
            field_dict["is_shared"] = is_shared

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.saved_filter_filter_params import SavedFilterFilterParams

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        _filter_params = d.pop("filter_params", UNSET)
        filter_params: Union[Unset, SavedFilterFilterParams]
        if isinstance(_filter_params, Unset):
            filter_params = UNSET
        else:
            filter_params = SavedFilterFilterParams.from_dict(_filter_params)

        is_shared = d.pop("is_shared", UNSET)

        saved_filter = cls(
            url=url,
            uuid=uuid,
            name=name,
            created=created,
            modified=modified,
            filter_params=filter_params,
            is_shared=is_shared,
        )

        saved_filter.additional_properties = d
        return saved_filter

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
