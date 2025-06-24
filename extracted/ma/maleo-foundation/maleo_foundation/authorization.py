from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field

TOKEN_SCHEME = HTTPBearer()

class Authorization(BaseModel):
    scheme: str = Field(..., description="Authorization's scheme")
    credentials: str = Field(..., description="Authorization's credentials")