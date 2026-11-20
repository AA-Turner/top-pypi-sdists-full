from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.queued_job_flow_status_test_subflows_additional_property import (
        QueuedJobFlowStatusTestSubflowsAdditionalProperty,
    )


T = TypeVar("T", bound="QueuedJobFlowStatusTestSubflows")


@_attrs_define
class QueuedJobFlowStatusTestSubflows:
    """In a flow test run, deployed subflow path -> the flow value with the test's step overrides applied, run in place of
    the deployed subflow.

    """

    additional_properties: Dict[str, "QueuedJobFlowStatusTestSubflowsAdditionalProperty"] = _attrs_field(
        init=False, factory=dict
    )

    def to_dict(self) -> Dict[str, Any]:
        pass

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        field_dict.update({})

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.queued_job_flow_status_test_subflows_additional_property import (
            QueuedJobFlowStatusTestSubflowsAdditionalProperty,
        )

        d = src_dict.copy()
        queued_job_flow_status_test_subflows = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = QueuedJobFlowStatusTestSubflowsAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        queued_job_flow_status_test_subflows.additional_properties = additional_properties
        return queued_job_flow_status_test_subflows

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> "QueuedJobFlowStatusTestSubflowsAdditionalProperty":
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: "QueuedJobFlowStatusTestSubflowsAdditionalProperty") -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
