from types import SimpleNamespace
from typing import Optional

from pydantic import BaseModel

PaginationDefaults = SimpleNamespace(starting_token=0, limit=100)


class PaginationRequest(BaseModel):
    starting_token: int = PaginationDefaults.starting_token
    limit: int = PaginationDefaults.limit


class PaginationResponse(PaginationRequest):
    paginated: bool = False
    next_starting_token: Optional[int] = None
