from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast






T = TypeVar("T", bound="ManagedAgentsVerdictMetric")



@_attrs_define
class ManagedAgentsVerdictMetric:
    """ Pass, fail, not-applicable, rate, and adjacent-window comparison for one verdict population.

        Example:
            {'delta_pp': 1.5, 'fail_count': 1, 'not_applicable_count': 1, 'pass_count': 1, 'prior_rate': 1, 'rate': 1}

        Attributes:
            delta_pp (float | None): Current rate minus prior rate in percentage points, or null when either rate is null.
            fail_count (int): Immutable fail verdicts in the current window.
            not_applicable_count (int): Immutable not-applicable verdicts in the current window.
            pass_count (int): Immutable pass verdicts in the current window.
            prior_rate (float | None): Equivalent pass rate for the adjacent prior window, or null at zero denominator.
            rate (float | None): Pass divided by pass plus fail, or null at a zero denominator.
     """

    delta_pp: float | None
    fail_count: int
    not_applicable_count: int
    pass_count: int
    prior_rate: float | None
    rate: float | None





    def to_dict(self) -> dict[str, Any]:
        delta_pp: float | None
        delta_pp = self.delta_pp

        fail_count = self.fail_count

        not_applicable_count = self.not_applicable_count

        pass_count = self.pass_count

        prior_rate: float | None
        prior_rate = self.prior_rate

        rate: float | None
        rate = self.rate


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "delta_pp": delta_pp,
            "fail_count": fail_count,
            "not_applicable_count": not_applicable_count,
            "pass_count": pass_count,
            "prior_rate": prior_rate,
            "rate": rate,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        def _parse_delta_pp(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        delta_pp = _parse_delta_pp(d.pop("delta_pp"))


        fail_count = d.pop("fail_count")

        not_applicable_count = d.pop("not_applicable_count")

        pass_count = d.pop("pass_count")

        def _parse_prior_rate(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        prior_rate = _parse_prior_rate(d.pop("prior_rate"))


        def _parse_rate(data: object) -> float | None:
            if data is None:
                return data
            return cast(float | None, data)

        rate = _parse_rate(d.pop("rate"))


        managed_agents_verdict_metric = cls(
            delta_pp=delta_pp,
            fail_count=fail_count,
            not_applicable_count=not_applicable_count,
            pass_count=pass_count,
            prior_rate=prior_rate,
            rate=rate,
        )

        return managed_agents_verdict_metric

