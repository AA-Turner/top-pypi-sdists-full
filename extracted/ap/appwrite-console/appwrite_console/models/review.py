from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class Review(AppwriteModel):
    """
    Review

    Attributes
    ----------
    name : str
        Name of user
    image : str
        Reviewer image
    description : str
        Reviewer description
    review : str
        Review
    """

    name: str = Field(..., alias='name')
    image: str = Field(..., alias='image')
    description: str = Field(..., alias='description')
    review: str = Field(..., alias='review')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'name' not in data:
            data['name'] = ''
        if 'image' not in data:
            data['image'] = ''
        if 'description' not in data:
            data['description'] = ''
        if 'review' not in data:
            data['review'] = ''
        return data
