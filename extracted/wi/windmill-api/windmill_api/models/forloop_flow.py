from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.forloop_flow_type import ForloopFlowType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.forloop_flow_iterator_type_0 import ForloopFlowIteratorType0
    from ..models.forloop_flow_iterator_type_1 import ForloopFlowIteratorType1
    from ..models.forloop_flow_modules_item import ForloopFlowModulesItem
    from ..models.forloop_flow_parallelism_type_0 import ForloopFlowParallelismType0
    from ..models.forloop_flow_parallelism_type_1 import ForloopFlowParallelismType1


T = TypeVar("T", bound="ForloopFlow")


@_attrs_define
class ForloopFlow:
    """Executes nested modules in a loop over an iterator. Inside the loop, use 'flow_input.iter.value' to access the
    current iteration value, and 'flow_input.iter.index' for the index. Supports parallel execution for better
    performance on I/O-bound operations

        Attributes:
            modules (List['ForloopFlowModulesItem']): Steps to execute for each iteration. These can reference the iteration
                value via 'flow_input.iter.value'
            iterator (Union['ForloopFlowIteratorType0', 'ForloopFlowIteratorType1']): Maps input parameters for a step. Can
                be a static value or a JavaScript expression that references previous results or flow inputs
            skip_failures (bool): If true, iteration failures don't stop the loop. Failed iterations return null
            type (ForloopFlowType):
            parallel (Union[Unset, bool]): If true, iterations run concurrently (faster for I/O-bound operations). Use with
                parallelism to control concurrency
            parallelism (Union['ForloopFlowParallelismType0', 'ForloopFlowParallelismType1', Unset]): Maps input parameters
                for a step. Can be a static value or a JavaScript expression that references previous results or flow inputs
            squash (Union[Unset, bool]):
    """

    modules: List["ForloopFlowModulesItem"]
    iterator: Union["ForloopFlowIteratorType0", "ForloopFlowIteratorType1"]
    skip_failures: bool
    type: ForloopFlowType
    parallel: Union[Unset, bool] = UNSET
    parallelism: Union["ForloopFlowParallelismType0", "ForloopFlowParallelismType1", Unset] = UNSET
    squash: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.forloop_flow_iterator_type_0 import ForloopFlowIteratorType0
        from ..models.forloop_flow_parallelism_type_0 import ForloopFlowParallelismType0

        modules = []
        for modules_item_data in self.modules:
            modules_item = modules_item_data.to_dict()

            modules.append(modules_item)

        iterator: Dict[str, Any]

        if isinstance(self.iterator, ForloopFlowIteratorType0):
            iterator = self.iterator.to_dict()

        else:
            iterator = self.iterator.to_dict()

        skip_failures = self.skip_failures
        type = self.type.value

        parallel = self.parallel
        parallelism: Union[Dict[str, Any], Unset]
        if isinstance(self.parallelism, Unset):
            parallelism = UNSET

        elif isinstance(self.parallelism, ForloopFlowParallelismType0):
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
                "iterator": iterator,
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
        from ..models.forloop_flow_iterator_type_0 import ForloopFlowIteratorType0
        from ..models.forloop_flow_iterator_type_1 import ForloopFlowIteratorType1
        from ..models.forloop_flow_modules_item import ForloopFlowModulesItem
        from ..models.forloop_flow_parallelism_type_0 import ForloopFlowParallelismType0
        from ..models.forloop_flow_parallelism_type_1 import ForloopFlowParallelismType1

        d = src_dict.copy()
        modules = []
        _modules = d.pop("modules")
        for modules_item_data in _modules:
            modules_item = ForloopFlowModulesItem.from_dict(modules_item_data)

            modules.append(modules_item)

        def _parse_iterator(data: object) -> Union["ForloopFlowIteratorType0", "ForloopFlowIteratorType1"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                iterator_type_0 = ForloopFlowIteratorType0.from_dict(data)

                return iterator_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            iterator_type_1 = ForloopFlowIteratorType1.from_dict(data)

            return iterator_type_1

        iterator = _parse_iterator(d.pop("iterator"))

        skip_failures = d.pop("skip_failures")

        type = ForloopFlowType(d.pop("type"))

        parallel = d.pop("parallel", UNSET)

        def _parse_parallelism(
            data: object,
        ) -> Union["ForloopFlowParallelismType0", "ForloopFlowParallelismType1", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _parallelism_type_0 = data
                parallelism_type_0: Union[Unset, ForloopFlowParallelismType0]
                if isinstance(_parallelism_type_0, Unset):
                    parallelism_type_0 = UNSET
                else:
                    parallelism_type_0 = ForloopFlowParallelismType0.from_dict(_parallelism_type_0)

                return parallelism_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _parallelism_type_1 = data
            parallelism_type_1: Union[Unset, ForloopFlowParallelismType1]
            if isinstance(_parallelism_type_1, Unset):
                parallelism_type_1 = UNSET
            else:
                parallelism_type_1 = ForloopFlowParallelismType1.from_dict(_parallelism_type_1)

            return parallelism_type_1

        parallelism = _parse_parallelism(d.pop("parallelism", UNSET))

        squash = d.pop("squash", UNSET)

        forloop_flow = cls(
            modules=modules,
            iterator=iterator,
            skip_failures=skip_failures,
            type=type,
            parallel=parallel,
            parallelism=parallelism,
            squash=squash,
        )

        forloop_flow.additional_properties = d
        return forloop_flow

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
