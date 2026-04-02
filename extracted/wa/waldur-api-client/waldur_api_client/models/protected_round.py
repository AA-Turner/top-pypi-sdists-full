import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.allocation_time_enum import AllocationTimeEnum
from ..models.deciding_entity_enum import DecidingEntityEnum
from ..models.review_strategy_enum import ReviewStrategyEnum
from ..models.round_status import RoundStatus
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.protected_proposal_list import ProtectedProposalList


T = TypeVar("T", bound="ProtectedRound")


@_attrs_define
class ProtectedRound:
    """
    Attributes:
        uuid (UUID):
        slug (str):
        name (str):
        start_time (datetime.datetime):
        cutoff_time (datetime.datetime):
        status (RoundStatus):
        url (str):
        proposals (list['ProtectedProposalList']):
        review_strategy (Union[Unset, ReviewStrategyEnum]):
        deciding_entity (Union[Unset, DecidingEntityEnum]):
        allocation_time (Union[Unset, AllocationTimeEnum]):
        allocation_date (Union[None, Unset, datetime.datetime]):
        minimal_average_scoring (Union[None, Unset, str]):
        review_duration_in_days (Union[Unset, int]):
        minimum_number_of_reviewers (Union[None, Unset, int]):
    """

    uuid: UUID
    slug: str
    name: str
    start_time: datetime.datetime
    cutoff_time: datetime.datetime
    status: RoundStatus
    url: str
    proposals: list["ProtectedProposalList"]
    review_strategy: Union[Unset, ReviewStrategyEnum] = UNSET
    deciding_entity: Union[Unset, DecidingEntityEnum] = UNSET
    allocation_time: Union[Unset, AllocationTimeEnum] = UNSET
    allocation_date: Union[None, Unset, datetime.datetime] = UNSET
    minimal_average_scoring: Union[None, Unset, str] = UNSET
    review_duration_in_days: Union[Unset, int] = UNSET
    minimum_number_of_reviewers: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid = str(self.uuid)

        slug = self.slug

        name = self.name

        start_time = self.start_time.isoformat()

        cutoff_time = self.cutoff_time.isoformat()

        status = self.status.value

        url = self.url

        proposals = []
        for proposals_item_data in self.proposals:
            proposals_item = proposals_item_data.to_dict()
            proposals.append(proposals_item)

        review_strategy: Union[Unset, str] = UNSET
        if not isinstance(self.review_strategy, Unset):
            review_strategy = self.review_strategy.value

        deciding_entity: Union[Unset, str] = UNSET
        if not isinstance(self.deciding_entity, Unset):
            deciding_entity = self.deciding_entity.value

        allocation_time: Union[Unset, str] = UNSET
        if not isinstance(self.allocation_time, Unset):
            allocation_time = self.allocation_time.value

        allocation_date: Union[None, Unset, str]
        if isinstance(self.allocation_date, Unset):
            allocation_date = UNSET
        elif isinstance(self.allocation_date, datetime.datetime):
            allocation_date = self.allocation_date.isoformat()
        else:
            allocation_date = self.allocation_date

        minimal_average_scoring: Union[None, Unset, str]
        if isinstance(self.minimal_average_scoring, Unset):
            minimal_average_scoring = UNSET
        else:
            minimal_average_scoring = self.minimal_average_scoring

        review_duration_in_days = self.review_duration_in_days

        minimum_number_of_reviewers: Union[None, Unset, int]
        if isinstance(self.minimum_number_of_reviewers, Unset):
            minimum_number_of_reviewers = UNSET
        else:
            minimum_number_of_reviewers = self.minimum_number_of_reviewers

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
                "url": url,
                "proposals": proposals,
            }
        )
        if review_strategy is not UNSET:
            field_dict["review_strategy"] = review_strategy
        if deciding_entity is not UNSET:
            field_dict["deciding_entity"] = deciding_entity
        if allocation_time is not UNSET:
            field_dict["allocation_time"] = allocation_time
        if allocation_date is not UNSET:
            field_dict["allocation_date"] = allocation_date
        if minimal_average_scoring is not UNSET:
            field_dict["minimal_average_scoring"] = minimal_average_scoring
        if review_duration_in_days is not UNSET:
            field_dict["review_duration_in_days"] = review_duration_in_days
        if minimum_number_of_reviewers is not UNSET:
            field_dict["minimum_number_of_reviewers"] = minimum_number_of_reviewers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.protected_proposal_list import ProtectedProposalList

        d = dict(src_dict)
        uuid = UUID(d.pop("uuid"))

        slug = d.pop("slug")

        name = d.pop("name")

        start_time = isoparse(d.pop("start_time"))

        cutoff_time = isoparse(d.pop("cutoff_time"))

        status = RoundStatus(d.pop("status"))

        url = d.pop("url")

        proposals = []
        _proposals = d.pop("proposals")
        for proposals_item_data in _proposals:
            proposals_item = ProtectedProposalList.from_dict(proposals_item_data)

            proposals.append(proposals_item)

        _review_strategy = d.pop("review_strategy", UNSET)
        review_strategy: Union[Unset, ReviewStrategyEnum]
        if isinstance(_review_strategy, Unset):
            review_strategy = UNSET
        else:
            review_strategy = ReviewStrategyEnum(_review_strategy)

        _deciding_entity = d.pop("deciding_entity", UNSET)
        deciding_entity: Union[Unset, DecidingEntityEnum]
        if isinstance(_deciding_entity, Unset):
            deciding_entity = UNSET
        else:
            deciding_entity = DecidingEntityEnum(_deciding_entity)

        _allocation_time = d.pop("allocation_time", UNSET)
        allocation_time: Union[Unset, AllocationTimeEnum]
        if isinstance(_allocation_time, Unset):
            allocation_time = UNSET
        else:
            allocation_time = AllocationTimeEnum(_allocation_time)

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

        def _parse_minimal_average_scoring(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        minimal_average_scoring = _parse_minimal_average_scoring(d.pop("minimal_average_scoring", UNSET))

        review_duration_in_days = d.pop("review_duration_in_days", UNSET)

        def _parse_minimum_number_of_reviewers(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        minimum_number_of_reviewers = _parse_minimum_number_of_reviewers(d.pop("minimum_number_of_reviewers", UNSET))

        protected_round = cls(
            uuid=uuid,
            slug=slug,
            name=name,
            start_time=start_time,
            cutoff_time=cutoff_time,
            status=status,
            url=url,
            proposals=proposals,
            review_strategy=review_strategy,
            deciding_entity=deciding_entity,
            allocation_time=allocation_time,
            allocation_date=allocation_date,
            minimal_average_scoring=minimal_average_scoring,
            review_duration_in_days=review_duration_in_days,
            minimum_number_of_reviewers=minimum_number_of_reviewers,
        )

        protected_round.additional_properties = d
        return protected_round

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
