from __future__ import annotations

from typing import Optional
from warnings import warn

from jsonschema.exceptions import ValidationError as JsonSchemaValidationError
from pydantic import VERSION as PYDANTIC_VERSION
from pydantic import (
    BaseModel as PydanticBaseModel,
)
from pydantic import (
    ValidationError as PydanticValidationError,
)

from ..exceptions import SchemaValidationError, ValidationError

__all__ = ["BaseModel"]

IS_PYDANTIC_V1 = PYDANTIC_VERSION.startswith("1.")


class BaseModel(PydanticBaseModel):
    def __init__(self, dict_: Optional[dict] = None, **kwargs):  # noqa UP007
        init_kwargs = {**(dict_ or {}), **kwargs}
        try:
            super().__init__(**init_kwargs)
        except PydanticValidationError as e:
            raise ValidationError(e) from e

    def validate_schema(self):
        """This method is redundant since pydantic performs schema validation"""
        warn(
            "validate_schema is deprecated and will be removed in version 2.x",
            DeprecationWarning,
            stacklevel=2,
        )
        try:
            if IS_PYDANTIC_V1:
                _ = self.__class__(**self.__dict__)
                for validator in (
                    self.__pre_root_validators__ + self.__post_root_validators__
                ):
                    _ = validator(self.__class__, {**self.__dict__})
                object.__setattr__(self, "__dict__", {**self.__dict__})

            else:
                self.model_validate(self.as_dict(), strict=True, from_attributes=True)
        except (PydanticValidationError, ValidationError) as e:
            raise SchemaValidationError(
                JsonSchemaValidationError(message=str(e))
            ) from e

    def as_dict(self) -> dict:
        if IS_PYDANTIC_V1:
            return self.dict()  # noqa
        else:
            return self.model_dump()
