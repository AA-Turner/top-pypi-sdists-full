from pydantic import BaseModel


class RpaSistemaDTO(BaseModel):
    sistema: str
    timeout: float

    class Config:
        populate_by_name = True
