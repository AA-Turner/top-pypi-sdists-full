from dataclasses import dataclass
from typing import List, Optional, Literal

SeedKind = Literal["const", "arg", "account"]

@dataclass
class PDASeed:
    kind: SeedKind
    type: str
    value: Optional[str] = None
    path: Optional[str] = None

@dataclass
class PDAAccountSpec:
    account_name: str
    seeds: List[PDASeed]
