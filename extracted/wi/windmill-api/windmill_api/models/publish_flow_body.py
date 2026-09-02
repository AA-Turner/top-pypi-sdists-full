from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.publish_flow_body_flow import PublishFlowBodyFlow


T = TypeVar("T", bound="PublishFlowBody")


@_attrs_define
class PublishFlowBody:
    """
    Attributes:
        flow (PublishFlowBodyFlow):
        apps (List[str]):
        project_slug (str): hub project slug (3-50 chars, lowercase alphanumeric and hyphens, no leading/trailing
            hyphen)
        path (Union[Unset, str]):
        source_path (Union[Unset, str]):
    """

    flow: "PublishFlowBodyFlow"
    apps: List[str]
    project_slug: str
    path: Union[Unset, str] = UNSET
    source_path: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        flow = self.flow.to_dict()

        apps = self.apps

        project_slug = self.project_slug
        path = self.path
        source_path = self.source_path

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "flow": flow,
                "apps": apps,
                "project_slug": project_slug,
            }
        )
        if path is not UNSET:
            field_dict["path"] = path
        if source_path is not UNSET:
            field_dict["source_path"] = source_path

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.publish_flow_body_flow import PublishFlowBodyFlow

        d = src_dict.copy()
        flow = PublishFlowBodyFlow.from_dict(d.pop("flow"))

        apps = cast(List[str], d.pop("apps"))

        project_slug = d.pop("project_slug")

        path = d.pop("path", UNSET)

        source_path = d.pop("source_path", UNSET)

        publish_flow_body = cls(
            flow=flow,
            apps=apps,
            project_slug=project_slug,
            path=path,
            source_path=source_path,
        )

        publish_flow_body.additional_properties = d
        return publish_flow_body

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
