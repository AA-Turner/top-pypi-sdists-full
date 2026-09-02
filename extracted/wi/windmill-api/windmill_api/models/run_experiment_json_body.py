from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.run_experiment_json_body_subject import RunExperimentJsonBodySubject


T = TypeVar("T", bound="RunExperimentJsonBody")


@_attrs_define
class RunExperimentJsonBody:
    """
    Attributes:
        dataset (str):
        subject (RunExperimentJsonBodySubject): What an eval run is executed against.
    """

    dataset: str
    subject: "RunExperimentJsonBodySubject"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        dataset = self.dataset
        subject = self.subject.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "dataset": dataset,
                "subject": subject,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.run_experiment_json_body_subject import RunExperimentJsonBodySubject

        d = src_dict.copy()
        dataset = d.pop("dataset")

        subject = RunExperimentJsonBodySubject.from_dict(d.pop("subject"))

        run_experiment_json_body = cls(
            dataset=dataset,
            subject=subject,
        )

        run_experiment_json_body.additional_properties = d
        return run_experiment_json_body

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
