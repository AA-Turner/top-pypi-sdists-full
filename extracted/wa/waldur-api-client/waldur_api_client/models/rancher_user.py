from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.rancher_user_cluster_link import RancherUserClusterLink
    from ..models.rancher_user_project_link import RancherUserProjectLink


T = TypeVar("T", bound="RancherUser")


@_attrs_define
class RancherUser:
    """
    Attributes:
        url (str):
        uuid (UUID):
        user (str):
        cluster_roles (list['RancherUserClusterLink']):
        project_roles (list['RancherUserProjectLink']):
        settings (str):
        user_name (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_ characters
        full_name (str):
        is_active (Union[Unset, bool]):
    """

    url: str
    uuid: UUID
    user: str
    cluster_roles: list["RancherUserClusterLink"]
    project_roles: list["RancherUserProjectLink"]
    settings: str
    user_name: str
    full_name: str
    is_active: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        user = self.user

        cluster_roles = []
        for cluster_roles_item_data in self.cluster_roles:
            cluster_roles_item = cluster_roles_item_data.to_dict()
            cluster_roles.append(cluster_roles_item)

        project_roles = []
        for project_roles_item_data in self.project_roles:
            project_roles_item = project_roles_item_data.to_dict()
            project_roles.append(project_roles_item)

        settings = self.settings

        user_name = self.user_name

        full_name = self.full_name

        is_active = self.is_active

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "user": user,
                "cluster_roles": cluster_roles,
                "project_roles": project_roles,
                "settings": settings,
                "user_name": user_name,
                "full_name": full_name,
            }
        )
        if is_active is not UNSET:
            field_dict["is_active"] = is_active

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.rancher_user_cluster_link import RancherUserClusterLink
        from ..models.rancher_user_project_link import RancherUserProjectLink

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        user = d.pop("user")

        cluster_roles = []
        _cluster_roles = d.pop("cluster_roles")
        for cluster_roles_item_data in _cluster_roles:
            cluster_roles_item = RancherUserClusterLink.from_dict(cluster_roles_item_data)

            cluster_roles.append(cluster_roles_item)

        project_roles = []
        _project_roles = d.pop("project_roles")
        for project_roles_item_data in _project_roles:
            project_roles_item = RancherUserProjectLink.from_dict(project_roles_item_data)

            project_roles.append(project_roles_item)

        settings = d.pop("settings")

        user_name = d.pop("user_name")

        full_name = d.pop("full_name")

        is_active = d.pop("is_active", UNSET)

        rancher_user = cls(
            url=url,
            uuid=uuid,
            user=user,
            cluster_roles=cluster_roles,
            project_roles=project_roles,
            settings=settings,
            user_name=user_name,
            full_name=full_name,
            is_active=is_active,
        )

        rancher_user.additional_properties = d
        return rancher_user

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
