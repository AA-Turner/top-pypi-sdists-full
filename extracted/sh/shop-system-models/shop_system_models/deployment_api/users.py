# import re


from pydantic import BaseModel


class UserHeadersUpdatingModel(BaseModel):
    tg_id: int
    first_name: str | None = ""
    last_name: str | None = ""
    tg_language: str | None = ""
    username: str | None = None


class UserModel(UserHeadersUpdatingModel):
    password: str | None = None
    preview_url: str | None = None
    rights: str = "user"
    delivery_addresses: list[str] | None = None


class ReferralUser(BaseModel):
    tg_id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None


class InvitedUser(ReferralUser):
    tg_language: str | None = ""
    language: str | None = None


class UserDeploymentModel(BaseModel):
    id: str
    first_name: str
    last_name: str | None = None
    username: str | None = None
    tg_id: int
    tg_language: str = ""
    invited_by_id: str | None = None
    invited_by_user: ReferralUser | None = None
    roles: list[str] | None = None
    shops_available: int = 5
    invited_users: list[InvitedUser] | None
