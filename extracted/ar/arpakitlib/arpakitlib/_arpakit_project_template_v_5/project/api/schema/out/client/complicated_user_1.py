from __future__ import annotations

from project.api.schema.out.client.user import User1ClientSO
from project.api.schema.out.client.user_token import UserToken1ClientSO
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM


class ComplicatedUser1ClientSO(User1ClientSO):
    user_tokens: list[UserToken1ClientSO]

    @classmethod
    def from_dbm(cls, *, simple_dbm: UserDBM, **kwargs) -> ComplicatedUser1ClientSO:
        return cls.model_validate(simple_dbm.simple_dict(
            include_columns_and_sd_properties=cls.model_fields.keys(),
            kwargs={
                "user_tokens": [
                    UserToken1ClientSO.from_dbm(simple_dbm=d)
                    for d in simple_dbm.user_tokens
                ]
            }
        ))
