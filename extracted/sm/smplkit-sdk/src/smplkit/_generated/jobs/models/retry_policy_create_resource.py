from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Literal

if TYPE_CHECKING:
    from ..models.retry_policy import RetryPolicy


T = TypeVar("T", bound="RetryPolicyCreateResource")


@_attrs_define
class RetryPolicyCreateResource:
    """JSON:API resource envelope for creating a retry policy (id required).

    Example:
        {'attributes': {'backoff': 'exponential', 'delay_seconds': 2, 'max_delay_seconds': 60, 'max_retries': 5, 'name':
            'Retry on server errors', 'retry_on': {'reasons': ['TIMEOUT', 'CONNECTION_ERROR'], 'statuses': [429, 503]}},
            'id': 'retry-on-5xx', 'type': 'retry_policy'}

    Attributes:
        id (str): Client-supplied resource id.
        attributes (RetryPolicy): A named, reusable automatic-retry policy.

            A policy decides whether and how a failed run is retried. Reference it from
            a job's `retry_policy` (and optionally override it per environment). A job
            that references nothing uses the built-in `Default` policy, which never
            retries.
        type_ (Literal['retry_policy'] | Unset):  Default: 'retry_policy'.
    """

    id: str
    attributes: RetryPolicy
    type_: Literal["retry_policy"] | Unset = "retry_policy"
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        attributes = self.attributes.to_dict()

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "attributes": attributes,
            }
        )
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.retry_policy import RetryPolicy

        d = dict(src_dict)
        id = d.pop("id")

        attributes = RetryPolicy.from_dict(d.pop("attributes"))

        type_ = cast(Literal["retry_policy"] | Unset, d.pop("type", UNSET))
        if type_ != "retry_policy" and not isinstance(type_, Unset):
            raise ValueError(f"type must match const 'retry_policy', got '{type_}'")

        retry_policy_create_resource = cls(
            id=id,
            attributes=attributes,
            type_=type_,
        )

        retry_policy_create_resource.additional_properties = d
        return retry_policy_create_resource

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
