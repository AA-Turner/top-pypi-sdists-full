from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="NavPullRequestCount")



@_attrs_define
class NavPullRequestCount:
    """ A pull request page's numbers. `running`, `failed`, `passed` and
    `cancelled` count the pull requests whose CI is pending, failing,
    succeeded and cancelled, and `noChecks` those with no checks at all.
    One held for workflow approval is in `total` only, so the numbers
    need not add up. All six are always present.

        Attributes:
            total (int): How many pull requests the page lists.
            running (int): How many of them have CI that is still pending.
            failed (int): How many of them have failing CI. A pull request whose only
                failure is workflow runs held until someone approves them
                (`awaitingWorkflowApproval`) is counted in `total` and not here,
                as nothing failed; one with a job that really failed beside a
                held run still counts.
            passed (int): How many of them have CI that succeeded.
            cancelled (int): How many of them have CI whose only non-passing runs were
                cancelled. Not counted as `failed`: nothing broke.
            no_checks (int): How many of them have no checks (CI `none`). Not counted as
                running: nothing is pending, so there is nothing to wait for
                that the pull request itself can show.
     """

    total: int
    running: int
    failed: int
    passed: int
    cancelled: int
    no_checks: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        total = self.total

        running = self.running

        failed = self.failed

        passed = self.passed

        cancelled = self.cancelled

        no_checks = self.no_checks


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "total": total,
            "running": running,
            "failed": failed,
            "passed": passed,
            "cancelled": cancelled,
            "noChecks": no_checks,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        total = d.pop("total")

        running = d.pop("running")

        failed = d.pop("failed")

        passed = d.pop("passed")

        cancelled = d.pop("cancelled")

        no_checks = d.pop("noChecks")

        nav_pull_request_count = cls(
            total=total,
            running=running,
            failed=failed,
            passed=passed,
            cancelled=cancelled,
            no_checks=no_checks,
        )


        nav_pull_request_count.additional_properties = d
        return nav_pull_request_count

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
