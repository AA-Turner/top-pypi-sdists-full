from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.hpc_job import HpcJob
    from ..models.hpc_job_stream import HpcJobStream


T = TypeVar("T", bound="HpcJobOutput")


@_attrs_define
class HpcJobOutput:
    """
    Attributes:
        job (HpcJob):
        script (Union[None, str]):
        standard_output (HpcJobStream):
        standard_error (HpcJobStream):
    """

    job: "HpcJob"
    script: Union[None, str]
    standard_output: "HpcJobStream"
    standard_error: "HpcJobStream"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        job = self.job.to_dict()

        script: Union[None, str]
        script = self.script

        standard_output = self.standard_output.to_dict()

        standard_error = self.standard_error.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job": job,
                "script": script,
                "standard_output": standard_output,
                "standard_error": standard_error,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.hpc_job import HpcJob
        from ..models.hpc_job_stream import HpcJobStream

        d = dict(src_dict)
        job = HpcJob.from_dict(d.pop("job"))

        def _parse_script(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        script = _parse_script(d.pop("script"))

        standard_output = HpcJobStream.from_dict(d.pop("standard_output"))

        standard_error = HpcJobStream.from_dict(d.pop("standard_error"))

        hpc_job_output = cls(
            job=job,
            script=script,
            standard_output=standard_output,
            standard_error=standard_error,
        )

        hpc_job_output.additional_properties = d
        return hpc_job_output

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
