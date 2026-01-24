from functools import cached_property

import httpx
from pydantic import BaseModel, ConfigDict, model_validator
from typing_extensions import Self

from fitrequest.errors import MultipleAuthenticationError
from fitrequest.fit_var import ValidFitVar
from fitrequest.token_auth import HeaderTokenAuth, ParamsTokenAuth


class Auth(BaseModel):
    username: ValidFitVar = None
    password: ValidFitVar = None
    header_token: ValidFitVar = None
    params_token: ValidFitVar = None
    custom: httpx.Auth | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True, extra='forbid', validate_default=True)

    @model_validator(mode='after')
    def validate_auth_method(self) -> Self:
        auth_method_count = sum(
            method is not None
            for method in [
                self.custom,
                self.header_token,
                self.params_token,
                (self.username and self.password),
            ]
        )
        if auth_method_count > 1:
            raise MultipleAuthenticationError
        return self

    @cached_property
    def authentication(self) -> httpx.Auth | None:
        if self.custom:
            return self.custom
        if self.username and self.password:
            return httpx.BasicAuth(str(self.username), str(self.password))
        if self.header_token:
            return HeaderTokenAuth(str(self.header_token))
        if self.params_token:
            return ParamsTokenAuth(str(self.params_token))
        return None
