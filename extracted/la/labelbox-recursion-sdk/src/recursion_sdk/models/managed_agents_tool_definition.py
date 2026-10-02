from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_tool_definition_input_schema_type_0 import ManagedAgentsToolDefinitionInputSchemaType0





T = TypeVar("T", bound="ManagedAgentsToolDefinition")



@_attrs_define
class ManagedAgentsToolDefinition:
    """ One tool as it was offered to the model, in the Anthropic and OpenAI tool-definition vocabulary. Recorded on the
    event for a model turn so a reader can see exactly what the model could call.

        Example:
            {'description': 'example', 'input_schema': {'key': 'example'}, 'name': 'example-name'}

        Attributes:
            description (str): Natural-language explanation of what the tool does and when to use it, supplied to the model
                verbatim.
            input_schema (ManagedAgentsToolDefinitionInputSchemaType0 | None): JSON Schema for the tool's arguments, in the
                same shape the Anthropic and OpenAI tool APIs expect. Passed to the provider unchanged.
            name (str): Tool name the model calls, matching the name on the resulting tool_use content block.
     """

    description: str
    input_schema: ManagedAgentsToolDefinitionInputSchemaType0 | None
    name: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_tool_definition_input_schema_type_0 import ManagedAgentsToolDefinitionInputSchemaType0 # noqa: PLC0415
        description = self.description

        input_schema: dict[str, Any] | None
        if isinstance(self.input_schema, ManagedAgentsToolDefinitionInputSchemaType0):
            input_schema = self.input_schema.to_dict()
        else:
            input_schema = self.input_schema

        name = self.name


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "description": description,
            "input_schema": input_schema,
            "name": name,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_tool_definition_input_schema_type_0 import ManagedAgentsToolDefinitionInputSchemaType0 # noqa: PLC0415
        d = dict(src_dict)
        description = d.pop("description")

        def _parse_input_schema(data: object) -> ManagedAgentsToolDefinitionInputSchemaType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_schema_type_0 = ManagedAgentsToolDefinitionInputSchemaType0.from_dict(data)



                return input_schema_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ManagedAgentsToolDefinitionInputSchemaType0 | None, data)

        input_schema = _parse_input_schema(d.pop("input_schema"))


        name = d.pop("name")

        managed_agents_tool_definition = cls(
            description=description,
            input_schema=input_schema,
            name=name,
        )


        managed_agents_tool_definition.additional_properties = d
        return managed_agents_tool_definition

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
