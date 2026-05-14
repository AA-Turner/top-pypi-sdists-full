import dataclasses
from typing import Generic, Optional, TypeVar

T = TypeVar("T")


@dataclasses.dataclass
class FeatureValidation(Generic[T]):
    min: Optional[T]
    max: Optional[T]
    min_length: Optional[int]
    max_length: Optional[int]
    contains: Optional[T]
    strict: bool = False
