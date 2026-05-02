from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class RpaRobo(BaseModel):
    uuidRobo: Optional[str] = Field(None, alias="uuidRobo")
    nomRobo: str = Field(..., alias="nomRobo")
    desRobo: str = Field(..., alias="desRobo")
    vmRobo: Optional[str] = Field(None, alias="vmRobo")
    ativo: bool = Field(..., alias="ativo")
    ipVm: Optional[str] = Field(None, alias="ipVm")
    userVm: Optional[str] = Field(None, alias="userVm")
    passwordVm: Optional[str] = Field(None, alias="passwordVm")
    versao: Optional[str] = Field(None, alias="versao")
    tipoRobo: str = Field(..., alias="tipoRobo")
    disponibilidade: Optional[str] = Field(None, alias="disponibilidade")
    provisionar: Optional[str] = Field(None, alias="provisionar")
    gitAppName: Optional[str] = Field(None, alias="gitAppName")
    controllerRobo: Optional[str] = Field(None, alias="controllerRobo")
    cloudStatus: Optional[str] = Field(None, alias="cloudStatus")
    lastAlive: Optional[str] = Field(None, alias="lastAlive")
    observacao: Optional[str] = Field(None, alias="observacao")
    createdAt: Optional[datetime] = Field(None, alias="createdAt")
    updatedAt: Optional[datetime] = Field(None, alias="updatedAt")

    class Config:
        populate_by_name = True
