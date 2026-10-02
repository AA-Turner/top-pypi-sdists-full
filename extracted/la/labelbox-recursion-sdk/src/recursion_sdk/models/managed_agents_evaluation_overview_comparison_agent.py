from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.managed_agents_evaluation_overview_comparison_version import ManagedAgentsEvaluationOverviewComparisonVersion





T = TypeVar("T", bound="ManagedAgentsEvaluationOverviewComparisonAgent")



@_attrs_define
class ManagedAgentsEvaluationOverviewComparisonAgent:
    """ One selected target agent and its bounded immutable-version picker options.

        Example:
            {'default_target_agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'display_name': 'example-name',
                'target_agent_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'version_options': [{'created_at':
                '2026-02-18T09:30:00Z', 'has_current_observations': True, 'identity_status': 'catalog', 'is_latest': True,
                'selected': True, 'target_agent_version_id': '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'version_number': 1}],
                'version_options_truncated': True}

        Attributes:
            default_target_agent_version_id (UUID): Newest immutable version before the frozen watermark, selected
                automatically.
            display_name (str): Stable human-readable name from the frozen latest catalog version, or Deleted agent when
                only retained history remains.
            target_agent_id (UUID): Organization-scoped target agent represented by this comparison group.
            version_options (list[ManagedAgentsEvaluationOverviewComparisonVersion]): Latest plus a bounded preview of prior
                versions available for comparison.
            version_options_truncated (bool): Whether additional prior versions exist beyond this bounded option preview.
     """

    default_target_agent_version_id: UUID
    display_name: str
    target_agent_id: UUID
    version_options: list[ManagedAgentsEvaluationOverviewComparisonVersion]
    version_options_truncated: bool





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_evaluation_overview_comparison_version import ManagedAgentsEvaluationOverviewComparisonVersion # noqa: PLC0415
        default_target_agent_version_id = str(self.default_target_agent_version_id)

        display_name = self.display_name

        target_agent_id = str(self.target_agent_id)

        version_options = []
        for version_options_item_data in self.version_options:
            version_options_item = version_options_item_data.to_dict()
            version_options.append(version_options_item)



        version_options_truncated = self.version_options_truncated


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "default_target_agent_version_id": default_target_agent_version_id,
            "display_name": display_name,
            "target_agent_id": target_agent_id,
            "version_options": version_options,
            "version_options_truncated": version_options_truncated,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_evaluation_overview_comparison_version import ManagedAgentsEvaluationOverviewComparisonVersion # noqa: PLC0415
        d = dict(src_dict)
        default_target_agent_version_id = UUID(d.pop("default_target_agent_version_id"))




        display_name = d.pop("display_name")

        target_agent_id = UUID(d.pop("target_agent_id"))




        version_options = []
        _version_options = d.pop("version_options")
        for version_options_item_data in (_version_options):
            version_options_item = ManagedAgentsEvaluationOverviewComparisonVersion.from_dict(version_options_item_data)



            version_options.append(version_options_item)


        version_options_truncated = d.pop("version_options_truncated")

        managed_agents_evaluation_overview_comparison_agent = cls(
            default_target_agent_version_id=default_target_agent_version_id,
            display_name=display_name,
            target_agent_id=target_agent_id,
            version_options=version_options,
            version_options_truncated=version_options_truncated,
        )

        return managed_agents_evaluation_overview_comparison_agent

