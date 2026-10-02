from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_model_ref_capabilities import ManagedAgentsModelRefCapabilities
  from ..models.managed_agents_model_ref_metadata import ManagedAgentsModelRefMetadata





T = TypeVar("T", bound="ManagedAgentsModelRef")



@_attrs_define
class ManagedAgentsModelRef:
    """ Snapshot of the model that served one inference call, recorded on the event so a transcript stays interpretable
    after the catalog entry changes. Returned on model events; also accepted when pinning a session to a specific model.

        Example:
            {'base_url': 'https://example.com', 'capabilities': {'key': 'example'}, 'context_window': 1,
                'max_output_tokens': 1, 'metadata': {'key': 'example'}, 'model': 'example', 'model_ref_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'model_version': 'example', 'provider': 'example', 'provider_id':
                '9f8b1c2d-3e4f-5a6b-7c8d-9e0f1a2b3c4d', 'provider_type': 'example', 'serving_backend': 'example'}

        Attributes:
            model (str): Provider's own model id as sent on the wire, e.g. claude-sonnet-4-5 or anthropic/claude-sonnet-4-5.
            provider (str): Provider family that served the call, e.g. anthropic, openai, vertex, or mock. Carries the same
                value as provider_type and is kept for older readers.
            base_url (str | Unset): Endpoint the request was sent to, for self-hosted or gateway-fronted models. Empty means
                the provider's default endpoint.
            capabilities (ManagedAgentsModelRefCapabilities | Unset): Declared model capability flags, e.g. tool use,
                vision, or extended thinking support, as recorded from the catalog entry at call time.
            context_window (int | Unset): Maximum total tokens the model accepts in one request, prompt plus completion, as
                recorded from the catalog entry at call time. 0 means unknown.
            max_output_tokens (int | Unset): Maximum completion tokens the model can emit in one response, as recorded from
                the catalog entry at call time. 0 means unknown.
            metadata (ManagedAgentsModelRefMetadata | Unset): Extra key/value data copied from the catalog entry. Some keys
                are read by the service to shape the request, such as base_url and reasoning_style.
            model_ref_id (str | Unset): Model reference in the catalog this snapshot was resolved from (UUID). Empty when
                the session named a gateway model id instead of a catalog entry.
            model_version (str | Unset): Provider-specific version or snapshot pin recorded alongside the model id, when the
                catalog entry declares one.
            provider_id (str | Unset): Model provider record whose credentials and base URL were used (UUID).
            provider_type (str | Unset): Provider family that served the call, e.g. anthropic, openai, vertex, or mock.
                Selects which wire protocol the request used.
            serving_backend (str | Unset): Serving stack behind a self-hosted model, e.g. vllm. Empty for models called
                through a hosted provider API.
     """

    model: str
    provider: str
    base_url: str | Unset = UNSET
    capabilities: ManagedAgentsModelRefCapabilities | Unset = UNSET
    context_window: int | Unset = UNSET
    max_output_tokens: int | Unset = UNSET
    metadata: ManagedAgentsModelRefMetadata | Unset = UNSET
    model_ref_id: str | Unset = UNSET
    model_version: str | Unset = UNSET
    provider_id: str | Unset = UNSET
    provider_type: str | Unset = UNSET
    serving_backend: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_model_ref_capabilities import ManagedAgentsModelRefCapabilities # noqa: PLC0415
        from ..models.managed_agents_model_ref_metadata import ManagedAgentsModelRefMetadata # noqa: PLC0415
        model = self.model

        provider = self.provider

        base_url = self.base_url

        capabilities: dict[str, Any] | Unset = UNSET
        if not isinstance(self.capabilities, Unset):
            capabilities = self.capabilities.to_dict()

        context_window = self.context_window

        max_output_tokens = self.max_output_tokens

        metadata: dict[str, Any] | Unset = UNSET
        if not isinstance(self.metadata, Unset):
            metadata = self.metadata.to_dict()

        model_ref_id = self.model_ref_id

        model_version = self.model_version

        provider_id = self.provider_id

        provider_type = self.provider_type

        serving_backend = self.serving_backend


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "model": model,
            "provider": provider,
        })
        if base_url is not UNSET:
            field_dict["base_url"] = base_url
        if capabilities is not UNSET:
            field_dict["capabilities"] = capabilities
        if context_window is not UNSET:
            field_dict["context_window"] = context_window
        if max_output_tokens is not UNSET:
            field_dict["max_output_tokens"] = max_output_tokens
        if metadata is not UNSET:
            field_dict["metadata"] = metadata
        if model_ref_id is not UNSET:
            field_dict["model_ref_id"] = model_ref_id
        if model_version is not UNSET:
            field_dict["model_version"] = model_version
        if provider_id is not UNSET:
            field_dict["provider_id"] = provider_id
        if provider_type is not UNSET:
            field_dict["provider_type"] = provider_type
        if serving_backend is not UNSET:
            field_dict["serving_backend"] = serving_backend

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_model_ref_capabilities import ManagedAgentsModelRefCapabilities # noqa: PLC0415
        from ..models.managed_agents_model_ref_metadata import ManagedAgentsModelRefMetadata # noqa: PLC0415
        d = dict(src_dict)
        model = d.pop("model")

        provider = d.pop("provider")

        base_url = d.pop("base_url", UNSET)

        _capabilities = d.pop("capabilities", UNSET)
        capabilities: ManagedAgentsModelRefCapabilities | Unset
        if isinstance(_capabilities,  Unset):
            capabilities = UNSET
        else:
            capabilities = ManagedAgentsModelRefCapabilities.from_dict(_capabilities)




        context_window = d.pop("context_window", UNSET)

        max_output_tokens = d.pop("max_output_tokens", UNSET)

        _metadata = d.pop("metadata", UNSET)
        metadata: ManagedAgentsModelRefMetadata | Unset
        if isinstance(_metadata,  Unset):
            metadata = UNSET
        else:
            metadata = ManagedAgentsModelRefMetadata.from_dict(_metadata)




        model_ref_id = d.pop("model_ref_id", UNSET)

        model_version = d.pop("model_version", UNSET)

        provider_id = d.pop("provider_id", UNSET)

        provider_type = d.pop("provider_type", UNSET)

        serving_backend = d.pop("serving_backend", UNSET)

        managed_agents_model_ref = cls(
            model=model,
            provider=provider,
            base_url=base_url,
            capabilities=capabilities,
            context_window=context_window,
            max_output_tokens=max_output_tokens,
            metadata=metadata,
            model_ref_id=model_ref_id,
            model_version=model_version,
            provider_id=provider_id,
            provider_type=provider_type,
            serving_backend=serving_backend,
        )


        managed_agents_model_ref.additional_properties = d
        return managed_agents_model_ref

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
