import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.lifecycle_state_enum import LifecycleStateEnum
from ..models.round_status import RoundStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="NestedRound")


@_attrs_define
class NestedRound:
    """
    Attributes:
        uuid (Union[Unset, UUID]):
        slug (Union[Unset, str]):
        name (Union[Unset, str]):
        start_time (Union[Unset, datetime.datetime]):
        cutoff_time (Union[Unset, datetime.datetime]):
        status (Union[Unset, RoundStatus]):
        allocation_date (Union[None, Unset, datetime.datetime]):
        review_duration_in_days (Union[None, Unset, int]):
        lifecycle_state (Union[LifecycleStateEnum, None, Unset]): Where the round stands after its cut-off: evaluating,
            deciding, results_published or closed. Empty before the cut-off.
        evaluation_started_at (Union[None, Unset, datetime.datetime]):
        deciding_started_at (Union[None, Unset, datetime.datetime]):
        results_published_at (Union[None, Unset, datetime.datetime]):
        closed_at (Union[None, Unset, datetime.datetime]):
    """

    uuid: Union[Unset, UUID] = UNSET
    slug: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    cutoff_time: Union[Unset, datetime.datetime] = UNSET
    status: Union[Unset, RoundStatus] = UNSET
    allocation_date: Union[None, Unset, datetime.datetime] = UNSET
    review_duration_in_days: Union[None, Unset, int] = UNSET
    lifecycle_state: Union[LifecycleStateEnum, None, Unset] = UNSET
    evaluation_started_at: Union[None, Unset, datetime.datetime] = UNSET
    deciding_started_at: Union[None, Unset, datetime.datetime] = UNSET
    results_published_at: Union[None, Unset, datetime.datetime] = UNSET
    closed_at: Union[None, Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        slug = self.slug

        name = self.name

        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        cutoff_time: Union[Unset, str] = UNSET
        if not isinstance(self.cutoff_time, Unset):
            cutoff_time = self.cutoff_time.isoformat()

        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        allocation_date: Union[None, Unset, str]
        if isinstance(self.allocation_date, Unset):
            allocation_date = UNSET
        elif isinstance(self.allocation_date, datetime.datetime):
            allocation_date = self.allocation_date.isoformat()
        else:
            allocation_date = self.allocation_date

        review_duration_in_days: Union[None, Unset, int]
        if isinstance(self.review_duration_in_days, Unset):
            review_duration_in_days = UNSET
        else:
            review_duration_in_days = self.review_duration_in_days

        lifecycle_state: Union[None, Unset, str]
        if isinstance(self.lifecycle_state, Unset):
            lifecycle_state = UNSET
        elif isinstance(self.lifecycle_state, LifecycleStateEnum):
            lifecycle_state = self.lifecycle_state.value
        else:
            lifecycle_state = self.lifecycle_state

        evaluation_started_at: Union[None, Unset, str]
        if isinstance(self.evaluation_started_at, Unset):
            evaluation_started_at = UNSET
        elif isinstance(self.evaluation_started_at, datetime.datetime):
            evaluation_started_at = self.evaluation_started_at.isoformat()
        else:
            evaluation_started_at = self.evaluation_started_at

        deciding_started_at: Union[None, Unset, str]
        if isinstance(self.deciding_started_at, Unset):
            deciding_started_at = UNSET
        elif isinstance(self.deciding_started_at, datetime.datetime):
            deciding_started_at = self.deciding_started_at.isoformat()
        else:
            deciding_started_at = self.deciding_started_at

        results_published_at: Union[None, Unset, str]
        if isinstance(self.results_published_at, Unset):
            results_published_at = UNSET
        elif isinstance(self.results_published_at, datetime.datetime):
            results_published_at = self.results_published_at.isoformat()
        else:
            results_published_at = self.results_published_at

        closed_at: Union[None, Unset, str]
        if isinstance(self.closed_at, Unset):
            closed_at = UNSET
        elif isinstance(self.closed_at, datetime.datetime):
            closed_at = self.closed_at.isoformat()
        else:
            closed_at = self.closed_at

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if slug is not UNSET:
            field_dict["slug"] = slug
        if name is not UNSET:
            field_dict["name"] = name
        if start_time is not UNSET:
            field_dict["start_time"] = start_time
        if cutoff_time is not UNSET:
            field_dict["cutoff_time"] = cutoff_time
        if status is not UNSET:
            field_dict["status"] = status
        if allocation_date is not UNSET:
            field_dict["allocation_date"] = allocation_date
        if review_duration_in_days is not UNSET:
            field_dict["review_duration_in_days"] = review_duration_in_days
        if lifecycle_state is not UNSET:
            field_dict["lifecycle_state"] = lifecycle_state
        if evaluation_started_at is not UNSET:
            field_dict["evaluation_started_at"] = evaluation_started_at
        if deciding_started_at is not UNSET:
            field_dict["deciding_started_at"] = deciding_started_at
        if results_published_at is not UNSET:
            field_dict["results_published_at"] = results_published_at
        if closed_at is not UNSET:
            field_dict["closed_at"] = closed_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        slug = d.pop("slug", UNSET)

        name = d.pop("name", UNSET)

        _start_time = d.pop("start_time", UNSET)
        start_time: Union[Unset, datetime.datetime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        _cutoff_time = d.pop("cutoff_time", UNSET)
        cutoff_time: Union[Unset, datetime.datetime]
        if isinstance(_cutoff_time, Unset):
            cutoff_time = UNSET
        else:
            cutoff_time = isoparse(_cutoff_time)

        _status = d.pop("status", UNSET)
        status: Union[Unset, RoundStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = RoundStatus(_status)

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

        def _parse_review_duration_in_days(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        review_duration_in_days = _parse_review_duration_in_days(d.pop("review_duration_in_days", UNSET))

        def _parse_lifecycle_state(data: object) -> Union[LifecycleStateEnum, None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                lifecycle_state_type_0 = LifecycleStateEnum(data)

                return lifecycle_state_type_0
            except:  # noqa: E722
                pass
            return cast(Union[LifecycleStateEnum, None, Unset], data)

        lifecycle_state = _parse_lifecycle_state(d.pop("lifecycle_state", UNSET))

        def _parse_evaluation_started_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                evaluation_started_at_type_0 = isoparse(data)

                return evaluation_started_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        evaluation_started_at = _parse_evaluation_started_at(d.pop("evaluation_started_at", UNSET))

        def _parse_deciding_started_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deciding_started_at_type_0 = isoparse(data)

                return deciding_started_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        deciding_started_at = _parse_deciding_started_at(d.pop("deciding_started_at", UNSET))

        def _parse_results_published_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                results_published_at_type_0 = isoparse(data)

                return results_published_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        results_published_at = _parse_results_published_at(d.pop("results_published_at", UNSET))

        def _parse_closed_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                closed_at_type_0 = isoparse(data)

                return closed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        closed_at = _parse_closed_at(d.pop("closed_at", UNSET))

        nested_round = cls(
            uuid=uuid,
            slug=slug,
            name=name,
            start_time=start_time,
            cutoff_time=cutoff_time,
            status=status,
            allocation_date=allocation_date,
            review_duration_in_days=review_duration_in_days,
            lifecycle_state=lifecycle_state,
            evaluation_started_at=evaluation_started_at,
            deciding_started_at=deciding_started_at,
            results_published_at=results_published_at,
            closed_at=closed_at,
        )

        nested_round.additional_properties = d
        return nested_round

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
