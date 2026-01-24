from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass(frozen=True)
class Request:
    """Framework-agnostic HTTP request snapshot (files excluded)."""
    method: str
    path: str
    url: Optional[str]
    headers: Dict[str, str]
    raw_body: bytes
    query: Dict[str, List[str]] = field(default_factory=dict)
    cookies: Dict[str, str] = field(default_factory=dict)
    form: Dict[str, List[str]] = field(default_factory=dict)
