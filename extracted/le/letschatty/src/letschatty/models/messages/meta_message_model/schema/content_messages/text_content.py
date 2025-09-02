from pydantic import BaseModel
from typing import List, Dict, Union, Optional, TypeAlias
from enum import StrEnum

# Mensajes Clasicos
class MetaTextContent(BaseModel):
    body: str

    
# Mensajes de errores
class ErrorData(BaseModel):
    details: str

class MetaErrorContent(BaseModel):
    code: int
    title: str
    message: str
    error_data: ErrorData