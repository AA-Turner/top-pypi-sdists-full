from pydantic import BaseModel


class BasicResponseModel(BaseModel):
    message: str
