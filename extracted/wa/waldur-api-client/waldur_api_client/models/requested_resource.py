from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_requested_offering import NestedRequestedOffering
    from ..models.requested_resource_attributes import RequestedResourceAttributes
    from ..models.requested_resource_limits import RequestedResourceLimits


T = TypeVar("T", bound="RequestedResource")


@_attrs_define
class RequestedResource:
    """
    Attributes:
        uuid (UUID):
        url (str):
        requested_offering (NestedRequestedOffering):
        resource (Union[None, str]):
        resource_name (str):
        call_resource_template (str):
        call_resource_template_name (str):
        attachment (str):
        purchase_order_required (bool):
        has_purchase_order (bool): Either half satisfies the requirement.

            Some providers want the document, others only need the reference from
            the customer's finance system; demanding both would block the second
            group for no gain.
        created_by (Union[None, str]):
        created_by_name (str):
        attributes (Union[Unset, RequestedResourceAttributes]):
        limits (Union[Unset, RequestedResourceLimits]):
        purchase_order_reference (Union[Unset, str]):
        description (Union[Unset, str]):
    """

    uuid: UUID
    url: str
    requested_offering: "NestedRequestedOffering"
    resource: Union[None, str]
    resource_name: str
    call_resource_template: str
    call_resource_template_name: str
    attachment: str
    purchase_order_required: bool
    has_purchase_order: bool
    created_by: Union[None, str]
    created_by_name: str
    attributes: Union[Unset, "RequestedResourceAttributes"] = UNSET
    limits: Union[Unset, "RequestedResourceLimits"] = UNSET
    purchase_order_reference: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        requested_offering = self.requested_offering.to_dict()

        resource: Union[None, str]
        resource = self.resource

        resource_name = self.resource_name

        call_resource_template = self.call_resource_template

        call_resource_template_name = self.call_resource_template_name

        attachment = self.attachment

        purchase_order_required = self.purchase_order_required

        has_purchase_order = self.has_purchase_order

        created_by: Union[None, str]
        created_by = self.created_by

        created_by_name = self.created_by_name

        attributes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        purchase_order_reference = self.purchase_order_reference

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "requested_offering": requested_offering,
                "resource": resource,
                "resource_name": resource_name,
                "call_resource_template": call_resource_template,
                "call_resource_template_name": call_resource_template_name,
                "attachment": attachment,
                "purchase_order_required": purchase_order_required,
                "has_purchase_order": has_purchase_order,
                "created_by": created_by,
                "created_by_name": created_by_name,
            }
        )
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if limits is not UNSET:
            field_dict["limits"] = limits
        if purchase_order_reference is not UNSET:
            field_dict["purchase_order_reference"] = purchase_order_reference
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_requested_offering import NestedRequestedOffering
        from ..models.requested_resource_attributes import RequestedResourceAttributes
        from ..models.requested_resource_limits import RequestedResourceLimits

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        requested_offering = NestedRequestedOffering.from_dict(d.pop("requested_offering"))

        def _parse_resource(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        resource = _parse_resource(d.pop("resource"))

        resource_name = d.pop("resource_name")

        call_resource_template = d.pop("call_resource_template")

        call_resource_template_name = d.pop("call_resource_template_name")

        attachment = d.pop("attachment")

        purchase_order_required = d.pop("purchase_order_required")

        has_purchase_order = d.pop("has_purchase_order")

        def _parse_created_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        created_by = _parse_created_by(d.pop("created_by"))

        created_by_name = d.pop("created_by_name")

        _attributes = d.pop("attributes", UNSET)
        attributes: Union[Unset, RequestedResourceAttributes]
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = RequestedResourceAttributes.from_dict(_attributes)

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, RequestedResourceLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = RequestedResourceLimits.from_dict(_limits)

        purchase_order_reference = d.pop("purchase_order_reference", UNSET)

        description = d.pop("description", UNSET)

        requested_resource = cls(
            uuid=uuid,
            url=url,
            requested_offering=requested_offering,
            resource=resource,
            resource_name=resource_name,
            call_resource_template=call_resource_template,
            call_resource_template_name=call_resource_template_name,
            attachment=attachment,
            purchase_order_required=purchase_order_required,
            has_purchase_order=has_purchase_order,
            created_by=created_by,
            created_by_name=created_by_name,
            attributes=attributes,
            limits=limits,
            purchase_order_reference=purchase_order_reference,
            description=description,
        )

        requested_resource.additional_properties = d
        return requested_resource

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
