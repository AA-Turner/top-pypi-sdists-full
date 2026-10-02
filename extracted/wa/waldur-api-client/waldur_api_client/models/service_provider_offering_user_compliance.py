import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.service_provider_offering_user_compliance_state_enum import ServiceProviderOfferingUserComplianceStateEnum

T = TypeVar("T", bound="ServiceProviderOfferingUserCompliance")


@_attrs_define
class ServiceProviderOfferingUserCompliance:
    """
    Attributes:
        uuid (UUID):
        user_full_name (str):
        user_email (str):
        offering_name (str):
        checklist_name (Union[None, str]):
        username (Union[None, str]):
        state (ServiceProviderOfferingUserComplianceStateEnum):
        completion_percentage (Union[None, int]):
        compliance_status (str):
        last_updated (Union[None, datetime.datetime]):
        created (datetime.datetime):
    """

    uuid: UUID
    user_full_name: str
    user_email: str
    offering_name: str
    checklist_name: Union[None, str]
    username: Union[None, str]
    state: ServiceProviderOfferingUserComplianceStateEnum
    completion_percentage: Union[None, int]
    compliance_status: str
    last_updated: Union[None, datetime.datetime]
    created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        user_full_name = self.user_full_name

        user_email = self.user_email

        offering_name = self.offering_name

        checklist_name: Union[None, str]
        checklist_name = self.checklist_name

        username: Union[None, str]
        username = self.username

        state = self.state.value

        completion_percentage: Union[None, int]
        completion_percentage = self.completion_percentage

        compliance_status = self.compliance_status

        last_updated: Union[None, str]
        if isinstance(self.last_updated, datetime.datetime):
            last_updated = self.last_updated.isoformat()
        else:
            last_updated = self.last_updated

        created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "user_full_name": user_full_name,
                "user_email": user_email,
                "offering_name": offering_name,
                "checklist_name": checklist_name,
                "username": username,
                "state": state,
                "completion_percentage": completion_percentage,
                "compliance_status": compliance_status,
                "last_updated": last_updated,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        user_full_name = d.pop("user_full_name")

        user_email = d.pop("user_email")

        offering_name = d.pop("offering_name")

        def _parse_checklist_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        checklist_name = _parse_checklist_name(d.pop("checklist_name"))

        def _parse_username(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        username = _parse_username(d.pop("username"))

        state = ServiceProviderOfferingUserComplianceStateEnum(d.pop("state"))

        def _parse_completion_percentage(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        completion_percentage = _parse_completion_percentage(d.pop("completion_percentage"))

        compliance_status = d.pop("compliance_status")

        def _parse_last_updated(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                last_updated_type_0 = isoparse(data)

                return last_updated_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        last_updated = _parse_last_updated(d.pop("last_updated"))

        created = isoparse(d.pop("created"))

        service_provider_offering_user_compliance = cls(
            uuid=uuid,
            user_full_name=user_full_name,
            user_email=user_email,
            offering_name=offering_name,
            checklist_name=checklist_name,
            username=username,
            state=state,
            completion_percentage=completion_percentage,
            compliance_status=compliance_status,
            last_updated=last_updated,
            created=created,
        )

        service_provider_offering_user_compliance.additional_properties = d
        return service_provider_offering_user_compliance

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
