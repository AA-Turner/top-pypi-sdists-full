# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["AppListResponse", "App"]


class App(BaseModel):
    name: str


class AppListResponse(BaseModel):
    apps: List[App]
