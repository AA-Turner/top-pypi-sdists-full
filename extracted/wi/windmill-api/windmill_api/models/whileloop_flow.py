from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.whileloop_flow_type import WhileloopFlowType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.whileloop_flow_modules_item import WhileloopFlowModulesItem


T = TypeVar("T", bound="WhileloopFlow")


@_attrs_define
class WhileloopFlow:
    """
    Attributes:
        modules (List['WhileloopFlowModulesItem']):
        skip_failures (bool):
        type (WhileloopFlowType):
        parallel (Union[Unset, bool]):
        parallelism (Union[Unset, int]):
    """

    modules: List["WhileloopFlowModulesItem"]
    skip_failures: bool
    type: WhileloopFlowType
    parallel: Union[Unset, bool] = UNSET
    parallelism: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        modules = []
        for modules_item_data in self.modules:
            modules_item = modules_item_data.to_dict()

            modules.append(modules_item)

        skip_failures = self.skip_failures
        type = self.type.value

        parallel = self.parallel
        parallelism = self.parallelism

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "modules": modules,
                "skip_failures": skip_failures,
                "type": type,
            }
        )
        if parallel is not UNSET:
            field_dict["parallel"] = parallel
        if parallelism is not UNSET:
            field_dict["parallelism"] = parallelism

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.whileloop_flow_modules_item import WhileloopFlowModulesItem

        d = src_dict.copy()
        modules = []
        _modules = d.pop("modules")
        for modules_item_data in _modules:
            modules_item = WhileloopFlowModulesItem.from_dict(modules_item_data)

            modules.append(modules_item)

        skip_failures = d.pop("skip_failures")

        type = WhileloopFlowType(d.pop("type"))

        parallel = d.pop("parallel", UNSET)

        parallelism = d.pop("parallelism", UNSET)

        whileloop_flow = cls(
            modules=modules,
            skip_failures=skip_failures,
            type=type,
            parallel=parallel,
            parallelism=parallelism,
        )

        whileloop_flow.additional_properties = d
        return whileloop_flow

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
