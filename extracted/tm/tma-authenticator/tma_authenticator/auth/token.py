
from pydantic import BaseModel

from .users import User


class Token(User):
    initData: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    id_token: str
    expires_in: int
    scope: list[str] = []
