import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="CiTestResult")


@_attrs_define
class CiTestResult:
    """
    Attributes:
        test_script_path (str):
        job_id (Union[Unset, None, str]):
        status (Union[Unset, None, str]):
        started_at (Union[Unset, None, datetime.datetime]):
    """

    test_script_path: str
    job_id: Union[Unset, None, str] = UNSET
    status: Union[Unset, None, str] = UNSET
    started_at: Union[Unset, None, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        test_script_path = self.test_script_path
        job_id = self.job_id
        status = self.status
        started_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.started_at, Unset):
            started_at = self.started_at.isoformat() if self.started_at else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "test_script_path": test_script_path,
            }
        )
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if status is not UNSET:
            field_dict["status"] = status
        if started_at is not UNSET:
            field_dict["started_at"] = started_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        test_script_path = d.pop("test_script_path")

        job_id = d.pop("job_id", UNSET)

        status = d.pop("status", UNSET)

        _started_at = d.pop("started_at", UNSET)
        started_at: Union[Unset, None, datetime.datetime]
        if _started_at is None:
            started_at = None
        elif isinstance(_started_at, Unset):
            started_at = UNSET
        else:
            started_at = isoparse(_started_at)

        ci_test_result = cls(
            test_script_path=test_script_path,
            job_id=job_id,
            status=status,
            started_at=started_at,
        )

        ci_test_result.additional_properties = d
        return ci_test_result

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
