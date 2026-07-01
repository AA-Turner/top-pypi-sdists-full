# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ConfluenceDataSourceConfig"]


class ConfluenceDataSourceConfig(BaseModel):
    source: Literal["Confluence"]

    space_key: str
    """Confluence space key to retrieve contents from.

    See https://support.atlassian.com/confluence-cloud/docs/choose-a-space-key
    """
