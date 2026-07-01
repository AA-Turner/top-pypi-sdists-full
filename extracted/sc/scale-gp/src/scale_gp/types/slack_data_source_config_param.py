# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["SlackDataSourceConfigParam"]


class SlackDataSourceConfigParam(TypedDict, total=False):
    channel_id: Required[str]
    """Slack Channel or Conversation ID to retrieve history from.

    Open channel details and find the ID at bottom of 'About' section.
    """

    source: Required[Literal["Slack"]]
