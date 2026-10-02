from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_session_failure_category import ManagedAgentsSessionFailureCategory
from typing import cast
import datetime






T = TypeVar("T", bound="ManagedAgentsSessionFailure")



@_attrs_define
class ManagedAgentsSessionFailure:
    """ Structured, sanitized reason a session terminated abnormally. Present on a session only after a terminal failure;
    healthy and legacy sessions omit it.

        Example:
            {'at': '2026-02-18T09:30:00Z', 'category': 'transient', 'code': 'example', 'message': 'example', 'phase':
                'example', 'retryable': True}

        Attributes:
            at (datetime.datetime): Time the terminal failure was persisted.
            category (ManagedAgentsSessionFailureCategory): Who can act on this failure: transient (wait or retry),
                caller_error (change the request or configuration, retrying as-is will not help), or internal (report it).
                retryable=false with category=caller_error is a fixable mistake, not an outage. A retryable failure is never
                caller_error: if the platform will retry, changing the request is not the fix.
            code (str): Stable machine-readable failure code.
            message (str): Sanitized bounded operator-facing message; never contains raw provider response bodies or
                credentials.
            phase (str): Lifecycle phase that failed, such as provisioning, setup, workflow, or model.
            retryable (bool): Whether the platform will retry, or a retry of the same request may succeed on its own. False
                does not mean permanently broken -- read category to tell a transient condition from a request the caller must
                change.
     """

    at: datetime.datetime
    category: ManagedAgentsSessionFailureCategory
    code: str
    message: str
    phase: str
    retryable: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        at = self.at.isoformat()

        category = self.category.value

        code = self.code

        message = self.message

        phase = self.phase

        retryable = self.retryable


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "at": at,
            "category": category,
            "code": code,
            "message": message,
            "phase": phase,
            "retryable": retryable,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        at = datetime.datetime.fromisoformat(d.pop("at"))




        category = ManagedAgentsSessionFailureCategory(d.pop("category"))




        code = d.pop("code")

        message = d.pop("message")

        phase = d.pop("phase")

        retryable = d.pop("retryable")

        managed_agents_session_failure = cls(
            at=at,
            category=category,
            code=code,
            message=message,
            phase=phase,
            retryable=retryable,
        )


        managed_agents_session_failure.additional_properties = d
        return managed_agents_session_failure

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
