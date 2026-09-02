from pydantic import BaseModel


class Tokens(BaseModel):
    """Pydantic model to describe the tokens returned from /api/rest/v1/oauth/token"""

    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
