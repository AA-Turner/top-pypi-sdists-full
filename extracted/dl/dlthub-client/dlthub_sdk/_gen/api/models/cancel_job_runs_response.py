from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.bulk_item_failure import BulkItemFailure
    from ..models.cancelled_job_run import CancelledJobRun


T = TypeVar("T", bound="CancelJobRunsResponse")


@_attrs_define
class CancelJobRunsResponse:
    """
    Attributes:
        failed (list[BulkItemFailure]): Requested runs that do not exist in the workspace.
        skipped (list[CancelledJobRun]): Runs that were already in a terminal state.
        succeeded (list[CancelledJobRun]): Runs that were cancelled (or would be in dry-run mode).
    """

    failed: list[BulkItemFailure]
    skipped: list[CancelledJobRun]
    succeeded: list[CancelledJobRun]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        failed = []
        for failed_item_data in self.failed:
            failed_item = failed_item_data.to_dict()
            failed.append(failed_item)

        skipped = []
        for skipped_item_data in self.skipped:
            skipped_item = skipped_item_data.to_dict()
            skipped.append(skipped_item)

        succeeded = []
        for succeeded_item_data in self.succeeded:
            succeeded_item = succeeded_item_data.to_dict()
            succeeded.append(succeeded_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "failed": failed,
                "skipped": skipped,
                "succeeded": succeeded,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.bulk_item_failure import BulkItemFailure
        from ..models.cancelled_job_run import CancelledJobRun

        d = dict(src_dict)
        failed = []
        _failed = d.pop("failed")
        for failed_item_data in _failed:
            failed_item = BulkItemFailure.from_dict(failed_item_data)

            failed.append(failed_item)

        skipped = []
        _skipped = d.pop("skipped")
        for skipped_item_data in _skipped:
            skipped_item = CancelledJobRun.from_dict(skipped_item_data)

            skipped.append(skipped_item)

        succeeded = []
        _succeeded = d.pop("succeeded")
        for succeeded_item_data in _succeeded:
            succeeded_item = CancelledJobRun.from_dict(succeeded_item_data)

            succeeded.append(succeeded_item)

        cancel_job_runs_response = cls(
            failed=failed,
            skipped=skipped,
            succeeded=succeeded,
        )

        cancel_job_runs_response.additional_properties = d
        return cancel_job_runs_response

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
