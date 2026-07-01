# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ConfluenceDataSourceConfigParam"]


class ConfluenceDataSourceConfigParam(TypedDict, total=False):
    source: Required[Literal["Confluence"]]

    space_key: Required[str]
    """Confluence space key to retrieve contents from.

    See https://support.atlassian.com/confluence-cloud/docs/choose-a-space-key
    """
