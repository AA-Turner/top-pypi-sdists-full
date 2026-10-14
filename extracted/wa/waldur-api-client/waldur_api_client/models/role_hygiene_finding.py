from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.role_hygiene_finding_severity_enum import RoleHygieneFindingSeverityEnum
from ..models.role_type import RoleType

if TYPE_CHECKING:
    from ..models.role_hygiene_finding_details import RoleHygieneFindingDetails


T = TypeVar("T", bound="RoleHygieneFinding")


@_attrs_define
class RoleHygieneFinding:
    """
    Attributes:
        check (str):
        severity (RoleHygieneFindingSeverityEnum):
        role_uuid (str):
        role_name (str):
        role_description (str):
        scope_type (Union[None, RoleType]):
        is_system_role (bool):
        message (str):
        details (RoleHygieneFindingDetails):
    """

    check: str
    severity: RoleHygieneFindingSeverityEnum
    role_uuid: str
    role_name: str
    role_description: str
    scope_type: Union[None, RoleType]
    is_system_role: bool
    message: str
    details: "RoleHygieneFindingDetails"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        check = self.check

        severity = self.severity.value

        role_uuid = self.role_uuid

        role_name = self.role_name

        role_description = self.role_description

        scope_type: Union[None, str]
        if isinstance(self.scope_type, RoleType):
            scope_type = self.scope_type.value
        else:
            scope_type = self.scope_type

        is_system_role = self.is_system_role

        message = self.message

        details = self.details.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "check": check,
                "severity": severity,
                "role_uuid": role_uuid,
                "role_name": role_name,
                "role_description": role_description,
                "scope_type": scope_type,
                "is_system_role": is_system_role,
                "message": message,
                "details": details,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.role_hygiene_finding_details import RoleHygieneFindingDetails

        d = dict(src_dict)
        check = d.pop("check")

        severity = RoleHygieneFindingSeverityEnum(d.pop("severity"))

        role_uuid = d.pop("role_uuid")

        role_name = d.pop("role_name")

        role_description = d.pop("role_description")

        def _parse_scope_type(data: object) -> Union[None, RoleType]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                scope_type_type_0 = RoleType(data)

                return scope_type_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, RoleType], data)

        scope_type = _parse_scope_type(d.pop("scope_type"))

        is_system_role = d.pop("is_system_role")

        message = d.pop("message")

        details = RoleHygieneFindingDetails.from_dict(d.pop("details"))

        role_hygiene_finding = cls(
            check=check,
            severity=severity,
            role_uuid=role_uuid,
            role_name=role_name,
            role_description=role_description,
            scope_type=scope_type,
            is_system_role=is_system_role,
            message=message,
            details=details,
        )

        role_hygiene_finding.additional_properties = d
        return role_hygiene_finding

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
