from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestTypeAdmin")


@_attrs_define
class RequestTypeAdmin:
    """
    Attributes:
        url (str):
        uuid (UUID):
        name (str):
        issue_type_name (str):
        backend_id (Union[None, int]): Backend ID for synced types. Null for manually created types.
        backend_name (Union[None, str]):
        is_synced (bool): Returns True if the request type was synced from a backend.
        is_active (Union[Unset, bool]): Whether this request type is available for issue creation.
        order (Union[Unset, int]): Display order. First type (lowest order) is the default.
    """

    url: str
    uuid: UUID
    name: str
    issue_type_name: str
    backend_id: Union[None, int]
    backend_name: Union[None, str]
    is_synced: bool
    is_active: Union[Unset, bool] = UNSET
    order: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        name = self.name

        issue_type_name = self.issue_type_name

        backend_id: Union[None, int]
        backend_id = self.backend_id

        backend_name: Union[None, str]
        backend_name = self.backend_name

        is_synced = self.is_synced

        is_active = self.is_active

        order = self.order

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "name": name,
                "issue_type_name": issue_type_name,
                "backend_id": backend_id,
                "backend_name": backend_name,
                "is_synced": is_synced,
            }
        )
        if is_active is not UNSET:
            field_dict["is_active"] = is_active
        if order is not UNSET:
            field_dict["order"] = order

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        name = d.pop("name")

        issue_type_name = d.pop("issue_type_name")

        def _parse_backend_id(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        backend_id = _parse_backend_id(d.pop("backend_id"))

        def _parse_backend_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        backend_name = _parse_backend_name(d.pop("backend_name"))

        is_synced = d.pop("is_synced")

        is_active = d.pop("is_active", UNSET)

        order = d.pop("order", UNSET)

        request_type_admin = cls(
            url=url,
            uuid=uuid,
            name=name,
            issue_type_name=issue_type_name,
            backend_id=backend_id,
            backend_name=backend_name,
            is_synced=is_synced,
            is_active=is_active,
            order=order,
        )

        request_type_admin.additional_properties = d
        return request_type_admin

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
