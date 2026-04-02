import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.order_update_request_limits import OrderUpdateRequestLimits


T = TypeVar("T", bound="OrderUpdateRequest")


@_attrs_define
class OrderUpdateRequest:
    """
    Attributes:
        limits (Union[Unset, OrderUpdateRequestLimits]):
        attributes (Union[Unset, Any]):
        start_date (Union[None, Unset, datetime.date]): Enables delayed processing of resource provisioning order.
    """

    limits: Union[Unset, "OrderUpdateRequestLimits"] = UNSET
    attributes: Union[Unset, Any] = UNSET
    start_date: Union[None, Unset, datetime.date] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        attributes = self.attributes

        start_date: Union[None, Unset, str]
        if isinstance(self.start_date, Unset):
            start_date = UNSET
        elif isinstance(self.start_date, datetime.date):
            start_date = self.start_date.isoformat()
        else:
            start_date = self.start_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if limits is not UNSET:
            field_dict["limits"] = limits
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if start_date is not UNSET:
            field_dict["start_date"] = start_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.order_update_request_limits import OrderUpdateRequestLimits

        d = dict(src_dict)
        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, OrderUpdateRequestLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = OrderUpdateRequestLimits.from_dict(_limits)

        attributes = d.pop("attributes", UNSET)

        def _parse_start_date(data: object) -> Union[None, Unset, datetime.date]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                start_date_type_0 = isoparse(data).date()

                return start_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.date], data)

        start_date = _parse_start_date(d.pop("start_date", UNSET))

        order_update_request = cls(
            limits=limits,
            attributes=attributes,
            start_date=start_date,
        )

        order_update_request.additional_properties = d
        return order_update_request

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
