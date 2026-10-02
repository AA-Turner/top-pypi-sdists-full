# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["CliVersionResponse", "Install"]


class Install(BaseModel):
    macos_linux: str

    windows: str


class CliVersionResponse(BaseModel):
    install: Install

    latest: str

    message: Optional[str] = None

    minimum_supported: str

    update_available: bool

    update_required: bool
