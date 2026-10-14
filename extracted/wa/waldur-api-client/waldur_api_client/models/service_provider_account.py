import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.offering_user_state import OfferingUserState
from ..models.runtime_state_enum import RuntimeStateEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="ServiceProviderAccount")


@_attrs_define
class ServiceProviderAccount:
    """
    Attributes:
        url (Union[Unset, str]):
        uuid (Union[Unset, UUID]):
        created (Union[Unset, datetime.datetime]):
        modified (Union[Unset, datetime.datetime]):
        service_provider (Union[Unset, str]):
        service_provider_uuid (Union[Unset, UUID]):
        service_provider_name (Union[Unset, str]):
        user (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        user_username (Union[None, Unset, str]):
        user_full_name (Union[None, Unset, str]):
        user_email (Union[None, Unset, str]):
        username (Union[None, Unset, str]):
        state (Union[Unset, OfferingUserState]):
        runtime_state (Union[Unset, RuntimeStateEnum]):
        is_restricted (Union[Unset, bool]):
        service_provider_comment (Union[Unset, str]): Additional comment for pending states like validation or account
            linking
        service_provider_comment_url (Union[Unset, str]): URL link for additional information or actions related to
            service provider comment
        uidnumber (Union[None, Unset, int]):
        primarygroup (Union[None, Unset, int]):
        login_shell (Union[None, Unset, str]):
        home_directory (Union[None, Unset, str]):
        offering_count (Union[Unset, int]):
    """

    url: Union[Unset, str] = UNSET
    uuid: Union[Unset, UUID] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    modified: Union[Unset, datetime.datetime] = UNSET
    service_provider: Union[Unset, str] = UNSET
    service_provider_uuid: Union[Unset, UUID] = UNSET
    service_provider_name: Union[Unset, str] = UNSET
    user: Union[Unset, str] = UNSET
    user_uuid: Union[Unset, UUID] = UNSET
    user_username: Union[None, Unset, str] = UNSET
    user_full_name: Union[None, Unset, str] = UNSET
    user_email: Union[None, Unset, str] = UNSET
    username: Union[None, Unset, str] = UNSET
    state: Union[Unset, OfferingUserState] = UNSET
    runtime_state: Union[Unset, RuntimeStateEnum] = UNSET
    is_restricted: Union[Unset, bool] = UNSET
    service_provider_comment: Union[Unset, str] = UNSET
    service_provider_comment_url: Union[Unset, str] = UNSET
    uidnumber: Union[None, Unset, int] = UNSET
    primarygroup: Union[None, Unset, int] = UNSET
    login_shell: Union[None, Unset, str] = UNSET
    home_directory: Union[None, Unset, str] = UNSET
    offering_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
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

        service_provider = self.service_provider

        service_provider_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.service_provider_uuid, Unset):
            service_provider_uuid = str(self.service_provider_uuid)

        service_provider_name = self.service_provider_name

        user = self.user

        user_uuid: Union[Unset, str] = UNSET
        if not isinstance(self.user_uuid, Unset):
            user_uuid = str(self.user_uuid)

        user_username: Union[None, Unset, str]
        if isinstance(self.user_username, Unset):
            user_username = UNSET
        else:
            user_username = self.user_username

        user_full_name: Union[None, Unset, str]
        if isinstance(self.user_full_name, Unset):
            user_full_name = UNSET
        else:
            user_full_name = self.user_full_name

        user_email: Union[None, Unset, str]
        if isinstance(self.user_email, Unset):
            user_email = UNSET
        else:
            user_email = self.user_email

        username: Union[None, Unset, str]
        if isinstance(self.username, Unset):
            username = UNSET
        else:
            username = self.username

        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        runtime_state: Union[Unset, str] = UNSET
        if not isinstance(self.runtime_state, Unset):
            runtime_state = self.runtime_state.value

        is_restricted = self.is_restricted

        service_provider_comment = self.service_provider_comment

        service_provider_comment_url = self.service_provider_comment_url

        uidnumber: Union[None, Unset, int]
        if isinstance(self.uidnumber, Unset):
            uidnumber = UNSET
        else:
            uidnumber = self.uidnumber

        primarygroup: Union[None, Unset, int]
        if isinstance(self.primarygroup, Unset):
            primarygroup = UNSET
        else:
            primarygroup = self.primarygroup

        login_shell: Union[None, Unset, str]
        if isinstance(self.login_shell, Unset):
            login_shell = UNSET
        else:
            login_shell = self.login_shell

        home_directory: Union[None, Unset, str]
        if isinstance(self.home_directory, Unset):
            home_directory = UNSET
        else:
            home_directory = self.home_directory

        offering_count = self.offering_count

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
        if service_provider is not UNSET:
            field_dict["service_provider"] = service_provider
        if service_provider_uuid is not UNSET:
            field_dict["service_provider_uuid"] = service_provider_uuid
        if service_provider_name is not UNSET:
            field_dict["service_provider_name"] = service_provider_name
        if user is not UNSET:
            field_dict["user"] = user
        if user_uuid is not UNSET:
            field_dict["user_uuid"] = user_uuid
        if user_username is not UNSET:
            field_dict["user_username"] = user_username
        if user_full_name is not UNSET:
            field_dict["user_full_name"] = user_full_name
        if user_email is not UNSET:
            field_dict["user_email"] = user_email
        if username is not UNSET:
            field_dict["username"] = username
        if state is not UNSET:
            field_dict["state"] = state
        if runtime_state is not UNSET:
            field_dict["runtime_state"] = runtime_state
        if is_restricted is not UNSET:
            field_dict["is_restricted"] = is_restricted
        if service_provider_comment is not UNSET:
            field_dict["service_provider_comment"] = service_provider_comment
        if service_provider_comment_url is not UNSET:
            field_dict["service_provider_comment_url"] = service_provider_comment_url
        if uidnumber is not UNSET:
            field_dict["uidnumber"] = uidnumber
        if primarygroup is not UNSET:
            field_dict["primarygroup"] = primarygroup
        if login_shell is not UNSET:
            field_dict["login_shell"] = login_shell
        if home_directory is not UNSET:
            field_dict["home_directory"] = home_directory
        if offering_count is not UNSET:
            field_dict["offering_count"] = offering_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
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

        service_provider = d.pop("service_provider", UNSET)

        _service_provider_uuid = d.pop("service_provider_uuid", UNSET)
        service_provider_uuid: Union[Unset, UUID]
        if isinstance(_service_provider_uuid, Unset):
            service_provider_uuid = UNSET
        else:
            service_provider_uuid = UUID(_service_provider_uuid)

        service_provider_name = d.pop("service_provider_name", UNSET)

        user = d.pop("user", UNSET)

        _user_uuid = d.pop("user_uuid", UNSET)
        user_uuid: Union[Unset, UUID]
        if isinstance(_user_uuid, Unset):
            user_uuid = UNSET
        else:
            user_uuid = UUID(_user_uuid)

        def _parse_user_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_username = _parse_user_username(d.pop("user_username", UNSET))

        def _parse_user_full_name(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_full_name = _parse_user_full_name(d.pop("user_full_name", UNSET))

        def _parse_user_email(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        user_email = _parse_user_email(d.pop("user_email", UNSET))

        def _parse_username(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        username = _parse_username(d.pop("username", UNSET))

        _state = d.pop("state", UNSET)
        state: Union[Unset, OfferingUserState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = OfferingUserState(_state)

        _runtime_state = d.pop("runtime_state", UNSET)
        runtime_state: Union[Unset, RuntimeStateEnum]
        if isinstance(_runtime_state, Unset):
            runtime_state = UNSET
        else:
            runtime_state = RuntimeStateEnum(_runtime_state)

        is_restricted = d.pop("is_restricted", UNSET)

        service_provider_comment = d.pop("service_provider_comment", UNSET)

        service_provider_comment_url = d.pop("service_provider_comment_url", UNSET)

        def _parse_uidnumber(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        uidnumber = _parse_uidnumber(d.pop("uidnumber", UNSET))

        def _parse_primarygroup(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        primarygroup = _parse_primarygroup(d.pop("primarygroup", UNSET))

        def _parse_login_shell(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        login_shell = _parse_login_shell(d.pop("login_shell", UNSET))

        def _parse_home_directory(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        home_directory = _parse_home_directory(d.pop("home_directory", UNSET))

        offering_count = d.pop("offering_count", UNSET)

        service_provider_account = cls(
            url=url,
            uuid=uuid,
            created=created,
            modified=modified,
            service_provider=service_provider,
            service_provider_uuid=service_provider_uuid,
            service_provider_name=service_provider_name,
            user=user,
            user_uuid=user_uuid,
            user_username=user_username,
            user_full_name=user_full_name,
            user_email=user_email,
            username=username,
            state=state,
            runtime_state=runtime_state,
            is_restricted=is_restricted,
            service_provider_comment=service_provider_comment,
            service_provider_comment_url=service_provider_comment_url,
            uidnumber=uidnumber,
            primarygroup=primarygroup,
            login_shell=login_shell,
            home_directory=home_directory,
            offering_count=offering_count,
        )

        service_provider_account.additional_properties = d
        return service_provider_account

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
