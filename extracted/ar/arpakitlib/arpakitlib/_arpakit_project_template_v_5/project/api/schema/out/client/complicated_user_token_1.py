from __future__ import annotations

from project.api.schema.out.client.user import User1ClientSO
from project.api.schema.out.client.user_token import UserToken1ClientSO
from project.sqlalchemy_db_.sqlalchemy_model import UserTokenDBM


class ComplicatedUserToken1ClientSO(UserToken1ClientSO):
    user: User1ClientSO

    @classmethod
    def from_dbm(cls, *, simple_dbm: UserTokenDBM, **kwargs) -> ComplicatedUserToken1ClientSO:
        simple_dict = simple_dbm.simple_dict(
            include_columns_and_sd_properties=cls.model_fields.keys(),
            kwargs={
                "user": User1ClientSO.from_dbm(simple_dbm=simple_dbm.user)
            }
        )
        return cls.model_validate(simple_dict)
