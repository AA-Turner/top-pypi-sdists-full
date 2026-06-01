import json

from pydantic import BaseModel, model_validator


class FormDataModel(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return json.loads(value)
        return value
