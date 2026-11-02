from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.test_autoscaling_json_body_integration import TestAutoscalingJsonBodyIntegration


T = TypeVar("T", bound="TestAutoscalingJsonBody")


@_attrs_define
class TestAutoscalingJsonBody:
    """
    Attributes:
        desired_workers (int):
        integration (TestAutoscalingJsonBodyIntegration): The integration to run, as in the worker group's autoscaling
            config
    """

    desired_workers: int
    integration: "TestAutoscalingJsonBodyIntegration"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        desired_workers = self.desired_workers
        integration = self.integration.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "desired_workers": desired_workers,
                "integration": integration,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.test_autoscaling_json_body_integration import TestAutoscalingJsonBodyIntegration

        d = src_dict.copy()
        desired_workers = d.pop("desired_workers")

        integration = TestAutoscalingJsonBodyIntegration.from_dict(d.pop("integration"))

        test_autoscaling_json_body = cls(
            desired_workers=desired_workers,
            integration=integration,
        )

        test_autoscaling_json_body.additional_properties = d
        return test_autoscaling_json_body

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
