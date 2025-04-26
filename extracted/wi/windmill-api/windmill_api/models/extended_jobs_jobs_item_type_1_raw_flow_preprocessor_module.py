from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_mock import (
        ExtendedJobsJobsItemType1RawFlowPreprocessorModuleMock,
    )
    from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_retry import (
        ExtendedJobsJobsItemType1RawFlowPreprocessorModuleRetry,
    )
    from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_skip_if import (
        ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSkipIf,
    )
    from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_sleep_type_0 import (
        ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType0,
    )
    from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_sleep_type_1 import (
        ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType1,
    )
    from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_stop_after_all_iters_if import (
        ExtendedJobsJobsItemType1RawFlowPreprocessorModuleStopAfterAllItersIf,
    )
    from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_stop_after_if import (
        ExtendedJobsJobsItemType1RawFlowPreprocessorModuleStopAfterIf,
    )
    from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_suspend import (
        ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSuspend,
    )


T = TypeVar("T", bound="ExtendedJobsJobsItemType1RawFlowPreprocessorModule")


@_attrs_define
class ExtendedJobsJobsItemType1RawFlowPreprocessorModule:
    """
    Attributes:
        id (str):
        value (Any):
        stop_after_if (Union[Unset, ExtendedJobsJobsItemType1RawFlowPreprocessorModuleStopAfterIf]):
        stop_after_all_iters_if (Union[Unset, ExtendedJobsJobsItemType1RawFlowPreprocessorModuleStopAfterAllItersIf]):
        skip_if (Union[Unset, ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSkipIf]):
        sleep (Union['ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType0',
            'ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType1', Unset]):
        cache_ttl (Union[Unset, float]):
        timeout (Union[Unset, float]):
        delete_after_use (Union[Unset, bool]):
        summary (Union[Unset, str]):
        mock (Union[Unset, ExtendedJobsJobsItemType1RawFlowPreprocessorModuleMock]):
        suspend (Union[Unset, ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSuspend]):
        priority (Union[Unset, float]):
        continue_on_error (Union[Unset, bool]):
        retry (Union[Unset, ExtendedJobsJobsItemType1RawFlowPreprocessorModuleRetry]):
    """

    id: str
    value: Any
    stop_after_if: Union[Unset, "ExtendedJobsJobsItemType1RawFlowPreprocessorModuleStopAfterIf"] = UNSET
    stop_after_all_iters_if: Union[
        Unset, "ExtendedJobsJobsItemType1RawFlowPreprocessorModuleStopAfterAllItersIf"
    ] = UNSET
    skip_if: Union[Unset, "ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSkipIf"] = UNSET
    sleep: Union[
        "ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType0",
        "ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType1",
        Unset,
    ] = UNSET
    cache_ttl: Union[Unset, float] = UNSET
    timeout: Union[Unset, float] = UNSET
    delete_after_use: Union[Unset, bool] = UNSET
    summary: Union[Unset, str] = UNSET
    mock: Union[Unset, "ExtendedJobsJobsItemType1RawFlowPreprocessorModuleMock"] = UNSET
    suspend: Union[Unset, "ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSuspend"] = UNSET
    priority: Union[Unset, float] = UNSET
    continue_on_error: Union[Unset, bool] = UNSET
    retry: Union[Unset, "ExtendedJobsJobsItemType1RawFlowPreprocessorModuleRetry"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_sleep_type_0 import (
            ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType0,
        )

        id = self.id
        value = self.value
        stop_after_if: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_after_if, Unset):
            stop_after_if = self.stop_after_if.to_dict()

        stop_after_all_iters_if: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.stop_after_all_iters_if, Unset):
            stop_after_all_iters_if = self.stop_after_all_iters_if.to_dict()

        skip_if: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.skip_if, Unset):
            skip_if = self.skip_if.to_dict()

        sleep: Union[Dict[str, Any], Unset]
        if isinstance(self.sleep, Unset):
            sleep = UNSET

        elif isinstance(self.sleep, ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType0):
            sleep = UNSET
            if not isinstance(self.sleep, Unset):
                sleep = self.sleep.to_dict()

        else:
            sleep = UNSET
            if not isinstance(self.sleep, Unset):
                sleep = self.sleep.to_dict()

        cache_ttl = self.cache_ttl
        timeout = self.timeout
        delete_after_use = self.delete_after_use
        summary = self.summary
        mock: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.mock, Unset):
            mock = self.mock.to_dict()

        suspend: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.suspend, Unset):
            suspend = self.suspend.to_dict()

        priority = self.priority
        continue_on_error = self.continue_on_error
        retry: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.retry, Unset):
            retry = self.retry.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "value": value,
            }
        )
        if stop_after_if is not UNSET:
            field_dict["stop_after_if"] = stop_after_if
        if stop_after_all_iters_if is not UNSET:
            field_dict["stop_after_all_iters_if"] = stop_after_all_iters_if
        if skip_if is not UNSET:
            field_dict["skip_if"] = skip_if
        if sleep is not UNSET:
            field_dict["sleep"] = sleep
        if cache_ttl is not UNSET:
            field_dict["cache_ttl"] = cache_ttl
        if timeout is not UNSET:
            field_dict["timeout"] = timeout
        if delete_after_use is not UNSET:
            field_dict["delete_after_use"] = delete_after_use
        if summary is not UNSET:
            field_dict["summary"] = summary
        if mock is not UNSET:
            field_dict["mock"] = mock
        if suspend is not UNSET:
            field_dict["suspend"] = suspend
        if priority is not UNSET:
            field_dict["priority"] = priority
        if continue_on_error is not UNSET:
            field_dict["continue_on_error"] = continue_on_error
        if retry is not UNSET:
            field_dict["retry"] = retry

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_mock import (
            ExtendedJobsJobsItemType1RawFlowPreprocessorModuleMock,
        )
        from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_retry import (
            ExtendedJobsJobsItemType1RawFlowPreprocessorModuleRetry,
        )
        from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_skip_if import (
            ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSkipIf,
        )
        from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_sleep_type_0 import (
            ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType0,
        )
        from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_sleep_type_1 import (
            ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType1,
        )
        from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_stop_after_all_iters_if import (
            ExtendedJobsJobsItemType1RawFlowPreprocessorModuleStopAfterAllItersIf,
        )
        from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_stop_after_if import (
            ExtendedJobsJobsItemType1RawFlowPreprocessorModuleStopAfterIf,
        )
        from ..models.extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module_suspend import (
            ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSuspend,
        )

        d = src_dict.copy()
        id = d.pop("id")

        value = d.pop("value")

        _stop_after_if = d.pop("stop_after_if", UNSET)
        stop_after_if: Union[Unset, ExtendedJobsJobsItemType1RawFlowPreprocessorModuleStopAfterIf]
        if isinstance(_stop_after_if, Unset):
            stop_after_if = UNSET
        else:
            stop_after_if = ExtendedJobsJobsItemType1RawFlowPreprocessorModuleStopAfterIf.from_dict(_stop_after_if)

        _stop_after_all_iters_if = d.pop("stop_after_all_iters_if", UNSET)
        stop_after_all_iters_if: Union[Unset, ExtendedJobsJobsItemType1RawFlowPreprocessorModuleStopAfterAllItersIf]
        if isinstance(_stop_after_all_iters_if, Unset):
            stop_after_all_iters_if = UNSET
        else:
            stop_after_all_iters_if = ExtendedJobsJobsItemType1RawFlowPreprocessorModuleStopAfterAllItersIf.from_dict(
                _stop_after_all_iters_if
            )

        _skip_if = d.pop("skip_if", UNSET)
        skip_if: Union[Unset, ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSkipIf]
        if isinstance(_skip_if, Unset):
            skip_if = UNSET
        else:
            skip_if = ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSkipIf.from_dict(_skip_if)

        def _parse_sleep(
            data: object,
        ) -> Union[
            "ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType0",
            "ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType1",
            Unset,
        ]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _sleep_type_0 = data
                sleep_type_0: Union[Unset, ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType0]
                if isinstance(_sleep_type_0, Unset):
                    sleep_type_0 = UNSET
                else:
                    sleep_type_0 = ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType0.from_dict(_sleep_type_0)

                return sleep_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _sleep_type_1 = data
            sleep_type_1: Union[Unset, ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType1]
            if isinstance(_sleep_type_1, Unset):
                sleep_type_1 = UNSET
            else:
                sleep_type_1 = ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSleepType1.from_dict(_sleep_type_1)

            return sleep_type_1

        sleep = _parse_sleep(d.pop("sleep", UNSET))

        cache_ttl = d.pop("cache_ttl", UNSET)

        timeout = d.pop("timeout", UNSET)

        delete_after_use = d.pop("delete_after_use", UNSET)

        summary = d.pop("summary", UNSET)

        _mock = d.pop("mock", UNSET)
        mock: Union[Unset, ExtendedJobsJobsItemType1RawFlowPreprocessorModuleMock]
        if isinstance(_mock, Unset):
            mock = UNSET
        else:
            mock = ExtendedJobsJobsItemType1RawFlowPreprocessorModuleMock.from_dict(_mock)

        _suspend = d.pop("suspend", UNSET)
        suspend: Union[Unset, ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSuspend]
        if isinstance(_suspend, Unset):
            suspend = UNSET
        else:
            suspend = ExtendedJobsJobsItemType1RawFlowPreprocessorModuleSuspend.from_dict(_suspend)

        priority = d.pop("priority", UNSET)

        continue_on_error = d.pop("continue_on_error", UNSET)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, ExtendedJobsJobsItemType1RawFlowPreprocessorModuleRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = ExtendedJobsJobsItemType1RawFlowPreprocessorModuleRetry.from_dict(_retry)

        extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module = cls(
            id=id,
            value=value,
            stop_after_if=stop_after_if,
            stop_after_all_iters_if=stop_after_all_iters_if,
            skip_if=skip_if,
            sleep=sleep,
            cache_ttl=cache_ttl,
            timeout=timeout,
            delete_after_use=delete_after_use,
            summary=summary,
            mock=mock,
            suspend=suspend,
            priority=priority,
            continue_on_error=continue_on_error,
            retry=retry,
        )

        extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module.additional_properties = d
        return extended_jobs_jobs_item_type_1_raw_flow_preprocessor_module

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
