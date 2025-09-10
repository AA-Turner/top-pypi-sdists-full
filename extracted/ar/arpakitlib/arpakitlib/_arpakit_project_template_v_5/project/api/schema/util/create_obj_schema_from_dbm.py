from typing import Type

from arpakitlib.ar_sqlalchemy_util import BaseDBM
from pydantic import BaseModel


def create_obj_schema_from_dbm(*, schema: Type[BaseModel], dbm: BaseDBM, **kwargs) -> BaseModel:
    return schema.model_validate(dbm.simple_dict(
        include_columns_and_sd_properties=schema.model_fields.keys()
    ))
