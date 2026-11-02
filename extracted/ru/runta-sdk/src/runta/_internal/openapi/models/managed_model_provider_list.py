from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define

if TYPE_CHECKING:
    from ..models.managed_model_provider import ManagedModelProvider


T = TypeVar("T", bound="ManagedModelProviderList")


@_attrs_define
class ManagedModelProviderList:
    """
    Attributes:
        organization_id (str):
        model_providers (list[ManagedModelProvider]):
    """

    organization_id: str
    model_providers: list[ManagedModelProvider]

    def to_dict(self) -> dict[str, Any]:
        organization_id = self.organization_id

        model_providers = []
        for model_providers_item_data in self.model_providers:
            model_providers_item = model_providers_item_data.to_dict()
            model_providers.append(model_providers_item)

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "organization_id": organization_id,
                "model_providers": model_providers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_model_provider import ManagedModelProvider

        d = dict(src_dict)
        organization_id = d.pop("organization_id")

        model_providers = []
        _model_providers = d.pop("model_providers")
        for model_providers_item_data in _model_providers:
            model_providers_item = ManagedModelProvider.from_dict(
                model_providers_item_data
            )

            model_providers.append(model_providers_item)

        managed_model_provider_list = cls(
            organization_id=organization_id,
            model_providers=model_providers,
        )

        return managed_model_provider_list
