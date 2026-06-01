"""Token issuance and verification models."""

from csrd.models import BaseModel


class TokenRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    """JWT token issuance response."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


class VerifyRequest(BaseModel):
    token: str


class VerifyClaims(BaseModel):
    """JWT claim fields returned by the verify endpoint."""

    sub: str
    user_name: str
    authorities: list[str]
    iat: int
    exp: int
    iss: str
    aud: str


class VerifyResponse(BaseModel):
    """Token verification response."""

    active: bool
    claims: VerifyClaims
