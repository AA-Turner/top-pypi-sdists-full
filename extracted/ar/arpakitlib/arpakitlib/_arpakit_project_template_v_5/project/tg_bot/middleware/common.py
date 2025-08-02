from typing import Any

from pydantic import BaseModel, ConfigDict

from project.sqlalchemy_db_.sqlalchemy_model import UserDBM


class MiddlewareDataTgBot(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)

    current_user_dbm: UserDBM | None = None
    current_user_dbm_just_created: bool | None = None
    additional_data: dict[str, Any] = {}
