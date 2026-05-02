from typing import Optional
from datetime import datetime
from uuid import UUID
from datamodel.types import Text
from asyncdb.models import Column, Model
from navigator_auth.conf import AUTH_DB_SCHEMA, AUTH_USERS_VIEW

class User(Model):
    """Basic User notation."""

    user_id: int = Column(required=False, primary_key=True)
    first_name: str
    last_name: str
    display_name: str
    email: str = Column(required=False, max=254)
    alt_email: str = Column(required=False, max=254)
    password: str = Column(required=False, max=128)
    last_login: datetime = Column(required=False)
    username: str = Column(required=False)
    is_superuser: bool = Column(required=True, default=False)
    is_active: bool = Column(required=True, default=True)
    is_new: bool = Column(required=True, default=True)
    is_staff: bool = Column(required=False, default=True)
    title: str = Column(equired=False, max=90)
    avatar: str = Column(max=512)
    associate_id: str = Column(required=False)
    associate_oid: str = Column(required=False)
    department_code: str = Column(required=False)
    position_id: str = Column(required=False)
    group_id: list = Column(required=False)
    groups: list = Column(required=False)
    program_id: list = Column(required=False)
    programs: list = Column(required=False)
    created_at: datetime = Column(required=False)

    class Meta:
        driver = "pg"
        name = AUTH_USERS_VIEW
        schema = AUTH_DB_SCHEMA
        description = 'View Model for getting Users.'
        strict = True
        frozen = False


class UserIdentity(Model):

    identity_id: UUID = Column(
        required=False,
        primary_key=True,
        db_default="auto",
        repr=False
    )
    display_name: str = Column(required=False)
    title: str = Column(required=False)
    nickname: str = Column(required=False)
    email: str = Column(required=False)
    phone: str = Column(required=False)
    short_bio: Text = Column(required=False)
    avatar: str = Column(required=False)
    user_id: User = Column(required=False, repr=False)
    auth_provider: str = Column(required=False)
    auth_data: Optional[dict] = Column(required=False, repr=False)
    attributes: Optional[dict] = Column(required=False, repr=False)
    created_at: datetime = Column(
        required=False,
        default=datetime.now(),
        repr=False
    )

    class Meta:
        driver = "pg"
        name = "user_identities"
        description = 'Manage User Identities.'
        schema = AUTH_DB_SCHEMA
        strict = True
