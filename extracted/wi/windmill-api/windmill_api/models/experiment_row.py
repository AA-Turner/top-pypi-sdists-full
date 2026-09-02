from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.experiment_row_status import ExperimentRowStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.experiment_row_input import ExperimentRowInput
    from ..models.experiment_row_scores_item import ExperimentRowScoresItem


T = TypeVar("T", bound="ExperimentRow")


@_attrs_define
class ExperimentRow:
    """
    Attributes:
        case_id (str):
        input_ (ExperimentRowInput): The inputs a standalone run feeds the agent.
        status (ExperimentRowStatus): The case's status; `running` until its iteration completes, and `unavailable` for
            a case whose job was retained away before anything read what it produced.
        scores (List['ExperimentRowScoresItem']): One entry per scorer of the dataset, in column order.
        expected (Union[Unset, Any]):
        job_id (Union[Unset, str]): The iteration that ran this case. Absent between a run being recorded and its flow
            reaching this case, which reads as a case still to run.
        output (Union[Unset, str]): The agent's answer. The full trajectory stays reachable through job_id.
        subject_version (Union[Unset, int]): The agent version this cell ran against. Cells of one experiment can
            differ, which the table says rather than averaging two versions silently.
        subject_draft_hash (Union[Unset, str]): For a run of unsaved edits, the hash of the configuration this cell ran.
            Edits move without a version changing, so this is what identifies what ran, and what recognises a run whose
            edits were later saved as a run of that version.
    """

    case_id: str
    input_: "ExperimentRowInput"
    status: ExperimentRowStatus
    scores: List["ExperimentRowScoresItem"]
    expected: Union[Unset, Any] = UNSET
    job_id: Union[Unset, str] = UNSET
    output: Union[Unset, str] = UNSET
    subject_version: Union[Unset, int] = UNSET
    subject_draft_hash: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        case_id = self.case_id
        input_ = self.input_.to_dict()

        status = self.status.value

        scores = []
        for scores_item_data in self.scores:
            scores_item = scores_item_data.to_dict()

            scores.append(scores_item)

        expected = self.expected
        job_id = self.job_id
        output = self.output
        subject_version = self.subject_version
        subject_draft_hash = self.subject_draft_hash

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "case_id": case_id,
                "input": input_,
                "status": status,
                "scores": scores,
            }
        )
        if expected is not UNSET:
            field_dict["expected"] = expected
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if output is not UNSET:
            field_dict["output"] = output
        if subject_version is not UNSET:
            field_dict["subject_version"] = subject_version
        if subject_draft_hash is not UNSET:
            field_dict["subject_draft_hash"] = subject_draft_hash

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.experiment_row_input import ExperimentRowInput
        from ..models.experiment_row_scores_item import ExperimentRowScoresItem

        d = src_dict.copy()
        case_id = d.pop("case_id")

        input_ = ExperimentRowInput.from_dict(d.pop("input"))

        status = ExperimentRowStatus(d.pop("status"))

        scores = []
        _scores = d.pop("scores")
        for scores_item_data in _scores:
            scores_item = ExperimentRowScoresItem.from_dict(scores_item_data)

            scores.append(scores_item)

        expected = d.pop("expected", UNSET)

        job_id = d.pop("job_id", UNSET)

        output = d.pop("output", UNSET)

        subject_version = d.pop("subject_version", UNSET)

        subject_draft_hash = d.pop("subject_draft_hash", UNSET)

        experiment_row = cls(
            case_id=case_id,
            input_=input_,
            status=status,
            scores=scores,
            expected=expected,
            job_id=job_id,
            output=output,
            subject_version=subject_version,
            subject_draft_hash=subject_draft_hash,
        )

        experiment_row.additional_properties = d
        return experiment_row

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
