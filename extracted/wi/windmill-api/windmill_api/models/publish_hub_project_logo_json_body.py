from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.publish_hub_project_logo_json_body_logo import PublishHubProjectLogoJsonBodyLogo


T = TypeVar("T", bound="PublishHubProjectLogoJsonBody")


@_attrs_define
class PublishHubProjectLogoJsonBody:
    """
    Attributes:
        logo (Optional[PublishHubProjectLogoJsonBodyLogo]): the logo to set, or null to clear the project's current logo
    """

    logo: Optional["PublishHubProjectLogoJsonBodyLogo"]
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
        from ..models.publish_hub_project_logo_json_body_logo import PublishHubProjectLogoJsonBodyLogo

        d = src_dict.copy()
        _logo = d.pop("logo")
        logo: Optional[PublishHubProjectLogoJsonBodyLogo]
        if _logo is None:
            logo = None
        else:
            logo = PublishHubProjectLogoJsonBodyLogo.from_dict(_logo)

        publish_hub_project_logo_json_body = cls(
            logo=logo,
        )

        publish_hub_project_logo_json_body.additional_properties = d
        return publish_hub_project_logo_json_body

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
