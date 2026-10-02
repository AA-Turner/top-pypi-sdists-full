from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.grading_config_agentic import GradingConfigAgentic
  from ..models.grading_config_compute_exec import GradingConfigComputeExec
  from ..models.grading_config_max import GradingConfigMax
  from ..models.grading_config_mcp_tool_call import GradingConfigMcpToolCall
  from ..models.grading_config_none import GradingConfigNone
  from ..models.grading_config_programmatic import GradingConfigProgrammatic
  from ..models.grading_config_rubric import GradingConfigRubric
  from ..models.grading_config_weighted_sum import GradingConfigWeightedSum





T = TypeVar("T", bound="GradingConfigCompositionChild")



@_attrs_define
class GradingConfigCompositionChild:
    """ A child entry in a composition group (weighted-sum or max), pairing a config with its weight.

        Attributes:
            node (GradingConfigAgentic | GradingConfigComputeExec | GradingConfigMax | GradingConfigMcpToolCall |
                GradingConfigNone | GradingConfigProgrammatic | GradingConfigRubric | GradingConfigWeightedSum): Recursive
                grading configuration tree for a problem version: a leaf strategy (none, rubric, agentic, programmatic,
                mcp_tool_call, compute_exec) or a composition group (weighted-sum, max) of further configs. Tree depth must be ≤
                3.
            weight (float): Relative weight of this child within its parent composition (between 0 and 1).
     """

    node: GradingConfigAgentic | GradingConfigComputeExec | GradingConfigMax | GradingConfigMcpToolCall | GradingConfigNone | GradingConfigProgrammatic | GradingConfigRubric | GradingConfigWeightedSum
    weight: float





    def to_dict(self) -> dict[str, Any]:
        from ..models.grading_config_agentic import GradingConfigAgentic # noqa: PLC0415
        from ..models.grading_config_compute_exec import GradingConfigComputeExec # noqa: PLC0415
        from ..models.grading_config_max import GradingConfigMax # noqa: PLC0415
        from ..models.grading_config_mcp_tool_call import GradingConfigMcpToolCall # noqa: PLC0415
        from ..models.grading_config_none import GradingConfigNone # noqa: PLC0415
        from ..models.grading_config_programmatic import GradingConfigProgrammatic # noqa: PLC0415
        from ..models.grading_config_rubric import GradingConfigRubric # noqa: PLC0415
        from ..models.grading_config_weighted_sum import GradingConfigWeightedSum # noqa: PLC0415
        node: dict[str, Any]
        if isinstance(self.node, GradingConfigNone):
            node = self.node.to_dict()
        elif isinstance(self.node, GradingConfigRubric):
            node = self.node.to_dict()
        elif isinstance(self.node, GradingConfigAgentic):
            node = self.node.to_dict()
        elif isinstance(self.node, GradingConfigProgrammatic):
            node = self.node.to_dict()
        elif isinstance(self.node, GradingConfigMcpToolCall):
            node = self.node.to_dict()
        elif isinstance(self.node, GradingConfigComputeExec):
            node = self.node.to_dict()
        elif isinstance(self.node, GradingConfigWeightedSum):
            node = self.node.to_dict()
        else:
            node = self.node.to_dict()


        weight = self.weight


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "node": node,
            "weight": weight,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.grading_config_agentic import GradingConfigAgentic # noqa: PLC0415
        from ..models.grading_config_compute_exec import GradingConfigComputeExec # noqa: PLC0415
        from ..models.grading_config_max import GradingConfigMax # noqa: PLC0415
        from ..models.grading_config_mcp_tool_call import GradingConfigMcpToolCall # noqa: PLC0415
        from ..models.grading_config_none import GradingConfigNone # noqa: PLC0415
        from ..models.grading_config_programmatic import GradingConfigProgrammatic # noqa: PLC0415
        from ..models.grading_config_rubric import GradingConfigRubric # noqa: PLC0415
        from ..models.grading_config_weighted_sum import GradingConfigWeightedSum # noqa: PLC0415
        d = dict(src_dict)
        def _parse_node(data: object) -> GradingConfigAgentic | GradingConfigComputeExec | GradingConfigMax | GradingConfigMcpToolCall | GradingConfigNone | GradingConfigProgrammatic | GradingConfigRubric | GradingConfigWeightedSum:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_0 = GradingConfigNone.from_dict(data)



                return componentsschemas_grading_config_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_1 = GradingConfigRubric.from_dict(data)



                return componentsschemas_grading_config_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_2 = GradingConfigAgentic.from_dict(data)



                return componentsschemas_grading_config_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_3 = GradingConfigProgrammatic.from_dict(data)



                return componentsschemas_grading_config_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_4 = GradingConfigMcpToolCall.from_dict(data)



                return componentsschemas_grading_config_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_5 = GradingConfigComputeExec.from_dict(data)



                return componentsschemas_grading_config_type_5
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_type_6 = GradingConfigWeightedSum.from_dict(data)



                return componentsschemas_grading_config_type_6
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_grading_config_type_7 = GradingConfigMax.from_dict(data)



            return componentsschemas_grading_config_type_7

        node = _parse_node(d.pop("node"))


        weight = d.pop("weight")

        grading_config_composition_child = cls(
            node=node,
            weight=weight,
        )

        return grading_config_composition_child

