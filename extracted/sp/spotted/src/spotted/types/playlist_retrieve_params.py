# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["PlaylistRetrieveParams"]


class PlaylistRetrieveParams(TypedDict, total=False):
    additional_types: str
    """
    A comma-separated list of item types that your client supports besides the
    default `track` type. Valid types are: `track` and `episode`.<br/> _**Note**:
    This parameter was introduced to allow existing clients to maintain their
    current behaviour and might be deprecated in the future._<br/> In addition to
    providing this parameter, make sure that your client properly handles cases of
    new types in the future by checking against the `type` field of each object.
    """

    fields: str
    """Filters for the query: a comma-separated list of the fields to return.

    If omitted, all fields are returned. For example, to get just the playlist''s
    description and URI: `fields=description,uri`. A dot separator can be used to
    specify non-reoccurring fields, while parentheses can be used to specify
    reoccurring fields within objects. For example, to get just the added date and
    user ID of the adder: `fields=tracks.items(added_at,added_by.id)`. Use multiple
    parentheses to drill down into nested objects, for example:
    `fields=tracks.items(track(name,href,album(name,href)))`. Fields can be excluded
    by prefixing them with an exclamation mark, for example:
    `fields=tracks.items(track(name,href,album(!name,href)))`
    """

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
