from abc import ABC, abstractmethod

from pydantic import BaseModel


class CheckResult(BaseModel):
    name: str
    passed: bool
    details: str | None = None


class Check(ABC):
    @abstractmethod
    async def __call__(self) -> CheckResult:
        ...
