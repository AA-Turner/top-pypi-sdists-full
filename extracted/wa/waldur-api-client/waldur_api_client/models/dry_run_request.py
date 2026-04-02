from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.dry_run_type_enum import DryRunTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="DryRunRequest")


@_attrs_define
class DryRunRequest:
    """
    Attributes:
        plan (Union[None, Unset, str]):
        type_ (Union[Unset, DryRunTypeEnum]):  Default: DryRunTypeEnum.CREATE.
        attributes (Union[Unset, Any]):
        order_offering (Union[None, Unset, str]):
    """

    plan: Union[None, Unset, str] = UNSET
    type_: Union[Unset, DryRunTypeEnum] = DryRunTypeEnum.CREATE
    attributes: Union[Unset, Any] = UNSET
    order_offering: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        plan: Union[None, Unset, str]
        if isinstance(self.plan, Unset):
            plan = UNSET
        else:
            plan = self.plan

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        attributes = self.attributes

        order_offering: Union[None, Unset, str]
        if isinstance(self.order_offering, Unset):
            order_offering = UNSET
        else:
            order_offering = self.order_offering

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if plan is not UNSET:
            field_dict["plan"] = plan
        if type_ is not UNSET:
            field_dict["type"] = type_
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if order_offering is not UNSET:
            field_dict["order_offering"] = order_offering

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_plan(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        plan = _parse_plan(d.pop("plan", UNSET))

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, DryRunTypeEnum]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = DryRunTypeEnum(_type_)

        attributes = d.pop("attributes", UNSET)

        def _parse_order_offering(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        order_offering = _parse_order_offering(d.pop("order_offering", UNSET))

        dry_run_request = cls(
            plan=plan,
            type_=type_,
            attributes=attributes,
            order_offering=order_offering,
        )

        dry_run_request.additional_properties = d
        return dry_run_request

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
