from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.t_workspace_access_context_item import TWorkspaceAccessContextItem
from ..models.t_workspace_access_data_item import TWorkspaceAccessDataItem
from ..models.t_workspace_access_local_item import TWorkspaceAccessLocalItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="TWorkspaceAccess")


@_attrs_define
class TWorkspaceAccess:
    """
    Attributes:
        context (list[TWorkspaceAccessContextItem] | Unset):
        data (list[TWorkspaceAccessDataItem] | Unset):
        local (list[TWorkspaceAccessLocalItem] | Unset):
    """

    context: list[TWorkspaceAccessContextItem] | Unset = UNSET
    data: list[TWorkspaceAccessDataItem] | Unset = UNSET
    local: list[TWorkspaceAccessLocalItem] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        context: list[str] | Unset = UNSET
        if not isinstance(self.context, Unset):
            context = []
            for context_item_data in self.context:
                context_item = context_item_data.value
                context.append(context_item)

        data: list[str] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item = data_item_data.value
                data.append(data_item)

        local: list[str] | Unset = UNSET
        if not isinstance(self.local, Unset):
            local = []
            for local_item_data in self.local:
                local_item = local_item_data.value
                local.append(local_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if context is not UNSET:
            field_dict["context"] = context
        if data is not UNSET:
            field_dict["data"] = data
        if local is not UNSET:
            field_dict["local"] = local

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _context = d.pop("context", UNSET)
        context: list[TWorkspaceAccessContextItem] | Unset = UNSET
        if _context is not UNSET:
            context = []
            for context_item_data in _context:
                context_item = TWorkspaceAccessContextItem(context_item_data)

                context.append(context_item)

        _data = d.pop("data", UNSET)
        data: list[TWorkspaceAccessDataItem] | Unset = UNSET
        if _data is not UNSET:
            data = []
            for data_item_data in _data:
                data_item = TWorkspaceAccessDataItem(data_item_data)

                data.append(data_item)

        _local = d.pop("local", UNSET)
        local: list[TWorkspaceAccessLocalItem] | Unset = UNSET
        if _local is not UNSET:
            local = []
            for local_item_data in _local:
                local_item = TWorkspaceAccessLocalItem(local_item_data)

                local.append(local_item)

        t_workspace_access = cls(
            context=context,
            data=data,
            local=local,
        )

        t_workspace_access.additional_properties = d
        return t_workspace_access

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
