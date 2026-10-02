from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SyncResourcesRequestRequest")


@_attrs_define
class SyncResourcesRequestRequest:
    """
    Attributes:
        period_from (Union[Unset, str]): Start period in YYYY-MM format (default: 6 months ago, Arrow max)
        period_to (Union[Unset, str]): End period in YYYY-MM format (default: current month)
        settings_uuid (Union[Unset, UUID]):
        offering_uuid (Union[Unset, UUID]): Offering UUID for creating new resources
        project_uuid (Union[Unset, UUID]): Project UUID for creating new resources (ignored if force_import=True)
        force_import (Union[Unset, bool]): If True, auto-create Waldur Customers and Projects from Arrow data. Each
            Arrow customer gets a Waldur Customer with an 'Arrow Azure Subscriptions' project. Default: False.
    """

    period_from: Union[Unset, str] = UNSET
    period_to: Union[Unset, str] = UNSET
    settings_uuid: Union[Unset, UUID] = UNSET
    offering_uuid: Union[Unset, UUID] = UNSET
    project_uuid: Union[Unset, UUID] = UNSET
    force_import: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        period_from = self.period_from

        period_to = self.period_to

        settings_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.settings_uuid, Unset):
            settings_uuid = str(self.settings_uuid)

        offering_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.offering_uuid, Unset):
            offering_uuid = str(self.offering_uuid)

        project_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.project_uuid, Unset):
            project_uuid = str(self.project_uuid)

        force_import = self.force_import

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if period_from is not UNSET:
            field_dict["period_from"] = period_from
        if period_to is not UNSET:
            field_dict["period_to"] = period_to
        if settings_uuid is not UNSET:
            field_dict["settings_uuid"] = settings_uuid
        if offering_uuid is not UNSET:
            field_dict["offering_uuid"] = offering_uuid
        if project_uuid is not UNSET:
            field_dict["project_uuid"] = project_uuid
        if force_import is not UNSET:
            field_dict["force_import"] = force_import

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        period_from = d.pop("period_from", UNSET)

        period_to = d.pop("period_to", UNSET)

        _settings_uuid = d.pop("settings_uuid", UNSET)
        settings_uuid: Union[Unset, UUID]
        if isinstance(_settings_uuid, Unset):
            settings_uuid = UNSET
        else:
            settings_uuid = UUID(_settings_uuid)

        _offering_uuid = d.pop("offering_uuid", UNSET)
        offering_uuid: Union[Unset, UUID]
        if isinstance(_offering_uuid, Unset):
            offering_uuid = UNSET
        else:
            offering_uuid = UUID(_offering_uuid)

        _project_uuid = d.pop("project_uuid", UNSET)
        project_uuid: Union[Unset, UUID]
        if isinstance(_project_uuid, Unset):
            project_uuid = UNSET
        else:
            project_uuid = UUID(_project_uuid)

        force_import = d.pop("force_import", UNSET)

        sync_resources_request_request = cls(
            period_from=period_from,
            period_to=period_to,
            settings_uuid=settings_uuid,
            offering_uuid=offering_uuid,
            project_uuid=project_uuid,
            force_import=force_import,
        )

        sync_resources_request_request.additional_properties = d
        return sync_resources_request_request

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
