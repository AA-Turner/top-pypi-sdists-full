from dataclasses import dataclass

__all__ = ["Sequence"]


@dataclass
class Sequence:
    id: int
    name: str
    data: str
