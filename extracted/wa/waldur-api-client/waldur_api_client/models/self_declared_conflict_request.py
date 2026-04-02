from collections.abc import Mapping
from typing import Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.coi_severity_level import COISeverityLevel
from ..models.coi_type_enum import CoiTypeEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="SelfDeclaredConflictRequest")


@_attrs_define
class SelfDeclaredConflictRequest:
    """
    Attributes:
        proposal_uuid (UUID):
        coi_type (CoiTypeEnum):
        severity (Union[Unset, COISeverityLevel]):  Default: COISeverityLevel.APPARENT.
        description (Union[Unset, str]):  Default: ''.
    """

    proposal_uuid: UUID
    coi_type: CoiTypeEnum
    severity: Union[Unset, COISeverityLevel] = COISeverityLevel.APPARENT
    description: Union[Unset, str] = ""
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        proposal_uuid = str(self.proposal_uuid)

        coi_type = self.coi_type.value

        severity: Union[Unset, str] = UNSET
        if not isinstance(self.severity, Unset):
            severity = self.severity.value

        description = self.description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "proposal_uuid": proposal_uuid,
                "coi_type": coi_type,
            }
        )
        if severity is not UNSET:
            field_dict["severity"] = severity
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        proposal_uuid = UUID(d.pop("proposal_uuid"))

        coi_type = CoiTypeEnum(d.pop("coi_type"))

        _severity = d.pop("severity", UNSET)
        severity: Union[Unset, COISeverityLevel]
        if isinstance(_severity, Unset):
            severity = UNSET
        else:
            severity = COISeverityLevel(_severity)

        description = d.pop("description", UNSET)

        self_declared_conflict_request = cls(
            proposal_uuid=proposal_uuid,
            coi_type=coi_type,
            severity=severity,
            description=description,
        )

        self_declared_conflict_request.additional_properties = d
        return self_declared_conflict_request

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
