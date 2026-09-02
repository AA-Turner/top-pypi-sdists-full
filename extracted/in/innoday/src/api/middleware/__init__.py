"""
API Middleware for InnoDay Platform

This module contains middleware components for the FastAPI application,
including license compliance headers and other cross-cutting concerns.
"""

from .license_headers import LicenseHeadersMiddleware

__all__ = ["LicenseHeadersMiddleware"]
