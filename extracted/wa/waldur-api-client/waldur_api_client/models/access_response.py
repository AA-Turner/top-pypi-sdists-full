from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.access_response_projects import AccessResponseProjects


T = TypeVar("T", bound="AccessResponse")


@_attrs_define
class AccessResponse:
    """
    Attributes:
        email (str):
        status (str):
        short_name (str):
        projects (AccessResponseProjects):
        invited_by (str):
        reason (str):
    """

    email: str
    status: str
    short_name: str
    projects: "AccessResponseProjects"
    invited_by: str
    reason: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        status = self.status

        short_name = self.short_name

        projects = self.projects.to_dict()

        invited_by = self.invited_by

        reason = self.reason

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "email": email,
                "status": status,
                "short_name": short_name,
                "projects": projects,
                "invited_by": invited_by,
                "reason": reason,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.access_response_projects import AccessResponseProjects

        d = dict(src_dict)
        email = d.pop("email")

        status = d.pop("status")

        short_name = d.pop("short_name")

        projects = AccessResponseProjects.from_dict(d.pop("projects"))

        invited_by = d.pop("invited_by")

        reason = d.pop("reason")

        access_response = cls(
            email=email,
            status=status,
            short_name=short_name,
            projects=projects,
            invited_by=invited_by,
            reason=reason,
        )

        access_response.additional_properties = d
        return access_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
