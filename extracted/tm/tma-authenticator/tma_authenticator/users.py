from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    username: Optional[str] = ""
    tg_id: Optional[int] = None
    tg_language: Optional[str] = ""
    wallet_address: Optional[str] = None


class UserDB(User):
    is_service: bool = False
    cache_key: Optional[str] = None
