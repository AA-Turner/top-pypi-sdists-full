from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.create_run_config_dto_config_mcp_tools_item_input_schema_type_1 import CreateRunConfigDtoConfigMcpToolsItemInputSchemaType1





T = TypeVar("T", bound="CreateRunConfigDtoConfigMcpToolsItem")



@_attrs_define
class CreateRunConfigDtoConfigMcpToolsItem:
    """ One MCP tool from the MCP service list_tools() catalogue, persisted as metadata for future grader-UI use.

        Attributes:
            name (str): Tool name as exposed by the MCP service. The newer catalogue format encodes the service as a dotted
                prefix (e.g. "gitea.create_user"); use mcpToolServiceKey to extract it.
            description (str): Human-readable description of what the tool does.
            input_schema (CreateRunConfigDtoConfigMcpToolsItemInputSchemaType1 | str): Tool input JSON Schema, stored as an
                opaque JSON string (see comment).
            service (str | Unset): MCP service the tool belongs to. Omitted when encoded as the name prefix.
            category (str | Unset): Grouping category for the tool in UIs.
            sort_order (int | Unset): Display ordering hint within a category.
            read_only (bool | Unset): Whether the tool only reads state (no side effects). Omitted when unknown.
            timeout (int | Unset): Tool invocation timeout in seconds.
            service_label (str | Unset): Optional human-friendly label for the service (MCP wire key _service_label).
     """

    name: str
    description: str
    input_schema: CreateRunConfigDtoConfigMcpToolsItemInputSchemaType1 | str
    service: str | Unset = UNSET
    category: str | Unset = UNSET
    sort_order: int | Unset = UNSET
    read_only: bool | Unset = UNSET
    timeout: int | Unset = UNSET
    service_label: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.create_run_config_dto_config_mcp_tools_item_input_schema_type_1 import CreateRunConfigDtoConfigMcpToolsItemInputSchemaType1 # noqa: PLC0415
        name = self.name

        description = self.description

        input_schema: dict[str, Any] | str
        if isinstance(self.input_schema, CreateRunConfigDtoConfigMcpToolsItemInputSchemaType1):
            input_schema = self.input_schema.to_dict()
        else:
            input_schema = self.input_schema

        service = self.service

        category = self.category

        sort_order = self.sort_order

        read_only = self.read_only

        timeout = self.timeout

        service_label = self.service_label


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "description": description,
            "inputSchema": input_schema,
        })
        if service is not UNSET:
            field_dict["service"] = service
        if category is not UNSET:
            field_dict["category"] = category
        if sort_order is not UNSET:
            field_dict["sortOrder"] = sort_order
        if read_only is not UNSET:
            field_dict["readOnly"] = read_only
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if service_label is not UNSET:
            field_dict["serviceLabel"] = service_label

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_run_config_dto_config_mcp_tools_item_input_schema_type_1 import CreateRunConfigDtoConfigMcpToolsItemInputSchemaType1 # noqa: PLC0415
        d = dict(src_dict)
        name = d.pop("name")

        description = d.pop("description")

        def _parse_input_schema(data: object) -> CreateRunConfigDtoConfigMcpToolsItemInputSchemaType1 | str:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                input_schema_type_1 = CreateRunConfigDtoConfigMcpToolsItemInputSchemaType1.from_dict(data)



                return input_schema_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(CreateRunConfigDtoConfigMcpToolsItemInputSchemaType1 | str, data)

        input_schema = _parse_input_schema(d.pop("inputSchema"))


        service = d.pop("service", UNSET)

        category = d.pop("category", UNSET)

        sort_order = d.pop("sortOrder", UNSET)

        read_only = d.pop("readOnly", UNSET)

        timeout = d.pop("timeout", UNSET)

        service_label = d.pop("serviceLabel", UNSET)

        create_run_config_dto_config_mcp_tools_item = cls(
            name=name,
            description=description,
            input_schema=input_schema,
            service=service,
            category=category,
            sort_order=sort_order,
            read_only=read_only,
            timeout=timeout,
            service_label=service_label,
        )


        create_run_config_dto_config_mcp_tools_item.additional_properties = d
        return create_run_config_dto_config_mcp_tools_item

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
