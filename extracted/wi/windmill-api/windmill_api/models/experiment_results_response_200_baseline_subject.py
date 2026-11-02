from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.experiment_results_response_200_baseline_subject_kind import (
    ExperimentResultsResponse200BaselineSubjectKind,
)
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.experiment_results_response_200_baseline_subject_draft import (
        ExperimentResultsResponse200BaselineSubjectDraft,
    )


T = TypeVar("T", bound="ExperimentResultsResponse200BaselineSubject")


@_attrs_define
class ExperimentResultsResponse200BaselineSubject:
    """What an eval run is executed against.

    Attributes:
        kind (ExperimentResultsResponse200BaselineSubjectKind): `agent` runs the ai_agent resource as it is deployed
            when the run opens, `agent_draft` the caller's unsaved edits of it as the editor holds them (carried in
            `draft`), and `agent_version` one past version named by `version`. The first and last are read server-side; all
            three are inlined into the run, so every case of a run executes one configuration: a deploy part-way through
            changes what the next run measures, never this one.
        path (str): Path of the ai_agent resource.
        version (Union[Unset, None, int]): The agent's per-path version number when the run opened: how many times the
            resource had been saved, not a resource_version row id. For `agent` and `agent_draft` it names the configuration
            the run read and every case executed. For `agent_version` it is the request's own, says which version to inline,
            and is required.
        draft (Union[Unset, ExperimentResultsResponse200BaselineSubjectDraft]): The brain and tools of an agent, as the
            flow editor holds them. Carried by the request and present exactly when the subject kind is `agent_draft` — the
            edits exist only in the editor — where it is the whole definition of what ran: the run goes through the same
            unlinked branch of the agent executor the editor's own test uses.
        draft_hash (Union[Unset, str]): Hash of the configuration a draft run executed, stamped server-side. A draft
            moves without the version moving, so this is what dates a run of one. It is also what recognises a draft run
            whose configuration was later deployed: when it matches the agent as deployed, the run's kind and version are
            rewritten to that version, once, and the hash is kept as what the resolution rests on.
    """

    kind: ExperimentResultsResponse200BaselineSubjectKind
    path: str
    version: Union[Unset, None, int] = UNSET
    draft: Union[Unset, "ExperimentResultsResponse200BaselineSubjectDraft"] = UNSET
    draft_hash: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        path = self.path
        version = self.version
        draft: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.draft, Unset):
            draft = self.draft.to_dict()

        draft_hash = self.draft_hash

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "path": path,
            }
        )
        if version is not UNSET:
            field_dict["version"] = version
        if draft is not UNSET:
            field_dict["draft"] = draft
        if draft_hash is not UNSET:
            field_dict["draft_hash"] = draft_hash

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.experiment_results_response_200_baseline_subject_draft import (
            ExperimentResultsResponse200BaselineSubjectDraft,
        )

        d = src_dict.copy()
        kind = ExperimentResultsResponse200BaselineSubjectKind(d.pop("kind"))

        path = d.pop("path")

        version = d.pop("version", UNSET)

        _draft = d.pop("draft", UNSET)
        draft: Union[Unset, ExperimentResultsResponse200BaselineSubjectDraft]
        if isinstance(_draft, Unset):
            draft = UNSET
        else:
            draft = ExperimentResultsResponse200BaselineSubjectDraft.from_dict(_draft)

        draft_hash = d.pop("draft_hash", UNSET)

        experiment_results_response_200_baseline_subject = cls(
            kind=kind,
            path=path,
            version=version,
            draft=draft,
            draft_hash=draft_hash,
        )

        experiment_results_response_200_baseline_subject.additional_properties = d
        return experiment_results_response_200_baseline_subject

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
