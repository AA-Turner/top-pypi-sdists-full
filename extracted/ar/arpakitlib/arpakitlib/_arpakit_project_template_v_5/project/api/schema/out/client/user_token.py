from __future__ import annotations

from project.api.schema.out.client.common import SimpleDBMClientSO
from project.sqlalchemy_db_.sqlalchemy_model import UserTokenDBM


class UserToken1ClientSO(SimpleDBMClientSO):
    value: str
    user_id: int
    is_active: bool

    @classmethod
    def from_dbm(cls, *, simple_dbm: UserTokenDBM, **kwargs) -> UserToken1ClientSO:
        return cls.model_validate(simple_dbm.simple_dict(
            include_columns_and_sd_properties=cls.model_fields.keys()
        ))
