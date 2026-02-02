from pydantic import BaseModel


class AuthorizationRequest(BaseModel):
    """Authorization request model"""

    Authorization: str

    @property
    def token(self):
        return self.Authorization


class AuthenticationRequest(BaseModel):
    """Authentication request model"""

    user: str
    authcode: str


class User(BaseModel):
    """User model."""

    principal: str


class LoginResponse(BaseModel):
    """Login response model"""

    access_token: str

    def as_dict(self):
        return {"access_token": self.access_token}


class SuccessResponse(BaseModel):
    """Success response for simple http request."""

    message: str


if __name__ == "__main__":
    args = {
        "Authorization": "123",
    }
    request = AuthorizationRequest(**args)
    print(request)
