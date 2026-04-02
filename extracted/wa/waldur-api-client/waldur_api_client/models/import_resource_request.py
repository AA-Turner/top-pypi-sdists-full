from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ImportResourceRequest")


@_attrs_define
class ImportResourceRequest:
    """
    Attributes:
        backend_id (str): Backend identifier of the resource
        project (UUID): Target project for the resource
        plan (Union[Unset, UUID]):
        additional_details (Union[Unset, Any]):  Default: {}.
    """

    backend_id: str
    project: UUID
    plan: Union[Unset, UUID] = UNSET
    additional_details: Union[Unset, Any] = {}
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        backend_id = self.backend_id

        project = str(self.project)

        plan: Union[Unset, str] = UNSET
        if not isinstance(self.plan, Unset):
            plan = str(self.plan)

        additional_details = self.additional_details

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "backend_id": backend_id,
                "project": project,
            }
        )
        if plan is not UNSET:
            field_dict["plan"] = plan
        if additional_details is not UNSET:
            field_dict["additional_details"] = additional_details

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        backend_id = d.pop("backend_id")

        project = UUID(d.pop("project"))

        _plan = d.pop("plan", UNSET)
        plan: Union[Unset, UUID]
        if isinstance(_plan, Unset):
            plan = UNSET
        else:
            plan = UUID(_plan)

        additional_details = d.pop("additional_details", UNSET)

        import_resource_request = cls(
            backend_id=backend_id,
            project=project,
            plan=plan,
            additional_details=additional_details,
        )

        import_resource_request.additional_properties = d
        return import_resource_request

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
