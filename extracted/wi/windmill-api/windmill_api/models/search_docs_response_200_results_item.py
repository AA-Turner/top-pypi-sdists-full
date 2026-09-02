from typing import Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SearchDocsResponse200ResultsItem")


@_attrs_define
class SearchDocsResponse200ResultsItem:
    """
    Attributes:
        url (str):
        title (str):
        score (int):
        snippets (List[str]):
    """

    url: str
    title: str
    score: int
    snippets: List[str]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        title = self.title
        score = self.score
        snippets = self.snippets

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "title": title,
                "score": score,
                "snippets": snippets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url")

        title = d.pop("title")

        score = d.pop("score")

        snippets = cast(List[str], d.pop("snippets"))

        search_docs_response_200_results_item = cls(
            url=url,
            title=title,
            score=score,
            snippets=snippets,
        )

        search_docs_response_200_results_item.additional_properties = d
        return search_docs_response_200_results_item

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
