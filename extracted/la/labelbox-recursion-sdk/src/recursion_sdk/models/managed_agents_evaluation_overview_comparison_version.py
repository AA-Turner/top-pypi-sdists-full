from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.managed_agents_evaluation_overview_comparison_version_identity_status import ManagedAgentsEvaluationOverviewComparisonVersionIdentityStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="ManagedAgentsEvaluationOverviewComparisonVersion")



@_attrs_define
class ManagedAgentsEvaluationOverviewComparisonVersion:
    """ One bounded immutable target-version option for an evaluation comparison.

        Example:
            {'created_at': '2026-02-18T09:30:00Z', 'has_current_observations': True, 'identity_status': 'catalog',
                'is_latest': True, 'selected': True, 'target_agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d',
                'version_number': 1}

        Attributes:
            has_current_observations (bool): Whether the selected evaluator observed this version in the current chart
                window.
            identity_status (ManagedAgentsEvaluationOverviewComparisonVersionIdentityStatus): Whether live catalog metadata
                or retained same-organization history proves this identity.
            is_latest (bool): Whether this was the newest immutable version before the frozen watermark.
            selected (bool): Whether this version contributes a comparison trace in this response.
            target_agent_version_id (UUID): Immutable target-agent version represented by this option.
            created_at (datetime.datetime | Unset): Catalog creation time, omitted when only retained history proves the
                identity.
            version_number (int | Unset): Catalog version number, omitted when only retained history proves the identity.
     """

    has_current_observations: bool
    identity_status: ManagedAgentsEvaluationOverviewComparisonVersionIdentityStatus
    is_latest: bool
    selected: bool
    target_agent_version_id: UUID
    created_at: datetime.datetime | Unset = UNSET
    version_number: int | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        has_current_observations = self.has_current_observations

        identity_status = self.identity_status.value

        is_latest = self.is_latest

        selected = self.selected

        target_agent_version_id = str(self.target_agent_version_id)

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        version_number = self.version_number


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "has_current_observations": has_current_observations,
            "identity_status": identity_status,
            "is_latest": is_latest,
            "selected": selected,
            "target_agent_version_id": target_agent_version_id,
        })
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if version_number is not UNSET:
            field_dict["version_number"] = version_number

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        has_current_observations = d.pop("has_current_observations")

        identity_status = ManagedAgentsEvaluationOverviewComparisonVersionIdentityStatus(d.pop("identity_status"))




        is_latest = d.pop("is_latest")

        selected = d.pop("selected")

        target_agent_version_id = UUID(d.pop("target_agent_version_id"))




        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at,  Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(_created_at)




        version_number = d.pop("version_number", UNSET)

        managed_agents_evaluation_overview_comparison_version = cls(
            has_current_observations=has_current_observations,
            identity_status=identity_status,
            is_latest=is_latest,
            selected=selected,
            target_agent_version_id=target_agent_version_id,
            created_at=created_at,
            version_number=version_number,
        )

        return managed_agents_evaluation_overview_comparison_version

