from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.whileloop_flow_type import WhileloopFlowType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.whileloop_flow_modules_item import WhileloopFlowModulesItem
    from ..models.whileloop_flow_parallelism_type_0 import WhileloopFlowParallelismType0
    from ..models.whileloop_flow_parallelism_type_1 import WhileloopFlowParallelismType1


T = TypeVar("T", bound="WhileloopFlow")


@_attrs_define
class WhileloopFlow:
    """Executes nested modules repeatedly while a condition is true. The loop checks the condition after each iteration.
    Use stop_after_if on modules to control loop termination

        Attributes:
            modules (List['WhileloopFlowModulesItem']): Steps to execute in each iteration. Use stop_after_if to control
                when the loop ends
            skip_failures (bool): If true, iteration failures don't stop the loop. Failed iterations return null
            type (WhileloopFlowType):
            parallel (Union[Unset, bool]): If true, iterations run concurrently (use with caution in while loops)
            parallelism (Union['WhileloopFlowParallelismType0', 'WhileloopFlowParallelismType1', Unset]): Maps input
                parameters for a step. Can be a static value or a JavaScript expression that references previous results or flow
                inputs
            squash (Union[Unset, bool]):
    """

    modules: List["WhileloopFlowModulesItem"]
    skip_failures: bool
    type: WhileloopFlowType
    parallel: Union[Unset, bool] = UNSET
    parallelism: Union["WhileloopFlowParallelismType0", "WhileloopFlowParallelismType1", Unset] = UNSET
    squash: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.whileloop_flow_parallelism_type_0 import WhileloopFlowParallelismType0

        modules = []
        for modules_item_data in self.modules:
            modules_item = modules_item_data.to_dict()

            modules.append(modules_item)

        skip_failures = self.skip_failures
        type = self.type.value

        parallel = self.parallel
        parallelism: Union[Dict[str, Any], Unset]
        if isinstance(self.parallelism, Unset):
            parallelism = UNSET

        elif isinstance(self.parallelism, WhileloopFlowParallelismType0):
            parallelism = UNSET
            if not isinstance(self.parallelism, Unset):
                parallelism = self.parallelism.to_dict()

        else:
            parallelism = UNSET
            if not isinstance(self.parallelism, Unset):
                parallelism = self.parallelism.to_dict()

        squash = self.squash

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
        if squash is not UNSET:
            field_dict["squash"] = squash

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.whileloop_flow_modules_item import WhileloopFlowModulesItem
        from ..models.whileloop_flow_parallelism_type_0 import WhileloopFlowParallelismType0
        from ..models.whileloop_flow_parallelism_type_1 import WhileloopFlowParallelismType1

        d = src_dict.copy()
        modules = []
        _modules = d.pop("modules")
        for modules_item_data in _modules:
            modules_item = WhileloopFlowModulesItem.from_dict(modules_item_data)

            modules.append(modules_item)

        skip_failures = d.pop("skip_failures")

        type = WhileloopFlowType(d.pop("type"))

        parallel = d.pop("parallel", UNSET)

        def _parse_parallelism(
            data: object,
        ) -> Union["WhileloopFlowParallelismType0", "WhileloopFlowParallelismType1", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _parallelism_type_0 = data
                parallelism_type_0: Union[Unset, WhileloopFlowParallelismType0]
                if isinstance(_parallelism_type_0, Unset):
                    parallelism_type_0 = UNSET
                else:
                    parallelism_type_0 = WhileloopFlowParallelismType0.from_dict(_parallelism_type_0)

                return parallelism_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _parallelism_type_1 = data
            parallelism_type_1: Union[Unset, WhileloopFlowParallelismType1]
            if isinstance(_parallelism_type_1, Unset):
                parallelism_type_1 = UNSET
            else:
                parallelism_type_1 = WhileloopFlowParallelismType1.from_dict(_parallelism_type_1)

            return parallelism_type_1

        parallelism = _parse_parallelism(d.pop("parallelism", UNSET))

        squash = d.pop("squash", UNSET)

        whileloop_flow = cls(
            modules=modules,
            skip_failures=skip_failures,
            type=type,
            parallel=parallel,
            parallelism=parallelism,
            squash=squash,
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
