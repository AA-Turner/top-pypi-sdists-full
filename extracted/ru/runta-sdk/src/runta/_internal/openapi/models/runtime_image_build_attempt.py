from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define

from ..models.runtime_image_build_attempt_outcome import RuntimeImageBuildAttemptOutcome
from ..types import UNSET, Unset

T = TypeVar("T", bound="RuntimeImageBuildAttempt")


@_attrs_define
class RuntimeImageBuildAttempt:
    """
    Attributes:
        attempt (int):
        started_at (datetime.datetime):
        completed_at (datetime.datetime | Unset):
        outcome (RuntimeImageBuildAttemptOutcome | Unset):
    """

    attempt: int
    started_at: datetime.datetime
    completed_at: datetime.datetime | Unset = UNSET
    outcome: RuntimeImageBuildAttemptOutcome | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        attempt = self.attempt

        started_at = self.started_at.isoformat()

        completed_at: str | Unset = UNSET
        if not isinstance(self.completed_at, Unset):
            completed_at = self.completed_at.isoformat()

        outcome: str | Unset = UNSET
        if not isinstance(self.outcome, Unset):
            outcome = self.outcome.value

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "attempt": attempt,
                "started_at": started_at,
            }
        )
        if completed_at is not UNSET:
            field_dict["completed_at"] = completed_at
        if outcome is not UNSET:
            field_dict["outcome"] = outcome

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        attempt = d.pop("attempt")

        started_at = datetime.datetime.fromisoformat(
            d.pop("started_at").replace("Z", "+00:00")
        )

        _completed_at = d.pop("completed_at", UNSET)
        completed_at: datetime.datetime | Unset
        if isinstance(_completed_at, Unset):
            completed_at = UNSET
        else:
            completed_at = datetime.datetime.fromisoformat(
                _completed_at.replace("Z", "+00:00")
            )

        _outcome = d.pop("outcome", UNSET)
        outcome: RuntimeImageBuildAttemptOutcome | Unset
        if isinstance(_outcome, Unset):
            outcome = UNSET
        else:
            outcome = RuntimeImageBuildAttemptOutcome(_outcome)

        runtime_image_build_attempt = cls(
            attempt=attempt,
            started_at=started_at,
            completed_at=completed_at,
            outcome=outcome,
        )

        return runtime_image_build_attempt
