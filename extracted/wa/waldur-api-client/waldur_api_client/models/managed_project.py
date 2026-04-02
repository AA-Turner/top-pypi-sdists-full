import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.project import Project
    from ..models.project_template import ProjectTemplate


T = TypeVar("T", bound="ManagedProject")


@_attrs_define
class ManagedProject:
    """
    Attributes:
        state (str):
        created (datetime.datetime):
        reviewed_at (Union[None, datetime.datetime]): Timestamp when the review was completed
        reviewed_by_full_name (str):
        reviewed_by_uuid (UUID):
        identifier (str):
        destination (str): The destination used to send instructions from the remote portal.
        details (Any): Details of the project as provided by the remote OpenPortal.
        project (str):
        project_data (Project):
        project_template (str):
        project_template_data (ProjectTemplate):
        review_comment (Union[None, Unset, str]): Optional comment provided during review
        local_identifier (Union[None, Unset, str]): The local project identifier in this portal.
    """

    state: str
    created: datetime.datetime
    reviewed_at: Union[None, datetime.datetime]
    reviewed_by_full_name: str
    reviewed_by_uuid: UUID
    identifier: str
    destination: str
    details: Any
    project: str
    project_data: "Project"
    project_template: str
    project_template_data: "ProjectTemplate"
    review_comment: Union[None, Unset, str] = UNSET
    local_identifier: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        state = self.state

        created = self.created.isoformat()

        reviewed_at: Union[None, str]
        if isinstance(self.reviewed_at, datetime.datetime):
            reviewed_at = self.reviewed_at.isoformat()
        else:
            reviewed_at = self.reviewed_at

        reviewed_by_full_name = self.reviewed_by_full_name

        reviewed_by_uuid = str(self.reviewed_by_uuid)

        identifier = self.identifier

        destination = self.destination

        details = self.details

        project = self.project

        project_data = self.project_data.to_dict()

        project_template = self.project_template

        project_template_data = self.project_template_data.to_dict()

        review_comment: Union[None, Unset, str]
        if isinstance(self.review_comment, Unset):
            review_comment = UNSET
        else:
            review_comment = self.review_comment

        local_identifier: Union[None, Unset, str]
        if isinstance(self.local_identifier, Unset):
            local_identifier = UNSET
        else:
            local_identifier = self.local_identifier

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "state": state,
                "created": created,
                "reviewed_at": reviewed_at,
                "reviewed_by_full_name": reviewed_by_full_name,
                "reviewed_by_uuid": reviewed_by_uuid,
                "identifier": identifier,
                "destination": destination,
                "details": details,
                "project": project,
                "project_data": project_data,
                "project_template": project_template,
                "project_template_data": project_template_data,
            }
        )
        if review_comment is not UNSET:
            field_dict["review_comment"] = review_comment
        if local_identifier is not UNSET:
            field_dict["local_identifier"] = local_identifier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project import Project
        from ..models.project_template import ProjectTemplate

        d = dict(src_dict)
        state = d.pop("state")

        created = isoparse(d.pop("created"))

        def _parse_reviewed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                reviewed_at_type_0 = isoparse(data)

                return reviewed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        reviewed_at = _parse_reviewed_at(d.pop("reviewed_at"))

        reviewed_by_full_name = d.pop("reviewed_by_full_name")

        reviewed_by_uuid = UUID(d.pop("reviewed_by_uuid"))

        identifier = d.pop("identifier")

        destination = d.pop("destination")

        details = d.pop("details")

        project = d.pop("project")

        project_data = Project.from_dict(d.pop("project_data"))

        project_template = d.pop("project_template")

        project_template_data = ProjectTemplate.from_dict(d.pop("project_template_data"))

        def _parse_review_comment(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        review_comment = _parse_review_comment(d.pop("review_comment", UNSET))

        def _parse_local_identifier(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        local_identifier = _parse_local_identifier(d.pop("local_identifier", UNSET))

        managed_project = cls(
            state=state,
            created=created,
            reviewed_at=reviewed_at,
            reviewed_by_full_name=reviewed_by_full_name,
            reviewed_by_uuid=reviewed_by_uuid,
            identifier=identifier,
            destination=destination,
            details=details,
            project=project,
            project_data=project_data,
            project_template=project_template,
            project_template_data=project_template_data,
            review_comment=review_comment,
            local_identifier=local_identifier,
        )

        managed_project.additional_properties = d
        return managed_project

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
