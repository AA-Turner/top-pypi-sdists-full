# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["SessionCostResponse", "Usage", "UsageBrowser", "UsageCaptcha", "UsageProxy"]


class UsageBrowser(BaseModel):
    unit: Literal["minute", "second"]
    """Billing unit for browser usage"""

    value: float
    """Billable browser usage value"""


class UsageCaptcha(BaseModel):
    solves: int
    """Billable captcha solves"""


class UsageProxy(BaseModel):
    bytes: int
    """Billable Steel proxy bytes for the session"""


class Usage(BaseModel):
    """Billable usage inputs used to calculate the costs"""

    browser: UsageBrowser

    captcha: UsageCaptcha

    proxy: UsageProxy


class SessionCostResponse(BaseModel):
    """Session cost breakdown in US dollars"""

    id: str
    """Session ID"""

    currency: Literal["usd"]
    """Currency used for the cost values"""

    total_cost: float = FieldInfo(alias="totalCost")
    """Exact total session cost in US dollars (e.g.

    0.031905), with no rounding to whole cents. Rounded only to micro-dollar
    precision (6 decimal places) for precise billing passthrough.
    """

    unit: Literal["dollar"]
    """Cost unit. Values are expressed in US dollars."""

    usage: Usage
    """Billable usage inputs used to calculate the costs"""
