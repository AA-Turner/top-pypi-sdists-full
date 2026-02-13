import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.detailed_health_response_status import DetailedHealthResponseStatus

if TYPE_CHECKING:
    from ..models.detailed_health_response_checks import DetailedHealthResponseChecks


T = TypeVar("T", bound="DetailedHealthResponse")


@_attrs_define
class DetailedHealthResponse:
    """Detailed health status response (always fresh, no caching)

    Attributes:
        status (DetailedHealthResponseStatus): Overall health status
        checked_at (datetime.datetime): Timestamp when the health check was performed
        version (str): Server version (e.g., "EE 1.615.3")
        checks (DetailedHealthResponseChecks): Detailed health checks
    """

    status: DetailedHealthResponseStatus
    checked_at: datetime.datetime
    version: str
    checks: "DetailedHealthResponseChecks"
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
        from ..models.detailed_health_response_checks import DetailedHealthResponseChecks

        d = src_dict.copy()
        status = DetailedHealthResponseStatus(d.pop("status"))

        checked_at = isoparse(d.pop("checked_at"))

        version = d.pop("version")

        checks = DetailedHealthResponseChecks.from_dict(d.pop("checks"))

        detailed_health_response = cls(
            status=status,
            checked_at=checked_at,
            version=version,
            checks=checks,
        )

        detailed_health_response.additional_properties = d
        return detailed_health_response

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
