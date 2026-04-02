import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.execution_state_enum import ExecutionStateEnum
from ..models.invitation_state_enum import InvitationStateEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="Invitation")


@_attrs_define
class Invitation:
    """
    Attributes:
        scope_uuid (UUID): UUID of the invitation scope (Customer or Project)
        scope_name (str): Name of the invitation scope
        scope_description (str): Description of the invitation scope
        scope_type (Union[None, str]): Type of the invitation scope (e.g., 'customer', 'project')
        customer_uuid (UUID): UUID of the customer organization
        customer_name (str): Name of the customer organization
        role_name (str): Name of the role being granted (e.g., 'PROJECT.ADMIN')
        role_description (str): Description of the role being granted
        created_by_full_name (str): Full name of the user who created this invitation
        created_by_username (str): Username of the user who created this invitation
        created_by_image (str): Profile image of the user who created this invitation
        url (str):
        uuid (UUID):
        role (UUID): UUID of the role to grant to the invited user
        created (datetime.datetime):
        expires (datetime.datetime): Expiration date and time of the invitation
        email (str): Invitation link will be sent to this email. Note that user can accept invitation with different
            email.
        state (InvitationStateEnum):
        error_message (str):
        execution_state (ExecutionStateEnum):
        full_name (Union[Unset, str]):
        native_name (Union[Unset, str]):
        phone_number (Union[Unset, str]):
        organization (Union[Unset, str]):
        job_title (Union[Unset, str]):
        civil_number (Union[Unset, str]): Civil number of invited user. If civil number is not defined any user can
            accept invitation.
        extra_invitation_text (Union[Unset, str]):
    """

    scope_uuid: UUID
    scope_name: str
    scope_description: str
    scope_type: Union[None, str]
    customer_uuid: UUID
    customer_name: str
    role_name: str
    role_description: str
    created_by_full_name: str
    created_by_username: str
    created_by_image: str
    url: str
    uuid: UUID
    role: UUID
    created: datetime.datetime
    expires: datetime.datetime
    email: str
    state: InvitationStateEnum
    error_message: str
    execution_state: ExecutionStateEnum
    full_name: Union[Unset, str] = UNSET
    native_name: Union[Unset, str] = UNSET
    phone_number: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET
    job_title: Union[Unset, str] = UNSET
    civil_number: Union[Unset, str] = UNSET
    extra_invitation_text: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        scope_uuid = str(self.scope_uuid)

        scope_name = self.scope_name

        scope_description = self.scope_description

        scope_type: Union[None, str]
        scope_type = self.scope_type

        customer_uuid = str(self.customer_uuid)

        customer_name = self.customer_name

        role_name = self.role_name

        role_description = self.role_description

        created_by_full_name = self.created_by_full_name

        created_by_username = self.created_by_username

        created_by_image = self.created_by_image

        url = self.url

        uuid = str(self.uuid)

        role = str(self.role)

        created = self.created.isoformat()

        expires = self.expires.isoformat()

        email = self.email

        state = self.state.value

        error_message = self.error_message

        execution_state = self.execution_state.value

        full_name = self.full_name

        native_name = self.native_name

        phone_number = self.phone_number

        organization = self.organization

        job_title = self.job_title

        civil_number = self.civil_number

        extra_invitation_text = self.extra_invitation_text

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "scope_uuid": scope_uuid,
                "scope_name": scope_name,
                "scope_description": scope_description,
                "scope_type": scope_type,
                "customer_uuid": customer_uuid,
                "customer_name": customer_name,
                "role_name": role_name,
                "role_description": role_description,
                "created_by_full_name": created_by_full_name,
                "created_by_username": created_by_username,
                "created_by_image": created_by_image,
                "url": url,
                "uuid": uuid,
                "role": role,
                "created": created,
                "expires": expires,
                "email": email,
                "state": state,
                "error_message": error_message,
                "execution_state": execution_state,
            }
        )
        if full_name is not UNSET:
            field_dict["full_name"] = full_name
        if native_name is not UNSET:
            field_dict["native_name"] = native_name
        if phone_number is not UNSET:
            field_dict["phone_number"] = phone_number
        if organization is not UNSET:
            field_dict["organization"] = organization
        if job_title is not UNSET:
            field_dict["job_title"] = job_title
        if civil_number is not UNSET:
            field_dict["civil_number"] = civil_number
        if extra_invitation_text is not UNSET:
            field_dict["extra_invitation_text"] = extra_invitation_text

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        scope_uuid = UUID(d.pop("scope_uuid"))

        scope_name = d.pop("scope_name")

        scope_description = d.pop("scope_description")

        def _parse_scope_type(data: object) -> Union[None, str]:
            if data is None:
                return data
            return cast(Union[None, str], data)

        scope_type = _parse_scope_type(d.pop("scope_type"))

        customer_uuid = UUID(d.pop("customer_uuid"))

        customer_name = d.pop("customer_name")

        role_name = d.pop("role_name")

        role_description = d.pop("role_description")

        created_by_full_name = d.pop("created_by_full_name")

        created_by_username = d.pop("created_by_username")

        created_by_image = d.pop("created_by_image")

        url = d.pop("url")

        uuid = UUID(d.pop("uuid"))

        role = UUID(d.pop("role"))

        created = isoparse(d.pop("created"))

        expires = isoparse(d.pop("expires"))

        email = d.pop("email")

        state = InvitationStateEnum(d.pop("state"))

        error_message = d.pop("error_message")

        execution_state = ExecutionStateEnum(d.pop("execution_state"))

        full_name = d.pop("full_name", UNSET)

        native_name = d.pop("native_name", UNSET)

        phone_number = d.pop("phone_number", UNSET)

        organization = d.pop("organization", UNSET)

        job_title = d.pop("job_title", UNSET)

        civil_number = d.pop("civil_number", UNSET)

        extra_invitation_text = d.pop("extra_invitation_text", UNSET)

        invitation = cls(
            scope_uuid=scope_uuid,
            scope_name=scope_name,
            scope_description=scope_description,
            scope_type=scope_type,
            customer_uuid=customer_uuid,
            customer_name=customer_name,
            role_name=role_name,
            role_description=role_description,
            created_by_full_name=created_by_full_name,
            created_by_username=created_by_username,
            created_by_image=created_by_image,
            url=url,
            uuid=uuid,
            role=role,
            created=created,
            expires=expires,
            email=email,
            state=state,
            error_message=error_message,
            execution_state=execution_state,
            full_name=full_name,
            native_name=native_name,
            phone_number=phone_number,
            organization=organization,
            job_title=job_title,
            civil_number=civil_number,
            extra_invitation_text=extra_invitation_text,
        )

        invitation.additional_properties = d
        return invitation

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
