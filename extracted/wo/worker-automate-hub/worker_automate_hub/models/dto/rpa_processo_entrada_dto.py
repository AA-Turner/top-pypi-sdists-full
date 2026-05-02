from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from worker_automate_hub.models.dto.rpa_sistema_dto import RpaSistemaDTO


class RpaProcessoEntradaDTO(BaseModel):
    datEntradaFila: datetime = Field(..., alias="datEntradaFila")
    configEntrada: dict = Field(..., alias="configEntrada")
    uuidProcesso: str = Field(..., alias="uuidProcesso")
    nomProcesso: str = Field(..., alias="nomProcesso")
    uuidFila: str = Field(..., alias="uuidFila")
    sistemas: List[RpaSistemaDTO] = Field(..., alias="sistemas")
    historico_id: Optional[str] = None
    prioridade: Optional[int] = None

    class Config:
        populate_by_name = True
