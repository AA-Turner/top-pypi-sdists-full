from typing import Union, Optional

from pydantic import BaseModel, Field


class Checks(BaseModel):
    """model for intent checks"""

    green: Union[int, str, dict] = Field(None, alias="0")
    blue: Union[int, str, dict] = Field(None, alias="10")
    amber: Union[int, str, dict] = Field(None, alias="20")
    red: Union[int, str, dict] = Field(None, alias="30")


class CheckResults(Checks):
    """model for intent check results"""

    nan: Union[int, str, dict] = Field(None, alias="-1")


class Description(BaseModel):
    """model for description of intent check"""

    general: Union[None, str] = None
    checks: Checks = Field(default_factory=Checks)


class Result(BaseModel):
    """model for results of intent check"""

    count: Union[int, None] = None
    checks: Checks = Field(default_factory=Checks)

    def compare(self, other: "Result") -> dict:
        """

        Args:
            other: intent check

        Returns:
            diction to use to compare intent checks
        """

        old = self.checks
        new = other.checks
        data = dict()
        if self.count is not None or other.count is not None:
            data["count"] = dict(
                loaded_snapshot=self.count or 0,
                compare_snapshot=other.count or 0,
                diff=(other.count or 0) - (self.count or 0),
            )

        for value in ["green", "blue", "amber", "red"]:
            if getattr(old, value) is not None or getattr(new, value) is not None:
                o = self.get_value(old, value)
                n = self.get_value(new, value)
                data[value] = dict(loaded_snapshot=o, compare_snapshot=n, diff=(n - o))
        return data

    @staticmethod
    def get_value(data: Checks, value: str):
        return int((getattr(data, value) if data else 0) or 0)


class Child(BaseModel):
    """model for child of intent check"""

    weight: int
    intent_id: str = Field(None, alias="id")


class Group(BaseModel):
    """model of a group of intent checks"""

    custom: bool
    name: str
    group_id: str = Field(None, alias="id")
    children: list[Child] = Field(default_factory=list)


class IntentCheck(BaseModel):
    """model for intent checks"""

    groups: list[Group]
    checks: Checks
    column: str
    custom: bool
    descriptions: Description
    name: str
    status: int
    result: Result
    api_endpoint: str = Field(None, alias="apiEndpoint")
    default_color: Union[None, int] = Field(None, alias="defaultColor")
    web_endpoint: str = Field(None, alias="webEndpoint")
    intent_id: str = Field(None, alias="id")
    result_data: Optional[CheckResults] = Field(default_factory=CheckResults)
