from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.template import Template


T = TypeVar("T", bound="PaginatedTemplatesResponse")


@_attrs_define
class PaginatedTemplatesResponse:
    """
    Attributes:
        templates (list['Template']): List of templates for the current page
        total (int): Total number of templates
        page (int): Current page number (1-based)
        limit (int): Number of items per page
        total_pages (int): Total number of pages
    """

    templates: list["Template"]
    total: int
    page: int
    limit: int
    total_pages: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        templates = []
        for templates_item_data in self.templates:
            templates_item = templates_item_data.to_dict()
            templates.append(templates_item)

        total = self.total

        page = self.page

        limit = self.limit

        total_pages = self.total_pages

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "templates": templates,
                "total": total,
                "page": page,
                "limit": limit,
                "totalPages": total_pages,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.template import Template

        d = dict(src_dict)
        templates = []
        _templates = d.pop("templates")
        for templates_item_data in _templates:
            templates_item = Template.from_dict(templates_item_data)
            templates.append(templates_item)

        total = d.pop("total")

        page = d.pop("page")

        limit = d.pop("limit")

        total_pages = d.pop("totalPages")

        paginated_templates_response = cls(
            templates=templates,
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
        )

        paginated_templates_response.additional_properties = d
        return paginated_templates_response

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
