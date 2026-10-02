from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsEnvironmentSetupRunSummary")



@_attrs_define
class ManagedAgentsEnvironmentSetupRunSummary:
    """ The outcome of one setup run, reduced to what a caller needs to fix it: exit code, failing line, stderr tail, and a
    hint when the cause is recognised.

        Example:
            {'duration_ms': 1, 'exit_code': 1, 'failed_command': 'example', 'failed_line': 1, 'hint': 'example',
                'hint_code': 'example', 'message': 'example', 'phase': 'example', 'setup_run_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status': 'example', 'stderr_tail': 'example'}

        Attributes:
            setup_run_id (str): Setup run this summary describes.
            status (str): succeeded, failed, or cancelled.
            duration_ms (int | Unset): Wall-clock duration of the run in milliseconds, provisioning included.
            exit_code (int | Unset): Exit code of the setup script when it ran. 124 means the timeout elapsed; absent when
                the run failed before the script started.
            failed_command (str | Unset): The failing line's command as written in the script, unexpanded, so it never
                contains a secret's value.
            failed_line (int | Unset): 1-based line in the setup script whose command exited non-zero. 0 when unknown.
            hint (str | Unset): Human-readable likely fix for a recognised failure cause. Absent rather than guessed when
                the cause is not recognised.
            hint_code (str | Unset): Stable identifier of the recognised failure cause, e.g. command_not_found,
                pip_not_installed, bash_lc_wrapper, egress_blocked, timeout. Absent when the cause was not recognised.
            message (str | Unset): One-sentence description of the outcome suitable for showing as is.
            phase (str | Unset): Phase the run ended in: provision, gpu_check, setup, profile, commit, or cleanup. A failure
                outside setup is about the platform, not the script.
            stderr_tail (str | Unset): Last lines of stderr from the script, redacted and bounded to 2 KiB.
     """

    setup_run_id: str
    status: str
    duration_ms: int | Unset = UNSET
    exit_code: int | Unset = UNSET
    failed_command: str | Unset = UNSET
    failed_line: int | Unset = UNSET
    hint: str | Unset = UNSET
    hint_code: str | Unset = UNSET
    message: str | Unset = UNSET
    phase: str | Unset = UNSET
    stderr_tail: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        setup_run_id = self.setup_run_id

        status = self.status

        duration_ms = self.duration_ms

        exit_code = self.exit_code

        failed_command = self.failed_command

        failed_line = self.failed_line

        hint = self.hint

        hint_code = self.hint_code

        message = self.message

        phase = self.phase

        stderr_tail = self.stderr_tail


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "setup_run_id": setup_run_id,
            "status": status,
        })
        if duration_ms is not UNSET:
            field_dict["duration_ms"] = duration_ms
        if exit_code is not UNSET:
            field_dict["exit_code"] = exit_code
        if failed_command is not UNSET:
            field_dict["failed_command"] = failed_command
        if failed_line is not UNSET:
            field_dict["failed_line"] = failed_line
        if hint is not UNSET:
            field_dict["hint"] = hint
        if hint_code is not UNSET:
            field_dict["hint_code"] = hint_code
        if message is not UNSET:
            field_dict["message"] = message
        if phase is not UNSET:
            field_dict["phase"] = phase
        if stderr_tail is not UNSET:
            field_dict["stderr_tail"] = stderr_tail

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        setup_run_id = d.pop("setup_run_id")

        status = d.pop("status")

        duration_ms = d.pop("duration_ms", UNSET)

        exit_code = d.pop("exit_code", UNSET)

        failed_command = d.pop("failed_command", UNSET)

        failed_line = d.pop("failed_line", UNSET)

        hint = d.pop("hint", UNSET)

        hint_code = d.pop("hint_code", UNSET)

        message = d.pop("message", UNSET)

        phase = d.pop("phase", UNSET)

        stderr_tail = d.pop("stderr_tail", UNSET)

        managed_agents_environment_setup_run_summary = cls(
            setup_run_id=setup_run_id,
            status=status,
            duration_ms=duration_ms,
            exit_code=exit_code,
            failed_command=failed_command,
            failed_line=failed_line,
            hint=hint,
            hint_code=hint_code,
            message=message,
            phase=phase,
            stderr_tail=stderr_tail,
        )


        managed_agents_environment_setup_run_summary.additional_properties = d
        return managed_agents_environment_setup_run_summary

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
