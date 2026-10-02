from dataclasses import dataclass


@dataclass
class QueryResult:
    id: str
    document: str
    metadata: dict
    distance: float

