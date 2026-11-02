from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.token_saving_method import TokenSavingMethod


T = TypeVar("T", bound="TokenSavingEvent")


@_attrs_define
class TokenSavingEvent:
    """
    Attributes:
        id (str):
        event_id (str):
        runtime_id (str):
        observed_at_unix_millis (int):
        provider (None | str):
        transport (None | str):
        endpoint (None | str):
        model (None | str):
        wire_bytes_before (int):
        wire_bytes_after (int):
        saved_wire_bytes (int):
        estimated_tokens_before (int):
        estimated_tokens_after (int):
        saved_estimated_tokens (int):
        elapsed_micros (int):
        methods (list[TokenSavingMethod]):
        parse_error (None | str):
        analyzer_version (int):
    """

    id: str
    event_id: str
    runtime_id: str
    observed_at_unix_millis: int
    provider: None | str
    transport: None | str
    endpoint: None | str
    model: None | str
    wire_bytes_before: int
    wire_bytes_after: int
    saved_wire_bytes: int
    estimated_tokens_before: int
    estimated_tokens_after: int
    saved_estimated_tokens: int
    elapsed_micros: int
    methods: list[TokenSavingMethod]
    parse_error: None | str
    analyzer_version: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        event_id = self.event_id

        runtime_id = self.runtime_id

        observed_at_unix_millis = self.observed_at_unix_millis

        provider: None | str
        provider = self.provider

        transport: None | str
        transport = self.transport

        endpoint: None | str
        endpoint = self.endpoint

        model: None | str
        model = self.model

        wire_bytes_before = self.wire_bytes_before

        wire_bytes_after = self.wire_bytes_after

        saved_wire_bytes = self.saved_wire_bytes

        estimated_tokens_before = self.estimated_tokens_before

        estimated_tokens_after = self.estimated_tokens_after

        saved_estimated_tokens = self.saved_estimated_tokens

        elapsed_micros = self.elapsed_micros

        methods = []
        for methods_item_data in self.methods:
            methods_item = methods_item_data.to_dict()
            methods.append(methods_item)

        parse_error: None | str
        parse_error = self.parse_error

        analyzer_version = self.analyzer_version

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "event_id": event_id,
                "runtime_id": runtime_id,
                "observed_at_unix_millis": observed_at_unix_millis,
                "provider": provider,
                "transport": transport,
                "endpoint": endpoint,
                "model": model,
                "wire_bytes_before": wire_bytes_before,
                "wire_bytes_after": wire_bytes_after,
                "saved_wire_bytes": saved_wire_bytes,
                "estimated_tokens_before": estimated_tokens_before,
                "estimated_tokens_after": estimated_tokens_after,
                "saved_estimated_tokens": saved_estimated_tokens,
                "elapsed_micros": elapsed_micros,
                "methods": methods,
                "parse_error": parse_error,
                "analyzer_version": analyzer_version,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.token_saving_method import TokenSavingMethod

        d = dict(src_dict)
        id = d.pop("id")

        event_id = d.pop("event_id")

        runtime_id = d.pop("runtime_id")

        observed_at_unix_millis = d.pop("observed_at_unix_millis")

        def _parse_provider(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        provider = _parse_provider(d.pop("provider"))

        def _parse_transport(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        transport = _parse_transport(d.pop("transport"))

        def _parse_endpoint(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        endpoint = _parse_endpoint(d.pop("endpoint"))

        def _parse_model(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        model = _parse_model(d.pop("model"))

        wire_bytes_before = d.pop("wire_bytes_before")

        wire_bytes_after = d.pop("wire_bytes_after")

        saved_wire_bytes = d.pop("saved_wire_bytes")

        estimated_tokens_before = d.pop("estimated_tokens_before")

        estimated_tokens_after = d.pop("estimated_tokens_after")

        saved_estimated_tokens = d.pop("saved_estimated_tokens")

        elapsed_micros = d.pop("elapsed_micros")

        methods = []
        _methods = d.pop("methods")
        for methods_item_data in _methods:
            methods_item = TokenSavingMethod.from_dict(methods_item_data)

            methods.append(methods_item)

        def _parse_parse_error(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        parse_error = _parse_parse_error(d.pop("parse_error"))

        analyzer_version = d.pop("analyzer_version")

        token_saving_event = cls(
            id=id,
            event_id=event_id,
            runtime_id=runtime_id,
            observed_at_unix_millis=observed_at_unix_millis,
            provider=provider,
            transport=transport,
            endpoint=endpoint,
            model=model,
            wire_bytes_before=wire_bytes_before,
            wire_bytes_after=wire_bytes_after,
            saved_wire_bytes=saved_wire_bytes,
            estimated_tokens_before=estimated_tokens_before,
            estimated_tokens_after=estimated_tokens_after,
            saved_estimated_tokens=saved_estimated_tokens,
            elapsed_micros=elapsed_micros,
            methods=methods,
            parse_error=parse_error,
            analyzer_version=analyzer_version,
        )

        token_saving_event.additional_properties = d
        return token_saving_event

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
