from typing import Dict

from pydantic import BaseModel


class SerializationMetadata(BaseModel):
    framework: str
    framework_version: str
    serialization_format: str
    runtime: str
    runtime_version: str

    @classmethod
    def from_json(cls, json_dict: Dict) -> "SerializationMetadata":
        return cls.model_validate(json_dict)
