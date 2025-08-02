from typing import Any

from pydantic import ConfigDict, BaseModel


class BaseSchema(BaseModel):
    model_config = ConfigDict(extra="ignore", arbitrary_types_allowed=True, from_attributes=True)

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        if not (
                cls.__name__.endswith("SO")
                or cls.__name__.endswith("SI")
                or cls.__name__.endswith("SchemaIn")
                or cls.__name__.endswith("SchemaOut")
        ):
            raise ValueError("APISchema class should ends with SO | SI | SchemaIn | SchemaOut")
        super().__init_subclass__(**kwargs)


class BaseSI(BaseSchema):
    pass


class BaseSO(BaseSchema):
    pass
