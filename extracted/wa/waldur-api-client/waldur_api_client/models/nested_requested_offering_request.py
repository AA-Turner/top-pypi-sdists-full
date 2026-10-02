from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_requested_offering_request_attributes import NestedRequestedOfferingRequestAttributes


T = TypeVar("T", bound="NestedRequestedOfferingRequest")


@_attrs_define
class NestedRequestedOfferingRequest:
    """
    Attributes:
        offering (str):
        attributes (Union[Unset, NestedRequestedOfferingRequestAttributes]):
        plan (Union[None, Unset, str]):
        require_purchase_order (Union[Unset, bool]): Whether a purchase order must accompany a resource request for this
            offering before the proposal can be submitted. Defaults to the offering's require_purchase_order_upload, and
            stays under the call manager's control afterwards.
    """

    offering: str
    attributes: Union[Unset, "NestedRequestedOfferingRequestAttributes"] = UNSET
    plan: Union[None, Unset, str] = UNSET
    require_purchase_order: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        offering = self.offering

        attributes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        plan: Union[None, Unset, str]
        if isinstance(self.plan, Unset):
            plan = UNSET
        else:
            plan = self.plan

        require_purchase_order = self.require_purchase_order

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "offering": offering,
            }
        )
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if plan is not UNSET:
            field_dict["plan"] = plan
        if require_purchase_order is not UNSET:
            field_dict["require_purchase_order"] = require_purchase_order

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_requested_offering_request_attributes import NestedRequestedOfferingRequestAttributes

        d = dict(src_dict)
        offering = d.pop("offering")

        _attributes = d.pop("attributes", UNSET)
        attributes: Union[Unset, NestedRequestedOfferingRequestAttributes]
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = NestedRequestedOfferingRequestAttributes.from_dict(_attributes)

        def _parse_plan(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        plan = _parse_plan(d.pop("plan", UNSET))

        require_purchase_order = d.pop("require_purchase_order", UNSET)

        nested_requested_offering_request = cls(
            offering=offering,
            attributes=attributes,
            plan=plan,
            require_purchase_order=require_purchase_order,
        )

        nested_requested_offering_request.additional_properties = d
        return nested_requested_offering_request

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
