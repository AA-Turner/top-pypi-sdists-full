from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.flag_bulk_item_type import check_flag_bulk_item_type
from ..models.flag_bulk_item_type import FlagBulkItemType
from typing import cast


T = TypeVar("T", bound="FlagBulkItem")


@_attrs_define
class FlagBulkItem:
    """One flag declaration reported by an SDK during bulk registration.

    Example:
        {'default': False, 'environment': 'production', 'id': 'dark-mode', 'service': 'api-gateway', 'type': 'BOOLEAN'}

    Attributes:
        id (str): Flag key as declared in code. URL-safe and stable for the lifetime of the flag.
        type_ (FlagBulkItemType): Value type the SDK declared for the flag. Accepted case-insensitively.
        default (Any): Default value the SDK declared for the flag. Used to create the flag if it does not already
            exist.
        service (None | str | Unset): Service reporting the declaration. Defaults to `unknown`.
        environment (None | str | Unset): Environment reporting the declaration. Defaults to `unknown`.
    """

    id: str
    type_: FlagBulkItemType
    default: Any
    service: None | str | Unset = UNSET
    environment: None | str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_: str = self.type_

        default = self.default

        service: None | str | Unset
        if isinstance(self.service, Unset):
            service = UNSET
        else:
            service = self.service

        environment: None | str | Unset
        if isinstance(self.environment, Unset):
            environment = UNSET
        else:
            environment = self.environment

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
                "default": default,
            }
        )
        if service is not UNSET:
            field_dict["service"] = service
        if environment is not UNSET:
            field_dict["environment"] = environment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        type_ = check_flag_bulk_item_type(d.pop("type"))

        default = d.pop("default")

        def _parse_service(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        service = _parse_service(d.pop("service", UNSET))

        def _parse_environment(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        environment = _parse_environment(d.pop("environment", UNSET))

        flag_bulk_item = cls(
            id=id,
            type_=type_,
            default=default,
            service=service,
            environment=environment,
        )

        flag_bulk_item.additional_properties = d
        return flag_bulk_item

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
