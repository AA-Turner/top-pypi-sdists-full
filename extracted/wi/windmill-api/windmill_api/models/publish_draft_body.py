from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="PublishDraftBody")


@_attrs_define
class PublishDraftBody:
    """
    Attributes:
        slug (str): hub project slug (3-50 chars, lowercase alphanumeric and hyphens, no leading/trailing hyphen)
        name (str):
        summary (str):
        readme (Union[Unset, str]):
    """

    slug: str
    name: str
    summary: str
    readme: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        slug = self.slug
        name = self.name
        summary = self.summary
        readme = self.readme

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "slug": slug,
                "name": name,
                "summary": summary,
            }
        )
        if readme is not UNSET:
            field_dict["readme"] = readme

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        slug = d.pop("slug")

        name = d.pop("name")

        summary = d.pop("summary")

        readme = d.pop("readme", UNSET)

        publish_draft_body = cls(
            slug=slug,
            name=name,
            summary=summary,
            readme=readme,
        )

        publish_draft_body.additional_properties = d
        return publish_draft_body

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
