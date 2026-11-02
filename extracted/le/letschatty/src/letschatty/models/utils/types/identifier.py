from typing import Any
from typing import Annotated
from bson import ObjectId
from pydantic import BeforeValidator, AfterValidator


def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return str(v)
    if ObjectId.is_valid(v):
        return v
    raise ValueError("Invalid ObjectId")


StrObjectId = Annotated[str, BeforeValidator(str), AfterValidator(validate_object_id)]
