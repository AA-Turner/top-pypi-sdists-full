# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["CategoryRetrieveParams"]


class CategoryRetrieveParams(TypedDict, total=False):
    locale: str
    """
    The desired language, consisting of an
    [ISO 639-1](http://en.wikipedia.org/wiki/ISO_639-1) language code and an
    [ISO 3166-1 alpha-2 country code](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2),
    joined by an underscore. For example: `es_MX`, meaning &quot;Spanish
    (Mexico)&quot;. Provide this parameter if you want the category strings returned
    in a particular language.<br/> _**Note**: if `locale` is not supplied, or if the
    specified language is not available, the category strings returned will be in
    the Spotify default language (American English)._
    """
