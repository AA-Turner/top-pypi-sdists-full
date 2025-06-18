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

from pydantic import BaseModel


class Identity(BaseModel):
    """
    Identity data class representing an identity in a custom application.
    One user can have multiple identities coming from different providers e.g. Google, Box, etc.
    """

    id: str
    """The unique identifier for the identity."""
    type: str
    """The type of the authentication schema (e.g., 'oauth2', 'datarobot')."""
    provider_type: str
    """The identity provider type (e.g., 'google', 'box')."""
    provider_user_id: str
    """The unique identifier for the user in the identity provider."""
    provider_identity_id: str | None = None
    """The unique identifier for the identity in the provider, if applicable."""
