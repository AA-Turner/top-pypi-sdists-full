import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="ArrowVendorOfferingMappingCreate")


@_attrs_define
class ArrowVendorOfferingMappingCreate:
    """
    Attributes:
        uuid (UUID):
        url (str):
        settings (UUID):
        settings_uuid (UUID):
        arrow_vendor_name (str): Arrow vendor name (e.g., 'Microsoft', 'Amazon Web Services')
        offering (UUID):
        offering_uuid (UUID):
        offering_name (str):
        offering_type (str):
        plan_uuid (UUID):
        plan_name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        plan (Union[None, UUID, Unset]):
        is_active (Union[Unset, bool]): Whether this mapping is active
    """

    uuid: UUID
    url: str
    settings: UUID
    settings_uuid: UUID
    arrow_vendor_name: str
    offering: UUID
    offering_uuid: UUID
    offering_name: str
    offering_type: str
    plan_uuid: UUID
    plan_name: str
    created: datetime.datetime
    modified: datetime.datetime
    plan: Union[None, UUID, Unset] = UNSET
    is_active: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        url = self.url

        settings = str(self.settings)

        settings_uuid = str(self.settings_uuid)

        arrow_vendor_name = self.arrow_vendor_name

        offering = str(self.offering)

        offering_uuid = str(self.offering_uuid)

        offering_name = self.offering_name

        offering_type = self.offering_type

        plan_uuid = str(self.plan_uuid)

        plan_name = self.plan_name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        plan: Union[None, Unset, str]
        if isinstance(self.plan, Unset):
            plan = UNSET
        elif isinstance(self.plan, UUID):
            plan = str(self.plan)
        else:
            plan = self.plan

        is_active = self.is_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "url": url,
                "settings": settings,
                "settings_uuid": settings_uuid,
                "arrow_vendor_name": arrow_vendor_name,
                "offering": offering,
                "offering_uuid": offering_uuid,
                "offering_name": offering_name,
                "offering_type": offering_type,
                "plan_uuid": plan_uuid,
                "plan_name": plan_name,
                "created": created,
                "modified": modified,
            }
        )
        if plan is not UNSET:
            field_dict["plan"] = plan
        if is_active is not UNSET:
            field_dict["is_active"] = is_active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        url = d.pop("url")

        settings = UUID(d.pop("settings"))

        settings_uuid = UUID(d.pop("settings_uuid"))

        arrow_vendor_name = d.pop("arrow_vendor_name")

        offering = UUID(d.pop("offering"))

        offering_uuid = UUID(d.pop("offering_uuid"))

        offering_name = d.pop("offering_name")

        offering_type = d.pop("offering_type")

        plan_uuid = UUID(d.pop("plan_uuid"))

        plan_name = d.pop("plan_name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

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

        is_active = d.pop("is_active", UNSET)

        arrow_vendor_offering_mapping_create = cls(
            uuid=uuid,
            url=url,
            settings=settings,
            settings_uuid=settings_uuid,
            arrow_vendor_name=arrow_vendor_name,
            offering=offering,
            offering_uuid=offering_uuid,
            offering_name=offering_name,
            offering_type=offering_type,
            plan_uuid=plan_uuid,
            plan_name=plan_name,
            created=created,
            modified=modified,
            plan=plan,
            is_active=is_active,
        )

        arrow_vendor_offering_mapping_create.additional_properties = d
        return arrow_vendor_offering_mapping_create

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
