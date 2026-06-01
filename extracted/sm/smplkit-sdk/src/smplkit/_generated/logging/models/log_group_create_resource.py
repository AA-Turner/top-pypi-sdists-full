from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


from typing import cast
from typing import Literal

if TYPE_CHECKING:
    from ..models.log_group import LogGroup


T = TypeVar("T", bound="LogGroupCreateResource")


@_attrs_define
class LogGroupCreateResource:
    """JSON:API resource envelope for creating a log group (id required).

    Example:
        {'attributes': {'environments': {'prod': {'level': 'ERROR'}}, 'level': 'WARN', 'name': 'Payment pipeline'},
            'id': 'payment-pipeline', 'type': 'log_group'}

    Attributes:
        id (str): Client-supplied resource id.
        type_ (Literal['log_group']):
        attributes (LogGroup): A named collection of loggers that share a level configuration.

            Assigning a logger to a group ties the logger's effective level to
            the group's level (and per-environment overrides). Loggers can move
            between groups or be detached from a group entirely. Example: {'created_at': '2026-04-01T10:00:00Z',
            'environments': {'production': {'level': 'ERROR'}}, 'level': 'WARN', 'name': 'Database Loggers', 'updated_at':
            '2026-04-01T10:00:00Z'}.
    """

    id: str
    type_: Literal["log_group"]
    attributes: LogGroup
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        type_ = self.type_

        attributes = self.attributes.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "type": type_,
                "attributes": attributes,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_group import LogGroup

        d = dict(src_dict)
        id = d.pop("id")

        type_ = cast(Literal["log_group"], d.pop("type"))
        if type_ != "log_group":
            raise ValueError(f"type must match const 'log_group', got '{type_}'")

        attributes = LogGroup.from_dict(d.pop("attributes"))

        log_group_create_resource = cls(
            id=id,
            type_=type_,
            attributes=attributes,
        )

        log_group_create_resource.additional_properties = d
        return log_group_create_resource

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
