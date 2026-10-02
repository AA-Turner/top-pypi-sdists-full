from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset






T = TypeVar("T", bound="ManagedAgentsManualAutomationDefinitionRunRequest")



@_attrs_define
class ManagedAgentsManualAutomationDefinitionRunRequest:
    """ Structured input for explicitly running a canonical automation.

        Example:
            {'payload': 'example'}

        Attributes:
            payload (Any | Unset): Optional deliberately open JSON value supplied to this run and frozen in its event
                context.
     """

    payload: Any | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        payload = self.payload


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if payload is not UNSET:
            field_dict["payload"] = payload

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        payload = d.pop("payload", UNSET)

        managed_agents_manual_automation_definition_run_request = cls(
            payload=payload,
        )

        return managed_agents_manual_automation_definition_run_request

