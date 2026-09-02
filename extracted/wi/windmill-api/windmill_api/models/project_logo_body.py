from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.project_logo_body_logo import ProjectLogoBodyLogo


T = TypeVar("T", bound="ProjectLogoBody")


@_attrs_define
class ProjectLogoBody:
    """
    Attributes:
        logo (Optional[ProjectLogoBodyLogo]): the logo to set, or null to clear the project's current logo
    """

    logo: Optional["ProjectLogoBodyLogo"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        logo = self.logo.to_dict() if self.logo else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "logo": logo,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.project_logo_body_logo import ProjectLogoBodyLogo

        d = src_dict.copy()
        _logo = d.pop("logo")
        logo: Optional[ProjectLogoBodyLogo]
        if _logo is None:
            logo = None
        else:
            logo = ProjectLogoBodyLogo.from_dict(_logo)

        project_logo_body = cls(
            logo=logo,
        )

        project_logo_body.additional_properties = d
        return project_logo_body

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
