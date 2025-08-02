from __future__ import annotations

from project.api.schema.out.general.common import SimpleDBMGeneralSO
from project.sqlalchemy_db_.sqlalchemy_model import ApiKeyDBM


class ApiKey1GeneralSO(SimpleDBMGeneralSO):
    title: str | None
    value: str
    is_active: bool

    @classmethod
    def from_dbm(cls, *, simple_dbm: ApiKeyDBM, **kwargs) -> ApiKey1GeneralSO:
        return cls.model_validate(simple_dbm.simple_dict(
            include_columns_and_sd_properties=cls.model_fields.keys()
        ))
