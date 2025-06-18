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

from typing import Generic, Sequence, TypeVar

from pydantic import BaseModel, ConfigDict

from datarobot.auth.identity import Identity
from datarobot.auth.users import User

T = TypeVar("T")


class AuthCtx(BaseModel, Generic[T]):
    """
    A serializable authentication context
    """

    user: User
    """The user metadata associated with the authentication context."""
    identities: Sequence[Identity]
    """A sequence of identities associated with the user."""
    metadata: T | None = None
    """Additional metadata associated with the authentication context."""

    model_config = ConfigDict(extra="ignore")
