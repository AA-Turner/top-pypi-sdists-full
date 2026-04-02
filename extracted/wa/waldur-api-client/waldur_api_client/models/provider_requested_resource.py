from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.nested_requested_offering import NestedRequestedOffering


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
        created_by_name (str):
        proposal_name (str):
        proposal (str):
        resource (Union[None, Unset, str]):
        attributes (Union[Unset, Any]):
        limits (Union[Unset, Any]):
        description (Union[Unset, str]):
        created_by (Union[None, Unset, str]):
    """

    uuid: UUID
    url: str
    requested_offering: "NestedRequestedOffering"
    resource_name: str
    call_resource_template: str
    call_resource_template_name: str
    created_by_name: str
    proposal_name: str
    proposal: str
    resource: Union[None, Unset, str] = UNSET
    attributes: Union[Unset, Any] = UNSET
    limits: Union[Unset, Any] = UNSET
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

        created_by_name = self.created_by_name

        proposal_name = self.proposal_name

        proposal = self.proposal

        resource: Union[None, Unset, str]
        if isinstance(self.resource, Unset):
            resource = UNSET
        else:
            resource = self.resource

        attributes = self.attributes

        limits = self.limits

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
        if description is not UNSET:
            field_dict["description"] = description
        if created_by is not UNSET:
            field_dict["created_by"] = created_by

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.nested_requested_offering import NestedRequestedOffering

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        requested_offering = NestedRequestedOffering.from_dict(d.pop("requested_offering"))

        resource_name = d.pop("resource_name")

        call_resource_template = d.pop("call_resource_template")

        call_resource_template_name = d.pop("call_resource_template_name")

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

        attributes = d.pop("attributes", UNSET)

        limits = d.pop("limits", UNSET)

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
            created_by_name=created_by_name,
            proposal_name=proposal_name,
            proposal=proposal,
            resource=resource,
            attributes=attributes,
            limits=limits,
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
