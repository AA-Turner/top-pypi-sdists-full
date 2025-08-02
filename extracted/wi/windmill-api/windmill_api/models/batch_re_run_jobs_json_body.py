from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.batch_re_run_jobs_json_body_flow_options_by_path import BatchReRunJobsJsonBodyFlowOptionsByPath
    from ..models.batch_re_run_jobs_json_body_script_options_by_path import BatchReRunJobsJsonBodyScriptOptionsByPath


T = TypeVar("T", bound="BatchReRunJobsJsonBody")


@_attrs_define
class BatchReRunJobsJsonBody:
    """
    Attributes:
        job_ids (List[str]):
        script_options_by_path (BatchReRunJobsJsonBodyScriptOptionsByPath):
        flow_options_by_path (BatchReRunJobsJsonBodyFlowOptionsByPath):
    """

    job_ids: List[str]
    script_options_by_path: "BatchReRunJobsJsonBodyScriptOptionsByPath"
    flow_options_by_path: "BatchReRunJobsJsonBodyFlowOptionsByPath"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        job_ids = self.job_ids

        script_options_by_path = self.script_options_by_path.to_dict()

        flow_options_by_path = self.flow_options_by_path.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job_ids": job_ids,
                "script_options_by_path": script_options_by_path,
                "flow_options_by_path": flow_options_by_path,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.batch_re_run_jobs_json_body_flow_options_by_path import BatchReRunJobsJsonBodyFlowOptionsByPath
        from ..models.batch_re_run_jobs_json_body_script_options_by_path import (
            BatchReRunJobsJsonBodyScriptOptionsByPath,
        )

        d = src_dict.copy()
        job_ids = cast(List[str], d.pop("job_ids"))

        script_options_by_path = BatchReRunJobsJsonBodyScriptOptionsByPath.from_dict(d.pop("script_options_by_path"))

        flow_options_by_path = BatchReRunJobsJsonBodyFlowOptionsByPath.from_dict(d.pop("flow_options_by_path"))

        batch_re_run_jobs_json_body = cls(
            job_ids=job_ids,
            script_options_by_path=script_options_by_path,
            flow_options_by_path=flow_options_by_path,
        )

        batch_re_run_jobs_json_body.additional_properties = d
        return batch_re_run_jobs_json_body

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
