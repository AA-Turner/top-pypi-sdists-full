import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.matching_algorithm import MatchingAlgorithm

T = TypeVar("T", bound="ProposedAssignment")


@_attrs_define
class ProposedAssignment:
    """
    Attributes:
        url (str):
        uuid (UUID):
        call (str):
        reviewer (str):
        reviewer_uuid (UUID):
        reviewer_name (str):
        proposal (str):
        proposal_uuid (UUID):
        proposal_name (str):
        affinity_score (float):
        algorithm_used (MatchingAlgorithm):
        rank (int): Assignment rank (1 = best match)
        is_deployed (bool):
        deployed_at (Union[None, datetime.datetime]):
        deployed_by (Union[None, str]):
        deployed_by_name (str):
        created (datetime.datetime):
    """

    url: str
    uuid: UUID
    call: str
    reviewer: str
    reviewer_uuid: UUID
    reviewer_name: str
    proposal: str
    proposal_uuid: UUID
    proposal_name: str
    affinity_score: float
    algorithm_used: MatchingAlgorithm
    rank: int
    is_deployed: bool
    deployed_at: Union[None, datetime.datetime]
    deployed_by: Union[None, str]
    deployed_by_name: str
    created: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        call = self.call

        reviewer = self.reviewer

        reviewer_uuid = str(self.reviewer_uuid)

        reviewer_name = self.reviewer_name

        proposal = self.proposal

        proposal_uuid = str(self.proposal_uuid)

        proposal_name = self.proposal_name

        affinity_score = self.affinity_score

        algorithm_used = self.algorithm_used.value

        rank = self.rank

        is_deployed = self.is_deployed

        deployed_at: Union[None, str]
        if isinstance(self.deployed_at, datetime.datetime):
            deployed_at = self.deployed_at.isoformat()
        else:
            deployed_at = self.deployed_at

        deployed_by: Union[None, str]
        deployed_by = self.deployed_by

        deployed_by_name = self.deployed_by_name

        created = self.created.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "call": call,
                "reviewer": reviewer,
                "reviewer_uuid": reviewer_uuid,
                "reviewer_name": reviewer_name,
                "proposal": proposal,
                "proposal_uuid": proposal_uuid,
                "proposal_name": proposal_name,
                "affinity_score": affinity_score,
                "algorithm_used": algorithm_used,
                "rank": rank,
                "is_deployed": is_deployed,
                "deployed_at": deployed_at,
                "deployed_by": deployed_by,
                "deployed_by_name": deployed_by_name,
                "created": created,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        call = d.pop("call")

        reviewer = d.pop("reviewer")

        reviewer_uuid = UUID(d.pop("reviewer_uuid"))

        reviewer_name = d.pop("reviewer_name")

        proposal = d.pop("proposal")

        proposal_uuid = UUID(d.pop("proposal_uuid"))

        proposal_name = d.pop("proposal_name")

        affinity_score = d.pop("affinity_score")

        algorithm_used = MatchingAlgorithm(d.pop("algorithm_used"))

        rank = d.pop("rank")

        is_deployed = d.pop("is_deployed")

        def _parse_deployed_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                deployed_at_type_0 = isoparse(data)

                return deployed_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        deployed_at = _parse_deployed_at(d.pop("deployed_at"))

        def _parse_deployed_by(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        deployed_by = _parse_deployed_by(d.pop("deployed_by"))

        deployed_by_name = d.pop("deployed_by_name")

        created = isoparse(d.pop("created"))

        proposed_assignment = cls(
            url=url,
            uuid=uuid,
            call=call,
            reviewer=reviewer,
            reviewer_uuid=reviewer_uuid,
            reviewer_name=reviewer_name,
            proposal=proposal,
            proposal_uuid=proposal_uuid,
            proposal_name=proposal_name,
            affinity_score=affinity_score,
            algorithm_used=algorithm_used,
            rank=rank,
            is_deployed=is_deployed,
            deployed_at=deployed_at,
            deployed_by=deployed_by,
            deployed_by_name=deployed_by_name,
            created=created,
        )

        proposed_assignment.additional_properties = d
        return proposed_assignment

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
