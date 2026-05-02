# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ConfluenceDataSourceAuthConfigParam"]


class ConfluenceDataSourceAuthConfigParam(TypedDict, total=False):
    api_key: Required[str]
    """
    API key to use for Confluence, set this to override api key configured in env
    vars.
    """

    atlassian_domain: Required[str]
    """
    Your Confluence API server's full domain, set to override domain configured in
    env vars. E.g. 'https://[your-company].atlassian.net'
    """

    client_email: Required[str]
    """
    Client email to use for Confluence, set to override client email set in env
    vars.
    """

    source: Required[Literal["Confluence"]]

    encrypted: bool
