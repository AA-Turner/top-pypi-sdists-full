from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="AiWebSearchResponse200ResultsItem")


@_attrs_define
class AiWebSearchResponse200ResultsItem:
    """
    Attributes:
        title (str):
        url (str):
        content (str):
        published_date (Union[Unset, str]):
    """

    title: str
    url: str
    content: str
    published_date: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        url = self.url
        content = self.content
        published_date = self.published_date

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "title": title,
                "url": url,
                "content": content,
            }
        )
        if published_date is not UNSET:
            field_dict["published_date"] = published_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title")

        url = d.pop("url")

        content = d.pop("content")

        published_date = d.pop("published_date", UNSET)

        ai_web_search_response_200_results_item = cls(
            title=title,
            url=url,
            content=content,
            published_date=published_date,
        )

        ai_web_search_response_200_results_item.additional_properties = d
        return ai_web_search_response_200_results_item

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
