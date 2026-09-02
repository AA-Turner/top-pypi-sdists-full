from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="ListAiUsageResponse200BucketsItem")


@_attrs_define
class ListAiUsageResponse200BucketsItem:
    """
    Attributes:
        key (str): the grouped dimension's value; empty when grouping by model
        provider (str):
        model (str):
        input_tokens (int):
        cache_read_tokens (int):
        cache_write_tokens (int):
        output_tokens (int):
        requests (int):
        reported_cost_nano_usd (Union[Unset, int]):
    """

    key: str
    provider: str
    model: str
    input_tokens: int
    cache_read_tokens: int
    cache_write_tokens: int
    output_tokens: int
    requests: int
    reported_cost_nano_usd: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        key = self.key
        provider = self.provider
        model = self.model
        input_tokens = self.input_tokens
        cache_read_tokens = self.cache_read_tokens
        cache_write_tokens = self.cache_write_tokens
        output_tokens = self.output_tokens
        requests = self.requests
        reported_cost_nano_usd = self.reported_cost_nano_usd

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "key": key,
                "provider": provider,
                "model": model,
                "input_tokens": input_tokens,
                "cache_read_tokens": cache_read_tokens,
                "cache_write_tokens": cache_write_tokens,
                "output_tokens": output_tokens,
                "requests": requests,
            }
        )
        if reported_cost_nano_usd is not UNSET:
            field_dict["reported_cost_nano_usd"] = reported_cost_nano_usd

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        key = d.pop("key")

        provider = d.pop("provider")

        model = d.pop("model")

        input_tokens = d.pop("input_tokens")

        cache_read_tokens = d.pop("cache_read_tokens")

        cache_write_tokens = d.pop("cache_write_tokens")

        output_tokens = d.pop("output_tokens")

        requests = d.pop("requests")

        reported_cost_nano_usd = d.pop("reported_cost_nano_usd", UNSET)

        list_ai_usage_response_200_buckets_item = cls(
            key=key,
            provider=provider,
            model=model,
            input_tokens=input_tokens,
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
            output_tokens=output_tokens,
            requests=requests,
            reported_cost_nano_usd=reported_cost_nano_usd,
        )

        list_ai_usage_response_200_buckets_item.additional_properties = d
        return list_ai_usage_response_200_buckets_item

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
