from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsCancelledResponse")



@_attrs_define
class ManagedAgentsCancelledResponse:
    """ Response body of POST /v1/sessions/{session_id}/cancel. Cancel is terminal for the run but not for the record: the
    workflow is stopped and the sandbox torn down, while the session, its events, and its outcomes remain readable. The
    session row itself is removed from reads only by the separate soft-delete endpoint.

        Example:
            {'cancelled': True}

        Attributes:
            cancelled (bool): Always true. The workflow was cancelled and the sandbox closed; failures are HTTP errors
                instead, so this field never reports false. It is also true when the session had already reached a terminal
                state, making cancel safe to retry.
     """

    cancelled: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        cancelled = self.cancelled


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "cancelled": cancelled,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        cancelled = d.pop("cancelled")

        managed_agents_cancelled_response = cls(
            cancelled=cancelled,
        )


        managed_agents_cancelled_response.additional_properties = d
        return managed_agents_cancelled_response

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
