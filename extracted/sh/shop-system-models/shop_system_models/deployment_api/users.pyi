from pydantic import BaseModel

class UserHeadersUpdatingModel(BaseModel):
    tg_id: int
    first_name: str | None
    last_name: str | None
    tg_language: str | None
    username: str | None

class UserModel(UserHeadersUpdatingModel):
    password: str | None
    preview_url: str | None
    rights: str
    delivery_addresses: list[str] | None

class ReferralUser(BaseModel):
    tg_id: int
    first_name: str
    last_name: str | None
    username: str | None

class InvitedUser(ReferralUser):
    tg_language: str | None
    language: str | None

class UserDeploymentModel(BaseModel):
    id: str
    first_name: str
    last_name: str | None
    username: str | None
    tg_id: int
    tg_language: str
    invited_by_id: str | None
    invited_by_user: ReferralUser | None
    roles: list[str] | None
    shops_available: int
    invited_users: list[InvitedUser] | None
