from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.project_logo_body_logo_mime import ProjectLogoBodyLogoMime

T = TypeVar("T", bound="ProjectLogoBodyLogo")


@_attrs_define
class ProjectLogoBodyLogo:
    """the logo to set, or null to clear the project's current logo

    Attributes:
        b64 (str): base64-encoded image bytes (decoded size max 512KB)
        mime (ProjectLogoBodyLogoMime):
    """

    b64: str
    mime: ProjectLogoBodyLogoMime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        b64 = self.b64
        mime = self.mime.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "b64": b64,
                "mime": mime,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        b64 = d.pop("b64")

        mime = ProjectLogoBodyLogoMime(d.pop("mime"))

        project_logo_body_logo = cls(
            b64=b64,
            mime=mime,
        )

        project_logo_body_logo.additional_properties = d
        return project_logo_body_logo

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
