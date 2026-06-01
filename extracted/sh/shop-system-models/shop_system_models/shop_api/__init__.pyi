from pydantic import BaseModel

class MetaBaseModel(BaseModel):
    metadata: dict
