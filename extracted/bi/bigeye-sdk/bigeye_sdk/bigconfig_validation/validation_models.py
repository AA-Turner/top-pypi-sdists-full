from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Any, Optional

from pydantic.v1 import BaseModel

from bigeye_sdk.log import get_logger

log = get_logger(__name__)


@dataclass()
class FileMatchResult:
    file_name: str
    lines: Dict[int, str]  # TODO could remove and just have a top line?  Think about reporting.
    error_message: str


class ValidationError(BaseModel):
    error_lines: Optional[List[str]] = None
    erroneous_configuration_cls_name: str
    error_message: str
    error_context_lines: Optional[List[str]] = None
    matched_in_file: bool = False

    def __init__(self, **data: Any):
        super().__init__(**data)
        log.warning(self.error_message)
