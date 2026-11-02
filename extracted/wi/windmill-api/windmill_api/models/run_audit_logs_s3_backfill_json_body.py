import datetime
from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

T = TypeVar("T", bound="RunAuditLogsS3BackfillJsonBody")


@_attrs_define
class RunAuditLogsS3BackfillJsonBody:
    """
    Attributes:
        from_ (datetime.datetime): inclusive lower bound of the window to export
        to (datetime.datetime): exclusive upper bound of the window to export
    """

    from_: datetime.datetime
    to: datetime.datetime
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from_ = self.from_.isoformat()

        to = self.to.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "from": from_,
                "to": to,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        from_ = isoparse(d.pop("from"))

        to = isoparse(d.pop("to"))

        run_audit_logs_s3_backfill_json_body = cls(
            from_=from_,
            to=to,
        )

        run_audit_logs_s3_backfill_json_body.additional_properties = d
        return run_audit_logs_s3_backfill_json_body

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
