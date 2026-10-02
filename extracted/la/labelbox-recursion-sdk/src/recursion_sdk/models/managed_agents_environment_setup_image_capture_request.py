from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_environment_setup_image_capture_request_status import ManagedAgentsEnvironmentSetupImageCaptureRequestStatus
from ..types import UNSET, Unset
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsEnvironmentSetupImageCaptureRequest")



@_attrs_define
class ManagedAgentsEnvironmentSetupImageCaptureRequest:
    """ Why a verified setup run published no new reusable image.

        Example:
            {'at': '2026-02-18T09:30:00Z', 'message': 'example', 'reason': 'example', 'setupRunId': 'example', 'status':
                'failed'}

        Attributes:
            at (datetime.datetime | Unset): When the capture failure was recorded.
            message (str | Unset): Sanitized bounded explanation.
            reason (str | Unset): Stable Agent Service capture failure reason.
            setup_run_id (str | Unset): Setup run whose capture failed.
            status (ManagedAgentsEnvironmentSetupImageCaptureRequestStatus | Unset): Always failed; successful capture is
                represented by image.
     """

    at: datetime.datetime | Unset = UNSET
    message: str | Unset = UNSET
    reason: str | Unset = UNSET
    setup_run_id: str | Unset = UNSET
    status: ManagedAgentsEnvironmentSetupImageCaptureRequestStatus | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        at: str | Unset = UNSET
        if not isinstance(self.at, Unset):
            at = self.at.isoformat()

        message = self.message

        reason = self.reason

        setup_run_id = self.setup_run_id

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if at is not UNSET:
            field_dict["at"] = at
        if message is not UNSET:
            field_dict["message"] = message
        if reason is not UNSET:
            field_dict["reason"] = reason
        if setup_run_id is not UNSET:
            field_dict["setupRunId"] = setup_run_id
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _at = d.pop("at", UNSET)
        at: datetime.datetime | Unset
        if isinstance(_at,  Unset):
            at = UNSET
        else:
            at = datetime.datetime.fromisoformat(_at)




        message = d.pop("message", UNSET)

        reason = d.pop("reason", UNSET)

        setup_run_id = d.pop("setupRunId", UNSET)

        _status = d.pop("status", UNSET)
        status: ManagedAgentsEnvironmentSetupImageCaptureRequestStatus | Unset
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = ManagedAgentsEnvironmentSetupImageCaptureRequestStatus(_status)




        managed_agents_environment_setup_image_capture_request = cls(
            at=at,
            message=message,
            reason=reason,
            setup_run_id=setup_run_id,
            status=status,
        )


        managed_agents_environment_setup_image_capture_request.additional_properties = d
        return managed_agents_environment_setup_image_capture_request

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
