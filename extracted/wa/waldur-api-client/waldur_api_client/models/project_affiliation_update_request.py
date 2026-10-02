from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectAffiliationUpdateRequest")


@_attrs_define
class ProjectAffiliationUpdateRequest:
    """
    Attributes:
        affiliation (Union[None, UUID, Unset]):
    """

    affiliation: Union[None, UUID, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        affiliation: Union[None, Unset, str]
        if isinstance(self.affiliation, Unset):
            affiliation = UNSET
        elif isinstance(self.affiliation, UUID):
            affiliation = str(self.affiliation)
        else:
            affiliation = self.affiliation

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if affiliation is not UNSET:
            field_dict["affiliation"] = affiliation

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)

        def _parse_affiliation(data: object) -> Union[None, UUID, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                affiliation_type_0 = UUID(data)

                return affiliation_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID, Unset], data)

        affiliation = _parse_affiliation(d.pop("affiliation", UNSET))

        project_affiliation_update_request = cls(
            affiliation=affiliation,
        )

        project_affiliation_update_request.additional_properties = d
        return project_affiliation_update_request

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
