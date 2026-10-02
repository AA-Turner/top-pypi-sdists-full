from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.arrow_sync_error import ArrowSyncError
    from ..models.preview_period import PreviewPeriod


T = TypeVar("T", bound="SyncResourceHistoricalConsumptionResponse")


@_attrs_define
class SyncResourceHistoricalConsumptionResponse:
    """
    Attributes:
        resource_uuid (UUID):
        resource_name (str):
        periods_synced (int):
        periods_skipped (int):
        periods_no_data (Union[Unset, int]):  Default: 0.
        errors (Union[Unset, list['ArrowSyncError']]):
        dry_run (Union[Unset, bool]):  Default: False.
        preview_periods (Union[Unset, list['PreviewPeriod']]):
    """

    resource_uuid: UUID
    resource_name: str
    periods_synced: int
    periods_skipped: int
    periods_no_data: Union[Unset, int] = 0
    errors: Union[Unset, list["ArrowSyncError"]] = UNSET
    dry_run: Union[Unset, bool] = False
    preview_periods: Union[Unset, list["PreviewPeriod"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        resource_uuid = str(self.resource_uuid)

        resource_name = self.resource_name

        periods_synced = self.periods_synced

        periods_skipped = self.periods_skipped

        periods_no_data = self.periods_no_data

        errors: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.errors, Unset):
            errors = []
            for errors_item_data in self.errors:
                errors_item = errors_item_data.to_dict()
                errors.append(errors_item)

        dry_run = self.dry_run

        preview_periods: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.preview_periods, Unset):
            preview_periods = []
            for preview_periods_item_data in self.preview_periods:
                preview_periods_item = preview_periods_item_data.to_dict()
                preview_periods.append(preview_periods_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "periods_synced": periods_synced,
                "periods_skipped": periods_skipped,
            }
        )
        if periods_no_data is not UNSET:
            field_dict["periods_no_data"] = periods_no_data
        if errors is not UNSET:
            field_dict["errors"] = errors
        if dry_run is not UNSET:
            field_dict["dry_run"] = dry_run
        if preview_periods is not UNSET:
            field_dict["preview_periods"] = preview_periods

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.arrow_sync_error import ArrowSyncError
        from ..models.preview_period import PreviewPeriod

        d = dict(src_dict)
        resource_uuid = UUID(d.pop("resource_uuid"))

        resource_name = d.pop("resource_name")

        periods_synced = d.pop("periods_synced")

        periods_skipped = d.pop("periods_skipped")

        periods_no_data = d.pop("periods_no_data", UNSET)

        errors = []
        _errors = d.pop("errors", UNSET)
        for errors_item_data in _errors or []:
            errors_item = ArrowSyncError.from_dict(errors_item_data)

            errors.append(errors_item)

        dry_run = d.pop("dry_run", UNSET)

        preview_periods = []
        _preview_periods = d.pop("preview_periods", UNSET)
        for preview_periods_item_data in _preview_periods or []:
            preview_periods_item = PreviewPeriod.from_dict(preview_periods_item_data)

            preview_periods.append(preview_periods_item)

        sync_resource_historical_consumption_response = cls(
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            periods_synced=periods_synced,
            periods_skipped=periods_skipped,
            periods_no_data=periods_no_data,
            errors=errors,
            dry_run=dry_run,
            preview_periods=preview_periods,
        )

        sync_resource_historical_consumption_response.additional_properties = d
        return sync_resource_historical_consumption_response

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
