import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.robot_account_states import RobotAccountStates
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.basic_user import BasicUser
    from ..models.fingerprint import Fingerprint
    from ..models.merged_plugin_options import MergedPluginOptions
    from ..models.ssh_key import SshKey


T = TypeVar("T", bound="RobotAccountDetails")


@_attrs_define
class RobotAccountDetails:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        username (Union[Unset, str]):
        description (Union[Unset, str]):
        error_message (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
        state (Union[Unset, RobotAccountStates]):
        resource (Union[Unset, str]):
        type_ (Union[Unset, str]): Type of the robot account.
        users (Union[Unset, list['BasicUser']]):
        keys (Union[Unset, Any]):
        backend_id (Union[Unset, str]):
        fingerprints (Union[Unset, list['Fingerprint']]):
        responsible_user (Union['BasicUser', None, Unset]):
        user_keys (Union[Unset, list['SshKey']]):
        resource_name (Union[Unset, str]):
        resource_uuid (Union[Unset, UUID]):
        project_name (Union[Unset, str]):
        project_uuid (Union[Unset, UUID]):
        customer_uuid (Union[Unset, UUID]):
        customer_name (Union[Unset, str]):
        provider_uuid (Union[Unset, UUID]):
        provider_name (Union[Unset, str]):
        offering_plugin_options (Union[Unset, MergedPluginOptions]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    username: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    state: Union[Unset, RobotAccountStates] = UNSET
    resource: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    users: Union[Unset, list["BasicUser"]] = UNSET
    keys: Union[Unset, Any] = UNSET
    backend_id: Union[Unset, str] = UNSET
    fingerprints: Union[Unset, list["Fingerprint"]] = UNSET
    responsible_user: Union["BasicUser", None, Unset] = UNSET
    user_keys: Union[Unset, list["SshKey"]] = UNSET
    resource_name: Union[Unset, str] = UNSET
    resource_uuid: Union[Unset, UUID] = UNSET
    project_name: Union[Unset, str] = UNSET
    project_uuid: Union[Unset, UUID] = UNSET
    customer_uuid: Union[Unset, UUID] = UNSET
    customer_name: Union[Unset, str] = UNSET
    provider_uuid: Union[Unset, UUID] = UNSET
    provider_name: Union[Unset, str] = UNSET
    offering_plugin_options: Union[Unset, "MergedPluginOptions"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.basic_user import BasicUser

        url = self.url

        uuid: Union[Unset, str] = UNSET
        if not isinstance(self.uuid, Unset):
            uuid = str(self.uuid)

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        modified: Union[Unset, str] = UNSET
        if not isinstance(self.modified, Unset):
            modified = self.modified.isoformat()

        username = self.username

        description = self.description

        error_message = self.error_message

        error_traceback = self.error_traceback

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        resource = self.resource

        type_ = self.type_

        users: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.users, Unset):
            users = []
            for users_item_data in self.users:
                users_item = users_item_data.to_dict()
                users.append(users_item)

        keys = self.keys

        backend_id = self.backend_id

        fingerprints: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.fingerprints, Unset):
            fingerprints = []
            for fingerprints_item_data in self.fingerprints:
                fingerprints_item = fingerprints_item_data.to_dict()
                fingerprints.append(fingerprints_item)

        responsible_user: Union[None, Unset, dict[str, Any]]
        if isinstance(self.responsible_user, Unset):
            responsible_user = UNSET
        elif isinstance(self.responsible_user, BasicUser):
            responsible_user = self.responsible_user.to_dict()
        else:
            responsible_user = self.responsible_user

        user_keys: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.user_keys, Unset):
            user_keys = []
            for user_keys_item_data in self.user_keys:
                user_keys_item = user_keys_item_data.to_dict()
                user_keys.append(user_keys_item)

        resource_name = self.resource_name

        resource_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.resource_uuid, Unset):
            resource_uuid = str(self.resource_uuid)

        project_name = self.project_name

        project_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.project_uuid, Unset):
            project_uuid = str(self.project_uuid)

        customer_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.customer_uuid, Unset):
            customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        provider_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.provider_uuid, Unset):
            provider_uuid = str(self.provider_uuid)

        provider_name = self.provider_name

        offering_plugin_options: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.offering_plugin_options, Unset):
            offering_plugin_options = self.offering_plugin_options.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if url is not UNSET:
            field_dict["url"] = url
        if uuid is not UNSET:
            field_dict["uuid"] = uuid
        if created is not UNSET:
            field_dict["created"] = created
        if modified is not UNSET:
            field_dict["modified"] = modified
        if username is not UNSET:
            field_dict["username"] = username
        if description is not UNSET:
            field_dict["description"] = description
        if error_message is not UNSET:
            field_dict["error_message"] = error_message
        if error_traceback is not UNSET:
            field_dict["error_traceback"] = error_traceback
        if state is not UNSET:
            field_dict["state"] = state
        if resource is not UNSET:
            field_dict["resource"] = resource
        if type_ is not UNSET:
            field_dict["type"] = type_
        if users is not UNSET:
            field_dict["users"] = users
        if keys is not UNSET:
            field_dict["keys"] = keys
        if backend_id is not UNSET:
            field_dict["backend_id"] = backend_id
        if fingerprints is not UNSET:
            field_dict["fingerprints"] = fingerprints
        if responsible_user is not UNSET:
            field_dict["responsible_user"] = responsible_user
        if user_keys is not UNSET:
            field_dict["user_keys"] = user_keys
        if resource_name is not UNSET:
            field_dict["resource_name"] = resource_name
        if resource_uuid is not UNSET:
            field_dict["resource_uuid"] = resource_uuid
        if project_name is not UNSET:
            field_dict["project_name"] = project_name
        if project_uuid is not UNSET:
            field_dict["project_uuid"] = project_uuid
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if customer_name is not UNSET:
            field_dict["customer_name"] = customer_name
        if provider_uuid is not UNSET:
            field_dict["provider_uuid"] = provider_uuid
        if provider_name is not UNSET:
            field_dict["provider_name"] = provider_name
        if offering_plugin_options is not UNSET:
            field_dict["offering_plugin_options"] = offering_plugin_options

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.basic_user import BasicUser
        from ..models.fingerprint import Fingerprint
        from ..models.merged_plugin_options import MergedPluginOptions
        from ..models.ssh_key import SshKey

        d = dict(src_dict)
        url = d.pop("url", UNSET)

        _uuid = d.pop("uuid", UNSET)
        uuid: Union[Unset, UUID]
        if isinstance(_uuid, Unset):
            uuid = UNSET
        else:
            uuid = UUID(_uuid)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _modified = d.pop("modified", UNSET)
        modified: Union[Unset, datetime.datetime]
        if isinstance(_modified, Unset):
            modified = UNSET
        else:
            modified = isoparse(_modified)

        username = d.pop("username", UNSET)

        description = d.pop("description", UNSET)

        error_message = d.pop("error_message", UNSET)

        error_traceback = d.pop("error_traceback", UNSET)

        _state = d.pop("state", UNSET)
        state: Union[Unset, RobotAccountStates]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = RobotAccountStates(_state)

        resource = d.pop("resource", UNSET)

        type_ = d.pop("type", UNSET)

        users = []
        _users = d.pop("users", UNSET)
        for users_item_data in _users or []:
            users_item = BasicUser.from_dict(users_item_data)

            users.append(users_item)

        keys = d.pop("keys", UNSET)

        backend_id = d.pop("backend_id", UNSET)

        fingerprints = []
        _fingerprints = d.pop("fingerprints", UNSET)
        for fingerprints_item_data in _fingerprints or []:
            fingerprints_item = Fingerprint.from_dict(fingerprints_item_data)

            fingerprints.append(fingerprints_item)

        def _parse_responsible_user(data: object) -> Union["BasicUser", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                responsible_user_type_1 = BasicUser.from_dict(data)

                return responsible_user_type_1
            except:  # noqa: E722
                pass
            return cast(Union["BasicUser", None, Unset], data)

        responsible_user = _parse_responsible_user(d.pop("responsible_user", UNSET))

        user_keys = []
        _user_keys = d.pop("user_keys", UNSET)
        for user_keys_item_data in _user_keys or []:
            user_keys_item = SshKey.from_dict(user_keys_item_data)

            user_keys.append(user_keys_item)

        resource_name = d.pop("resource_name", UNSET)

        _resource_uuid = d.pop("resource_uuid", UNSET)
        resource_uuid: Union[Unset, UUID]
        if isinstance(_resource_uuid, Unset):
            resource_uuid = UNSET
        else:
            resource_uuid = UUID(_resource_uuid)

        project_name = d.pop("project_name", UNSET)

        _project_uuid = d.pop("project_uuid", UNSET)
        project_uuid: Union[Unset, UUID]
        if isinstance(_project_uuid, Unset):
            project_uuid = UNSET
        else:
            project_uuid = UUID(_project_uuid)

        _customer_uuid = d.pop("customer_uuid", UNSET)
        customer_uuid: Union[Unset, UUID]
        if isinstance(_customer_uuid, Unset):
            customer_uuid = UNSET
        else:
            customer_uuid = UUID(_customer_uuid)

        customer_name = d.pop("customer_name", UNSET)

        _provider_uuid = d.pop("provider_uuid", UNSET)
        provider_uuid: Union[Unset, UUID]
        if isinstance(_provider_uuid, Unset):
            provider_uuid = UNSET
        else:
            provider_uuid = UUID(_provider_uuid)

        provider_name = d.pop("provider_name", UNSET)

        _offering_plugin_options = d.pop("offering_plugin_options", UNSET)
        offering_plugin_options: Union[Unset, MergedPluginOptions]
        if isinstance(_offering_plugin_options, Unset):
            offering_plugin_options = UNSET
        else:
            offering_plugin_options = MergedPluginOptions.from_dict(_offering_plugin_options)

        robot_account_details = cls(
            url=url,
            uuid=uuid,
            created=created,
            modified=modified,
            username=username,
            description=description,
            error_message=error_message,
            error_traceback=error_traceback,
            state=state,
            resource=resource,
            type_=type_,
            users=users,
            keys=keys,
            backend_id=backend_id,
            fingerprints=fingerprints,
            responsible_user=responsible_user,
            user_keys=user_keys,
            resource_name=resource_name,
            resource_uuid=resource_uuid,
            project_name=project_name,
            project_uuid=project_uuid,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            provider_uuid=provider_uuid,
            provider_name=provider_name,
            offering_plugin_options=offering_plugin_options,
        )

        robot_account_details.additional_properties = d
        return robot_account_details

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
