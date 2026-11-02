from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.publish_app_body_app import PublishAppBodyApp


T = TypeVar("T", bound="PublishAppBody")


@_attrs_define
class PublishAppBody:
    """
    Attributes:
        app (PublishAppBodyApp):
        apps (List[str]):
        summary (str):
        project_slug (str): hub project slug (3-50 chars, lowercase alphanumeric and hyphens, no leading/trailing
            hyphen)
        description (Union[Unset, str]):
        path (Union[Unset, str]):
        source_path (Union[Unset, str]):
    """

    app: "PublishAppBodyApp"
    apps: List[str]
    summary: str
    project_slug: str
    description: Union[Unset, str] = UNSET
    path: Union[Unset, str] = UNSET
    source_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        app = self.app.to_dict()

        apps = self.apps

        summary = self.summary
        project_slug = self.project_slug
        description = self.description
        path = self.path
        source_path = self.source_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "app": app,
                "apps": apps,
                "summary": summary,
                "project_slug": project_slug,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if path is not UNSET:
            field_dict["path"] = path
        if source_path is not UNSET:
            field_dict["source_path"] = source_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.publish_app_body_app import PublishAppBodyApp

        d = src_dict.copy()
        app = PublishAppBodyApp.from_dict(d.pop("app"))

        apps = cast(List[str], d.pop("apps"))

        summary = d.pop("summary")

        project_slug = d.pop("project_slug")

        description = d.pop("description", UNSET)

        path = d.pop("path", UNSET)

        source_path = d.pop("source_path", UNSET)

        publish_app_body = cls(
            app=app,
            apps=apps,
            summary=summary,
            project_slug=project_slug,
            description=description,
            path=path,
            source_path=source_path,
        )

        publish_app_body.additional_properties = d
        return publish_app_body

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
