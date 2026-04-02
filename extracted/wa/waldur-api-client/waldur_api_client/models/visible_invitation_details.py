from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.execution_state_enum import ExecutionStateEnum
from ..models.invitation_state import InvitationState

T = TypeVar("T", bound="VisibleInvitationDetails")


@_attrs_define
class VisibleInvitationDetails:
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
        email (str): Invitation link will be sent to this email. Note that user can accept invitation with different
            email.
        error_message (str):
        execution_state (ExecutionStateEnum):
        state (InvitationState):
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
    email: str
    error_message: str
    execution_state: ExecutionStateEnum
    state: InvitationState
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

        email = self.email

        error_message = self.error_message

        execution_state = self.execution_state.value

        state = self.state.value

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
                "email": email,
                "error_message": error_message,
                "execution_state": execution_state,
                "state": state,
            }
        )

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

        email = d.pop("email")

        error_message = d.pop("error_message")

        execution_state = ExecutionStateEnum(d.pop("execution_state"))

        state = InvitationState(d.pop("state"))

        visible_invitation_details = cls(
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
            email=email,
            error_message=error_message,
            execution_state=execution_state,
            state=state,
        )

        visible_invitation_details.additional_properties = d
        return visible_invitation_details

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
