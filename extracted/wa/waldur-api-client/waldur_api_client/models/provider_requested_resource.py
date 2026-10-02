from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_requested_offering import NestedRequestedOffering
    from ..models.provider_requested_resource_attributes import ProviderRequestedResourceAttributes
    from ..models.provider_requested_resource_limits import ProviderRequestedResourceLimits


T = TypeVar("T", bound="ProviderRequestedResource")


@_attrs_define
class ProviderRequestedResource:
    """
    Attributes:
        uuid (UUID):
        url (str):
        requested_offering (NestedRequestedOffering):
        resource_name (str):
        call_resource_template (str):
        call_resource_template_name (str):
        attachment (str):
        purchase_order_required (bool):
        has_purchase_order (bool): Either half satisfies the requirement.

            Some providers want the document, others only need the reference from
            the customer's finance system; demanding both would block the second
            group for no gain.
        created_by_name (str):
        proposal_name (str):
        proposal (str):
        resource (Union[None, Unset, str]):
        attributes (Union[Unset, ProviderRequestedResourceAttributes]):
        limits (Union[Unset, ProviderRequestedResourceLimits]):
        purchase_order_reference (Union[Unset, str]):
        description (Union[Unset, str]):
        created_by (Union[None, Unset, str]):
    """

    uuid: UUID
    url: str
    requested_offering: "NestedRequestedOffering"
    resource_name: str
    call_resource_template: str
    call_resource_template_name: str
    attachment: str
    purchase_order_required: bool
    has_purchase_order: bool
    created_by_name: str
    proposal_name: str
    proposal: str
    resource: Union[None, Unset, str] = UNSET
    attributes: Union[Unset, "ProviderRequestedResourceAttributes"] = UNSET
    limits: Union[Unset, "ProviderRequestedResourceLimits"] = UNSET
    purchase_order_reference: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    created_by: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        requested_offering = self.requested_offering.to_dict()

        resource_name = self.resource_name

        call_resource_template = self.call_resource_template

        call_resource_template_name = self.call_resource_template_name

        attachment = self.attachment

        purchase_order_required = self.purchase_order_required

        has_purchase_order = self.has_purchase_order

        created_by_name = self.created_by_name

        proposal_name = self.proposal_name

        proposal = self.proposal

        resource: Union[None, Unset, str]
        if isinstance(self.resource, Unset):
            resource = UNSET
        else:
            resource = self.resource

        attributes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        purchase_order_reference = self.purchase_order_reference

        description = self.description

        created_by: Union[None, Unset, str]
        if isinstance(self.created_by, Unset):
            created_by = UNSET
        else:
            created_by = self.created_by

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "requested_offering": requested_offering,
                "resource_name": resource_name,
                "call_resource_template": call_resource_template,
                "call_resource_template_name": call_resource_template_name,
                "attachment": attachment,
                "purchase_order_required": purchase_order_required,
                "has_purchase_order": has_purchase_order,
                "created_by_name": created_by_name,
                "proposal_name": proposal_name,
                "proposal": proposal,
            }
        )
        if resource is not UNSET:
            field_dict["resource"] = resource
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if limits is not UNSET:
            field_dict["limits"] = limits
        if purchase_order_reference is not UNSET:
            field_dict["purchase_order_reference"] = purchase_order_reference
        if description is not UNSET:
            field_dict["description"] = description
        if created_by is not UNSET:
            field_dict["created_by"] = created_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_requested_offering import NestedRequestedOffering
        from ..models.provider_requested_resource_attributes import ProviderRequestedResourceAttributes
        from ..models.provider_requested_resource_limits import ProviderRequestedResourceLimits

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        requested_offering = NestedRequestedOffering.from_dict(d.pop("requested_offering"))

        resource_name = d.pop("resource_name")

        call_resource_template = d.pop("call_resource_template")

        call_resource_template_name = d.pop("call_resource_template_name")

        attachment = d.pop("attachment")

        purchase_order_required = d.pop("purchase_order_required")

        has_purchase_order = d.pop("has_purchase_order")

        created_by_name = d.pop("created_by_name")

        proposal_name = d.pop("proposal_name")

        proposal = d.pop("proposal")

        def _parse_resource(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        resource = _parse_resource(d.pop("resource", UNSET))

        _attributes = d.pop("attributes", UNSET)
        attributes: Union[Unset, ProviderRequestedResourceAttributes]
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = ProviderRequestedResourceAttributes.from_dict(_attributes)

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, ProviderRequestedResourceLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = ProviderRequestedResourceLimits.from_dict(_limits)

        purchase_order_reference = d.pop("purchase_order_reference", UNSET)

        description = d.pop("description", UNSET)

        def _parse_created_by(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        created_by = _parse_created_by(d.pop("created_by", UNSET))

        provider_requested_resource = cls(
            uuid=uuid,
            url=url,
            requested_offering=requested_offering,
            resource_name=resource_name,
            call_resource_template=call_resource_template,
            call_resource_template_name=call_resource_template_name,
            attachment=attachment,
            purchase_order_required=purchase_order_required,
            has_purchase_order=has_purchase_order,
            created_by_name=created_by_name,
            proposal_name=proposal_name,
            proposal=proposal,
            resource=resource,
            attributes=attributes,
            limits=limits,
            purchase_order_reference=purchase_order_reference,
            description=description,
            created_by=created_by,
        )

        provider_requested_resource.additional_properties = d
        return provider_requested_resource

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
