import datetime
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    Any,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.workspace_response_predefined_profiles import (
        WorkspaceResponsePredefinedProfiles,
    )


T = TypeVar("T", bound="WorkspaceResponse")


@_attrs_define
class WorkspaceResponse:
    """The most recently accessed workspace

    Attributes:
        date_added (datetime.datetime): datetime with the constraint that the value must have timezone info
        date_updated (datetime.datetime): datetime with the constraint that the value must have timezone info
        id (UUID): The unique ID of the entity
        name (str): The name of the workspace
        description (Union[None, Unset, str]): The description of the workspace
        predefined_profiles (Union[Unset, WorkspaceResponsePredefinedProfiles]): Predefined profile names keyed by
            access level name, e.g. {'DATA_WRITE': 'prod', 'DATA_READ': 'access'}
    """

    date_added: datetime.datetime
    date_updated: datetime.datetime
    id: UUID
    name: str
    description: Union[None, Unset, str] = UNSET
    predefined_profiles: Union[Unset, "WorkspaceResponsePredefinedProfiles"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date_added = self.date_added.isoformat()

        date_updated = self.date_updated.isoformat()

        id = str(self.id)

        name = self.name

        description: Union[None, Unset, str]
        if isinstance(self.description, Unset):
            description = UNSET
        else:
            description = self.description

        predefined_profiles: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.predefined_profiles, Unset):
            predefined_profiles = self.predefined_profiles.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "date_added": date_added,
                "date_updated": date_updated,
                "id": id,
                "name": name,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if predefined_profiles is not UNSET:
            field_dict["predefined_profiles"] = predefined_profiles

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.workspace_response_predefined_profiles import (
            WorkspaceResponsePredefinedProfiles,
        )

        d = dict(src_dict)
        date_added = isoparse(d.pop("date_added"))

        date_updated = isoparse(d.pop("date_updated"))

        id = UUID(d.pop("id"))

        name = d.pop("name")

        def _parse_description(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        description = _parse_description(d.pop("description", UNSET))

        _predefined_profiles = d.pop("predefined_profiles", UNSET)
        predefined_profiles: Union[Unset, WorkspaceResponsePredefinedProfiles]
        if isinstance(_predefined_profiles, Unset):
            predefined_profiles = UNSET
        else:
            predefined_profiles = WorkspaceResponsePredefinedProfiles.from_dict(
                _predefined_profiles
            )

        workspace_response = cls(
            date_added=date_added,
            date_updated=date_updated,
            id=id,
            name=name,
            description=description,
            predefined_profiles=predefined_profiles,
        )

        workspace_response.additional_properties = d
        return workspace_response

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
