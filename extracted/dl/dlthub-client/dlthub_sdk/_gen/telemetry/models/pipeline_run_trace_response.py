from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.pipeline_run_trace_response_execution_context import (
        PipelineRunTraceResponseExecutionContext,
    )
    from ..models.pipeline_run_trace_response_steps_item import (
        PipelineRunTraceResponseStepsItem,
    )


T = TypeVar("T", bound="PipelineRunTraceResponse")


@_attrs_define
class PipelineRunTraceResponse:
    """
    Attributes:
        execution_context (PipelineRunTraceResponseExecutionContext): The dlt, Python and host versions the pipeline ran
            with.
        pipeline_name (str): The pipeline that ran.
        steps (list[PipelineRunTraceResponseStepsItem]): The extract, normalize and load steps, in order.
        transaction_id (str): The dlt transaction the trace records.
    """

    execution_context: PipelineRunTraceResponseExecutionContext
    pipeline_name: str
    steps: list[PipelineRunTraceResponseStepsItem]
    transaction_id: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        execution_context = self.execution_context.to_dict()

        pipeline_name = self.pipeline_name

        steps = []
        for steps_item_data in self.steps:
            steps_item = steps_item_data.to_dict()
            steps.append(steps_item)

        transaction_id = self.transaction_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "execution_context": execution_context,
                "pipeline_name": pipeline_name,
                "steps": steps,
                "transaction_id": transaction_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pipeline_run_trace_response_execution_context import (
            PipelineRunTraceResponseExecutionContext,
        )
        from ..models.pipeline_run_trace_response_steps_item import (
            PipelineRunTraceResponseStepsItem,
        )

        d = dict(src_dict)
        execution_context = PipelineRunTraceResponseExecutionContext.from_dict(
            d.pop("execution_context")
        )

        pipeline_name = d.pop("pipeline_name")

        steps = []
        _steps = d.pop("steps")
        for steps_item_data in _steps:
            steps_item = PipelineRunTraceResponseStepsItem.from_dict(steps_item_data)

            steps.append(steps_item)

        transaction_id = d.pop("transaction_id")

        pipeline_run_trace_response = cls(
            execution_context=execution_context,
            pipeline_name=pipeline_name,
            steps=steps,
            transaction_id=transaction_id,
        )

        pipeline_run_trace_response.additional_properties = d
        return pipeline_run_trace_response

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
