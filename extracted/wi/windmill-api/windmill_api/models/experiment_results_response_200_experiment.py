import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.experiment_results_response_200_experiment_scores_item import (
        ExperimentResultsResponse200ExperimentScoresItem,
    )
    from ..models.experiment_results_response_200_experiment_subject import (
        ExperimentResultsResponse200ExperimentSubject,
    )


T = TypeVar("T", bound="ExperimentResultsResponse200Experiment")


@_attrs_define
class ExperimentResultsResponse200Experiment:
    """One run of a dataset: written once when the dataset is run, and only ever read afterwards. The case set it executed
    is returned by the results endpoint, not here: a listing would otherwise send the whole dataset back once per
    experiment.

        Attributes:
            id (str):
            dataset (str):
            subject (ExperimentResultsResponse200ExperimentSubject): What an eval run is executed against.
            run_number (int): This agent's nth run of this dataset, allocated once and never reused. What a run is called.
                Numbered per agent rather than per subject kind: runs of what is deployed and runs of its draft are the same
                agent's history.
            run_job_id (str): The flow executing the run: one job holding every case and its scores.
            case_count (int):
            created_at (datetime.datetime):
            created_by (str):
            scores (Union[Unset, List['ExperimentResultsResponse200ExperimentScoresItem']]): What the run scored, one entry
                per scorer that produced a number. Carried on the run itself so a list of runs can say what each one scored
                without reading every cell of every one of them. Empty on a run whose scores have not been read yet.
            running (Union[Unset, bool]): Whether the flow executing this run is still going. What makes a list of runs
                worth watching rather than worth reloading.
    """

    id: str
    dataset: str
    subject: "ExperimentResultsResponse200ExperimentSubject"
    run_number: int
    run_job_id: str
    case_count: int
    created_at: datetime.datetime
    created_by: str
    scores: Union[Unset, List["ExperimentResultsResponse200ExperimentScoresItem"]] = UNSET
    running: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        dataset = self.dataset
        subject = self.subject.to_dict()

        run_number = self.run_number
        run_job_id = self.run_job_id
        case_count = self.case_count
        created_at = self.created_at.isoformat()

        created_by = self.created_by
        scores: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.scores, Unset):
            scores = []
            for scores_item_data in self.scores:
                scores_item = scores_item_data.to_dict()

                scores.append(scores_item)

        running = self.running

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "dataset": dataset,
                "subject": subject,
                "run_number": run_number,
                "run_job_id": run_job_id,
                "case_count": case_count,
                "created_at": created_at,
                "created_by": created_by,
            }
        )
        if scores is not UNSET:
            field_dict["scores"] = scores
        if running is not UNSET:
            field_dict["running"] = running

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.experiment_results_response_200_experiment_scores_item import (
            ExperimentResultsResponse200ExperimentScoresItem,
        )
        from ..models.experiment_results_response_200_experiment_subject import (
            ExperimentResultsResponse200ExperimentSubject,
        )

        d = src_dict.copy()
        id = d.pop("id")

        dataset = d.pop("dataset")

        subject = ExperimentResultsResponse200ExperimentSubject.from_dict(d.pop("subject"))

        run_number = d.pop("run_number")

        run_job_id = d.pop("run_job_id")

        case_count = d.pop("case_count")

        created_at = isoparse(d.pop("created_at"))

        created_by = d.pop("created_by")

        scores = []
        _scores = d.pop("scores", UNSET)
        for scores_item_data in _scores or []:
            scores_item = ExperimentResultsResponse200ExperimentScoresItem.from_dict(scores_item_data)

            scores.append(scores_item)

        running = d.pop("running", UNSET)

        experiment_results_response_200_experiment = cls(
            id=id,
            dataset=dataset,
            subject=subject,
            run_number=run_number,
            run_job_id=run_job_id,
            case_count=case_count,
            created_at=created_at,
            created_by=created_by,
            scores=scores,
            running=running,
        )

        experiment_results_response_200_experiment.additional_properties = d
        return experiment_results_response_200_experiment

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
