import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.dry_run_state_enum import DryRunStateEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="DryRun")


@_attrs_define
class DryRun:
    """
    Attributes:
        url (str):
        uuid (UUID):
        order_attributes (Any):
        order_type (str):
        state (DryRunStateEnum):
        get_state_display (str):
        output (str):
        created (datetime.datetime):
        order_offering (Union[None, Unset, str]):
    """

    url: str
    uuid: UUID
    order_attributes: Any
    order_type: str
    state: DryRunStateEnum
    get_state_display: str
    output: str
    created: datetime.datetime
    order_offering: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        order_attributes = self.order_attributes

        order_type = self.order_type

        state = self.state.value

        get_state_display = self.get_state_display

        output = self.output

        created = self.created.isoformat()

        order_offering: Union[None, Unset, str]
        if isinstance(self.order_offering, Unset):
            order_offering = UNSET
        else:
            order_offering = self.order_offering

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "order_attributes": order_attributes,
                "order_type": order_type,
                "state": state,
                "get_state_display": get_state_display,
                "output": output,
                "created": created,
            }
        )
        if order_offering is not UNSET:
            field_dict["order_offering"] = order_offering

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        order_attributes = d.pop("order_attributes")

        order_type = d.pop("order_type")

        state = DryRunStateEnum(d.pop("state"))

        get_state_display = d.pop("get_state_display")

        output = d.pop("output")

        created = isoparse(d.pop("created"))

        def _parse_order_offering(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        order_offering = _parse_order_offering(d.pop("order_offering", UNSET))

        dry_run = cls(
            url=url,
            uuid=uuid,
            order_attributes=order_attributes,
            order_type=order_type,
            state=state,
            get_state_display=get_state_display,
            output=output,
            created=created,
            order_offering=order_offering,
        )

        dry_run.additional_properties = d
        return dry_run

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
