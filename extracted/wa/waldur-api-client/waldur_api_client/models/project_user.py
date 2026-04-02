import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.offering_user_state import OfferingUserState
from ..types import UNSET, Unset

T = TypeVar("T", bound="ProjectUser")


@_attrs_define
class ProjectUser:
    """
    Attributes:
        url (str):
        uuid (UUID):
        username (str): Required. 128 characters or fewer. Lowercase letters, numbers and @/./+/-/_ characters
        full_name (str):
        role (str):
        expiration_time (Union[None, datetime.datetime]):
        offering_user_username (Union[None, str]):
        offering_user_state (Union[None, OfferingUserState]):
        email (Union[Unset, str]):
    """

    url: str
    uuid: UUID
    username: str
    full_name: str
    role: str
    expiration_time: Union[None, datetime.datetime]
    offering_user_username: Union[None, str]
    offering_user_state: Union[None, OfferingUserState]
    email: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        url = self.url

        uuid = str(self.uuid)

        username = self.username

        full_name = self.full_name

        role = self.role

        expiration_time: Union[None, str]
        if isinstance(self.expiration_time, datetime.datetime):
            expiration_time = self.expiration_time.isoformat()
        else:
            expiration_time = self.expiration_time

        offering_user_username: Union[None, str]
        offering_user_username = self.offering_user_username

        offering_user_state: Union[None, str]
        if isinstance(self.offering_user_state, OfferingUserState):
            offering_user_state = self.offering_user_state.value
        else:
            offering_user_state = self.offering_user_state

        email = self.email

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "url": url,
                "uuid": uuid,
                "username": username,
                "full_name": full_name,
                "role": role,
                "expiration_time": expiration_time,
                "offering_user_username": offering_user_username,
                "offering_user_state": offering_user_state,
            }
        )
        if email is not UNSET:
            field_dict["email"] = email

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        username = d.pop("username")

        full_name = d.pop("full_name")

        role = d.pop("role")

        def _parse_expiration_time(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expiration_time_type_0 = isoparse(data)

                return expiration_time_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        expiration_time = _parse_expiration_time(d.pop("expiration_time"))

        def _parse_offering_user_username(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        offering_user_username = _parse_offering_user_username(d.pop("offering_user_username"))

        def _parse_offering_user_state(data: object) -> Union[None, OfferingUserState]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                offering_user_state_type_0 = OfferingUserState(data)

                return offering_user_state_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, OfferingUserState], data)

        offering_user_state = _parse_offering_user_state(d.pop("offering_user_state"))

        email = d.pop("email", UNSET)

        project_user = cls(
            url=url,
            uuid=uuid,
            username=username,
            full_name=full_name,
            role=role,
            expiration_time=expiration_time,
            offering_user_username=offering_user_username,
            offering_user_state=offering_user_state,
            email=email,
        )

        project_user.additional_properties = d
        return project_user

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
