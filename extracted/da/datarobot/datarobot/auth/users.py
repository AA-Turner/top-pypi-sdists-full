#
# Copyright 2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
# limitations under the License.
from __future__ import annotations

from pydantic import BaseModel, Field

from datarobot.auth.typing import Metadata


class User(BaseModel):
    """
    User data class representing a user in a custom application.
    """

    id: str
    """The unique identifier for the user on the custom application side."""
    email: str
    """The email address of the user."""
    phone_number: str | None = None
    """The phone number of the user, if available."""
    name: str | None = None
    """The full name of the user, if available."""
    given_name: str | None = None
    """The given name of the user, if available."""
    family_name: str | None = None
    """The family name of the user, if available."""
    profile_picture_url: str | None = None
    """The URL of the user's profile picture, if available."""
    metadata: Metadata | None = Field(default_factory=lambda: {})
    """Additional metadata about the user, if available."""
