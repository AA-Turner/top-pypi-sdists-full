import re
from pydantic import BaseModel, field_validator

class BasicAuthUser(BaseModel):
    """User model for basic authentication."""
    username: str
    password: str

    @field_validator('username')
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Username must be alphanumeric')
        return v