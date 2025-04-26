from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.get_suspended_job_flow_response_200_approvers_item import GetSuspendedJobFlowResponse200ApproversItem
    from ..models.get_suspended_job_flow_response_200_job_type_0 import GetSuspendedJobFlowResponse200JobType0
    from ..models.get_suspended_job_flow_response_200_job_type_1 import GetSuspendedJobFlowResponse200JobType1


T = TypeVar("T", bound="GetSuspendedJobFlowResponse200")


@_attrs_define
class GetSuspendedJobFlowResponse200:
    """
    Attributes:
        job (Union['GetSuspendedJobFlowResponse200JobType0', 'GetSuspendedJobFlowResponse200JobType1']):
        approvers (List['GetSuspendedJobFlowResponse200ApproversItem']):
    """

    job: Union["GetSuspendedJobFlowResponse200JobType0", "GetSuspendedJobFlowResponse200JobType1"]
    approvers: List["GetSuspendedJobFlowResponse200ApproversItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.get_suspended_job_flow_response_200_job_type_0 import GetSuspendedJobFlowResponse200JobType0

        job: Dict[str, Any]

        if isinstance(self.job, GetSuspendedJobFlowResponse200JobType0):
            job = self.job.to_dict()

        else:
            job = self.job.to_dict()

        approvers = []
        for approvers_item_data in self.approvers:
            approvers_item = approvers_item_data.to_dict()

            approvers.append(approvers_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "job": job,
                "approvers": approvers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_suspended_job_flow_response_200_approvers_item import (
            GetSuspendedJobFlowResponse200ApproversItem,
        )
        from ..models.get_suspended_job_flow_response_200_job_type_0 import GetSuspendedJobFlowResponse200JobType0
        from ..models.get_suspended_job_flow_response_200_job_type_1 import GetSuspendedJobFlowResponse200JobType1

        d = src_dict.copy()

        def _parse_job(
            data: object,
        ) -> Union["GetSuspendedJobFlowResponse200JobType0", "GetSuspendedJobFlowResponse200JobType1"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                job_type_0 = GetSuspendedJobFlowResponse200JobType0.from_dict(data)

                return job_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            job_type_1 = GetSuspendedJobFlowResponse200JobType1.from_dict(data)

            return job_type_1

        job = _parse_job(d.pop("job"))

        approvers = []
        _approvers = d.pop("approvers")
        for approvers_item_data in _approvers:
            approvers_item = GetSuspendedJobFlowResponse200ApproversItem.from_dict(approvers_item_data)

            approvers.append(approvers_item)

        get_suspended_job_flow_response_200 = cls(
            job=job,
            approvers=approvers,
        )

        get_suspended_job_flow_response_200.additional_properties = d
        return get_suspended_job_flow_response_200

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
