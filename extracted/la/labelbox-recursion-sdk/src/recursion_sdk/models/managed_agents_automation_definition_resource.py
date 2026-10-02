from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="ManagedAgentsAutomationDefinitionResource")



@_attrs_define
class ManagedAgentsAutomationDefinitionResource:
    """ A workspace file mounted at an explicit path for each automation session.

        Example:
            {'fileId': 'example', 'mountPath': 'example'}

        Attributes:
            file_id (str): File to attach from this workspace.
            mount_path (str): Absolute mount path beneath the session files directory.
     """

    file_id: str
    mount_path: str





    def to_dict(self) -> dict[str, Any]:
        file_id = self.file_id

        mount_path = self.mount_path


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "fileId": file_id,
            "mountPath": mount_path,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        file_id = d.pop("fileId")

        mount_path = d.pop("mountPath")

        managed_agents_automation_definition_resource = cls(
            file_id=file_id,
            mount_path=mount_path,
        )

        return managed_agents_automation_definition_resource

