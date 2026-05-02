from datetime import datetime
from typing import Optional

from worker_automate_hub.models.dto.rpa_historico_request_dto import RpaHistoricoStatusEnum, RpaRetornoProcessoDTO
from pydantic import BaseModel, Field


class RpaHistorico(BaseModel):
    uuidHistorico: str = Field(..., alias="uuidHistorico")
    uuidProcesso: str = Field(..., alias="uuidProcesso")
    uuidRobo: Optional[str] = Field(None, alias="uuidRobo")
    prioridade: int = Field(..., alias="prioridade")
    desStatus: RpaHistoricoStatusEnum = Field(..., alias="desStatus")
    configEntrada: Optional[dict] = Field(None, alias="configEntrada")
    retorno: Optional[RpaRetornoProcessoDTO] = Field(None, alias="retorno")
    datEntradaFila: Optional[datetime] = Field(None, alias="datEntradaFila")
    datInicioExecucao: Optional[datetime] = Field(None, alias="datInicioExecucao")
    datFimExecucao: Optional[datetime] = Field(None, alias="datFimExecucao")
    identificador: Optional[str] = Field(None, alias="identificador")

    class Config:
        populate_by_name = True
