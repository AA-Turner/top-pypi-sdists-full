from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.experiment_results_response_200_baseline import ExperimentResultsResponse200Baseline
    from ..models.experiment_results_response_200_experiment import ExperimentResultsResponse200Experiment
    from ..models.experiment_results_response_200_means_item import ExperimentResultsResponse200MeansItem
    from ..models.experiment_results_response_200_rows_item import ExperimentResultsResponse200RowsItem
    from ..models.experiment_results_response_200_scorers_item import ExperimentResultsResponse200ScorersItem


T = TypeVar("T", bound="ExperimentResultsResponse200")


@_attrs_define
class ExperimentResultsResponse200:
    """
    Attributes:
        experiment (ExperimentResultsResponse200Experiment): One run of a dataset: written once when the dataset is run,
            and only ever read afterwards. The case set it executed is returned by the results endpoint, not here: a listing
            would otherwise send the whole dataset back once per experiment.
        scorers (List['ExperimentResultsResponse200ScorersItem']): The columns, which belong to the dataset rather than
            the experiment.
        rows (List['ExperimentResultsResponse200RowsItem']):
        means (List['ExperimentResultsResponse200MeansItem']):
        regressed (int): Cells scoring lower than the baseline, across every column.
        baseline (Union[Unset, ExperimentResultsResponse200Baseline]): One run of a dataset: written once when the
            dataset is run, and only ever read afterwards. The case set it executed is returned by the results endpoint, not
            here: a listing would otherwise send the whole dataset back once per experiment.
        subject_current_version (Union[Unset, int]): The version the subject is on now. A row that ran against an
            earlier one describes an agent that no longer exists.
        subject_deployed_hash (Union[Unset, str]): What the agent hashes to as deployed. A run of unsaved edits carrying
            this hash ran exactly what is deployed now — the edits were saved — so it is a run of that version rather than
            of edits.
    """

    experiment: "ExperimentResultsResponse200Experiment"
    scorers: List["ExperimentResultsResponse200ScorersItem"]
    rows: List["ExperimentResultsResponse200RowsItem"]
    means: List["ExperimentResultsResponse200MeansItem"]
    regressed: int
    baseline: Union[Unset, "ExperimentResultsResponse200Baseline"] = UNSET
    subject_current_version: Union[Unset, int] = UNSET
    subject_deployed_hash: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        experiment = self.experiment.to_dict()

        scorers = []
        for scorers_item_data in self.scorers:
            scorers_item = scorers_item_data.to_dict()

            scorers.append(scorers_item)

        rows = []
        for rows_item_data in self.rows:
            rows_item = rows_item_data.to_dict()

            rows.append(rows_item)

        means = []
        for means_item_data in self.means:
            means_item = means_item_data.to_dict()

            means.append(means_item)

        regressed = self.regressed
        baseline: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.baseline, Unset):
            baseline = self.baseline.to_dict()

        subject_current_version = self.subject_current_version
        subject_deployed_hash = self.subject_deployed_hash

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "experiment": experiment,
                "scorers": scorers,
                "rows": rows,
                "means": means,
                "regressed": regressed,
            }
        )
        if baseline is not UNSET:
            field_dict["baseline"] = baseline
        if subject_current_version is not UNSET:
            field_dict["subject_current_version"] = subject_current_version
        if subject_deployed_hash is not UNSET:
            field_dict["subject_deployed_hash"] = subject_deployed_hash

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.experiment_results_response_200_baseline import ExperimentResultsResponse200Baseline
        from ..models.experiment_results_response_200_experiment import ExperimentResultsResponse200Experiment
        from ..models.experiment_results_response_200_means_item import ExperimentResultsResponse200MeansItem
        from ..models.experiment_results_response_200_rows_item import ExperimentResultsResponse200RowsItem
        from ..models.experiment_results_response_200_scorers_item import ExperimentResultsResponse200ScorersItem

        d = src_dict.copy()
        experiment = ExperimentResultsResponse200Experiment.from_dict(d.pop("experiment"))

        scorers = []
        _scorers = d.pop("scorers")
        for scorers_item_data in _scorers:
            scorers_item = ExperimentResultsResponse200ScorersItem.from_dict(scorers_item_data)

            scorers.append(scorers_item)

        rows = []
        _rows = d.pop("rows")
        for rows_item_data in _rows:
            rows_item = ExperimentResultsResponse200RowsItem.from_dict(rows_item_data)

            rows.append(rows_item)

        means = []
        _means = d.pop("means")
        for means_item_data in _means:
            means_item = ExperimentResultsResponse200MeansItem.from_dict(means_item_data)

            means.append(means_item)

        regressed = d.pop("regressed")

        _baseline = d.pop("baseline", UNSET)
        baseline: Union[Unset, ExperimentResultsResponse200Baseline]
        if isinstance(_baseline, Unset):
            baseline = UNSET
        else:
            baseline = ExperimentResultsResponse200Baseline.from_dict(_baseline)

        subject_current_version = d.pop("subject_current_version", UNSET)

        subject_deployed_hash = d.pop("subject_deployed_hash", UNSET)

        experiment_results_response_200 = cls(
            experiment=experiment,
            scorers=scorers,
            rows=rows,
            means=means,
            regressed=regressed,
            baseline=baseline,
            subject_current_version=subject_current_version,
            subject_deployed_hash=subject_deployed_hash,
        )

        experiment_results_response_200.additional_properties = d
        return experiment_results_response_200

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
