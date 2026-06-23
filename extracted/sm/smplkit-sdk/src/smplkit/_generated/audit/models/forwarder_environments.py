from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.forwarder_environments_additional_property import ForwarderEnvironmentsAdditionalProperty


T = TypeVar("T", bound="ForwarderEnvironments")


@_attrs_define
class ForwarderEnvironments:
    """Per-environment overrides keyed by environment key (e.g. `production`, `staging`). Each entry is a sparse map of
    only the fields that differ in that environment: `enabled` (whether the forwarder delivers there) plus any of `url`,
    `method`, `success_status`, `tls_verify`, `ca_cert`, and individual headers as `headers.<name>` (e.g.
    `headers.Authorization`). Fields you omit are inherited from the base `configuration`; an entry never needs to
    repeat the whole configuration. A forwarder with no entry for an environment is disabled there. Every referenced
    environment must exist and be managed for the account.

    """

    additional_properties: dict[str, ForwarderEnvironmentsAdditionalProperty] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = prop.to_dict()

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.forwarder_environments_additional_property import ForwarderEnvironmentsAdditionalProperty

        d = dict(src_dict)
        forwarder_environments = cls()

        additional_properties = {}
        for prop_name, prop_dict in d.items():
            additional_property = ForwarderEnvironmentsAdditionalProperty.from_dict(prop_dict)

            additional_properties[prop_name] = additional_property

        forwarder_environments.additional_properties = additional_properties
        return forwarder_environments

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> ForwarderEnvironmentsAdditionalProperty:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: ForwarderEnvironmentsAdditionalProperty) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
