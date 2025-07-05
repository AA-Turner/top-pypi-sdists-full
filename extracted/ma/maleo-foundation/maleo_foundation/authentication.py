from pydantic import BaseModel, ConfigDict, Field, model_validator
from starlette.authentication import AuthCredentials, BaseUser
from typing import Optional, Self, Sequence
from maleo_foundation.enums import BaseEnums
from maleo_foundation.models.transfers.general.token import MaleoFoundationTokenGeneralTransfers

class Token(BaseModel):
    type: BaseEnums.TokenType = Field(..., description="Token's type")
    payload: MaleoFoundationTokenGeneralTransfers.DecodePayload = Field(..., description="Token's payload")

class Credentials(AuthCredentials):
    def __init__(
        self,
        token: Optional[Token] = None,
        scopes: Optional[Sequence[str]] = None
    ) -> None:
        self._token = token
        super().__init__(scopes)

    @property
    def token(self) -> Optional[Token]:
        return self._token

class CredentialsModel(BaseModel):
    token: Optional[Token] = Field(None, description="Token")
    scopes: Optional[Sequence[str]] = Field(None, description="Scopes")

class User(BaseUser):
    def __init__(
        self,
        authenticated: bool = True,
        username: str = "",
        email: str = ""
    ) -> None:
        self._authenticated = authenticated
        self._username = username
        self._email = email

    @property
    def is_authenticated(self) -> bool:
        return self._authenticated

    @property
    def display_name(self) -> str:
        return self._username

    @property
    def identity(self) -> str:
        return self._email

class UserModel(BaseModel):
    is_authenticated: bool = Field(True, description="Authenticated")
    display_name: str = Field("", description="Username")
    identity: str = Field("", description="Email")

class Authentication(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    credentials: Credentials = Field(..., description="Credentials's information", exclude=True)
    credentials_model: CredentialsModel = Field(default_factory=CredentialsModel, description="Credential's model", serialization_alias="credentials")
    user: User = Field(..., description="User's information", exclude=True)
    user_model: UserModel = Field(default_factory=UserModel, description="User's model", serialization_alias="user")

    @model_validator(mode="after")
    def define_models(self) -> Self:
        self.credentials_model.token = self.credentials.token
        self.credentials_model.scopes = self.credentials.scopes
        self.user_model.is_authenticated = self.user.is_authenticated
        self.user_model.display_name = self.user.display_name
        self.user_model.identity = self.user.identity
        return self