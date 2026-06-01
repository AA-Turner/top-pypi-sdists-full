from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field


if TYPE_CHECKING:
    from ..models.pagination_meta import PaginationMeta


T = TypeVar("T", bound="ListMeta")


@_attrs_define
class ListMeta:
    """Top-level ``meta`` block included on every JSON:API list response.

    Attributes:
        pagination (PaginationMeta): Pagination block returned inside ``meta`` on every list response.

            ``page`` and ``size`` are always present and echo the parameters that
            served the response (their defaults when the client omitted them).
            ``total`` and ``total_pages`` are present only when the request included
            ``meta[total]=true``.
    """

    pagination: PaginationMeta
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pagination = self.pagination.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "pagination": pagination,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.pagination_meta import PaginationMeta

        d = dict(src_dict)
        pagination = PaginationMeta.from_dict(d.pop("pagination"))

        list_meta = cls(
            pagination=pagination,
        )

        list_meta.additional_properties = d
        return list_meta

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
