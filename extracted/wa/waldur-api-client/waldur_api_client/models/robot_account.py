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
    from ..models.fingerprint import Fingerprint


T = TypeVar("T", bound="RobotAccount")


@_attrs_define
class RobotAccount:
    """
    Attributes:
        url (str):
        uuid (UUID):
        created (datetime.datetime):
        modified (datetime.datetime):
        resource (str):
        type_ (str): Type of the robot account.
        backend_id (str):
        fingerprints (list['Fingerprint']):
        username (Union[Unset, str]):
        description (Union[Unset, str]):
        error_message (Union[Unset, str]):
        error_traceback (Union[Unset, str]):
        state (Union[Unset, RobotAccountStates]):
        users (Union[Unset, list[str]]): Users who have access to this robot account.
        keys (Union[Unset, Any]):
        responsible_user (Union[None, Unset, str]):
    """

    url: str
    uuid: UUID
    created: datetime.datetime
    modified: datetime.datetime
    resource: str
    type_: str
    backend_id: str
    fingerprints: list["Fingerprint"]
    username: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    error_message: Union[Unset, str] = UNSET
    error_traceback: Union[Unset, str] = UNSET
    state: Union[Unset, RobotAccountStates] = UNSET
    users: Union[Unset, list[str]] = UNSET
    keys: Union[Unset, Any] = UNSET
    responsible_user: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        created = self.created.isoformat()

        modified = self.modified.isoformat()

        resource = self.resource

        type_ = self.type_

        backend_id = self.backend_id

        fingerprints = []
        for fingerprints_item_data in self.fingerprints:
            fingerprints_item = fingerprints_item_data.to_dict()
            fingerprints.append(fingerprints_item)

        username = self.username

        description = self.description

        error_message = self.error_message

        error_traceback = self.error_traceback

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        users: Union[Unset, list[str]] = UNSET
        if not isinstance(self.users, Unset):
            users = self.users

        keys = self.keys

        responsible_user: Union[None, Unset, str]
        if isinstance(self.responsible_user, Unset):
            responsible_user = UNSET
        else:
            responsible_user = self.responsible_user

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "created": created,
                "modified": modified,
                "resource": resource,
                "type": type_,
                "backend_id": backend_id,
                "fingerprints": fingerprints,
            }
        )
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
        if users is not UNSET:
            field_dict["users"] = users
        if keys is not UNSET:
            field_dict["keys"] = keys
        if responsible_user is not UNSET:
            field_dict["responsible_user"] = responsible_user

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.fingerprint import Fingerprint

        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        created = isoparse(d.pop("created"))

        modified = isoparse(d.pop("modified"))

        resource = d.pop("resource")

        type_ = d.pop("type")

        backend_id = d.pop("backend_id")

        fingerprints = []
        _fingerprints = d.pop("fingerprints")
        for fingerprints_item_data in _fingerprints:
            fingerprints_item = Fingerprint.from_dict(fingerprints_item_data)

            fingerprints.append(fingerprints_item)

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

        users = cast(list[str], d.pop("users", UNSET))

        keys = d.pop("keys", UNSET)

        def _parse_responsible_user(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        responsible_user = _parse_responsible_user(d.pop("responsible_user", UNSET))

        robot_account = cls(
            url=url,
            uuid=uuid,
            created=created,
            modified=modified,
            resource=resource,
            type_=type_,
            backend_id=backend_id,
            fingerprints=fingerprints,
            username=username,
            description=description,
            error_message=error_message,
            error_traceback=error_traceback,
            state=state,
            users=users,
            keys=keys,
            responsible_user=responsible_user,
        )

        robot_account.additional_properties = d
        return robot_account

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
