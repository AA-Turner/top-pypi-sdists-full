from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.whileloop_flow_type import WhileloopFlowType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.whileloop_flow_failure_threshold_type_0 import WhileloopFlowFailureThresholdType0
    from ..models.whileloop_flow_failure_threshold_type_1 import WhileloopFlowFailureThresholdType1
    from ..models.whileloop_flow_failure_threshold_type_2 import WhileloopFlowFailureThresholdType2
    from ..models.whileloop_flow_modules_item import WhileloopFlowModulesItem
    from ..models.whileloop_flow_parallelism_type_0 import WhileloopFlowParallelismType0
    from ..models.whileloop_flow_parallelism_type_1 import WhileloopFlowParallelismType1
    from ..models.whileloop_flow_parallelism_type_2 import WhileloopFlowParallelismType2


T = TypeVar("T", bound="WhileloopFlow")


@_attrs_define
class WhileloopFlow:
    """Executes nested modules repeatedly until stopped. The implicit iterator is the iteration counter, so
    'flow_input.iter.value' equals 'flow_input.iter.index' (0, 1, 2, ...) and never carries state. To carry state across
    iterations, a step reads its own previous-iteration result via 'results.<its_own_id>' with a first-iteration
    fallback - the loop's stop_after_if must then be on that inner step (a plain single-step body with stop_after_if on
    the loop module does not resolve 'results' across iterations and never terminates); plain counters can instead be
    derived from 'flow_input.iter.index', which works in every configuration. stop_after_if is evaluated after each
    iteration - on the loop module 'result' is the last iteration's result

        Attributes:
            modules (List['WhileloopFlowModulesItem']): Steps to execute in each iteration
            skip_failures (bool): If true, iteration failures don't stop the loop. Failed iterations return null
            type (WhileloopFlowType):
            parallel (Union[Unset, bool]): If true, iterations run concurrently (use with caution in while loops)
            parallelism (Union['WhileloopFlowParallelismType0', 'WhileloopFlowParallelismType1',
                'WhileloopFlowParallelismType2', Unset]): Maps input parameters for a step. Can be a static value or a
                JavaScript expression that references previous results or flow inputs
            squash (Union[Unset, bool]):
            max_iterations (Union[Unset, int]): Maximum number of iterations. Checked after each iteration; when reached and
                stop_after_if did not stop the loop, the loop fails with an error named 'LoopExhausted'
            max_duration_secs (Union[Unset, int]): Maximum wall-clock seconds since the first iteration started, checked
                after each iteration. A running iteration is not interrupted, so the loop can exceed the limit by up to one
                iteration; the timeout of the body's steps caps an iteration. When reached and stop_after_if did not stop the
                loop, the loop fails with an error named 'LoopExhausted'
            failure_threshold (Union['WhileloopFlowFailureThresholdType0', 'WhileloopFlowFailureThresholdType1',
                'WhileloopFlowFailureThresholdType2', Unset]): Maps input parameters for a step. Can be a static value or a
                JavaScript expression that references previous results or flow inputs
    """

    modules: List["WhileloopFlowModulesItem"]
    skip_failures: bool
    type: WhileloopFlowType
    parallel: Union[Unset, bool] = UNSET
    parallelism: Union[
        "WhileloopFlowParallelismType0", "WhileloopFlowParallelismType1", "WhileloopFlowParallelismType2", Unset
    ] = UNSET
    squash: Union[Unset, bool] = UNSET
    max_iterations: Union[Unset, int] = UNSET
    max_duration_secs: Union[Unset, int] = UNSET
    failure_threshold: Union[
        "WhileloopFlowFailureThresholdType0",
        "WhileloopFlowFailureThresholdType1",
        "WhileloopFlowFailureThresholdType2",
        Unset,
    ] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.whileloop_flow_failure_threshold_type_0 import WhileloopFlowFailureThresholdType0
        from ..models.whileloop_flow_failure_threshold_type_1 import WhileloopFlowFailureThresholdType1
        from ..models.whileloop_flow_parallelism_type_0 import WhileloopFlowParallelismType0
        from ..models.whileloop_flow_parallelism_type_1 import WhileloopFlowParallelismType1

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

        elif isinstance(self.parallelism, WhileloopFlowParallelismType1):
            parallelism = UNSET
            if not isinstance(self.parallelism, Unset):
                parallelism = self.parallelism.to_dict()

        else:
            parallelism = UNSET
            if not isinstance(self.parallelism, Unset):
                parallelism = self.parallelism.to_dict()

        squash = self.squash
        max_iterations = self.max_iterations
        max_duration_secs = self.max_duration_secs
        failure_threshold: Union[Dict[str, Any], Unset]
        if isinstance(self.failure_threshold, Unset):
            failure_threshold = UNSET

        elif isinstance(self.failure_threshold, WhileloopFlowFailureThresholdType0):
            failure_threshold = UNSET
            if not isinstance(self.failure_threshold, Unset):
                failure_threshold = self.failure_threshold.to_dict()

        elif isinstance(self.failure_threshold, WhileloopFlowFailureThresholdType1):
            failure_threshold = UNSET
            if not isinstance(self.failure_threshold, Unset):
                failure_threshold = self.failure_threshold.to_dict()

        else:
            failure_threshold = UNSET
            if not isinstance(self.failure_threshold, Unset):
                failure_threshold = self.failure_threshold.to_dict()

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
        if max_iterations is not UNSET:
            field_dict["max_iterations"] = max_iterations
        if max_duration_secs is not UNSET:
            field_dict["max_duration_secs"] = max_duration_secs
        if failure_threshold is not UNSET:
            field_dict["failure_threshold"] = failure_threshold

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.whileloop_flow_failure_threshold_type_0 import WhileloopFlowFailureThresholdType0
        from ..models.whileloop_flow_failure_threshold_type_1 import WhileloopFlowFailureThresholdType1
        from ..models.whileloop_flow_failure_threshold_type_2 import WhileloopFlowFailureThresholdType2
        from ..models.whileloop_flow_modules_item import WhileloopFlowModulesItem
        from ..models.whileloop_flow_parallelism_type_0 import WhileloopFlowParallelismType0
        from ..models.whileloop_flow_parallelism_type_1 import WhileloopFlowParallelismType1
        from ..models.whileloop_flow_parallelism_type_2 import WhileloopFlowParallelismType2

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
        ) -> Union[
            "WhileloopFlowParallelismType0", "WhileloopFlowParallelismType1", "WhileloopFlowParallelismType2", Unset
        ]:
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
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _parallelism_type_1 = data
                parallelism_type_1: Union[Unset, WhileloopFlowParallelismType1]
                if isinstance(_parallelism_type_1, Unset):
                    parallelism_type_1 = UNSET
                else:
                    parallelism_type_1 = WhileloopFlowParallelismType1.from_dict(_parallelism_type_1)

                return parallelism_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _parallelism_type_2 = data
            parallelism_type_2: Union[Unset, WhileloopFlowParallelismType2]
            if isinstance(_parallelism_type_2, Unset):
                parallelism_type_2 = UNSET
            else:
                parallelism_type_2 = WhileloopFlowParallelismType2.from_dict(_parallelism_type_2)

            return parallelism_type_2

        parallelism = _parse_parallelism(d.pop("parallelism", UNSET))

        squash = d.pop("squash", UNSET)

        max_iterations = d.pop("max_iterations", UNSET)

        max_duration_secs = d.pop("max_duration_secs", UNSET)

        def _parse_failure_threshold(
            data: object,
        ) -> Union[
            "WhileloopFlowFailureThresholdType0",
            "WhileloopFlowFailureThresholdType1",
            "WhileloopFlowFailureThresholdType2",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _failure_threshold_type_0 = data
                failure_threshold_type_0: Union[Unset, WhileloopFlowFailureThresholdType0]
                if isinstance(_failure_threshold_type_0, Unset):
                    failure_threshold_type_0 = UNSET
                else:
                    failure_threshold_type_0 = WhileloopFlowFailureThresholdType0.from_dict(_failure_threshold_type_0)

                return failure_threshold_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _failure_threshold_type_1 = data
                failure_threshold_type_1: Union[Unset, WhileloopFlowFailureThresholdType1]
                if isinstance(_failure_threshold_type_1, Unset):
                    failure_threshold_type_1 = UNSET
                else:
                    failure_threshold_type_1 = WhileloopFlowFailureThresholdType1.from_dict(_failure_threshold_type_1)

                return failure_threshold_type_1
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _failure_threshold_type_2 = data
            failure_threshold_type_2: Union[Unset, WhileloopFlowFailureThresholdType2]
            if isinstance(_failure_threshold_type_2, Unset):
                failure_threshold_type_2 = UNSET
            else:
                failure_threshold_type_2 = WhileloopFlowFailureThresholdType2.from_dict(_failure_threshold_type_2)

            return failure_threshold_type_2

        failure_threshold = _parse_failure_threshold(d.pop("failure_threshold", UNSET))

        whileloop_flow = cls(
            modules=modules,
            skip_failures=skip_failures,
            type=type,
            parallel=parallel,
            parallelism=parallelism,
            squash=squash,
            max_iterations=max_iterations,
            max_duration_secs=max_duration_secs,
            failure_threshold=failure_threshold,
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
