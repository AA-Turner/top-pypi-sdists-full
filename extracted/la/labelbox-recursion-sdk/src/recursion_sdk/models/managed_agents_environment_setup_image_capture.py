from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_environment_setup_image_capture_status import ManagedAgentsEnvironmentSetupImageCaptureStatus
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsEnvironmentSetupImageCapture")



@_attrs_define
class ManagedAgentsEnvironmentSetupImageCapture:
    """ Why a verified setup run published no new reusable image.

        Example:
            {'at': '2026-02-18T09:30:00Z', 'message': 'example', 'reason': 'example', 'setupRunId': 'example', 'status':
                'failed'}

        Attributes:
            at (datetime.datetime): When the capture failure was recorded.
            setup_run_id (str): Setup run whose capture failed.
            status (ManagedAgentsEnvironmentSetupImageCaptureStatus): Always failed; successful capture is represented by
                image.
            message (str | Unset): Sanitized bounded explanation.
            reason (str | Unset): Stable Agent Service capture failure reason.
     """

    at: datetime.datetime
    setup_run_id: str
    status: ManagedAgentsEnvironmentSetupImageCaptureStatus
    message: str | Unset = UNSET
    reason: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        at = self.at.isoformat()

        setup_run_id = self.setup_run_id

        status = self.status.value

        message = self.message

        reason = self.reason


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "at": at,
            "setupRunId": setup_run_id,
            "status": status,
        })
        if message is not UNSET:
            field_dict["message"] = message
        if reason is not UNSET:
            field_dict["reason"] = reason

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        at = datetime.datetime.fromisoformat(d.pop("at"))




        setup_run_id = d.pop("setupRunId")

        status = ManagedAgentsEnvironmentSetupImageCaptureStatus(d.pop("status"))




        message = d.pop("message", UNSET)

        reason = d.pop("reason", UNSET)

        managed_agents_environment_setup_image_capture = cls(
            at=at,
            setup_run_id=setup_run_id,
            status=status,
            message=message,
            reason=reason,
        )


        managed_agents_environment_setup_image_capture.additional_properties = d
        return managed_agents_environment_setup_image_capture

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
