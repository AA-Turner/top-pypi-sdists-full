from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from worker_automate_hub.models.dao.rpa_robo import RpaRobo


class RpaFila(BaseModel):
    uuidFila: Optional[str] = Field(None, alias="uuidFila")
    robos: Optional[List[RpaRobo]] = Field(None, alias="robos")
    fkRobos: Optional[str] = Field(None, alias="fkRobos")
    uuidProcesso: str = Field(..., alias="uuidProcesso")
    prioridade: int = Field(..., alias="prioridade")
    configEntrada: Optional[dict] = Field(None, alias="configEntrada")
    dtLeituraFila: Optional[datetime] = Field(None, alias="dtLeituraFila")
    lock: Optional[bool] = Field(None, alias="lock")
    mutarNotificacao: Optional[int] = Field(None, alias="mutarNotificacao")

    class Config:
        populate_by_name = True
