import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="GetAuditLogsS3StatusResponse200")


@_attrs_define
class GetAuditLogsS3StatusResponse200:
    """
    Attributes:
        last_xmin (int):
        bootstrapping (bool):
        last_run_exported (int):
        updated_at (datetime.datetime):
        last_ts (Union[Unset, None, datetime.datetime]):
        last_exported_audit_ts (Union[Unset, None, datetime.datetime]):
        last_run_at (Union[Unset, None, datetime.datetime]):
        owner (Union[Unset, None, str]):
    """

    last_xmin: int
    bootstrapping: bool
    last_run_exported: int
    updated_at: datetime.datetime
    last_ts: Union[Unset, None, datetime.datetime] = UNSET
    last_exported_audit_ts: Union[Unset, None, datetime.datetime] = UNSET
    last_run_at: Union[Unset, None, datetime.datetime] = UNSET
    owner: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        last_xmin = self.last_xmin
        bootstrapping = self.bootstrapping
        last_run_exported = self.last_run_exported
        updated_at = self.updated_at.isoformat()

        last_ts: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_ts, Unset):
            last_ts = self.last_ts.isoformat() if self.last_ts else None

        last_exported_audit_ts: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_exported_audit_ts, Unset):
            last_exported_audit_ts = self.last_exported_audit_ts.isoformat() if self.last_exported_audit_ts else None

        last_run_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_run_at, Unset):
            last_run_at = self.last_run_at.isoformat() if self.last_run_at else None

        owner = self.owner

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "last_xmin": last_xmin,
                "bootstrapping": bootstrapping,
                "last_run_exported": last_run_exported,
                "updated_at": updated_at,
            }
        )
        if last_ts is not UNSET:
            field_dict["last_ts"] = last_ts
        if last_exported_audit_ts is not UNSET:
            field_dict["last_exported_audit_ts"] = last_exported_audit_ts
        if last_run_at is not UNSET:
            field_dict["last_run_at"] = last_run_at
        if owner is not UNSET:
            field_dict["owner"] = owner

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        last_xmin = d.pop("last_xmin")

        bootstrapping = d.pop("bootstrapping")

        last_run_exported = d.pop("last_run_exported")

        updated_at = isoparse(d.pop("updated_at"))

        _last_ts = d.pop("last_ts", UNSET)
        last_ts: Union[Unset, None, datetime.datetime]
        if _last_ts is None:
            last_ts = None
        elif isinstance(_last_ts, Unset):
            last_ts = UNSET
        else:
            last_ts = isoparse(_last_ts)

        _last_exported_audit_ts = d.pop("last_exported_audit_ts", UNSET)
        last_exported_audit_ts: Union[Unset, None, datetime.datetime]
        if _last_exported_audit_ts is None:
            last_exported_audit_ts = None
        elif isinstance(_last_exported_audit_ts, Unset):
            last_exported_audit_ts = UNSET
        else:
            last_exported_audit_ts = isoparse(_last_exported_audit_ts)

        _last_run_at = d.pop("last_run_at", UNSET)
        last_run_at: Union[Unset, None, datetime.datetime]
        if _last_run_at is None:
            last_run_at = None
        elif isinstance(_last_run_at, Unset):
            last_run_at = UNSET
        else:
            last_run_at = isoparse(_last_run_at)

        owner = d.pop("owner", UNSET)

        get_audit_logs_s3_status_response_200 = cls(
            last_xmin=last_xmin,
            bootstrapping=bootstrapping,
            last_run_exported=last_run_exported,
            updated_at=updated_at,
            last_ts=last_ts,
            last_exported_audit_ts=last_exported_audit_ts,
            last_run_at=last_run_at,
            owner=owner,
        )

        get_audit_logs_s3_status_response_200.additional_properties = d
        return get_audit_logs_s3_status_response_200

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
