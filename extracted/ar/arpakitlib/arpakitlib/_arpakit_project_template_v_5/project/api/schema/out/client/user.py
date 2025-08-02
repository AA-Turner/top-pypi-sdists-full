from __future__ import annotations

import datetime as dt
from typing import Any

from project.api.schema.out.client.common import SimpleDBMClientSO
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM


class User1ClientSO(SimpleDBMClientSO):
    fullname: str | None
    email: str | None
    username: str | None
    roles: list[str]
    is_active: bool
    is_verified: bool
    tg_id: int | None
    tg_bot_last_action_dt: dt.datetime | None
    tg_data: dict[str, Any]

    roles_has_admin: bool
    roles_has_client: bool
    allowed_roles: list[str]
    tg_data_first_name: str | None
    tg_data_last_name: str | None
    tg_data_language_code: str | None
    tg_data_username: str | None
    tg_data_at_username: str | None
    tg_data_fullname: str | None
    tg_data_link_by_username: str | None
    email_prefix: str | None

    @classmethod
    def from_dbm(cls, *, simple_dbm: UserDBM, **kwargs) -> User1ClientSO:
        return cls.model_validate(simple_dbm.simple_dict(
            include_columns_and_sd_properties=cls.model_fields.keys()
        ))
