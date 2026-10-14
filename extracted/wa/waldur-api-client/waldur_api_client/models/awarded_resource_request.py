from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.awarded_resource_request_attributes import AwardedResourceRequestAttributes
    from ..models.awarded_resource_request_limits import AwardedResourceRequestLimits


T = TypeVar("T", bound="AwardedResourceRequest")


@_attrs_define
class AwardedResourceRequest:
    """
    Attributes:
        requested_offering_uuid (Union[Unset, UUID]): An accepted offering of the proposal's call to award the item on.
            Required when adding an item.
        plan (Union[None, UUID, Unset]): Plan of the awarded offering. Read back as the plan the item is provisioned on:
            the call offering's plan unless another was set. Null (or leaving it out when adding or moving) follows the call
            offering's plan.
        attributes (Union[Unset, AwardedResourceRequestAttributes]):
        limits (Union[Unset, AwardedResourceRequestLimits]):
        description (Union[Unset, str]):
    """

    requested_offering_uuid: Union[Unset, UUID] = UNSET
    plan: Union[None, UUID, Unset] = UNSET
    attributes: Union[Unset, "AwardedResourceRequestAttributes"] = UNSET
    limits: Union[Unset, "AwardedResourceRequestLimits"] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        requested_offering_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.requested_offering_uuid, Unset):
            requested_offering_uuid = str(self.requested_offering_uuid)

        plan: Union[None, Unset, str]
        if isinstance(self.plan, Unset):
            plan = UNSET
        elif isinstance(self.plan, UUID):
            plan = str(self.plan)
        else:
            plan = self.plan

        attributes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if requested_offering_uuid is not UNSET:
            field_dict["requested_offering_uuid"] = requested_offering_uuid
        if plan is not UNSET:
            field_dict["plan"] = plan
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if limits is not UNSET:
            field_dict["limits"] = limits
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.awarded_resource_request_attributes import AwardedResourceRequestAttributes
        from ..models.awarded_resource_request_limits import AwardedResourceRequestLimits

        d = dict(src_dict)
        _requested_offering_uuid = d.pop("requested_offering_uuid", UNSET)
        requested_offering_uuid: Union[Unset, UUID]
        if isinstance(_requested_offering_uuid, Unset):
            requested_offering_uuid = UNSET
        else:
            requested_offering_uuid = UUID(_requested_offering_uuid)

        def _parse_plan(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                plan_type_0 = UUID(data)

                return plan_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        plan = _parse_plan(d.pop("plan", UNSET))

        _attributes = d.pop("attributes", UNSET)
        attributes: Union[Unset, AwardedResourceRequestAttributes]
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = AwardedResourceRequestAttributes.from_dict(_attributes)

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, AwardedResourceRequestLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = AwardedResourceRequestLimits.from_dict(_limits)

        description = d.pop("description", UNSET)

        awarded_resource_request = cls(
            requested_offering_uuid=requested_offering_uuid,
            plan=plan,
            attributes=attributes,
            limits=limits,
            description=description,
        )

        awarded_resource_request.additional_properties = d
        return awarded_resource_request

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
