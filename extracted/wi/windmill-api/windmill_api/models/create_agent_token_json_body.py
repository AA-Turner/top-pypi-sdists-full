from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateAgentTokenJsonBody")


@_attrs_define
class CreateAgentTokenJsonBody:
    """
    Attributes:
        worker_group (str):
        tags (List[str]):
        exp (int):
    """

    worker_group: str
    tags: List[str]
    exp: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        worker_group = self.worker_group
        tags = self.tags

        exp = self.exp

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "worker_group": worker_group,
                "tags": tags,
                "exp": exp,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        worker_group = d.pop("worker_group")

        tags = cast(List[str], d.pop("tags"))

        exp = d.pop("exp")

        create_agent_token_json_body = cls(
            worker_group=worker_group,
            tags=tags,
            exp=exp,
        )

        create_agent_token_json_body.additional_properties = d
        return create_agent_token_json_body

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
