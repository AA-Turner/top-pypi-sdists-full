from typing import Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ResolveCompletedJobsJsonBody")


@_attrs_define
class ResolveCompletedJobsJsonBody:
    """
    Attributes:
        job_ids (List[str]):
        note (Union[Unset, str]): a person's explanation of why the failure is considered handled. Enterprise-only:
            ignored outside enterprise
        superseded_by (Union[Unset, str]): id of a later successful run of the same runnable that supersedes the
            failure. Verified server-side, and the resulting note is the server's own wording, so it is recorded regardless
            of licence. A claim that cannot be verified resolves nothing
    """

    job_ids: List[str]
    note: Union[Unset, str] = UNSET
    superseded_by: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_ids = self.job_ids

        note = self.note
        superseded_by = self.superseded_by

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_ids": job_ids,
            }
        )
        if note is not UNSET:
            field_dict["note"] = note
        if superseded_by is not UNSET:
            field_dict["superseded_by"] = superseded_by

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        job_ids = cast(List[str], d.pop("job_ids"))

        note = d.pop("note", UNSET)

        superseded_by = d.pop("superseded_by", UNSET)

        resolve_completed_jobs_json_body = cls(
            job_ids=job_ids,
            note=note,
            superseded_by=superseded_by,
        )

        resolve_completed_jobs_json_body.additional_properties = d
        return resolve_completed_jobs_json_body

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
