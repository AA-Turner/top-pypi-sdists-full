from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ConfigEntradaSAP(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user: str
    password: str
    empresa: str
    historico_id: Optional[str] = None

    def get(self, key, default=None):
        return getattr(self, key, default)

class RpaProcessoSapDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    configEntrada: ConfigEntradaSAP
    uuidProcesso: str = Field(..., alias="uuidProcesso")
