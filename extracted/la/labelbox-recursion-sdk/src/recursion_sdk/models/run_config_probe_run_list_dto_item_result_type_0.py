from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime






T = TypeVar("T", bound="RunConfigProbeRunListDtoItemResultType0")



@_attrs_define
class RunConfigProbeRunListDtoItemResultType0:
    """ Persisted shape of the probe-run result on terminal rows — the probe outcome plus the time it completed.

        Attributes:
            passed (bool): True when the harness exited cleanly and the LLM judge ruled the transcript satisfies the quality
                check.
            exit_code (int | None): Harness exit code. Null when the harness never reached the exit step (build failure,
                submit-call rejection).
            transcript (str): JSON-encoded array of agent-service events captured during the probe run. The frontend re-
                parses it for the transcript viewer.
            failure_reason (None | str): Human-readable reason the probe failed. For exit-code failures: the upstream error.
                For judge failures: the judge's one-line explanation. Null on passing runs.
            run_at (datetime.datetime): Timestamp when this probe run reached its terminal state (ISO-8601, UTC). Lets the
                UI render "last probed N minutes ago" without a second source of truth.
     """

    passed: bool
    exit_code: int | None
    transcript: str
    failure_reason: None | str
    run_at: datetime.datetime





    def to_dict(self) -> dict[str, Any]:
        passed = self.passed

        exit_code: int | None
        exit_code = self.exit_code

        transcript = self.transcript

        failure_reason: None | str
        failure_reason = self.failure_reason

        run_at = self.run_at.isoformat()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "passed": passed,
            "exitCode": exit_code,
            "transcript": transcript,
            "failureReason": failure_reason,
            "runAt": run_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        passed = d.pop("passed")

        def _parse_exit_code(data: object) -> int | None:
            if data is None:
                return data
            return cast(int | None, data)

        exit_code = _parse_exit_code(d.pop("exitCode"))


        transcript = d.pop("transcript")

        def _parse_failure_reason(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        failure_reason = _parse_failure_reason(d.pop("failureReason"))


        run_at = datetime.datetime.fromisoformat(d.pop("runAt"))




        run_config_probe_run_list_dto_item_result_type_0 = cls(
            passed=passed,
            exit_code=exit_code,
            transcript=transcript,
            failure_reason=failure_reason,
            run_at=run_at,
        )

        return run_config_probe_run_list_dto_item_result_type_0

