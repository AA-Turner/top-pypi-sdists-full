from typing import (
    Any,
    Dict,
    Type,
    TypeVar,
    Tuple,
    Optional,
    BinaryIO,
    TextIO,
    TYPE_CHECKING,
)

from typing import List


import attr

from ..types import UNSET, Unset

from typing import Union
from typing import cast, List
from typing import Optional
from ..types import UNSET, Unset


T = TypeVar("T", bound="GetWhoamiResponse200")


@attr.s(auto_attribs=True)
class GetWhoamiResponse200:
    """
    ### Attributes:
    * `username (Union[Unset, str])`: None Example: admin
    * `email (Union[Unset, None, str])`: None
    * `async_channel (Union[Unset, str])`: None Example: 051a3050-bed1-4059-98db-533547787ac6
    * `os_jwt (Union[Unset, str])`: None Example: eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiJ9.eyJ0aW1icl9iYXNlX3VybCI6Imh0dHBzOi8vZnVzaW9uLmRldi5vY3Rvc3Rhci5jb20iLCJpZCI6MywidXNlcm5hbWUiOiJhZG1pbiIsImVtYWlsIjoiYWRtaW5AZmFiLm9yZyIsInJvbGVzIjpbIkFkbWluIl0sInRpbWJyX3Rva2VuX2VuYyI6IjA0OWJmZjIyMjcwOTUxNzUyMmYzYjI0MjE2NTAzZGJhNzFhMDliMzY1OTNkMjZiZmI4MWIyM2ZmOWM4ODNhNzQzMWVlM2I4MWFiNDY5YzE0ZjFlMDQ2ZTk2NjRjMmRmMzVmNThhMjg5OGYyYzFiYTFlZjVmZjUyYmFjNjQ3N2FlYTQzYjdkZmE4NTk1MGI4ZWFmNzRiYWUwNGIxZTI2Yzg2NTJiMTQ0NDBiNjJjMjU5MWQ0NGE5MGRlNTk1OWFkMGRlOTliZTI1ZTY3YWMxM2UzZGZjYTExMzNkODFkNmZiZWVjNmU0ZTZmMTA0Y2VkNzBiNGQ1MTBlOWM0YTQ5OWIyY2E4ZmIwZTMzNzk1OGRhMGM2MjlmNjc3ZDIwZjVlYTE3YjQwMzNmZWZjZTg4NTdjNmExNGJjNjE3ZDZlM2MyMmQ2NjQ2NjQiLCJhc3luY19jaGFubmVsIjoiMDUxYTMwNTAtYmVkMS00MDU5LTk4ZGItNTMzNTQ3Nzg3YWM2Iiwic3ViIjozLCJpYXQiOjE3NDQzMTUzMzcsImV4cCI6MTc0NTYxMTMzNywiaXNzIjoib2N0b3N0YXJfcGxhdGZvcm0ifQ.u_ilbjAlQRK8tirf3WwA3zrOZBISIzwMJq_xm7o3gojALf7BkOymzdy1nON3g4euhDSPAUDlRa7ItcU5YNCgRA
    * `is_superuser (Union[Unset, bool])`: None Example: True
    * `roles (Union[Unset, List[str]])`: None Example: ['Admin']
    * `timbr_roles (Union[Unset, List[str]])`: None Example: ['admin']
    """

    username: Union[Unset, str] = UNSET
    email: Union[Unset, None, str] = UNSET
    async_channel: Union[Unset, str] = UNSET
    os_jwt: Union[Unset, str] = UNSET
    is_superuser: Union[Unset, bool] = UNSET
    roles: Union[Unset, List[str]] = UNSET
    timbr_roles: Union[Unset, List[str]] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        username = self.username
        email = self.email
        async_channel = self.async_channel
        os_jwt = self.os_jwt
        is_superuser = self.is_superuser
        roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.roles, Unset):
            roles = self.roles

        timbr_roles: Union[Unset, List[str]] = UNSET
        if not isinstance(self.timbr_roles, Unset):
            timbr_roles = self.timbr_roles

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if username is not UNSET:
            field_dict["username"] = username
        if email is not UNSET:
            field_dict["email"] = email
        if async_channel is not UNSET:
            field_dict["async_channel"] = async_channel
        if os_jwt is not UNSET:
            field_dict["os_jwt"] = os_jwt
        if is_superuser is not UNSET:
            field_dict["is_superuser"] = is_superuser
        if roles is not UNSET:
            field_dict["roles"] = roles
        if timbr_roles is not UNSET:
            field_dict["timbr_roles"] = timbr_roles

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        username = d.pop("username", UNSET)

        email = d.pop("email", UNSET)

        async_channel = d.pop("async_channel", UNSET)

        os_jwt = d.pop("os_jwt", UNSET)

        is_superuser = d.pop("is_superuser", UNSET)

        roles = cast(List[str], d.pop("roles", UNSET))

        timbr_roles = cast(List[str], d.pop("timbr_roles", UNSET))

        get_whoami_response_200 = cls(
            username=username,
            email=email,
            async_channel=async_channel,
            os_jwt=os_jwt,
            is_superuser=is_superuser,
            roles=roles,
            timbr_roles=timbr_roles,
        )

        get_whoami_response_200.additional_properties = d
        return get_whoami_response_200

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
