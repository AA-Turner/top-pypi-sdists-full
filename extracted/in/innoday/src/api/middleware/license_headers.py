"""
License Headers Middleware

Adds AGPL v3 compliance headers to all API responses to ensure
users are aware of the license and source code availability.
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class LicenseHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add license compliance headers to all API responses.

    This ensures AGPL v3 compliance by informing users of:
    - The license type
    - Source code availability
    - Commercial licensing options
    """

    async def dispatch(self, request: Request, call_next):
        """Add license headers to response."""
        response = await call_next(request)

        # Add AGPL compliance headers
        response.headers["X-License"] = "AGPL-3.0-or-later"
        response.headers["X-License-URL"] = "https://www.gnu.org/licenses/agpl-3.0.html"
        response.headers["X-Source-Code"] = (
            "https://github.com/havilandsoftware/innoday"
        )
        response.headers["X-Commercial-License"] = "Available"
        response.headers["X-Commercial-Contact"] = "sales@havilandsoftware.com"

        # Add additional headers for transparency
        response.headers["X-CLA-Required"] = "true"
        response.headers["X-CLA-URL"] = (
            "https://github.com/havilandsoftware/innoday/blob/main/CLA.md"
        )

        return response
