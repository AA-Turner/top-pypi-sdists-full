# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["GoogleDriveDataSourceAuthConfigParam"]


class GoogleDriveDataSourceAuthConfigParam(TypedDict, total=False):
    client_email: Required[str]
    """
    Client email to use for google drive, set to override client email set in env
    vars
    """

    client_id: Required[str]
    """Client id to use for google drive, set to override client id set in env vars"""

    private_key: Required[str]
    """
    Private key to use for google drive, set to override private key set in env vars
    """

    source: Required[Literal["GoogleDrive"]]

    token_uri: Required[str]
    """Token uri to use for google drive, set to override token uri set in env vars"""

    encrypted: bool
