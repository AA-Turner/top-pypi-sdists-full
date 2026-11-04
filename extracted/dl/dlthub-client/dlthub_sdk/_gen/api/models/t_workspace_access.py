from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.t_workspace_access_context_item_type_0 import (
    TWorkspaceAccessContextItemType0,
)
from ..models.t_workspace_access_data_item_type_0 import TWorkspaceAccessDataItemType0
from ..models.t_workspace_access_local_item_type_0 import TWorkspaceAccessLocalItemType0
from ..types import UNSET, Unset

T = TypeVar("T", bound="TWorkspaceAccess")


@_attrs_define
class TWorkspaceAccess:
    """
    Attributes:
        context (list[str | TWorkspaceAccessContextItemType0] | Unset):
        data (list[str | TWorkspaceAccessDataItemType0] | Unset):
        local (list[str | TWorkspaceAccessLocalItemType0] | Unset):
    """

    context: list[str | TWorkspaceAccessContextItemType0] | Unset = UNSET
    data: list[str | TWorkspaceAccessDataItemType0] | Unset = UNSET
    local: list[str | TWorkspaceAccessLocalItemType0] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        context: list[str] | Unset = UNSET
        if not isinstance(self.context, Unset):
            context = []
            for context_item_data in self.context:
                context_item: str
                if isinstance(context_item_data, TWorkspaceAccessContextItemType0):
                    context_item = context_item_data.value
                else:
                    context_item = context_item_data
                context.append(context_item)

        data: list[str] | Unset = UNSET
        if not isinstance(self.data, Unset):
            data = []
            for data_item_data in self.data:
                data_item: str
                if isinstance(data_item_data, TWorkspaceAccessDataItemType0):
                    data_item = data_item_data.value
                else:
                    data_item = data_item_data
                data.append(data_item)

        local: list[str] | Unset = UNSET
        if not isinstance(self.local, Unset):
            local = []
            for local_item_data in self.local:
                local_item: str
                if isinstance(local_item_data, TWorkspaceAccessLocalItemType0):
                    local_item = local_item_data.value
                else:
                    local_item = local_item_data
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
        context: list[str | TWorkspaceAccessContextItemType0] | Unset = UNSET
        if _context is not UNSET:
            context = []
            for context_item_data in _context:

                def _parse_context_item(
                    data: object,
                ) -> str | TWorkspaceAccessContextItemType0:
                    try:
                        if not isinstance(data, str):
                            raise TypeError()
                        context_item_type_0 = TWorkspaceAccessContextItemType0(data)

                        return context_item_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    return cast(str | TWorkspaceAccessContextItemType0, data)

                context_item = _parse_context_item(context_item_data)

                context.append(context_item)

        _data = d.pop("data", UNSET)
        data: list[str | TWorkspaceAccessDataItemType0] | Unset = UNSET
        if _data is not UNSET:
            data = []
            for data_item_data in _data:

                def _parse_data_item(
                    data: object,
                ) -> str | TWorkspaceAccessDataItemType0:
                    try:
                        if not isinstance(data, str):
                            raise TypeError()
                        data_item_type_0 = TWorkspaceAccessDataItemType0(data)

                        return data_item_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    return cast(str | TWorkspaceAccessDataItemType0, data)

                data_item = _parse_data_item(data_item_data)

                data.append(data_item)

        _local = d.pop("local", UNSET)
        local: list[str | TWorkspaceAccessLocalItemType0] | Unset = UNSET
        if _local is not UNSET:
            local = []
            for local_item_data in _local:

                def _parse_local_item(
                    data: object,
                ) -> str | TWorkspaceAccessLocalItemType0:
                    try:
                        if not isinstance(data, str):
                            raise TypeError()
                        local_item_type_0 = TWorkspaceAccessLocalItemType0(data)

                        return local_item_type_0
                    except (TypeError, ValueError, AttributeError, KeyError):
                        pass
                    return cast(str | TWorkspaceAccessLocalItemType0, data)

                local_item = _parse_local_item(local_item_data)

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
