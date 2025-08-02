from pydantic import ConfigDict, BaseModel


class BaseAM(BaseModel):
    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True, from_attributes=True)
