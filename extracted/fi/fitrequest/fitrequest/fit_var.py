import os
from functools import cached_property
from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, Field, model_serializer

from fitrequest.aws_var import AWSRegionEnum, AWSSecretTypeEnum, AWSVar


class FitVar(BaseModel):
    aws_path: str | None = None
    aws_type: AWSSecretTypeEnum = AWSSecretTypeEnum.ssm
    aws_region: AWSRegionEnum = AWSRegionEnum.eu_central_1

    env_name: str | None = None
    init_value: str | None = None

    @cached_property
    def aws_value(self) -> str | None:
        if not self.aws_path:
            return None
        return AWSVar(region=self.aws_region, path=self.aws_path, secret_type=self.aws_type).value

    @cached_property
    def env_value(self) -> str | None:
        if not self.env_name:
            return None
        return os.environ.get(self.env_name)

    def __str__(self) -> str:
        """
        Return value with the following priority:
        1/ init value (manually set field on instance initialization)
        2/ environment variable
        3/ aws value if aws_type and aws_path are set
        4/ default '' value
        """
        return self.init_value or self.env_value or self.aws_value or ''

    @model_serializer
    def fit_var_serializer(self) -> str | None:
        return str(self)


def validate_init_value(value: Any) -> FitVar | None:
    if isinstance(value, str):
        return FitVar(init_value=value)
    if isinstance(value, FitVar):
        return value
    if isinstance(value, dict):
        return FitVar(**value)
    return None


ValidFitVar = Annotated[
    FitVar | dict | str | None,
    Field(validate_default=True),
    BeforeValidator(validate_init_value),
]
