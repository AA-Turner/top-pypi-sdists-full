from typing import Dict, Optional
from pydantic import BaseModel

class ConfigEntrada(BaseModel):
    ip: str
    user: str
    password: str
    processo: str
    uuid_robo: Optional[str]

    def get(self, key, default=None):
        return getattr(self, key, default)

class RpaProcessoRdpDTO(BaseModel):
    configEntrada: ConfigEntrada
