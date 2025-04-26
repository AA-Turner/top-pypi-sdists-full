from typing import Optional
from pydantic import BaseModel, Field


class ConfigEntradaSAP(BaseModel):
    user: str
    password: str
    empresa: str
    historico_id: Optional[str] = None

    def get(self, key, default=None):
        return getattr(self, key, default)

class RpaProcessoSapDTO(BaseModel):
    configEntrada: ConfigEntradaSAP
    uuidProcesso: str = Field(..., alias="uuidProcesso")
