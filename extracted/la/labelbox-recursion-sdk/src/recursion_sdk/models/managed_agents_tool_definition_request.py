from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_tool_definition_request_input_schema_type_0 import ManagedAgentsToolDefinitionRequestInputSchemaType0





T = TypeVar("T", bound="ManagedAgentsToolDefinitionRequest")



@_attrs_define
class ManagedAgentsToolDefinitionRequest:
    """ One tool as it was offered to the model, in the Anthropic and OpenAI tool-definition vocabulary. Recorded on the
    event for a model turn so a reader can see exactly what the model could call.

        Example:
            {'description': 'example', 'input_schema': {'key': 'example'}, 'name': 'example-name'}

        Attributes:
            description (str | Unset): Natural-language explanation of what the tool does and when to use it, supplied to
                the model verbatim.
            input_schema (ManagedAgentsToolDefinitionRequestInputSchemaType0 | None | Unset): JSON Schema for the tool's
                arguments, in the same shape the Anthropic and OpenAI tool APIs expect. Passed to the provider unchanged.
            name (str | Unset): Tool name the model calls, matching the name on the resulting tool_use content block.
     """

    description: str | Unset = UNSET
    input_schema: ManagedAgentsToolDefinitionRequestInputSchemaType0 | None | Unset = UNSET
    name: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_tool_definition_request_input_schema_type_0 import ManagedAgentsToolDefinitionRequestInputSchemaType0 # noqa: PLC0415
        description = self.description

        input_schema: dict[str, Any] | None | Unset
        if isinstance(self.input_schema, Unset):
            input_schema = UNSET
        elif isinstance(self.input_schema, ManagedAgentsToolDefinitionRequestInputSchemaType0):
            input_schema = self.input_schema.to_dict()
        else:
            input_schema = self.input_schema

        name = self.name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if description is not UNSET:
            field_dict["description"] = description
        if input_schema is not UNSET:
            field_dict["input_schema"] = input_schema
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_tool_definition_request_input_schema_type_0 import ManagedAgentsToolDefinitionRequestInputSchemaType0 # noqa: PLC0415
        d = dict(src_dict)
        description = d.pop("description", UNSET)

        def _parse_input_schema(data: object) -> ManagedAgentsToolDefinitionRequestInputSchemaType0 | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_schema_type_0 = ManagedAgentsToolDefinitionRequestInputSchemaType0.from_dict(data)



                return input_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ManagedAgentsToolDefinitionRequestInputSchemaType0 | None | Unset, data)

        input_schema = _parse_input_schema(d.pop("input_schema", UNSET))


        name = d.pop("name", UNSET)

        managed_agents_tool_definition_request = cls(
            description=description,
            input_schema=input_schema,
            name=name,
        )


        managed_agents_tool_definition_request.additional_properties = d
        return managed_agents_tool_definition_request

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
