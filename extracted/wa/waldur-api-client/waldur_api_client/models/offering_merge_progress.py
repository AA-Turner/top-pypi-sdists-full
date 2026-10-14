import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="OfferingMergeProgress")


@_attrs_define
class OfferingMergeProgress:
    """
    Attributes:
        step (str): Registry entry label or phase being run, or 'done'.
        steps_done (int):
        steps_total (int):
        rows_done (int):
        rows_total (int):
        updated_at (datetime.datetime):
    """

    step: str
    steps_done: int
    steps_total: int
    rows_done: int
    rows_total: int
    updated_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        step = self.step

        steps_done = self.steps_done

        steps_total = self.steps_total

        rows_done = self.rows_done

        rows_total = self.rows_total

        updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "step": step,
                "steps_done": steps_done,
                "steps_total": steps_total,
                "rows_done": rows_done,
                "rows_total": rows_total,
                "updated_at": updated_at,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        step = d.pop("step")

        steps_done = d.pop("steps_done")

        steps_total = d.pop("steps_total")

        rows_done = d.pop("rows_done")

        rows_total = d.pop("rows_total")

        updated_at = isoparse(d.pop("updated_at"))

        offering_merge_progress = cls(
            step=step,
            steps_done=steps_done,
            steps_total=steps_total,
            rows_done=rows_done,
            rows_total=rows_total,
            updated_at=updated_at,
        )

        offering_merge_progress.additional_properties = d
        return offering_merge_progress

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
