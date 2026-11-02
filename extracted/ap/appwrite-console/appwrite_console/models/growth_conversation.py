from typing import Any, Dict, List, Optional, Union, cast
from pydantic import Field, PrivateAttr, model_validator

from .base_model import AppwriteModel


class GrowthConversation(AppwriteModel):
    """
    Growth Conversation

    Attributes
    ----------
    type : str
        Conversation type.
    email : str
        Email address the conversation was filed under. For a signed in console user this is the account email.
    organizationid : str
        Organization ID the conversation was filed against. Empty when none was given or the user is not a member.
    """

    type: str = Field(..., alias='type')
    email: str = Field(..., alias='email')
    organizationid: str = Field(..., alias='organizationId')

    @model_validator(mode='before')
    @classmethod
    def _apply_defaults(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        data = dict(data)
        if 'type' not in data:
            data['type'] = ''
        if 'email' not in data:
            data['email'] = ''
        if 'organizationId' not in data and 'organizationid' not in data:
            data['organizationId'] = ''
        return data
