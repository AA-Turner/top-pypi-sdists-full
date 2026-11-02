from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.ai_token_usage_event_provider import AITokenUsageEventProvider
from ..types import UNSET, Unset

T = TypeVar("T", bound="AITokenUsageEvent")


@_attrs_define
class AITokenUsageEvent:
    """
    Attributes:
        provider (AITokenUsageEventProvider):
        model (str):
        session_id (Union[Unset, str]):
        input_tokens (Union[Unset, int]):
        cache_read_tokens (Union[Unset, int]):
        cache_write_tokens (Union[Unset, int]):
        output_tokens (Union[Unset, int]):
        reported_cost_nano_usd (Union[Unset, int]): only set by providers that bill back an exact figure
        requests (Union[Unset, int]):
    """

    provider: AITokenUsageEventProvider
    model: str
    session_id: Union[Unset, str] = UNSET
    input_tokens: Union[Unset, int] = UNSET
    cache_read_tokens: Union[Unset, int] = UNSET
    cache_write_tokens: Union[Unset, int] = UNSET
    output_tokens: Union[Unset, int] = UNSET
    reported_cost_nano_usd: Union[Unset, int] = UNSET
    requests: Union[Unset, int] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        provider = self.provider.value

        model = self.model
        session_id = self.session_id
        input_tokens = self.input_tokens
        cache_read_tokens = self.cache_read_tokens
        cache_write_tokens = self.cache_write_tokens
        output_tokens = self.output_tokens
        reported_cost_nano_usd = self.reported_cost_nano_usd
        requests = self.requests

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "provider": provider,
                "model": model,
            }
        )
        if session_id is not UNSET:
            field_dict["session_id"] = session_id
        if input_tokens is not UNSET:
            field_dict["input_tokens"] = input_tokens
        if cache_read_tokens is not UNSET:
            field_dict["cache_read_tokens"] = cache_read_tokens
        if cache_write_tokens is not UNSET:
            field_dict["cache_write_tokens"] = cache_write_tokens
        if output_tokens is not UNSET:
            field_dict["output_tokens"] = output_tokens
        if reported_cost_nano_usd is not UNSET:
            field_dict["reported_cost_nano_usd"] = reported_cost_nano_usd
        if requests is not UNSET:
            field_dict["requests"] = requests

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        provider = AITokenUsageEventProvider(d.pop("provider"))

        model = d.pop("model")

        session_id = d.pop("session_id", UNSET)

        input_tokens = d.pop("input_tokens", UNSET)

        cache_read_tokens = d.pop("cache_read_tokens", UNSET)

        cache_write_tokens = d.pop("cache_write_tokens", UNSET)

        output_tokens = d.pop("output_tokens", UNSET)

        reported_cost_nano_usd = d.pop("reported_cost_nano_usd", UNSET)

        requests = d.pop("requests", UNSET)

        ai_token_usage_event = cls(
            provider=provider,
            model=model,
            session_id=session_id,
            input_tokens=input_tokens,
            cache_read_tokens=cache_read_tokens,
            cache_write_tokens=cache_write_tokens,
            output_tokens=output_tokens,
            reported_cost_nano_usd=reported_cost_nano_usd,
            requests=requests,
        )

        ai_token_usage_event.additional_properties = d
        return ai_token_usage_event

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
