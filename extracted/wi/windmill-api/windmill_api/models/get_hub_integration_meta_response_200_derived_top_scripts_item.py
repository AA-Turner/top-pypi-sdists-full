from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetHubIntegrationMetaResponse200DerivedTopScriptsItem")


@_attrs_define
class GetHubIntegrationMetaResponse200DerivedTopScriptsItem:
    """
    Attributes:
        path (str):
        summary (str):
        kind (str):
        ask_id (Union[Unset, float]):
        version_id (Union[Unset, float]):
        description (Union[Unset, None, str]):
        language (Union[Unset, None, str]):
        views (Union[Unset, float]):
        votes (Union[Unset, float]):
    """

    path: str
    summary: str
    kind: str
    ask_id: Union[Unset, float] = UNSET
    version_id: Union[Unset, float] = UNSET
    description: Union[Unset, None, str] = UNSET
    language: Union[Unset, None, str] = UNSET
    views: Union[Unset, float] = UNSET
    votes: Union[Unset, float] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        summary = self.summary
        kind = self.kind
        ask_id = self.ask_id
        version_id = self.version_id
        description = self.description
        language = self.language
        views = self.views
        votes = self.votes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "summary": summary,
                "kind": kind,
            }
        )
        if ask_id is not UNSET:
            field_dict["ask_id"] = ask_id
        if version_id is not UNSET:
            field_dict["version_id"] = version_id
        if description is not UNSET:
            field_dict["description"] = description
        if language is not UNSET:
            field_dict["language"] = language
        if views is not UNSET:
            field_dict["views"] = views
        if votes is not UNSET:
            field_dict["votes"] = votes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        summary = d.pop("summary")

        kind = d.pop("kind")

        ask_id = d.pop("ask_id", UNSET)

        version_id = d.pop("version_id", UNSET)

        description = d.pop("description", UNSET)

        language = d.pop("language", UNSET)

        views = d.pop("views", UNSET)

        votes = d.pop("votes", UNSET)

        get_hub_integration_meta_response_200_derived_top_scripts_item = cls(
            path=path,
            summary=summary,
            kind=kind,
            ask_id=ask_id,
            version_id=version_id,
            description=description,
            language=language,
            views=views,
            votes=votes,
        )

        get_hub_integration_meta_response_200_derived_top_scripts_item.additional_properties = d
        return get_hub_integration_meta_response_200_derived_top_scripts_item

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
