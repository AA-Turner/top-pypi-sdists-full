from __future__ import annotations

import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define

from ..models.runtime_image_architectures_item import RuntimeImageArchitecturesItem
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.runtime_image_disk_capability import RuntimeImageDiskCapability
    from ..models.runtime_image_model_provider import RuntimeImageModelProvider
    from ..models.runtime_image_recommended_resources import (
        RuntimeImageRecommendedResources,
    )
    from ..models.runtime_image_web_ui import RuntimeImageWebUi


T = TypeVar("T", bound="RuntimeImage")


@_attrs_define
class RuntimeImage:
    """A selectable Runtime Image product variant.

    Attributes:
        id (str):
        name (str):
        description (str):
        icon_key (str):
        architectures (list[RuntimeImageArchitecturesItem]):
        disk (RuntimeImageDiskCapability):
        recommended_resources (RuntimeImageRecommendedResources):
        is_default (bool):
        is_custom (bool):
        exposed_ports (list[int]): TCP ports declared by the image. They are discovery hints and are not published
            automatically.
        created_at (datetime.datetime | Unset):
        model_provider (RuntimeImageModelProvider | Unset):
        web_ui (RuntimeImageWebUi | Unset): A browser surface the image serves. It is published through the runtime's
            ingress on demand, behind a session gateway, rather than being exposed for the lifetime of the runtime.
    """

    id: str
    name: str
    description: str
    icon_key: str
    architectures: list[RuntimeImageArchitecturesItem]
    disk: RuntimeImageDiskCapability
    recommended_resources: RuntimeImageRecommendedResources
    is_default: bool
    is_custom: bool
    exposed_ports: list[int]
    created_at: datetime.datetime | Unset = UNSET
    model_provider: RuntimeImageModelProvider | Unset = UNSET
    web_ui: RuntimeImageWebUi | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        name = self.name

        description = self.description

        icon_key = self.icon_key

        architectures = []
        for architectures_item_data in self.architectures:
            architectures_item = architectures_item_data.value
            architectures.append(architectures_item)

        disk = self.disk.to_dict()

        recommended_resources = self.recommended_resources.to_dict()

        is_default = self.is_default

        is_custom = self.is_custom

        exposed_ports = self.exposed_ports

        created_at: str | Unset = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        model_provider: dict[str, Any] | Unset = UNSET
        if not isinstance(self.model_provider, Unset):
            model_provider = self.model_provider.to_dict()

        web_ui: dict[str, Any] | Unset = UNSET
        if not isinstance(self.web_ui, Unset):
            web_ui = self.web_ui.to_dict()

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "id": id,
                "name": name,
                "description": description,
                "icon_key": icon_key,
                "architectures": architectures,
                "disk": disk,
                "recommended_resources": recommended_resources,
                "is_default": is_default,
                "is_custom": is_custom,
                "exposed_ports": exposed_ports,
            }
        )
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if model_provider is not UNSET:
            field_dict["model_provider"] = model_provider
        if web_ui is not UNSET:
            field_dict["web_ui"] = web_ui

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.runtime_image_disk_capability import RuntimeImageDiskCapability
        from ..models.runtime_image_model_provider import RuntimeImageModelProvider
        from ..models.runtime_image_recommended_resources import (
            RuntimeImageRecommendedResources,
        )
        from ..models.runtime_image_web_ui import RuntimeImageWebUi

        d = dict(src_dict)
        id = d.pop("id")

        name = d.pop("name")

        description = d.pop("description")

        icon_key = d.pop("icon_key")

        architectures = []
        _architectures = d.pop("architectures")
        for architectures_item_data in _architectures:
            architectures_item = RuntimeImageArchitecturesItem(architectures_item_data)

            architectures.append(architectures_item)

        disk = RuntimeImageDiskCapability.from_dict(d.pop("disk"))

        recommended_resources = RuntimeImageRecommendedResources.from_dict(
            d.pop("recommended_resources")
        )

        is_default = d.pop("is_default")

        is_custom = d.pop("is_custom")

        exposed_ports = cast(list[int], d.pop("exposed_ports"))

        _created_at = d.pop("created_at", UNSET)
        created_at: datetime.datetime | Unset
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = datetime.datetime.fromisoformat(
                _created_at.replace("Z", "+00:00")
            )

        _model_provider = d.pop("model_provider", UNSET)
        model_provider: RuntimeImageModelProvider | Unset
        if isinstance(_model_provider, Unset):
            model_provider = UNSET
        else:
            model_provider = RuntimeImageModelProvider.from_dict(_model_provider)

        _web_ui = d.pop("web_ui", UNSET)
        web_ui: RuntimeImageWebUi | Unset
        if isinstance(_web_ui, Unset):
            web_ui = UNSET
        else:
            web_ui = RuntimeImageWebUi.from_dict(_web_ui)

        runtime_image = cls(
            id=id,
            name=name,
            description=description,
            icon_key=icon_key,
            architectures=architectures,
            disk=disk,
            recommended_resources=recommended_resources,
            is_default=is_default,
            is_custom=is_custom,
            exposed_ports=exposed_ports,
            created_at=created_at,
            model_provider=model_provider,
            web_ui=web_ui,
        )

        return runtime_image
