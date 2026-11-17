from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="CheckCounts")



@_attrs_define
class CheckCounts:
    """ How many checks are in each state, so a client can say how far a
    pipeline is without opening it. It is on every pull request and on
    every default branch, for a passed, a failed and a running pipeline
    alike. The server tallies them from what it already reads to work out
    the overall state, so they cost no request. Always present, all zero
    when there are no checks.

    `waiting` is a check that has not started: queued, or pending where the
    forge doesn't tell queued from running. A failed pipeline can still have
    checks running or waiting, and says so. A pull request's counts agree
    with its `ci`: one whose `ci` is `pending` has `failed` at 0, and one
    whose `ci` is `success` has nothing running, waiting or failed. On a
    pull request or branch a cancelled run and a run held for approval
    have counts of their own, `cancelled` and `held`, and are never in
    `failed`: a push or a concurrency group superseded a cancelled run, and
    the overall state does not read it as a failure while others still run.
    A held run is also said by `awaitingWorkflowApproval`. Every check the
    pipeline lists is in exactly one count, so the counts add up to the
    jobs the pipeline lists, on a pull request and a default branch alike.
    A failed branch can have a `failed` of 0 when a held or cancelled run is what
    failed it. A timed-out or stale check counts as `failed`, a skipped,
    neutral or bare completed one as `passed`, on Forgejo too.

    `unknown` is how many checks are in a state the server cannot grade: a
    status or conclusion the forge added after the server was written. It
    is none of the others, so a check nobody can name is not hidden in a
    count that means something. A pull request or branch whose only odd
    check is unknown is neither failing nor passing: a branch that would
    read `passed` reads `running` while one is present. The server always
    sends it; a client that may talk to an older server reads a missing
    one as zero.

    `skipped` is a newer field and says how many of the `passed` checks
    were skipped. It never exceeds `passed`: it is inside `passed`, not
    beside it, so `passed` still counts every check that needs nothing more
    and the counts still add up to the checks the pipeline lists, on a pull
    request and a default branch alike. The
    server always sends it, which is why it is required; a client that may
    talk to an older server may read a missing one as zero. A neutral or bare
    completed check is passed without being skipped. A client that draws the
    two side by side must subtract `skipped` from `passed` for the passed figure, or a skipped check is
    counted twice, and a pipeline where every passed check was skipped can
    read as skipped.

    On GitHub the counts come from the same rollup as the overall state,
    for a pull request and a branch alike; on Forgejo a pull request counts
    the statuses of the combined commit status, which only say pending, and
    takes the running ones out of the pending count by reading the jobs of
    the commit's runs that are still going. A pending status of a job in a
    run that has failed is no wait: its needs failed, so Forgejo leaves it
    blocked and nothing will start it, and it counts as `notStarted`, not
    `waiting`. A default branch counts the jobs of the workflow runs of the
    newest commit that has one,
    where a running job is `running`, a queued one `waiting`, and a blocked
    one `waiting` unless its run has failed. A run
    whose jobs can't be read counts as one check by its own status. Forgejo
    answers one page of those statuses, and when its total says there are
    more than the page holds a pull request's counts are all zero rather
    than an undercount. When GitHub's rollup of a pull request is of an
    earlier commit than the head (a push still being processed), the counts
    are zero too. GitHub's unauthenticated fallback has no such counts, so
    there they are all zero.

        Attributes:
            passed (int):
            running (int):
            waiting (int):
            failed (int):
            skipped (int):
            unknown (int):
            cancelled (int | Unset): How many runs were cancelled, on a pull request and a default
                branch alike, so the counts add up to the jobs the pipeline lists.
                Absent when none were. A newer field, so a client treats a missing
                one as 0.
            held (int | Unset): How many runs are held for approval, so the counts add up. A pull
                request also says so with `awaitingWorkflowApproval`. Forgejo does
                not tell a held job from a waiting one, so it never sets this: the
                job is in `waiting`. Absent when none are. A newer field, so a
                client treats a missing one as 0.
            not_started (int | Unset): How many jobs are queued in a run that has already failed, so
                nothing will start them. Forgejo leaves a job whose needs failed
                blocked in the finished run and says pending for it. It is neither
                `waiting` nor `failed`, so a failed pull request stays failed and
                the counts still add up. Only Forgejo pull requests set it. Absent
                when none are. A newer field, so a client treats a missing one as
                0.
     """

    passed: int
    running: int
    waiting: int
    failed: int
    skipped: int
    unknown: int
    cancelled: int | Unset = UNSET
    held: int | Unset = UNSET
    not_started: int | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        passed = self.passed

        running = self.running

        waiting = self.waiting

        failed = self.failed

        skipped = self.skipped

        unknown = self.unknown

        cancelled = self.cancelled

        held = self.held

        not_started = self.not_started


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "passed": passed,
            "running": running,
            "waiting": waiting,
            "failed": failed,
            "skipped": skipped,
            "unknown": unknown,
        })
        if cancelled is not UNSET:
            field_dict["cancelled"] = cancelled
        if held is not UNSET:
            field_dict["held"] = held
        if not_started is not UNSET:
            field_dict["notStarted"] = not_started

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        passed = d.pop("passed")

        running = d.pop("running")

        waiting = d.pop("waiting")

        failed = d.pop("failed")

        skipped = d.pop("skipped")

        unknown = d.pop("unknown")

        cancelled = d.pop("cancelled", UNSET)

        held = d.pop("held", UNSET)

        not_started = d.pop("notStarted", UNSET)

        check_counts = cls(
            passed=passed,
            running=running,
            waiting=waiting,
            failed=failed,
            skipped=skipped,
            unknown=unknown,
            cancelled=cancelled,
            held=held,
            not_started=not_started,
        )


        check_counts.additional_properties = d
        return check_counts

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
