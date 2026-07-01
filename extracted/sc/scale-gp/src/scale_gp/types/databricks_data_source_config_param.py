# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["DatabricksDataSourceConfigParam"]


class DatabricksDataSourceConfigParam(TypedDict, total=False):
    http_path: Required[str]
    """HTTP path for the Databricks cluster or SQL warehouse"""

    server_hostname: Required[str]
    """Databricks server hostname"""

    source: Required[Literal["Databricks"]]
