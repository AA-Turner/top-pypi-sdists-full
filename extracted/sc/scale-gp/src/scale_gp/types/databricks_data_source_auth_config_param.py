# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["DatabricksDataSourceAuthConfigParam"]


class DatabricksDataSourceAuthConfigParam(TypedDict, total=False):
    access_token: Required[str]
    """Databricks access token for authentication"""

    source: Required[Literal["Databricks"]]

    encrypted: bool
