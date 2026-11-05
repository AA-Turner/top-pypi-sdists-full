from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.get_instance_group_response_200_instance_role import GetInstanceGroupResponse200InstanceRole
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.get_instance_group_response_200_workspaces_item import GetInstanceGroupResponse200WorkspacesItem


T = TypeVar("T", bound="GetInstanceGroupResponse200")


@_attrs_define
class GetInstanceGroupResponse200:
    """
    Attributes:
        name (str):
        summary (Union[Unset, str]):
        emails (Union[Unset, List[str]]):
        instance_role (Union[Unset, None, GetInstanceGroupResponse200InstanceRole]):
        external_id (Union[Unset, None, str]): IdP group this group is linked to; its membership then follows the SSO
            groups claim
        scim_managed (Union[Unset, bool]): Provisioned by SCIM, which then owns external_id
        workspaces (Union[Unset, List['GetInstanceGroupResponse200WorkspacesItem']]):
    """

    name: str
    summary: Union[Unset, str] = UNSET
    emails: Union[Unset, List[str]] = UNSET
    instance_role: Union[Unset, None, GetInstanceGroupResponse200InstanceRole] = UNSET
    external_id: Union[Unset, None, str] = UNSET
    scim_managed: Union[Unset, bool] = UNSET
    workspaces: Union[Unset, List["GetInstanceGroupResponse200WorkspacesItem"]] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        summary = self.summary
        emails: Union[Unset, List[str]] = UNSET
        if not isinstance(self.emails, Unset):
            emails = self.emails

        instance_role: Union[Unset, None, str] = UNSET
        if not isinstance(self.instance_role, Unset):
            instance_role = self.instance_role.value if self.instance_role else None

        external_id = self.external_id
        scim_managed = self.scim_managed
        workspaces: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.workspaces, Unset):
            workspaces = []
            for workspaces_item_data in self.workspaces:
                workspaces_item = workspaces_item_data.to_dict()

                workspaces.append(workspaces_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
            }
        )
        if summary is not UNSET:
            field_dict["summary"] = summary
        if emails is not UNSET:
            field_dict["emails"] = emails
        if instance_role is not UNSET:
            field_dict["instance_role"] = instance_role
        if external_id is not UNSET:
            field_dict["external_id"] = external_id
        if scim_managed is not UNSET:
            field_dict["scim_managed"] = scim_managed
        if workspaces is not UNSET:
            field_dict["workspaces"] = workspaces

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.get_instance_group_response_200_workspaces_item import GetInstanceGroupResponse200WorkspacesItem

        d = src_dict.copy()
        name = d.pop("name")

        summary = d.pop("summary", UNSET)

        emails = cast(List[str], d.pop("emails", UNSET))

        _instance_role = d.pop("instance_role", UNSET)
        instance_role: Union[Unset, None, GetInstanceGroupResponse200InstanceRole]
        if _instance_role is None:
            instance_role = None
        elif isinstance(_instance_role, Unset):
            instance_role = UNSET
        else:
            instance_role = GetInstanceGroupResponse200InstanceRole(_instance_role)

        external_id = d.pop("external_id", UNSET)

        scim_managed = d.pop("scim_managed", UNSET)

        workspaces = []
        _workspaces = d.pop("workspaces", UNSET)
        for workspaces_item_data in _workspaces or []:
            workspaces_item = GetInstanceGroupResponse200WorkspacesItem.from_dict(workspaces_item_data)

            workspaces.append(workspaces_item)

        get_instance_group_response_200 = cls(
            name=name,
            summary=summary,
            emails=emails,
            instance_role=instance_role,
            external_id=external_id,
            scim_managed=scim_managed,
            workspaces=workspaces,
        )

        get_instance_group_response_200.additional_properties = d
        return get_instance_group_response_200

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
