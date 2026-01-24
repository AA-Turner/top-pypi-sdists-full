from re import match as re_match
from typing import Union

from pydantic import BaseModel, field_validator


class ScorerNameValidatorMixin(BaseModel):
    name: Union[str, None] = None

    @field_validator("name")
    def validate_name(cls, name: str) -> str:
        """Pydantic field validator for the name field to ensure not empty and no unwanted special characters."""
        if (
            name is not None
        ):  # Allow None to be passed in for optional fields, especially in the case of an UpdateRequest
            if name == "":
                raise ValueError(f"Invalid {cls.__name__}: The name of the scorer cannot be empty.")
            if not re_match(r"^[\w -]+$", name):
                raise ValueError(
                    f"Invalid {cls.__name__}: The scorer cannot contain special characters -- only letters, numbers, space, - and _."
                )
        return name
