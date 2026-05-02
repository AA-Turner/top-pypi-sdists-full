# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["RecommendationListAvailableGenreSeedsResponse"]


class RecommendationListAvailableGenreSeedsResponse(BaseModel):
    genres: List[str]
