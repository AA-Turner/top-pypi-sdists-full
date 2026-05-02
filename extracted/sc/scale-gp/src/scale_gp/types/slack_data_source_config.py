# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["SlackDataSourceConfig"]


class SlackDataSourceConfig(BaseModel):
    channel_id: str
    """Slack Channel or Conversation ID to retrieve history from.

    Open channel details and find the ID at bottom of 'About' section.
    """

    source: Literal["Slack"]
