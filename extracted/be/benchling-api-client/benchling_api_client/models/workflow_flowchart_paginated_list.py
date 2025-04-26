from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.workflow_flowchart import WorkflowFlowchart
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkflowFlowchartPaginatedList")


@attr.s(auto_attribs=True, repr=False)
class WorkflowFlowchartPaginatedList:
    """  """

    _next_token: Union[Unset, str] = UNSET
    _workflow_flowcharts: Union[Unset, List[WorkflowFlowchart]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("next_token={}".format(repr(self._next_token)))
        fields.append("workflow_flowcharts={}".format(repr(self._workflow_flowcharts)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "WorkflowFlowchartPaginatedList({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        next_token = self._next_token
        workflow_flowcharts: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._workflow_flowcharts, Unset):
            workflow_flowcharts = []
            for workflow_flowcharts_item_data in self._workflow_flowcharts:
                workflow_flowcharts_item = workflow_flowcharts_item_data.to_dict()

                workflow_flowcharts.append(workflow_flowcharts_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if next_token is not UNSET:
            field_dict["nextToken"] = next_token
        if workflow_flowcharts is not UNSET:
            field_dict["workflowFlowcharts"] = workflow_flowcharts

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_next_token() -> Union[Unset, str]:
            next_token = d.pop("nextToken")
            return next_token

        try:
            next_token = get_next_token()
        except KeyError:
            if strict:
                raise
            next_token = cast(Union[Unset, str], UNSET)

        def get_workflow_flowcharts() -> Union[Unset, List[WorkflowFlowchart]]:
            workflow_flowcharts = []
            _workflow_flowcharts = d.pop("workflowFlowcharts")
            for workflow_flowcharts_item_data in _workflow_flowcharts or []:
                workflow_flowcharts_item = WorkflowFlowchart.from_dict(
                    workflow_flowcharts_item_data, strict=False
                )

                workflow_flowcharts.append(workflow_flowcharts_item)

            return workflow_flowcharts

        try:
            workflow_flowcharts = get_workflow_flowcharts()
        except KeyError:
            if strict:
                raise
            workflow_flowcharts = cast(Union[Unset, List[WorkflowFlowchart]], UNSET)

        workflow_flowchart_paginated_list = cls(
            next_token=next_token,
            workflow_flowcharts=workflow_flowcharts,
        )

        workflow_flowchart_paginated_list.additional_properties = d
        return workflow_flowchart_paginated_list

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def next_token(self) -> str:
        if isinstance(self._next_token, Unset):
            raise NotPresentError(self, "next_token")
        return self._next_token

    @next_token.setter
    def next_token(self, value: str) -> None:
        self._next_token = value

    @next_token.deleter
    def next_token(self) -> None:
        self._next_token = UNSET

    @property
    def workflow_flowcharts(self) -> List[WorkflowFlowchart]:
        if isinstance(self._workflow_flowcharts, Unset):
            raise NotPresentError(self, "workflow_flowcharts")
        return self._workflow_flowcharts

    @workflow_flowcharts.setter
    def workflow_flowcharts(self, value: List[WorkflowFlowchart]) -> None:
        self._workflow_flowcharts = value

    @workflow_flowcharts.deleter
    def workflow_flowcharts(self) -> None:
        self._workflow_flowcharts = UNSET
