from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.scope_variables_response import ScopeVariablesResponse


T = TypeVar("T", bound="WorkspaceVariablesResponse")


@_attrs_define
class WorkspaceVariablesResponse:
    """
    Attributes:
        scopes (list[ScopeVariablesResponse]): Workspace-wide scope first, then each profile scope holding variables
    """

    scopes: list[ScopeVariablesResponse]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scopes = []
        for scopes_item_data in self.scopes:
            scopes_item = scopes_item_data.to_dict()
            scopes.append(scopes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scopes": scopes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.scope_variables_response import ScopeVariablesResponse

        d = dict(src_dict)
        scopes = []
        _scopes = d.pop("scopes")
        for scopes_item_data in _scopes:
            scopes_item = ScopeVariablesResponse.from_dict(scopes_item_data)

            scopes.append(scopes_item)

        workspace_variables_response = cls(
            scopes=scopes,
        )

        workspace_variables_response.additional_properties = d
        return workspace_variables_response

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
