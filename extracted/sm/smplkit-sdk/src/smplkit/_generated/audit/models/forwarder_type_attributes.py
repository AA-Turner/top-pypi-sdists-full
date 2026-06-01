from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
    from ..models.forwarder_type_attributes_placeholders import ForwarderTypeAttributesPlaceholders
    from ..models.forwarder_type_http_configuration import ForwarderTypeHttpConfiguration
    from ..models.forwarder_type_transform import ForwarderTypeTransform


T = TypeVar("T", bound="ForwarderTypeAttributes")


@_attrs_define
class ForwarderTypeAttributes:
    """The catalog entry's attributes — one branded forwarder type or the
    synthetic Custom HTTP entry.

        Attributes:
            name (str): Human-readable label shown in the type-picker.
            icon (str): Absolute URL to the icon asset, served by audit at `/api/v1/forwarder_types/{id}/icon`.
            base_type (str): Transport family — today only `HTTP`. New base types will add their own configuration shape and
                runtime handler.
            is_custom (bool): True for the synthetic `http` Custom HTTP entry, which has no vendor template — the customer
                supplies URL, headers, and transform from scratch. False for branded types.
            configuration (ForwarderTypeHttpConfiguration): HTTP-base-type delivery template.
            placeholders (ForwarderTypeAttributesPlaceholders): UI metadata keyed by placeholder name. Each `{name}` token
                appearing in `configuration` (URL, header value) has a matching entry here describing how to prompt for it.
            docs_url (None | str | Unset): Link to the vendor's own documentation for this destination.
            transform (ForwarderTypeTransform | None | Unset): Default transform shipped with the type, or `null` if none.
    """

    name: str
    icon: str
    base_type: str
    is_custom: bool
    configuration: ForwarderTypeHttpConfiguration
    placeholders: ForwarderTypeAttributesPlaceholders
    docs_url: None | str | Unset = UNSET
    transform: ForwarderTypeTransform | None | Unset = UNSET

    def to_dict(self) -> dict[str, Any]:
        from ..models.forwarder_type_transform import ForwarderTypeTransform

        name = self.name

        icon = self.icon

        base_type = self.base_type

        is_custom = self.is_custom

        configuration = self.configuration.to_dict()

        placeholders = self.placeholders.to_dict()

        docs_url: None | str | Unset
        if isinstance(self.docs_url, Unset):
            docs_url = UNSET
        else:
            docs_url = self.docs_url

        transform: dict[str, Any] | None | Unset
        if isinstance(self.transform, Unset):
            transform = UNSET
        elif isinstance(self.transform, ForwarderTypeTransform):
            transform = self.transform.to_dict()
        else:
            transform = self.transform

        field_dict: dict[str, Any] = {}

        field_dict.update(
            {
                "name": name,
                "icon": icon,
                "base_type": base_type,
                "is_custom": is_custom,
                "configuration": configuration,
                "placeholders": placeholders,
            }
        )
        if docs_url is not UNSET:
            field_dict["docs_url"] = docs_url
        if transform is not UNSET:
            field_dict["transform"] = transform

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.forwarder_type_attributes_placeholders import ForwarderTypeAttributesPlaceholders
        from ..models.forwarder_type_http_configuration import ForwarderTypeHttpConfiguration
        from ..models.forwarder_type_transform import ForwarderTypeTransform

        d = dict(src_dict)
        name = d.pop("name")

        icon = d.pop("icon")

        base_type = d.pop("base_type")

        is_custom = d.pop("is_custom")

        configuration = ForwarderTypeHttpConfiguration.from_dict(d.pop("configuration"))

        placeholders = ForwarderTypeAttributesPlaceholders.from_dict(d.pop("placeholders"))

        def _parse_docs_url(data: object) -> None | str | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(None | str | Unset, data)

        docs_url = _parse_docs_url(d.pop("docs_url", UNSET))

        def _parse_transform(data: object) -> ForwarderTypeTransform | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                transform_type_0 = ForwarderTypeTransform.from_dict(data)

                return transform_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(ForwarderTypeTransform | None | Unset, data)

        transform = _parse_transform(d.pop("transform", UNSET))

        forwarder_type_attributes = cls(
            name=name,
            icon=icon,
            base_type=base_type,
            is_custom=is_custom,
            configuration=configuration,
            placeholders=placeholders,
            docs_url=docs_url,
            transform=transform,
        )

        return forwarder_type_attributes
