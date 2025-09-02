# Copyright 2025 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

import time
from typing import (
    Any,
)

from jwt.api_jwt import decode


class JwtMixin:
    """Mixin with JWT convenience functions."""

    @staticmethod
    def _get_payload(access_token: str) -> dict[str, Any]:
        """Returns the access token payload."""
        return decode(access_token, options={"verify_signature": False})

    @classmethod
    def _expires_within(cls, access_token: str, threshold: int) -> bool:
        """
        Checks if the access token expires within the given threshold.

        Parameters
        ----------
        access_token : str
            A JWT access token.
        threshold : int
            Number of seconds.
        """
        payload = cls._get_payload(access_token)
        expires_at = payload.get("exp")
        return expires_at is not None and ((expires_at - time.time()) < threshold)
