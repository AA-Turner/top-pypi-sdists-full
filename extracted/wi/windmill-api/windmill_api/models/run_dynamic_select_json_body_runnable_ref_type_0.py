from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.run_dynamic_select_json_body_runnable_ref_type_0_runnable_kind import (
    RunDynamicSelectJsonBodyRunnableRefType0RunnableKind,
)
from ..models.run_dynamic_select_json_body_runnable_ref_type_0_source import (
    RunDynamicSelectJsonBodyRunnableRefType0Source,
)

T = TypeVar("T", bound="RunDynamicSelectJsonBodyRunnableRefType0")


@_attrs_define
class RunDynamicSelectJsonBodyRunnableRefType0:
    """
    Attributes:
        source (RunDynamicSelectJsonBodyRunnableRefType0Source):
        path (str): Path to the deployed script or flow
        runnable_kind (RunDynamicSelectJsonBodyRunnableRefType0RunnableKind):
    """

    source: RunDynamicSelectJsonBodyRunnableRefType0Source
    path: str
    runnable_kind: RunDynamicSelectJsonBodyRunnableRefType0RunnableKind
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        source = self.source.value

        path = self.path
        runnable_kind = self.runnable_kind.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "source": source,
                "path": path,
                "runnable_kind": runnable_kind,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        source = RunDynamicSelectJsonBodyRunnableRefType0Source(d.pop("source"))

        path = d.pop("path")

        runnable_kind = RunDynamicSelectJsonBodyRunnableRefType0RunnableKind(d.pop("runnable_kind"))

        run_dynamic_select_json_body_runnable_ref_type_0 = cls(
            source=source,
            path=path,
            runnable_kind=runnable_kind,
        )

        run_dynamic_select_json_body_runnable_ref_type_0.additional_properties = d
        return run_dynamic_select_json_body_runnable_ref_type_0

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
