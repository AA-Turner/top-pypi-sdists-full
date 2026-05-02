from pydantic import BaseModel, Field


class RpaConfiguracao(BaseModel):
    uuidConfiguracao: str = Field(..., alias="uuidConfiguracao")
    labConfiguracao: str = Field(..., alias="labConfiguracao")
    conConfiguracao: dict = Field(None, alias="conConfiguracao")

    class Config:
        populate_by_name = True
