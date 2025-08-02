from pydantic import BaseModel
from typing import Optional

class CreateDDLResponse(BaseModel):
    ddl: str
    ddl_path: Optional[str] = None
