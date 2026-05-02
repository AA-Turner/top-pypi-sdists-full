from dataclasses import dataclass, field
from typing import Any, Dict
from loguru import logger


@dataclass
class SPRequest:
    requestType: Any
    json: Dict[str, Any] = field(default_factory=dict)
    text: str = ""
    headers: Dict[str, Any] = field(default_factory=dict)
    logger: logger = logger
    
