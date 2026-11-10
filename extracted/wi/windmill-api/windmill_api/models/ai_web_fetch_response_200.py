from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AiWebFetchResponse200")


@_attrs_define
class AiWebFetchResponse200:
    """
    Attributes:
        url (str):
        content (str):
        truncated (bool):
        title (Union[Unset, str]):
    """

    url: str
    content: str
    truncated: bool
    title: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        content = self.content
        truncated = self.truncated
        title = self.title

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "content": content,
                "truncated": truncated,
            }
        )
        if title is not UNSET:
            field_dict["title"] = title

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url")

        content = d.pop("content")

        truncated = d.pop("truncated")

        title = d.pop("title", UNSET)

        ai_web_fetch_response_200 = cls(
            url=url,
            content=content,
            truncated=truncated,
            title=title,
        )

        ai_web_fetch_response_200.additional_properties = d
        return ai_web_fetch_response_200

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
