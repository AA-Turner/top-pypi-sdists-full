from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.plain_public_variable import PlainPublicVariable
    from ..models.secret_public_variable import SecretPublicVariable


T = TypeVar("T", bound="ScopeVariablesResponse")


@_attrs_define
class ScopeVariablesResponse:
    """
    Attributes:
        profile (None | str): Profile owning this scope; `null` is the workspace-wide scope
        variables (list[PlainPublicVariable | SecretPublicVariable]): Variables in this scope, secrets redacted
    """

    profile: None | str
    variables: list[PlainPublicVariable | SecretPublicVariable]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.plain_public_variable import PlainPublicVariable

        profile: None | str
        profile = self.profile

        variables = []
        for variables_item_data in self.variables:
            variables_item: dict[str, Any]
            if isinstance(variables_item_data, PlainPublicVariable):
                variables_item = variables_item_data.to_dict()
            else:
                variables_item = variables_item_data.to_dict()

            variables.append(variables_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "profile": profile,
                "variables": variables,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.plain_public_variable import PlainPublicVariable
        from ..models.secret_public_variable import SecretPublicVariable

        d = dict(src_dict)

        def _parse_profile(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        profile = _parse_profile(d.pop("profile"))

        variables = []
        _variables = d.pop("variables")
        for variables_item_data in _variables:

            def _parse_variables_item(
                data: object,
            ) -> PlainPublicVariable | SecretPublicVariable:
                try:
                    if not isinstance(data, dict):
                        raise TypeError()
                    variables_item_type_0 = PlainPublicVariable.from_dict(data)

                    return variables_item_type_0
                except (TypeError, ValueError, AttributeError, KeyError):
                    pass
                if not isinstance(data, dict):
                    raise TypeError()
                variables_item_type_1 = SecretPublicVariable.from_dict(data)

                return variables_item_type_1

            variables_item = _parse_variables_item(variables_item_data)

            variables.append(variables_item)

        scope_variables_response = cls(
            profile=profile,
            variables=variables,
        )

        scope_variables_response.additional_properties = d
        return scope_variables_response

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
