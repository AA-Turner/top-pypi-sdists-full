from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.grading_config_input_agentic import GradingConfigInputAgentic
  from ..models.grading_config_input_compute_exec import GradingConfigInputComputeExec
  from ..models.grading_config_input_max import GradingConfigInputMax
  from ..models.grading_config_input_mcp_tool_call import GradingConfigInputMcpToolCall
  from ..models.grading_config_input_none import GradingConfigInputNone
  from ..models.grading_config_input_programmatic import GradingConfigInputProgrammatic
  from ..models.grading_config_input_rubric import GradingConfigInputRubric
  from ..models.grading_config_input_weighted_sum import GradingConfigInputWeightedSum





T = TypeVar("T", bound="GradingConfigInputCompositionChild")



@_attrs_define
class GradingConfigInputCompositionChild:
    """ A child entry in a composition group (weighted-sum or max), pairing a config with its weight.

        Attributes:
            node (GradingConfigInputAgentic | GradingConfigInputComputeExec | GradingConfigInputMax |
                GradingConfigInputMcpToolCall | GradingConfigInputNone | GradingConfigInputProgrammatic |
                GradingConfigInputRubric | GradingConfigInputWeightedSum): Recursive grading configuration tree for a problem
                version: a leaf strategy (none, rubric, agentic, programmatic, mcp_tool_call, compute_exec) or a composition
                group (weighted-sum, max) of further configs. Tree depth must be ≤ 3.
            weight (float): Relative weight of this child within its parent composition (between 0 and 1).
     """

    node: GradingConfigInputAgentic | GradingConfigInputComputeExec | GradingConfigInputMax | GradingConfigInputMcpToolCall | GradingConfigInputNone | GradingConfigInputProgrammatic | GradingConfigInputRubric | GradingConfigInputWeightedSum
    weight: float
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.grading_config_input_agentic import GradingConfigInputAgentic # noqa: PLC0415
        from ..models.grading_config_input_compute_exec import GradingConfigInputComputeExec # noqa: PLC0415
        from ..models.grading_config_input_max import GradingConfigInputMax # noqa: PLC0415
        from ..models.grading_config_input_mcp_tool_call import GradingConfigInputMcpToolCall # noqa: PLC0415
        from ..models.grading_config_input_none import GradingConfigInputNone # noqa: PLC0415
        from ..models.grading_config_input_programmatic import GradingConfigInputProgrammatic # noqa: PLC0415
        from ..models.grading_config_input_rubric import GradingConfigInputRubric # noqa: PLC0415
        from ..models.grading_config_input_weighted_sum import GradingConfigInputWeightedSum # noqa: PLC0415
        node: dict[str, Any]
        if isinstance(self.node, GradingConfigInputNone):
            node = self.node.to_dict()
        elif isinstance(self.node, GradingConfigInputRubric):
            node = self.node.to_dict()
        elif isinstance(self.node, GradingConfigInputAgentic):
            node = self.node.to_dict()
        elif isinstance(self.node, GradingConfigInputProgrammatic):
            node = self.node.to_dict()
        elif isinstance(self.node, GradingConfigInputMcpToolCall):
            node = self.node.to_dict()
        elif isinstance(self.node, GradingConfigInputComputeExec):
            node = self.node.to_dict()
        elif isinstance(self.node, GradingConfigInputWeightedSum):
            node = self.node.to_dict()
        else:
            node = self.node.to_dict()


        weight = self.weight


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "node": node,
            "weight": weight,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.grading_config_input_agentic import GradingConfigInputAgentic # noqa: PLC0415
        from ..models.grading_config_input_compute_exec import GradingConfigInputComputeExec # noqa: PLC0415
        from ..models.grading_config_input_max import GradingConfigInputMax # noqa: PLC0415
        from ..models.grading_config_input_mcp_tool_call import GradingConfigInputMcpToolCall # noqa: PLC0415
        from ..models.grading_config_input_none import GradingConfigInputNone # noqa: PLC0415
        from ..models.grading_config_input_programmatic import GradingConfigInputProgrammatic # noqa: PLC0415
        from ..models.grading_config_input_rubric import GradingConfigInputRubric # noqa: PLC0415
        from ..models.grading_config_input_weighted_sum import GradingConfigInputWeightedSum # noqa: PLC0415
        d = dict(src_dict)
        def _parse_node(data: object) -> GradingConfigInputAgentic | GradingConfigInputComputeExec | GradingConfigInputMax | GradingConfigInputMcpToolCall | GradingConfigInputNone | GradingConfigInputProgrammatic | GradingConfigInputRubric | GradingConfigInputWeightedSum:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_input_type_0 = GradingConfigInputNone.from_dict(data)



                return componentsschemas_grading_config_input_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_input_type_1 = GradingConfigInputRubric.from_dict(data)



                return componentsschemas_grading_config_input_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_input_type_2 = GradingConfigInputAgentic.from_dict(data)



                return componentsschemas_grading_config_input_type_2
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_input_type_3 = GradingConfigInputProgrammatic.from_dict(data)



                return componentsschemas_grading_config_input_type_3
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_input_type_4 = GradingConfigInputMcpToolCall.from_dict(data)



                return componentsschemas_grading_config_input_type_4
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_input_type_5 = GradingConfigInputComputeExec.from_dict(data)



                return componentsschemas_grading_config_input_type_5
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_grading_config_input_type_6 = GradingConfigInputWeightedSum.from_dict(data)



                return componentsschemas_grading_config_input_type_6
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            componentsschemas_grading_config_input_type_7 = GradingConfigInputMax.from_dict(data)



            return componentsschemas_grading_config_input_type_7

        node = _parse_node(d.pop("node"))


        weight = d.pop("weight")

        grading_config_input_composition_child = cls(
            node=node,
            weight=weight,
        )


        grading_config_input_composition_child.additional_properties = d
        return grading_config_input_composition_child

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
