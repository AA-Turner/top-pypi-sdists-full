from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field

class RpaHistoricoStatusEnum(str, Enum):
    Descartado = "D"
    Falha = "F"
    Processando = "P"
    Reservado = "R"
    Sucesso = "S"

class RpaTagEnum(str, Enum):
    Negocio = "NEGÓCIO"
    Tecnico = "TÉCNICO"

class RpaTagDTO(BaseModel):
    uuidTagRpa: Optional[str] = Field(None, alias="uuidTagRpa")
    descricao: RpaTagEnum = Field(..., alias="descricao")


    class Config:
        populate_by_name = True


class RpaRetornoProcessoDTO(BaseModel):
    sucesso: bool = Field(..., alias="sucesso")
    retorno: str = Field(..., alias="retorno")
    status: RpaHistoricoStatusEnum = Field(..., alias="status")
    tags: Optional[List[RpaTagDTO]] = Field(None, alias="tags")


    class Config:
        populate_by_name = True



class RpaHistoricoRequestDTO(BaseModel):
    uuidHistorico: Optional[str] = Field(None, alias="uuidHistorico")
    uuidProcesso: str = Field(..., alias="uuidProcesso")
    uuidRobo: Optional[str] = Field(None, alias="uuidRobo")
    prioridade: int
    desStatus: RpaHistoricoStatusEnum = Field(..., alias="desStatus")
    configEntrada: Optional[dict] = Field(None, alias="configEntrada")
    retorno: Optional[RpaRetornoProcessoDTO] = Field(None, alias="retorno")
    datEntradaFila: Optional[datetime] = Field(None, alias="datEntradaFila")
    datInicioExecucao: Optional[datetime] = Field(None, alias="datInicioExecucao")
    datFimExecucao: Optional[datetime] = Field(None, alias="datFimExecucao")
    identificador: Optional[str] = Field(None, alias="identificador")
    tags: Optional[List[RpaTagDTO]] = Field(None, alias="tags")

    class Config:
        populate_by_name = True
