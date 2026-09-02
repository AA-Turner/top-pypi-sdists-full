from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.endpoint_tool_body_schema import EndpointToolBodySchema
    from ..models.endpoint_tool_path_params_schema import EndpointToolPathParamsSchema
    from ..models.endpoint_tool_query_params_schema import EndpointToolQueryParamsSchema


T = TypeVar("T", bound="EndpointTool")


@_attrs_define
class EndpointTool:
    """
    Attributes:
        name (str): The tool name/operation ID
        description (str): Short description of the tool
        instructions (str): Detailed instructions for using the tool
        path (str): API endpoint path
        method (str): HTTP method (GET, POST, etc.)
        path_params_schema (Union[Unset, None, EndpointToolPathParamsSchema]): JSON schema for path parameters
        query_params_schema (Union[Unset, None, EndpointToolQueryParamsSchema]): JSON schema for query parameters
        body_schema (Union[Unset, None, EndpointToolBodySchema]): JSON schema for request body
    """

    name: str
    description: str
    instructions: str
    path: str
    method: str
    path_params_schema: Union[Unset, None, "EndpointToolPathParamsSchema"] = UNSET
    query_params_schema: Union[Unset, None, "EndpointToolQueryParamsSchema"] = UNSET
    body_schema: Union[Unset, None, "EndpointToolBodySchema"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        description = self.description
        instructions = self.instructions
        path = self.path
        method = self.method
        path_params_schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.path_params_schema, Unset):
            path_params_schema = self.path_params_schema.to_dict() if self.path_params_schema else None

        query_params_schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.query_params_schema, Unset):
            query_params_schema = self.query_params_schema.to_dict() if self.query_params_schema else None

        body_schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.body_schema, Unset):
            body_schema = self.body_schema.to_dict() if self.body_schema else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "description": description,
                "instructions": instructions,
                "path": path,
                "method": method,
            }
        )
        if path_params_schema is not UNSET:
            field_dict["path_params_schema"] = path_params_schema
        if query_params_schema is not UNSET:
            field_dict["query_params_schema"] = query_params_schema
        if body_schema is not UNSET:
            field_dict["body_schema"] = body_schema

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.endpoint_tool_body_schema import EndpointToolBodySchema
        from ..models.endpoint_tool_path_params_schema import EndpointToolPathParamsSchema
        from ..models.endpoint_tool_query_params_schema import EndpointToolQueryParamsSchema

        d = src_dict.copy()
        name = d.pop("name")

        description = d.pop("description")

        instructions = d.pop("instructions")

        path = d.pop("path")

        method = d.pop("method")

        _path_params_schema = d.pop("path_params_schema", UNSET)
        path_params_schema: Union[Unset, None, EndpointToolPathParamsSchema]
        if _path_params_schema is None:
            path_params_schema = None
        elif isinstance(_path_params_schema, Unset):
            path_params_schema = UNSET
        else:
            path_params_schema = EndpointToolPathParamsSchema.from_dict(_path_params_schema)

        _query_params_schema = d.pop("query_params_schema", UNSET)
        query_params_schema: Union[Unset, None, EndpointToolQueryParamsSchema]
        if _query_params_schema is None:
            query_params_schema = None
        elif isinstance(_query_params_schema, Unset):
            query_params_schema = UNSET
        else:
            query_params_schema = EndpointToolQueryParamsSchema.from_dict(_query_params_schema)

        _body_schema = d.pop("body_schema", UNSET)
        body_schema: Union[Unset, None, EndpointToolBodySchema]
        if _body_schema is None:
            body_schema = None
        elif isinstance(_body_schema, Unset):
            body_schema = UNSET
        else:
            body_schema = EndpointToolBodySchema.from_dict(_body_schema)

        endpoint_tool = cls(
            name=name,
            description=description,
            instructions=instructions,
            path=path,
            method=method,
            path_params_schema=path_params_schema,
            query_params_schema=query_params_schema,
            body_schema=body_schema,
        )

        endpoint_tool.additional_properties = d
        return endpoint_tool

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
