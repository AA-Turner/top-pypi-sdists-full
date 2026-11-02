import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.get_health_detailed_response_503_status import GetHealthDetailedResponse503Status

if TYPE_CHECKING:
    from ..models.get_health_detailed_response_503_checks import GetHealthDetailedResponse503Checks


T = TypeVar("T", bound="GetHealthDetailedResponse503")


@_attrs_define
class GetHealthDetailedResponse503:
    """Detailed health status response (always fresh, no caching)

    Attributes:
        status (GetHealthDetailedResponse503Status): Overall health status
        checked_at (datetime.datetime): Timestamp when the health check was performed
        version (str): Server version (e.g., "EE 1.615.3")
        checks (GetHealthDetailedResponse503Checks): Detailed health checks
    """

    status: GetHealthDetailedResponse503Status
    checked_at: datetime.datetime
    version: str
    checks: "GetHealthDetailedResponse503Checks"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        status = self.status.value

        checked_at = self.checked_at.isoformat()

        version = self.version
        checks = self.checks.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "status": status,
                "checked_at": checked_at,
                "version": version,
                "checks": checks,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_health_detailed_response_503_checks import GetHealthDetailedResponse503Checks

        d = src_dict.copy()
        status = GetHealthDetailedResponse503Status(d.pop("status"))

        checked_at = isoparse(d.pop("checked_at"))

        version = d.pop("version")

        checks = GetHealthDetailedResponse503Checks.from_dict(d.pop("checks"))

        get_health_detailed_response_503 = cls(
            status=status,
            checked_at=checked_at,
            version=version,
            checks=checks,
        )

        get_health_detailed_response_503.additional_properties = d
        return get_health_detailed_response_503

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
