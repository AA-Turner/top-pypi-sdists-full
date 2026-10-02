from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="SyncResourceHistoricalConsumptionRequestRequest")


@_attrs_define
class SyncResourceHistoricalConsumptionRequestRequest:
    """
    Attributes:
        resource_uuid (UUID): UUID of the resource to sync
        period_from (Union[Unset, str]): Start period in YYYY-MM format. Defaults to 12 months ago.
        period_to (Union[Unset, str]): End period in YYYY-MM format. Defaults to current month.
        force (Union[Unset, bool]): If True, sync even for finalized periods. Default: False.
        dry_run (Union[Unset, bool]): If True, preview consumption data without saving. Default: False.
    """

    resource_uuid: UUID
    period_from: Union[Unset, str] = UNSET
    period_to: Union[Unset, str] = UNSET
    force: Union[Unset, bool] = False
    dry_run: Union[Unset, bool] = False
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_uuid = str(self.resource_uuid)

        period_from = self.period_from

        period_to = self.period_to

        force = self.force

        dry_run = self.dry_run

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_uuid": resource_uuid,
            }
        )
        if period_from is not UNSET:
            field_dict["period_from"] = period_from
        if period_to is not UNSET:
            field_dict["period_to"] = period_to
        if force is not UNSET:
            field_dict["force"] = force
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        resource_uuid = UUID(d.pop("resource_uuid"))

        period_from = d.pop("period_from", UNSET)

        period_to = d.pop("period_to", UNSET)

        force = d.pop("force", UNSET)

        dry_run = d.pop("dry_run", UNSET)

        sync_resource_historical_consumption_request_request = cls(
            resource_uuid=resource_uuid,
            period_from=period_from,
            period_to=period_to,
            force=force,
            dry_run=dry_run,
        )

        sync_resource_historical_consumption_request_request.additional_properties = d
        return sync_resource_historical_consumption_request_request

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
