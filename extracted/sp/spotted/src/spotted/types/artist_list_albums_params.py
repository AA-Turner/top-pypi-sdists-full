# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["ArtistListAlbumsParams"]


class ArtistListAlbumsParams(TypedDict, total=False):
    include_groups: str
    """A comma-separated list of keywords that will be used to filter the response.

    If not supplied, all album types will be returned. <br/> Valid values are:<br/>-
    `album`<br/>- `single`<br/>- `appears_on`<br/>- `compilation`<br/>For example:
    `include_groups=album,single`.
    """

    limit: int
    """The maximum number of items to return. Default: 5. Minimum: 1. Maximum: 10."""

    market: str
    """
    An
    [ISO 3166-1 alpha-2 country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
    If a country code is specified, only content that is available in that market
    will be returned.<br/> If a valid user access token is specified in the request
    header, the country associated with the user account will take priority over
    this parameter.<br/> _**Note**: If neither market or user country are provided,
    the content is considered unavailable for the client._<br/> Users can view the
    country that is associated with their account in the
    [account settings](https://www.spotify.com/account/overview/).
    """

    offset: int
    """The index of the first item to return.

    Default: 0 (the first item). Use with limit to get the next set of items.
    """
