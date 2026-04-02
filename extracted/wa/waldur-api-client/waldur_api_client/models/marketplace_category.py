from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.category_component import CategoryComponent
    from ..models.category_help_article import CategoryHelpArticle
    from ..models.nested_column import NestedColumn
    from ..models.nested_section import NestedSection


T = TypeVar("T", bound="MarketplaceCategory")


@_attrs_define
class MarketplaceCategory:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        title (Union[Unset, str]):
        description (Union[Unset, str]):
        icon (Union[None, Unset, str]):
        default_vm_category (Union[Unset, bool]): Set to "true" if this category is for OpenStack VM. Only one category
            can have "true" value.
        default_volume_category (Union[Unset, bool]): Set to true if this category is for OpenStack Volume. Only one
            category can have "true" value.
        default_tenant_category (Union[Unset, bool]): Set to true if this category is for OpenStack Tenant. Only one
            category can have "true" value.
        offering_count (Union[Unset, int]):
        available_offerings_count (Union[Unset, int]):
        sections (Union[Unset, list['NestedSection']]):
        columns (Union[Unset, list['NestedColumn']]):
        components (Union[Unset, list['CategoryComponent']]):
        articles (Union[Unset, list['CategoryHelpArticle']]):
        group (Union[None, Unset, str]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    title: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    icon: Union[None, Unset, str] = UNSET
    default_vm_category: Union[Unset, bool] = UNSET
    default_volume_category: Union[Unset, bool] = UNSET
    default_tenant_category: Union[Unset, bool] = UNSET
    offering_count: Union[Unset, int] = UNSET
    available_offerings_count: Union[Unset, int] = UNSET
    sections: Union[Unset, list["NestedSection"]] = UNSET
    columns: Union[Unset, list["NestedColumn"]] = UNSET
    components: Union[Unset, list["CategoryComponent"]] = UNSET
    articles: Union[Unset, list["CategoryHelpArticle"]] = UNSET
    group: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        title = self.title

        description = self.description

        icon: Union[None, Unset, str]
        if isinstance(self.icon, Unset):
            icon = UNSET
        else:
            icon = self.icon

        default_vm_category = self.default_vm_category

        default_volume_category = self.default_volume_category

        default_tenant_category = self.default_tenant_category

        offering_count = self.offering_count

        available_offerings_count = self.available_offerings_count

        sections: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.sections, Unset):
            sections = []
            for sections_item_data in self.sections:
                sections_item = sections_item_data.to_dict()
                sections.append(sections_item)

        columns: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.columns, Unset):
            columns = []
            for columns_item_data in self.columns:
                columns_item = columns_item_data.to_dict()
                columns.append(columns_item)

        components: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.components, Unset):
            components = []
            for components_item_data in self.components:
                components_item = components_item_data.to_dict()
                components.append(components_item)

        articles: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.articles, Unset):
            articles = []
            for articles_item_data in self.articles:
                articles_item = articles_item_data.to_dict()
                articles.append(articles_item)

        group: Union[None, Unset, str]
        if isinstance(self.group, Unset):
            group = UNSET
        else:
            group = self.group

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if title is not UNSET:
            field_dict["title"] = title
        if description is not UNSET:
            field_dict["description"] = description
        if icon is not UNSET:
            field_dict["icon"] = icon
        if default_vm_category is not UNSET:
            field_dict["default_vm_category"] = default_vm_category
        if default_volume_category is not UNSET:
            field_dict["default_volume_category"] = default_volume_category
        if default_tenant_category is not UNSET:
            field_dict["default_tenant_category"] = default_tenant_category
        if offering_count is not UNSET:
            field_dict["offering_count"] = offering_count
        if available_offerings_count is not UNSET:
            field_dict["available_offerings_count"] = available_offerings_count
        if sections is not UNSET:
            field_dict["sections"] = sections
        if columns is not UNSET:
            field_dict["columns"] = columns
        if components is not UNSET:
            field_dict["components"] = components
        if articles is not UNSET:
            field_dict["articles"] = articles
        if group is not UNSET:
            field_dict["group"] = group

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.category_component import CategoryComponent
        from ..models.category_help_article import CategoryHelpArticle
        from ..models.nested_column import NestedColumn
        from ..models.nested_section import NestedSection

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        title = d.pop("title", UNSET)

        description = d.pop("description", UNSET)

        def _parse_icon(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        icon = _parse_icon(d.pop("icon", UNSET))

        default_vm_category = d.pop("default_vm_category", UNSET)

        default_volume_category = d.pop("default_volume_category", UNSET)

        default_tenant_category = d.pop("default_tenant_category", UNSET)

        offering_count = d.pop("offering_count", UNSET)

        available_offerings_count = d.pop("available_offerings_count", UNSET)

        sections = []
        _sections = d.pop("sections", UNSET)
        for sections_item_data in _sections or []:
            sections_item = NestedSection.from_dict(sections_item_data)

            sections.append(sections_item)

        columns = []
        _columns = d.pop("columns", UNSET)
        for columns_item_data in _columns or []:
            columns_item = NestedColumn.from_dict(columns_item_data)

            columns.append(columns_item)

        components = []
        _components = d.pop("components", UNSET)
        for components_item_data in _components or []:
            components_item = CategoryComponent.from_dict(components_item_data)

            components.append(components_item)

        articles = []
        _articles = d.pop("articles", UNSET)
        for articles_item_data in _articles or []:
            articles_item = CategoryHelpArticle.from_dict(articles_item_data)

            articles.append(articles_item)

        def _parse_group(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        group = _parse_group(d.pop("group", UNSET))

        marketplace_category = cls(
            url=url,
            uuid=uuid,
            title=title,
            description=description,
            icon=icon,
            default_vm_category=default_vm_category,
            default_volume_category=default_volume_category,
            default_tenant_category=default_tenant_category,
            offering_count=offering_count,
            available_offerings_count=available_offerings_count,
            sections=sections,
            columns=columns,
            components=components,
            articles=articles,
            group=group,
        )

        marketplace_category.additional_properties = d
        return marketplace_category

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
