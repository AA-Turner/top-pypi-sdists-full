# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["DatabricksDataSourceConfig"]


class DatabricksDataSourceConfig(BaseModel):
    http_path: str
    """HTTP path for the Databricks cluster or SQL warehouse"""

    server_hostname: str
    """Databricks server hostname"""

    source: Literal["Databricks"]
