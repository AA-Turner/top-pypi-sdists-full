import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.blank_enum import BlankEnum
from ..models.lifecycle_state_enum import LifecycleStateEnum
from ..models.round_status import RoundStatus
from ..models.undecided_at_round_completion_enum import UndecidedAtRoundCompletionEnum
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.protected_proposal_list import ProtectedProposalList
    from ..models.publish_round_results_failure import PublishRoundResultsFailure


T = TypeVar("T", bound="CompleteRoundResponse")


@_attrs_define
class CompleteRoundResponse:
    """
    Attributes:
        uuid (UUID):
        slug (str):
        name (str):
        start_time (datetime.datetime):
        cutoff_time (datetime.datetime):
        status (RoundStatus):
        lifecycle_state (Union[LifecycleStateEnum, None]): Where the round stands after its cut-off: evaluating,
            deciding, results_published or closed. Empty before the cut-off.
        evaluation_started_at (Union[None, datetime.datetime]):
        deciding_started_at (Union[None, datetime.datetime]):
        results_published_at (Union[None, datetime.datetime]):
        closed_at (Union[None, datetime.datetime]):
        url (str):
        proposals (list['ProtectedProposalList']):
        results_published_by_name (Union[None, str]):
        held_decisions_count (Union[None, int]): Proposals of the round whose decision is recorded but not yet
            published. After publication, decisions that could not be carried out; publishing the results again retries
            them. Null for anyone who may not see held decisions.
        has_proposals (bool): Whether the round holds any proposal, in any state. A round with proposals cannot be
            deleted. Unlike the proposals list, which leaves out what the viewer may not see, this counts every one.
        results_forced_reason (Union[None, str]): Why results were published while some proposals of the round still had
            no decision.
        adopted_at (Union[None, datetime.date]): When the round's results were adopted.
        adoption_note (Union[None, str]):
        adoption_document (Union[None, str]):
        rejected_proposals (list['PublishRoundResultsFailure']): Proposals without a decision that completing the round
            rejected.
        failed_proposals (list['PublishRoundResultsFailure']): Proposals without a decision whose rejection failed. The
            round stays open; completing it again retries them.
        allocation_date (Union[None, Unset, datetime.datetime]):
        review_duration_in_days (Union[Unset, int]):
        undecided_at_round_completion (Union[BlankEnum, None, UndecidedAtRoundCompletionEnum, Unset]): Overrides the
            call's rule for proposals still without a decision when the round is completed. Empty: the call's rule applies.
    """

    uuid: UUID
    slug: str
    name: str
    start_time: datetime.datetime
    cutoff_time: datetime.datetime
    status: RoundStatus
    lifecycle_state: Union[LifecycleStateEnum, None]
    evaluation_started_at: Union[None, datetime.datetime]
    deciding_started_at: Union[None, datetime.datetime]
    results_published_at: Union[None, datetime.datetime]
    closed_at: Union[None, datetime.datetime]
    url: str
    proposals: list["ProtectedProposalList"]
    results_published_by_name: Union[None, str]
    held_decisions_count: Union[None, int]
    has_proposals: bool
    results_forced_reason: Union[None, str]
    adopted_at: Union[None, datetime.date]
    adoption_note: Union[None, str]
    adoption_document: Union[None, str]
    rejected_proposals: list["PublishRoundResultsFailure"]
    failed_proposals: list["PublishRoundResultsFailure"]
    allocation_date: Union[None, Unset, datetime.datetime] = UNSET
    review_duration_in_days: Union[Unset, int] = UNSET
    undecided_at_round_completion: Union[BlankEnum, None, UndecidedAtRoundCompletionEnum, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        slug = self.slug

        name = self.name

        start_time = self.start_time.isoformat()

        cutoff_time = self.cutoff_time.isoformat()

        status = self.status.value

        lifecycle_state: Union[None, str]
        if isinstance(self.lifecycle_state, LifecycleStateEnum):
            lifecycle_state = self.lifecycle_state.value
        else:
            lifecycle_state = self.lifecycle_state

        evaluation_started_at: Union[None, str]
        if isinstance(self.evaluation_started_at, datetime.datetime):
            evaluation_started_at = self.evaluation_started_at.isoformat()
        else:
            evaluation_started_at = self.evaluation_started_at

        deciding_started_at: Union[None, str]
        if isinstance(self.deciding_started_at, datetime.datetime):
            deciding_started_at = self.deciding_started_at.isoformat()
        else:
            deciding_started_at = self.deciding_started_at

        results_published_at: Union[None, str]
        if isinstance(self.results_published_at, datetime.datetime):
            results_published_at = self.results_published_at.isoformat()
        else:
            results_published_at = self.results_published_at

        closed_at: Union[None, str]
        if isinstance(self.closed_at, datetime.datetime):
            closed_at = self.closed_at.isoformat()
        else:
            closed_at = self.closed_at

        url = self.url

        proposals = []
        for proposals_item_data in self.proposals:
            proposals_item = proposals_item_data.to_dict()
            proposals.append(proposals_item)

        results_published_by_name: Union[None, str]
        results_published_by_name = self.results_published_by_name

        held_decisions_count: Union[None, int]
        held_decisions_count = self.held_decisions_count

        has_proposals = self.has_proposals

        results_forced_reason: Union[None, str]
        results_forced_reason = self.results_forced_reason

        adopted_at: Union[None, str]
        if isinstance(self.adopted_at, datetime.date):
            adopted_at = self.adopted_at.isoformat()
        else:
            adopted_at = self.adopted_at

        adoption_note: Union[None, str]
        adoption_note = self.adoption_note

        adoption_document: Union[None, str]
        adoption_document = self.adoption_document

        rejected_proposals = []
        for rejected_proposals_item_data in self.rejected_proposals:
            rejected_proposals_item = rejected_proposals_item_data.to_dict()
            rejected_proposals.append(rejected_proposals_item)

        failed_proposals = []
        for failed_proposals_item_data in self.failed_proposals:
            failed_proposals_item = failed_proposals_item_data.to_dict()
            failed_proposals.append(failed_proposals_item)

        allocation_date: Union[None, Unset, str]
        if isinstance(self.allocation_date, Unset):
            allocation_date = UNSET
        elif isinstance(self.allocation_date, datetime.datetime):
            allocation_date = self.allocation_date.isoformat()
        else:
            allocation_date = self.allocation_date

        review_duration_in_days = self.review_duration_in_days

        undecided_at_round_completion: Union[None, Unset, str]
        if isinstance(self.undecided_at_round_completion, Unset):
            undecided_at_round_completion = UNSET
        elif isinstance(self.undecided_at_round_completion, UndecidedAtRoundCompletionEnum):
            undecided_at_round_completion = self.undecided_at_round_completion.value
        elif isinstance(self.undecided_at_round_completion, BlankEnum):
            undecided_at_round_completion = self.undecided_at_round_completion.value
        else:
            undecided_at_round_completion = self.undecided_at_round_completion

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "slug": slug,
                "name": name,
                "start_time": start_time,
                "cutoff_time": cutoff_time,
                "status": status,
                "lifecycle_state": lifecycle_state,
                "evaluation_started_at": evaluation_started_at,
                "deciding_started_at": deciding_started_at,
                "results_published_at": results_published_at,
                "closed_at": closed_at,
                "url": url,
                "proposals": proposals,
                "results_published_by_name": results_published_by_name,
                "held_decisions_count": held_decisions_count,
                "has_proposals": has_proposals,
                "results_forced_reason": results_forced_reason,
                "adopted_at": adopted_at,
                "adoption_note": adoption_note,
                "adoption_document": adoption_document,
                "rejected_proposals": rejected_proposals,
                "failed_proposals": failed_proposals,
            }
        )
        if allocation_date is not UNSET:
            field_dict["allocation_date"] = allocation_date
        if review_duration_in_days is not UNSET:
            field_dict["review_duration_in_days"] = review_duration_in_days
        if undecided_at_round_completion is not UNSET:
            field_dict["undecided_at_round_completion"] = undecided_at_round_completion

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.protected_proposal_list import ProtectedProposalList
        from ..models.publish_round_results_failure import PublishRoundResultsFailure

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        slug = d.pop("slug")

        name = d.pop("name")

        start_time = isoparse(d.pop("start_time"))

        cutoff_time = isoparse(d.pop("cutoff_time"))

        status = RoundStatus(d.pop("status"))

        def _parse_lifecycle_state(data: object) -> Union[LifecycleStateEnum, None]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                lifecycle_state_type_0 = LifecycleStateEnum(data)

                return lifecycle_state_type_0
            except:  # noqa: E722
                pass
            return cast(Union[LifecycleStateEnum, None], data)

        lifecycle_state = _parse_lifecycle_state(d.pop("lifecycle_state"))

        def _parse_evaluation_started_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                evaluation_started_at_type_0 = isoparse(data)

                return evaluation_started_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        evaluation_started_at = _parse_evaluation_started_at(d.pop("evaluation_started_at"))

        def _parse_deciding_started_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deciding_started_at_type_0 = isoparse(data)

                return deciding_started_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        deciding_started_at = _parse_deciding_started_at(d.pop("deciding_started_at"))

        def _parse_results_published_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                results_published_at_type_0 = isoparse(data)

                return results_published_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        results_published_at = _parse_results_published_at(d.pop("results_published_at"))

        def _parse_closed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                closed_at_type_0 = isoparse(data)

                return closed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        closed_at = _parse_closed_at(d.pop("closed_at"))

        url = d.pop("url")

        proposals = []
        _proposals = d.pop("proposals")
        for proposals_item_data in _proposals:
            proposals_item = ProtectedProposalList.from_dict(proposals_item_data)

            proposals.append(proposals_item)

        def _parse_results_published_by_name(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        results_published_by_name = _parse_results_published_by_name(d.pop("results_published_by_name"))

        def _parse_held_decisions_count(data: object) -> Union[None, int]:
            if data is None:
                return data
            return cast(Union[None, int], data)

        held_decisions_count = _parse_held_decisions_count(d.pop("held_decisions_count"))

        has_proposals = d.pop("has_proposals")

        def _parse_results_forced_reason(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        results_forced_reason = _parse_results_forced_reason(d.pop("results_forced_reason"))

        def _parse_adopted_at(data: object) -> Union[None, datetime.date]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                adopted_at_type_0 = isoparse(data).date()

                return adopted_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.date], data)

        adopted_at = _parse_adopted_at(d.pop("adopted_at"))

        def _parse_adoption_note(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        adoption_note = _parse_adoption_note(d.pop("adoption_note"))

        def _parse_adoption_document(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        adoption_document = _parse_adoption_document(d.pop("adoption_document"))

        rejected_proposals = []
        _rejected_proposals = d.pop("rejected_proposals")
        for rejected_proposals_item_data in _rejected_proposals:
            rejected_proposals_item = PublishRoundResultsFailure.from_dict(rejected_proposals_item_data)

            rejected_proposals.append(rejected_proposals_item)

        failed_proposals = []
        _failed_proposals = d.pop("failed_proposals")
        for failed_proposals_item_data in _failed_proposals:
            failed_proposals_item = PublishRoundResultsFailure.from_dict(failed_proposals_item_data)

            failed_proposals.append(failed_proposals_item)

        def _parse_allocation_date(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                allocation_date_type_0 = isoparse(data)

                return allocation_date_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        allocation_date = _parse_allocation_date(d.pop("allocation_date", UNSET))

        review_duration_in_days = d.pop("review_duration_in_days", UNSET)

        def _parse_undecided_at_round_completion(
            data: object,
        ) -> Union[BlankEnum, None, UndecidedAtRoundCompletionEnum, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                undecided_at_round_completion_type_0 = UndecidedAtRoundCompletionEnum(data)

                return undecided_at_round_completion_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, str):
                    raise TypeError()
                undecided_at_round_completion_type_1 = BlankEnum(data)

                return undecided_at_round_completion_type_1
            except:  # noqa: E722
                pass
            return cast(Union[BlankEnum, None, UndecidedAtRoundCompletionEnum, Unset], data)

        undecided_at_round_completion = _parse_undecided_at_round_completion(
            d.pop("undecided_at_round_completion", UNSET)
        )

        complete_round_response = cls(
            uuid=uuid,
            slug=slug,
            name=name,
            start_time=start_time,
            cutoff_time=cutoff_time,
            status=status,
            lifecycle_state=lifecycle_state,
            evaluation_started_at=evaluation_started_at,
            deciding_started_at=deciding_started_at,
            results_published_at=results_published_at,
            closed_at=closed_at,
            url=url,
            proposals=proposals,
            results_published_by_name=results_published_by_name,
            held_decisions_count=held_decisions_count,
            has_proposals=has_proposals,
            results_forced_reason=results_forced_reason,
            adopted_at=adopted_at,
            adoption_note=adoption_note,
            adoption_document=adoption_document,
            rejected_proposals=rejected_proposals,
            failed_proposals=failed_proposals,
            allocation_date=allocation_date,
            review_duration_in_days=review_duration_in_days,
            undecided_at_round_completion=undecided_at_round_completion,
        )

        complete_round_response.additional_properties = d
        return complete_round_response

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
