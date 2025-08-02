from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.completed_job_raw_flow_modules_item_mock import CompletedJobRawFlowModulesItemMock
    from ..models.completed_job_raw_flow_modules_item_retry import CompletedJobRawFlowModulesItemRetry
    from ..models.completed_job_raw_flow_modules_item_skip_if import CompletedJobRawFlowModulesItemSkipIf
    from ..models.completed_job_raw_flow_modules_item_sleep_type_0 import CompletedJobRawFlowModulesItemSleepType0
    from ..models.completed_job_raw_flow_modules_item_sleep_type_1 import CompletedJobRawFlowModulesItemSleepType1
    from ..models.completed_job_raw_flow_modules_item_stop_after_all_iters_if import (
        CompletedJobRawFlowModulesItemStopAfterAllItersIf,
    )
    from ..models.completed_job_raw_flow_modules_item_stop_after_if import CompletedJobRawFlowModulesItemStopAfterIf
    from ..models.completed_job_raw_flow_modules_item_suspend import CompletedJobRawFlowModulesItemSuspend


T = TypeVar("T", bound="CompletedJobRawFlowModulesItem")


@_attrs_define
class CompletedJobRawFlowModulesItem:
    """
    Attributes:
        id (str):
        value (Any):
        stop_after_if (Union[Unset, CompletedJobRawFlowModulesItemStopAfterIf]):
        stop_after_all_iters_if (Union[Unset, CompletedJobRawFlowModulesItemStopAfterAllItersIf]):
        skip_if (Union[Unset, CompletedJobRawFlowModulesItemSkipIf]):
        sleep (Union['CompletedJobRawFlowModulesItemSleepType0', 'CompletedJobRawFlowModulesItemSleepType1', Unset]):
        cache_ttl (Union[Unset, float]):
        timeout (Union[Unset, float]):
        delete_after_use (Union[Unset, bool]):
        summary (Union[Unset, str]):
        mock (Union[Unset, CompletedJobRawFlowModulesItemMock]):
        suspend (Union[Unset, CompletedJobRawFlowModulesItemSuspend]):
        priority (Union[Unset, float]):
        continue_on_error (Union[Unset, bool]):
        retry (Union[Unset, CompletedJobRawFlowModulesItemRetry]):
    """

    id: str
    value: Any
    stop_after_if: Union[Unset, "CompletedJobRawFlowModulesItemStopAfterIf"] = UNSET
    stop_after_all_iters_if: Union[Unset, "CompletedJobRawFlowModulesItemStopAfterAllItersIf"] = UNSET
    skip_if: Union[Unset, "CompletedJobRawFlowModulesItemSkipIf"] = UNSET
    sleep: Union["CompletedJobRawFlowModulesItemSleepType0", "CompletedJobRawFlowModulesItemSleepType1", Unset] = UNSET
    cache_ttl: Union[Unset, float] = UNSET
    timeout: Union[Unset, float] = UNSET
    delete_after_use: Union[Unset, bool] = UNSET
    summary: Union[Unset, str] = UNSET
    mock: Union[Unset, "CompletedJobRawFlowModulesItemMock"] = UNSET
    suspend: Union[Unset, "CompletedJobRawFlowModulesItemSuspend"] = UNSET
    priority: Union[Unset, float] = UNSET
    continue_on_error: Union[Unset, bool] = UNSET
    retry: Union[Unset, "CompletedJobRawFlowModulesItemRetry"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.completed_job_raw_flow_modules_item_sleep_type_0 import CompletedJobRawFlowModulesItemSleepType0

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

        elif isinstance(self.sleep, CompletedJobRawFlowModulesItemSleepType0):
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
        from ..models.completed_job_raw_flow_modules_item_mock import CompletedJobRawFlowModulesItemMock
        from ..models.completed_job_raw_flow_modules_item_retry import CompletedJobRawFlowModulesItemRetry
        from ..models.completed_job_raw_flow_modules_item_skip_if import CompletedJobRawFlowModulesItemSkipIf
        from ..models.completed_job_raw_flow_modules_item_sleep_type_0 import CompletedJobRawFlowModulesItemSleepType0
        from ..models.completed_job_raw_flow_modules_item_sleep_type_1 import CompletedJobRawFlowModulesItemSleepType1
        from ..models.completed_job_raw_flow_modules_item_stop_after_all_iters_if import (
            CompletedJobRawFlowModulesItemStopAfterAllItersIf,
        )
        from ..models.completed_job_raw_flow_modules_item_stop_after_if import CompletedJobRawFlowModulesItemStopAfterIf
        from ..models.completed_job_raw_flow_modules_item_suspend import CompletedJobRawFlowModulesItemSuspend

        d = src_dict.copy()
        id = d.pop("id")

        value = d.pop("value")

        _stop_after_if = d.pop("stop_after_if", UNSET)
        stop_after_if: Union[Unset, CompletedJobRawFlowModulesItemStopAfterIf]
        if isinstance(_stop_after_if, Unset):
            stop_after_if = UNSET
        else:
            stop_after_if = CompletedJobRawFlowModulesItemStopAfterIf.from_dict(_stop_after_if)

        _stop_after_all_iters_if = d.pop("stop_after_all_iters_if", UNSET)
        stop_after_all_iters_if: Union[Unset, CompletedJobRawFlowModulesItemStopAfterAllItersIf]
        if isinstance(_stop_after_all_iters_if, Unset):
            stop_after_all_iters_if = UNSET
        else:
            stop_after_all_iters_if = CompletedJobRawFlowModulesItemStopAfterAllItersIf.from_dict(
                _stop_after_all_iters_if
            )

        _skip_if = d.pop("skip_if", UNSET)
        skip_if: Union[Unset, CompletedJobRawFlowModulesItemSkipIf]
        if isinstance(_skip_if, Unset):
            skip_if = UNSET
        else:
            skip_if = CompletedJobRawFlowModulesItemSkipIf.from_dict(_skip_if)

        def _parse_sleep(
            data: object,
        ) -> Union["CompletedJobRawFlowModulesItemSleepType0", "CompletedJobRawFlowModulesItemSleepType1", Unset]:
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _sleep_type_0 = data
                sleep_type_0: Union[Unset, CompletedJobRawFlowModulesItemSleepType0]
                if isinstance(_sleep_type_0, Unset):
                    sleep_type_0 = UNSET
                else:
                    sleep_type_0 = CompletedJobRawFlowModulesItemSleepType0.from_dict(_sleep_type_0)

                return sleep_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _sleep_type_1 = data
            sleep_type_1: Union[Unset, CompletedJobRawFlowModulesItemSleepType1]
            if isinstance(_sleep_type_1, Unset):
                sleep_type_1 = UNSET
            else:
                sleep_type_1 = CompletedJobRawFlowModulesItemSleepType1.from_dict(_sleep_type_1)

            return sleep_type_1

        sleep = _parse_sleep(d.pop("sleep", UNSET))

        cache_ttl = d.pop("cache_ttl", UNSET)

        timeout = d.pop("timeout", UNSET)

        delete_after_use = d.pop("delete_after_use", UNSET)

        summary = d.pop("summary", UNSET)

        _mock = d.pop("mock", UNSET)
        mock: Union[Unset, CompletedJobRawFlowModulesItemMock]
        if isinstance(_mock, Unset):
            mock = UNSET
        else:
            mock = CompletedJobRawFlowModulesItemMock.from_dict(_mock)

        _suspend = d.pop("suspend", UNSET)
        suspend: Union[Unset, CompletedJobRawFlowModulesItemSuspend]
        if isinstance(_suspend, Unset):
            suspend = UNSET
        else:
            suspend = CompletedJobRawFlowModulesItemSuspend.from_dict(_suspend)

        priority = d.pop("priority", UNSET)

        continue_on_error = d.pop("continue_on_error", UNSET)

        _retry = d.pop("retry", UNSET)
        retry: Union[Unset, CompletedJobRawFlowModulesItemRetry]
        if isinstance(_retry, Unset):
            retry = UNSET
        else:
            retry = CompletedJobRawFlowModulesItemRetry.from_dict(_retry)

        completed_job_raw_flow_modules_item = cls(
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

        completed_job_raw_flow_modules_item.additional_properties = d
        return completed_job_raw_flow_modules_item

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
