from __future__ import annotations

import datetime as dt

from project.api.schema.common import BaseSO
from project.sqlalchemy_db_.sqlalchemy_model import SimpleDBM


class SimpleDBMClientSO(BaseSO):
    id: int
    long_id: str
    slug: str | None
    creation_dt: dt.datetime

    entity_name: str

    @classmethod
    def from_dbm(cls, *, simple_dbm: SimpleDBM, **kwargs) -> SimpleDBMClientSO:
        return cls.model_validate(simple_dbm.simple_dict(
            include_columns_and_sd_properties=cls.model_fields.keys()
        ))
