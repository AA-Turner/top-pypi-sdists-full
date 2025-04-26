from pydantic import BaseModel


class AccioRequest(BaseModel):
    object_name: str


class AccioResponse(BaseModel):
    success: bool
