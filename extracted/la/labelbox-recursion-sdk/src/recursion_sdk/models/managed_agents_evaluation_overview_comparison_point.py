from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsEvaluationOverviewComparisonPoint")



@_attrs_define
class ManagedAgentsEvaluationOverviewComparisonPoint:
    """ One aligned verdict aggregate for a selected target-agent version.

        Example:
            {'bucket_start': '2026-02-18T09:30:00Z', 'fail_count': 1, 'not_applicable_count': 1, 'pass_count': 1, 'rate': 1}

        Attributes:
            bucket_start (datetime.datetime): Exact evaluation time or inclusive UTC start of this aligned interval; legacy
                responses use window-anchored 24-hour buckets.
            fail_count (int): Fail verdicts for this version at this exact time or in this interval.
            not_applicable_count (int): Not-applicable verdicts for this version at this exact time or in this interval.
            pass_count (int): Pass verdicts for this version at this exact time or in this interval.
            rate (float | None): Pass divided by pass plus fail, or null at a zero denominator.
     """

    bucket_start: datetime.datetime
    fail_count: int
    not_applicable_count: int
    pass_count: int
    rate: float | None





    def to_dict(self) -> dict[str, Any]:
        bucket_start = self.bucket_start.isoformat()

        fail_count = self.fail_count

        not_applicable_count = self.not_applicable_count

        pass_count = self.pass_count

        rate: float | None
        rate = self.rate


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "bucket_start": bucket_start,
            "fail_count": fail_count,
            "not_applicable_count": not_applicable_count,
            "pass_count": pass_count,
            "rate": rate,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        bucket_start = datetime.datetime.fromisoformat(d.pop("bucket_start"))




        fail_count = d.pop("fail_count")

        not_applicable_count = d.pop("not_applicable_count")

        pass_count = d.pop("pass_count")

        def _parse_rate(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        rate = _parse_rate(d.pop("rate"))


        managed_agents_evaluation_overview_comparison_point = cls(
            bucket_start=bucket_start,
            fail_count=fail_count,
            not_applicable_count=not_applicable_count,
            pass_count=pass_count,
            rate=rate,
        )

        return managed_agents_evaluation_overview_comparison_point

