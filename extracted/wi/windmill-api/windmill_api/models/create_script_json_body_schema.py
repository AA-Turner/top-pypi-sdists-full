from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateScriptJsonBodySchema")


@_attrs_define
class CreateScriptJsonBodySchema:
    """JSON Schema of the arguments of `main`, which is what a run form and an MCP tool offer. Omitted (or `{}`), it is
    inferred from `content` for TypeScript, Python, Go, Bash, PowerShell, SQL, GraphQL and Ansible scripts. For other
    languages, or code that does not parse, a new script gets none. A new version of an existing script also keeps what
    the previous version's schema says about each argument, or that whole schema when nothing can be inferred. A dbt
    script always takes its schema from its descriptor, whatever is sent.

    """

    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        create_script_json_body_schema = cls()

        create_script_json_body_schema.additional_properties = d
        return create_script_json_body_schema

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
