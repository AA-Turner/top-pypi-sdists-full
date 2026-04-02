from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResourceSuggestNameRequest")


@_attrs_define
class ResourceSuggestNameRequest:
    """
    Attributes:
        project (UUID):
        offering (UUID):
        plan (Union[None, UUID, Unset]):
        attributes (Union[Unset, Any]):
    """

    project: UUID
    offering: UUID
    plan: Union[None, UUID, Unset] = UNSET
    attributes: Union[Unset, Any] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        project = str(self.project)

        offering = str(self.offering)

        plan: Union[None, Unset, str]
        if isinstance(self.plan, Unset):
            plan = UNSET
        elif isinstance(self.plan, UUID):
            plan = str(self.plan)
        else:
            plan = self.plan

        attributes = self.attributes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "project": project,
                "offering": offering,
            }
        )
        if plan is not UNSET:
            field_dict["plan"] = plan
        if attributes is not UNSET:
            field_dict["attributes"] = attributes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        project = UUID(d.pop("project"))

        offering = UUID(d.pop("offering"))

        def _parse_plan(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                plan_type_0 = UUID(data)

                return plan_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        plan = _parse_plan(d.pop("plan", UNSET))

        attributes = d.pop("attributes", UNSET)

        resource_suggest_name_request = cls(
            project=project,
            offering=offering,
            plan=plan,
            attributes=attributes,
        )

        resource_suggest_name_request.additional_properties = d
        return resource_suggest_name_request

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
