from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..types import UNSET, Unset

from ..models.retry_on_reasons_item import check_retry_on_reasons_item
from ..models.retry_on_reasons_item import RetryOnReasonsItem
from typing import cast


T = TypeVar("T", bound="RetryOn")


@_attrs_define
class RetryOn:
    """Which failures a policy retries. An empty policy (both lists empty or
    absent) retries nothing.

        Attributes:
            statuses (list[int] | Unset): Response status codes that should be retried when a run fails because the response
                did not match the job's success status (for example `[429, 503]` to retry on rate-limit and unavailable). Each
                is a 3-digit HTTP status code. Empty matches no status.
            reasons (list[RetryOnReasonsItem] | Unset): Failure reasons that should be retried: `TIMEOUT` (the run did not
                complete in time), `CONNECTION_ERROR` (the endpoint could not be reached), or `NON_SUCCESS_STATUS` (any non-
                success response, regardless of `statuses`). Empty matches no reason.
    """

    statuses: list[int] | Unset = UNSET
    reasons: list[RetryOnReasonsItem] | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        statuses: list[int] | Unset = UNSET
        if not isinstance(self.statuses, Unset):
            statuses = self.statuses

        reasons: list[str] | Unset = UNSET
        if not isinstance(self.reasons, Unset):
            reasons = []
            for reasons_item_data in self.reasons:
                reasons_item: str = reasons_item_data
                reasons.append(reasons_item)

        field_dict: dict[str, Any] = {}

        field_dict.update({})
        if statuses is not UNSET:
            field_dict["statuses"] = statuses
        if reasons is not UNSET:
            field_dict["reasons"] = reasons

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        statuses = cast(list[int], d.pop("statuses", UNSET))

        _reasons = d.pop("reasons", UNSET)
        reasons: list[RetryOnReasonsItem] | Unset = UNSET
        if _reasons is not UNSET:
            reasons = []
            for reasons_item_data in _reasons:
                reasons_item = check_retry_on_reasons_item(reasons_item_data)

                reasons.append(reasons_item)

        retry_on = cls(
            statuses=statuses,
            reasons=reasons,
        )

        return retry_on
