from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast


T = TypeVar("T", bound="PaginationMeta")


@_attrs_define
class PaginationMeta:
    """Pagination block returned inside ``meta`` on every list response.

    ``page`` and ``size`` are always present and echo the parameters that
    served the response (their defaults when the client omitted them).
    ``total`` and ``total_pages`` are present only when the request included
    ``meta[total]=true``.

        Attributes:
            page (int): 1-based page number returned.
            size (int): Number of items per page.
            total (int | None | Unset): Total number of matching items across all pages. Present only when the request
                included `meta[total]=true`.
            total_pages (int | None | Unset): Total number of pages at the requested page size. Present only when the
                request included `meta[total]=true`.
    """

    page: int
    size: int
    total: int | None | Unset = UNSET
    total_pages: int | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        page = self.page

        size = self.size

        total: int | None | Unset
        if isinstance(self.total, Unset):
            total = UNSET
        else:
            total = self.total

        total_pages: int | None | Unset
        if isinstance(self.total_pages, Unset):
            total_pages = UNSET
        else:
            total_pages = self.total_pages

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "page": page,
                "size": size,
            }
        )
        if total is not UNSET:
            field_dict["total"] = total
        if total_pages is not UNSET:
            field_dict["total_pages"] = total_pages

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        page = d.pop("page")

        size = d.pop("size")

        def _parse_total(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total = _parse_total(d.pop("total", UNSET))

        def _parse_total_pages(data: object) -> int | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(int | None | Unset, data)

        total_pages = _parse_total_pages(d.pop("total_pages", UNSET))

        pagination_meta = cls(
            page=page,
            size=size,
            total=total,
            total_pages=total_pages,
        )

        pagination_meta.additional_properties = d
        return pagination_meta

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
