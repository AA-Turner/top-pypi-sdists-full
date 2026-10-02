from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsSessionCreatedResponse")



@_attrs_define
class ManagedAgentsSessionCreatedResponse:
    """ Response body of POST /v1/sessions, returned with HTTP 202 and a Location header. The 202 is load-bearing: the
    session is accepted, not started, so no status, sandbox, or event exists yet and nothing here reports success of the
    run. Poll status_path, or stream events, to observe provisioning and execution.

        Example:
            {'session_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'status_path': 'example'}

        Attributes:
            session_id (str): Identifier for this session (UUID). Server-assigned. Derived deterministically from the
                Idempotency-Key when one was sent, so a retried create returns the same id rather than starting a second
                session.
            status_path (str): Path to poll for provisioning, execution, and structured failure state.
     """

    session_id: str
    status_path: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        session_id = self.session_id

        status_path = self.status_path


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "session_id": session_id,
            "status_path": status_path,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        session_id = d.pop("session_id")

        status_path = d.pop("status_path")

        managed_agents_session_created_response = cls(
            session_id=session_id,
            status_path=status_path,
        )


        managed_agents_session_created_response.additional_properties = d
        return managed_agents_session_created_response

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
