from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_overview_comparison_series_identity_status import ManagedAgentsEvaluationOverviewComparisonSeriesIdentityStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.managed_agents_evaluation_overview_comparison_point import ManagedAgentsEvaluationOverviewComparisonPoint





T = TypeVar("T", bound="ManagedAgentsEvaluationOverviewComparisonSeries")



@_attrs_define
class ManagedAgentsEvaluationOverviewComparisonSeries:
    """ One selected immutable target-version trace in an evaluation comparison.

        Example:
            {'created_at': '2026-02-18T09:30:00Z', 'identity_status': 'catalog', 'is_latest': True, 'points':
                [{'bucket_start': '2026-02-18T09:30:00Z', 'fail_count': 1, 'not_applicable_count': 1, 'pass_count': 1, 'rate':
                1}], 'target_agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'target_agent_version_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'version_number': 1}

        Attributes:
            identity_status (ManagedAgentsEvaluationOverviewComparisonSeriesIdentityStatus): Whether catalog metadata or
                retained history proves this trace identity.
            is_latest (bool): Whether this was the newest version at the frozen watermark.
            points (list[ManagedAgentsEvaluationOverviewComparisonPoint]): Exact timestamps observed for this trace, or
                shared aligned interval positions; legacy responses contain one fixed 24-hour point per day.
            target_agent_id (UUID): Target agent owning this comparison trace.
            target_agent_version_id (UUID): Immutable target-agent version whose stored evaluations form this trace.
            created_at (datetime.datetime | Unset): Catalog version creation time, omitted for retained-history-only
                identities.
            version_number (int | Unset): Catalog version number, omitted for retained-history-only identities.
     """

    identity_status: ManagedAgentsEvaluationOverviewComparisonSeriesIdentityStatus
    is_latest: bool
    points: list[ManagedAgentsEvaluationOverviewComparisonPoint]
    target_agent_id: UUID
    target_agent_version_id: UUID
    created_at: datetime.datetime | Unset = UNSET
    version_number: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_evaluation_overview_comparison_point import ManagedAgentsEvaluationOverviewComparisonPoint # noqa: PLC0415
        identity_status = self.identity_status.value

        is_latest = self.is_latest

        points = []
        for points_item_data in self.points:
            points_item = points_item_data.to_dict()
            points.append(points_item)



        target_agent_id = str(self.target_agent_id)

        target_agent_version_id = str(self.target_agent_version_id)

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        version_number = self.version_number


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "identity_status": identity_status,
            "is_latest": is_latest,
            "points": points,
            "target_agent_id": target_agent_id,
            "target_agent_version_id": target_agent_version_id,
        })
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if version_number is not UNSET:
            field_dict["version_number"] = version_number

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_evaluation_overview_comparison_point import ManagedAgentsEvaluationOverviewComparisonPoint # noqa: PLC0415
        d = dict(src_dict)
        identity_status = ManagedAgentsEvaluationOverviewComparisonSeriesIdentityStatus(d.pop("identity_status"))




        is_latest = d.pop("is_latest")

        points = []
        _points = d.pop("points")
        for points_item_data in (_points):
            points_item = ManagedAgentsEvaluationOverviewComparisonPoint.from_dict(points_item_data)



            points.append(points_item)


        target_agent_id = UUID(d.pop("target_agent_id"))




        target_agent_version_id = UUID(d.pop("target_agent_version_id"))




        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)




        version_number = d.pop("version_number", UNSET)

        managed_agents_evaluation_overview_comparison_series = cls(
            identity_status=identity_status,
            is_latest=is_latest,
            points=points,
            target_agent_id=target_agent_id,
            target_agent_version_id=target_agent_version_id,
            created_at=created_at,
            version_number=version_number,
        )

        return managed_agents_evaluation_overview_comparison_series

