from pydantic import BaseModel as _BaseModel
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel

model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class BaseModel(_BaseModel):
    model_config = model_config
