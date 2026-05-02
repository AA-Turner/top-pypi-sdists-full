# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["SlackDataSourceAuthConfigParam"]


class SlackDataSourceAuthConfigParam(TypedDict, total=False):
    bot_token: Required[str]
    """Your Slack app's Bot OAuth token. See https://api.slack.com/quickstart"""

    source: Required[Literal["Slack"]]

    encrypted: bool
