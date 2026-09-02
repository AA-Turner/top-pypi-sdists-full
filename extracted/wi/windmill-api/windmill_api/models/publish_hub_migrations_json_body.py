from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.publish_hub_migrations_json_body_migrations_item import PublishHubMigrationsJsonBodyMigrationsItem


T = TypeVar("T", bound="PublishHubMigrationsJsonBody")


@_attrs_define
class PublishHubMigrationsJsonBody:
    """
    Attributes:
        migrations (List['PublishHubMigrationsJsonBodyMigrationsItem']):
        project_slug (str): hub project slug (3-50 chars, lowercase alphanumeric and hyphens, no leading/trailing
            hyphen)
    """

    migrations: List["PublishHubMigrationsJsonBodyMigrationsItem"]
    project_slug: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        migrations = []
        for migrations_item_data in self.migrations:
            migrations_item = migrations_item_data.to_dict()

            migrations.append(migrations_item)

        project_slug = self.project_slug

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "migrations": migrations,
                "project_slug": project_slug,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.publish_hub_migrations_json_body_migrations_item import PublishHubMigrationsJsonBodyMigrationsItem

        d = src_dict.copy()
        migrations = []
        _migrations = d.pop("migrations")
        for migrations_item_data in _migrations:
            migrations_item = PublishHubMigrationsJsonBodyMigrationsItem.from_dict(migrations_item_data)

            migrations.append(migrations_item)

        project_slug = d.pop("project_slug")

        publish_hub_migrations_json_body = cls(
            migrations=migrations,
            project_slug=project_slug,
        )

        publish_hub_migrations_json_body.additional_properties = d
        return publish_hub_migrations_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
