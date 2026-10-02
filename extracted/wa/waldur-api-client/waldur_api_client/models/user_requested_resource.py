import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.user_requested_resource_attributes import UserRequestedResourceAttributes
    from ..models.user_requested_resource_limits import UserRequestedResourceLimits


T = TypeVar("T", bound="UserRequestedResource")


@_attrs_define
class UserRequestedResource:
    """
    Attributes:
        uuid (UUID):
        created (datetime.datetime):
        offering_name (str):
        offering_uuid (UUID):
        call_name (str):
        call_uuid (UUID):
        proposal (str):
        proposal_name (str):
        proposal_uuid (UUID):
        proposal_state (str):
        resource_name (Union[None, str]):
        resource_uuid (Union[None, UUID]):
        resource_state (Union[None, str]):
        description (Union[Unset, str]):
        attributes (Union[Unset, UserRequestedResourceAttributes]):
        limits (Union[Unset, UserRequestedResourceLimits]):
    """

    uuid: UUID
    created: datetime.datetime
    offering_name: str
    offering_uuid: UUID
    call_name: str
    call_uuid: UUID
    proposal: str
    proposal_name: str
    proposal_uuid: UUID
    proposal_state: str
    resource_name: Union[None, str]
    resource_uuid: Union[None, UUID]
    resource_state: Union[None, str]
    description: Union[Unset, str] = UNSET
    attributes: Union[Unset, "UserRequestedResourceAttributes"] = UNSET
    limits: Union[Unset, "UserRequestedResourceLimits"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        created = self.created.isoformat()

        offering_name = self.offering_name

        offering_uuid = str(self.offering_uuid)

        call_name = self.call_name

        call_uuid = str(self.call_uuid)

        proposal = self.proposal

        proposal_name = self.proposal_name

        proposal_uuid = str(self.proposal_uuid)

        proposal_state = self.proposal_state

        resource_name: Union[None, str]
        resource_name = self.resource_name

        resource_uuid: Union[None, str]
        if isinstance(self.resource_uuid, UUID):
            resource_uuid = str(self.resource_uuid)
        else:
            resource_uuid = self.resource_uuid

        resource_state: Union[None, str]
        resource_state = self.resource_state

        description = self.description

        attributes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.attributes, Unset):
            attributes = self.attributes.to_dict()

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "created": created,
                "offering_name": offering_name,
                "offering_uuid": offering_uuid,
                "call_name": call_name,
                "call_uuid": call_uuid,
                "proposal": proposal,
                "proposal_name": proposal_name,
                "proposal_uuid": proposal_uuid,
                "proposal_state": proposal_state,
                "resource_name": resource_name,
                "resource_uuid": resource_uuid,
                "resource_state": resource_state,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if attributes is not UNSET:
            field_dict["attributes"] = attributes
        if limits is not UNSET:
            field_dict["limits"] = limits

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.user_requested_resource_attributes import UserRequestedResourceAttributes
        from ..models.user_requested_resource_limits import UserRequestedResourceLimits

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        offering_name = d.pop("offering_name")

        offering_uuid = UUID(d.pop("offering_uuid"))

        call_name = d.pop("call_name")

        call_uuid = UUID(d.pop("call_uuid"))

        proposal = d.pop("proposal")

        proposal_name = d.pop("proposal_name")

        proposal_uuid = UUID(d.pop("proposal_uuid"))

        proposal_state = d.pop("proposal_state")

        def _parse_resource_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        resource_name = _parse_resource_name(d.pop("resource_name"))

        def _parse_resource_uuid(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resource_uuid_type_0 = UUID(data)

                return resource_uuid_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        resource_uuid = _parse_resource_uuid(d.pop("resource_uuid"))

        def _parse_resource_state(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        resource_state = _parse_resource_state(d.pop("resource_state"))

        description = d.pop("description", UNSET)

        _attributes = d.pop("attributes", UNSET)
        attributes: Union[Unset, UserRequestedResourceAttributes]
        if isinstance(_attributes, Unset):
            attributes = UNSET
        else:
            attributes = UserRequestedResourceAttributes.from_dict(_attributes)

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, UserRequestedResourceLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = UserRequestedResourceLimits.from_dict(_limits)

        user_requested_resource = cls(
            uuid=uuid,
            created=created,
            offering_name=offering_name,
            offering_uuid=offering_uuid,
            call_name=call_name,
            call_uuid=call_uuid,
            proposal=proposal,
            proposal_name=proposal_name,
            proposal_uuid=proposal_uuid,
            proposal_state=proposal_state,
            resource_name=resource_name,
            resource_uuid=resource_uuid,
            resource_state=resource_state,
            description=description,
            attributes=attributes,
            limits=limits,
        )

        user_requested_resource.additional_properties = d
        return user_requested_resource

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
