from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_suspended_job_flow_response_200_job_type_1_raw_flow_failure_module import (
        GetSuspendedJobFlowResponse200JobType1RawFlowFailureModule,
    )
    from ..models.get_suspended_job_flow_response_200_job_type_1_raw_flow_flow_env import (
        GetSuspendedJobFlowResponse200JobType1RawFlowFlowEnv,
    )
    from ..models.get_suspended_job_flow_response_200_job_type_1_raw_flow_modules_item import (
        GetSuspendedJobFlowResponse200JobType1RawFlowModulesItem,
    )
    from ..models.get_suspended_job_flow_response_200_job_type_1_raw_flow_notes_item import (
        GetSuspendedJobFlowResponse200JobType1RawFlowNotesItem,
    )
    from ..models.get_suspended_job_flow_response_200_job_type_1_raw_flow_preprocessor_module import (
        GetSuspendedJobFlowResponse200JobType1RawFlowPreprocessorModule,
    )


T = TypeVar("T", bound="GetSuspendedJobFlowResponse200JobType1RawFlow")


@_attrs_define
class GetSuspendedJobFlowResponse200JobType1RawFlow:
    """The flow structure containing modules and optional preprocessor/failure handlers

    Attributes:
        modules (List['GetSuspendedJobFlowResponse200JobType1RawFlowModulesItem']): Array of steps that execute in
            sequence. Each step can be a script, subflow, loop, or branch
        failure_module (Union[Unset, GetSuspendedJobFlowResponse200JobType1RawFlowFailureModule]): A single step in a
            flow. Can be a script, subflow, loop, or branch
        preprocessor_module (Union[Unset, GetSuspendedJobFlowResponse200JobType1RawFlowPreprocessorModule]): A single
            step in a flow. Can be a script, subflow, loop, or branch
        same_worker (Union[Unset, bool]): If true, all steps run on the same worker for better performance
        concurrent_limit (Union[Unset, float]): Maximum number of concurrent executions of this flow
        concurrency_key (Union[Unset, str]): Expression to group concurrent executions (e.g., by user ID)
        concurrency_time_window_s (Union[Unset, float]): Time window in seconds for concurrent_limit
        debounce_delay_s (Union[Unset, float]): Delay in seconds to debounce flow executions
        debounce_key (Union[Unset, str]): Expression to group debounced executions
        debounce_args_to_accumulate (Union[Unset, List[str]]): Arguments to accumulate across debounced executions
        max_total_debouncing_time (Union[Unset, float]): Maximum total time in seconds that a job can be debounced
        max_total_debounces_amount (Union[Unset, float]): Maximum number of times a job can be debounced
        skip_expr (Union[Unset, str]): JavaScript expression to conditionally skip the entire flow
        cache_ttl (Union[Unset, float]): Cache duration in seconds for flow results
        cache_ignore_s3_path (Union[Unset, bool]):
        flow_env (Union[Unset, GetSuspendedJobFlowResponse200JobType1RawFlowFlowEnv]): Environment variables available
            to all steps
        priority (Union[Unset, float]): Execution priority (higher numbers run first)
        early_return (Union[Unset, str]): JavaScript expression to return early from the flow
        chat_input_enabled (Union[Unset, bool]): Whether this flow accepts chat-style input
        notes (Union[Unset, List['GetSuspendedJobFlowResponse200JobType1RawFlowNotesItem']]): Sticky notes attached to
            the flow
    """

    modules: List["GetSuspendedJobFlowResponse200JobType1RawFlowModulesItem"]
    failure_module: Union[Unset, "GetSuspendedJobFlowResponse200JobType1RawFlowFailureModule"] = UNSET
    preprocessor_module: Union[Unset, "GetSuspendedJobFlowResponse200JobType1RawFlowPreprocessorModule"] = UNSET
    same_worker: Union[Unset, bool] = UNSET
    concurrent_limit: Union[Unset, float] = UNSET
    concurrency_key: Union[Unset, str] = UNSET
    concurrency_time_window_s: Union[Unset, float] = UNSET
    debounce_delay_s: Union[Unset, float] = UNSET
    debounce_key: Union[Unset, str] = UNSET
    debounce_args_to_accumulate: Union[Unset, List[str]] = UNSET
    max_total_debouncing_time: Union[Unset, float] = UNSET
    max_total_debounces_amount: Union[Unset, float] = UNSET
    skip_expr: Union[Unset, str] = UNSET
    cache_ttl: Union[Unset, float] = UNSET
    cache_ignore_s3_path: Union[Unset, bool] = UNSET
    flow_env: Union[Unset, "GetSuspendedJobFlowResponse200JobType1RawFlowFlowEnv"] = UNSET
    priority: Union[Unset, float] = UNSET
    early_return: Union[Unset, str] = UNSET
    chat_input_enabled: Union[Unset, bool] = UNSET
    notes: Union[Unset, List["GetSuspendedJobFlowResponse200JobType1RawFlowNotesItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        modules = []
        for modules_item_data in self.modules:
            modules_item = modules_item_data.to_dict()

            modules.append(modules_item)

        failure_module: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.failure_module, Unset):
            failure_module = self.failure_module.to_dict()

        preprocessor_module: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.preprocessor_module, Unset):
            preprocessor_module = self.preprocessor_module.to_dict()

        same_worker = self.same_worker
        concurrent_limit = self.concurrent_limit
        concurrency_key = self.concurrency_key
        concurrency_time_window_s = self.concurrency_time_window_s
        debounce_delay_s = self.debounce_delay_s
        debounce_key = self.debounce_key
        debounce_args_to_accumulate: Union[Unset, List[str]] = UNSET
        if not isinstance(self.debounce_args_to_accumulate, Unset):
            debounce_args_to_accumulate = self.debounce_args_to_accumulate

        max_total_debouncing_time = self.max_total_debouncing_time
        max_total_debounces_amount = self.max_total_debounces_amount
        skip_expr = self.skip_expr
        cache_ttl = self.cache_ttl
        cache_ignore_s3_path = self.cache_ignore_s3_path
        flow_env: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.flow_env, Unset):
            flow_env = self.flow_env.to_dict()

        priority = self.priority
        early_return = self.early_return
        chat_input_enabled = self.chat_input_enabled
        notes: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.notes, Unset):
            notes = []
            for notes_item_data in self.notes:
                notes_item = notes_item_data.to_dict()

                notes.append(notes_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "modules": modules,
            }
        )
        if failure_module is not UNSET:
            field_dict["failure_module"] = failure_module
        if preprocessor_module is not UNSET:
            field_dict["preprocessor_module"] = preprocessor_module
        if same_worker is not UNSET:
            field_dict["same_worker"] = same_worker
        if concurrent_limit is not UNSET:
            field_dict["concurrent_limit"] = concurrent_limit
        if concurrency_key is not UNSET:
            field_dict["concurrency_key"] = concurrency_key
        if concurrency_time_window_s is not UNSET:
            field_dict["concurrency_time_window_s"] = concurrency_time_window_s
        if debounce_delay_s is not UNSET:
            field_dict["debounce_delay_s"] = debounce_delay_s
        if debounce_key is not UNSET:
            field_dict["debounce_key"] = debounce_key
        if debounce_args_to_accumulate is not UNSET:
            field_dict["debounce_args_to_accumulate"] = debounce_args_to_accumulate
        if max_total_debouncing_time is not UNSET:
            field_dict["max_total_debouncing_time"] = max_total_debouncing_time
        if max_total_debounces_amount is not UNSET:
            field_dict["max_total_debounces_amount"] = max_total_debounces_amount
        if skip_expr is not UNSET:
            field_dict["skip_expr"] = skip_expr
        if cache_ttl is not UNSET:
            field_dict["cache_ttl"] = cache_ttl
        if cache_ignore_s3_path is not UNSET:
            field_dict["cache_ignore_s3_path"] = cache_ignore_s3_path
        if flow_env is not UNSET:
            field_dict["flow_env"] = flow_env
        if priority is not UNSET:
            field_dict["priority"] = priority
        if early_return is not UNSET:
            field_dict["early_return"] = early_return
        if chat_input_enabled is not UNSET:
            field_dict["chat_input_enabled"] = chat_input_enabled
        if notes is not UNSET:
            field_dict["notes"] = notes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_suspended_job_flow_response_200_job_type_1_raw_flow_failure_module import (
            GetSuspendedJobFlowResponse200JobType1RawFlowFailureModule,
        )
        from ..models.get_suspended_job_flow_response_200_job_type_1_raw_flow_flow_env import (
            GetSuspendedJobFlowResponse200JobType1RawFlowFlowEnv,
        )
        from ..models.get_suspended_job_flow_response_200_job_type_1_raw_flow_modules_item import (
            GetSuspendedJobFlowResponse200JobType1RawFlowModulesItem,
        )
        from ..models.get_suspended_job_flow_response_200_job_type_1_raw_flow_notes_item import (
            GetSuspendedJobFlowResponse200JobType1RawFlowNotesItem,
        )
        from ..models.get_suspended_job_flow_response_200_job_type_1_raw_flow_preprocessor_module import (
            GetSuspendedJobFlowResponse200JobType1RawFlowPreprocessorModule,
        )

        d = src_dict.copy()
        modules = []
        _modules = d.pop("modules")
        for modules_item_data in _modules:
            modules_item = GetSuspendedJobFlowResponse200JobType1RawFlowModulesItem.from_dict(modules_item_data)

            modules.append(modules_item)

        _failure_module = d.pop("failure_module", UNSET)
        failure_module: Union[Unset, GetSuspendedJobFlowResponse200JobType1RawFlowFailureModule]
        if isinstance(_failure_module, Unset):
            failure_module = UNSET
        else:
            failure_module = GetSuspendedJobFlowResponse200JobType1RawFlowFailureModule.from_dict(_failure_module)

        _preprocessor_module = d.pop("preprocessor_module", UNSET)
        preprocessor_module: Union[Unset, GetSuspendedJobFlowResponse200JobType1RawFlowPreprocessorModule]
        if isinstance(_preprocessor_module, Unset):
            preprocessor_module = UNSET
        else:
            preprocessor_module = GetSuspendedJobFlowResponse200JobType1RawFlowPreprocessorModule.from_dict(
                _preprocessor_module
            )

        same_worker = d.pop("same_worker", UNSET)

        concurrent_limit = d.pop("concurrent_limit", UNSET)

        concurrency_key = d.pop("concurrency_key", UNSET)

        concurrency_time_window_s = d.pop("concurrency_time_window_s", UNSET)

        debounce_delay_s = d.pop("debounce_delay_s", UNSET)

        debounce_key = d.pop("debounce_key", UNSET)

        debounce_args_to_accumulate = cast(List[str], d.pop("debounce_args_to_accumulate", UNSET))

        max_total_debouncing_time = d.pop("max_total_debouncing_time", UNSET)

        max_total_debounces_amount = d.pop("max_total_debounces_amount", UNSET)

        skip_expr = d.pop("skip_expr", UNSET)

        cache_ttl = d.pop("cache_ttl", UNSET)

        cache_ignore_s3_path = d.pop("cache_ignore_s3_path", UNSET)

        _flow_env = d.pop("flow_env", UNSET)
        flow_env: Union[Unset, GetSuspendedJobFlowResponse200JobType1RawFlowFlowEnv]
        if isinstance(_flow_env, Unset):
            flow_env = UNSET
        else:
            flow_env = GetSuspendedJobFlowResponse200JobType1RawFlowFlowEnv.from_dict(_flow_env)

        priority = d.pop("priority", UNSET)

        early_return = d.pop("early_return", UNSET)

        chat_input_enabled = d.pop("chat_input_enabled", UNSET)

        notes = []
        _notes = d.pop("notes", UNSET)
        for notes_item_data in _notes or []:
            notes_item = GetSuspendedJobFlowResponse200JobType1RawFlowNotesItem.from_dict(notes_item_data)

            notes.append(notes_item)

        get_suspended_job_flow_response_200_job_type_1_raw_flow = cls(
            modules=modules,
            failure_module=failure_module,
            preprocessor_module=preprocessor_module,
            same_worker=same_worker,
            concurrent_limit=concurrent_limit,
            concurrency_key=concurrency_key,
            concurrency_time_window_s=concurrency_time_window_s,
            debounce_delay_s=debounce_delay_s,
            debounce_key=debounce_key,
            debounce_args_to_accumulate=debounce_args_to_accumulate,
            max_total_debouncing_time=max_total_debouncing_time,
            max_total_debounces_amount=max_total_debounces_amount,
            skip_expr=skip_expr,
            cache_ttl=cache_ttl,
            cache_ignore_s3_path=cache_ignore_s3_path,
            flow_env=flow_env,
            priority=priority,
            early_return=early_return,
            chat_input_enabled=chat_input_enabled,
            notes=notes,
        )

        get_suspended_job_flow_response_200_job_type_1_raw_flow.additional_properties = d
        return get_suspended_job_flow_response_200_job_type_1_raw_flow

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
