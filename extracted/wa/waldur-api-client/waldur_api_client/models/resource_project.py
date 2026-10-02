import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.resource_project_current_usages import ResourceProjectCurrentUsages
    from ..models.resource_project_limits import ResourceProjectLimits
    from ..models.resource_project_termination_metadata_type_0 import ResourceProjectTerminationMetadataType0


T = TypeVar("T", bound="ResourceProject")


@_attrs_define
class ResourceProject:
    """
    Attributes:
        uuid (UUID):
        resource (UUID):
        name (str):
        backend_id (str):
        state (str):
        error_message (str):
        current_usages (ResourceProjectCurrentUsages): Dictionary mapping component types to current usage amounts.
            Populated by backend synchronization.
        resource_uuid (UUID):
        resource_name (str):
        created (datetime.datetime):
        modified (datetime.datetime):
        is_removed (bool):
        removed_date (Union[None, datetime.datetime]):
        removed_by (Union[None, int]):
        removed_by_username (Union[None, str]):
        created_by_username (Union[None, str]):
        termination_metadata (Union['ResourceProjectTerminationMetadataType0', None]):
        description (Union[Unset, str]):
        limits (Union[Unset, ResourceProjectLimits]): Dictionary mapping component types to quota values. Same format as
            Resource.limits.
    """

    uuid: UUID
    resource: UUID
    name: str
    backend_id: str
    state: str
    error_message: str
    current_usages: "ResourceProjectCurrentUsages"
    resource_uuid: UUID
    resource_name: str
    created: datetime.datetime
    modified: datetime.datetime
    is_removed: bool
    removed_date: Union[None, datetime.datetime]
    removed_by: Union[None, int]
    removed_by_username: Union[None, str]
    created_by_username: Union[None, str]
    termination_metadata: Union["ResourceProjectTerminationMetadataType0", None]
    description: Union[Unset, str] = UNSET
    limits: Union[Unset, "ResourceProjectLimits"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.resource_project_termination_metadata_type_0 import ResourceProjectTerminationMetadataType0

        uuid = str(self.uuid)

        resource = str(self.resource)

        name = self.name

        backend_id = self.backend_id

        state = self.state

        error_message = self.error_message

        current_usages = self.current_usages.to_dict()

        resource_uuid = str(self.resource_uuid)

        resource_name = self.resource_name

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        is_removed = self.is_removed

        removed_date: Union[None, str]
        if isinstance(self.removed_date, datetime.datetime):
            removed_date = self.removed_date.isoformat()
        else:
            removed_date = self.removed_date

        removed_by: Union[None, int]
        removed_by = self.removed_by

        removed_by_username: Union[None, str]
        removed_by_username = self.removed_by_username

        created_by_username: Union[None, str]
        created_by_username = self.created_by_username

        termination_metadata: Union[None, dict[str, Any]]
        if isinstance(self.termination_metadata, ResourceProjectTerminationMetadataType0):
            termination_metadata = self.termination_metadata.to_dict()
        else:
            termination_metadata = self.termination_metadata

        description = self.description

        limits: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.limits, Unset):
            limits = self.limits.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "resource": resource,
                "name": name,
                "backend_id": backend_id,
                "state": state,
                "error_message": error_message,
                "current_usages": current_usages,
                "resource_uuid": resource_uuid,
                "resource_name": resource_name,
                "created": created,
                "modified": modified,
                "is_removed": is_removed,
                "removed_date": removed_date,
                "removed_by": removed_by,
                "removed_by_username": removed_by_username,
                "created_by_username": created_by_username,
                "termination_metadata": termination_metadata,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if limits is not UNSET:
            field_dict["limits"] = limits

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.resource_project_current_usages import ResourceProjectCurrentUsages
        from ..models.resource_project_limits import ResourceProjectLimits
        from ..models.resource_project_termination_metadata_type_0 import ResourceProjectTerminationMetadataType0

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        resource = UUID(d.pop("resource"))

        name = d.pop("name")

        backend_id = d.pop("backend_id")

        state = d.pop("state")

        error_message = d.pop("error_message")

        current_usages = ResourceProjectCurrentUsages.from_dict(d.pop("current_usages"))

        resource_uuid = UUID(d.pop("resource_uuid"))

        resource_name = d.pop("resource_name")

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        is_removed = d.pop("is_removed")

        def _parse_removed_date(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                removed_date_type_0 = isoparse(data)

                return removed_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        removed_date = _parse_removed_date(d.pop("removed_date"))

        def _parse_removed_by(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        removed_by = _parse_removed_by(d.pop("removed_by"))

        def _parse_removed_by_username(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        removed_by_username = _parse_removed_by_username(d.pop("removed_by_username"))

        def _parse_created_by_username(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        created_by_username = _parse_created_by_username(d.pop("created_by_username"))

        def _parse_termination_metadata(data: object) -> Union["ResourceProjectTerminationMetadataType0", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                termination_metadata_type_0 = ResourceProjectTerminationMetadataType0.from_dict(data)

                return termination_metadata_type_0
            except:  # noqa: E722
                pass
            return cast(Union["ResourceProjectTerminationMetadataType0", None], data)

        termination_metadata = _parse_termination_metadata(d.pop("termination_metadata"))

        description = d.pop("description", UNSET)

        _limits = d.pop("limits", UNSET)
        limits: Union[Unset, ResourceProjectLimits]
        if isinstance(_limits, Unset):
            limits = UNSET
        else:
            limits = ResourceProjectLimits.from_dict(_limits)

        resource_project = cls(
            uuid=uuid,
            resource=resource,
            name=name,
            backend_id=backend_id,
            state=state,
            error_message=error_message,
            current_usages=current_usages,
            resource_uuid=resource_uuid,
            resource_name=resource_name,
            created=created,
            modified=modified,
            is_removed=is_removed,
            removed_date=removed_date,
            removed_by=removed_by,
            removed_by_username=removed_by_username,
            created_by_username=created_by_username,
            termination_metadata=termination_metadata,
            description=description,
            limits=limits,
        )

        resource_project.additional_properties = d
        return resource_project

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
