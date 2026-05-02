"""
Spotlight FastAPI Integration

This module provides the FastAPI middleware integration.
The middleware is also available directly from the main package.

Usage:
    from spotlight_monitor import Spotlight, SpotlightMiddleware

    app = FastAPI()
    spotlight = Spotlight(api_key="sp_xxx", service_slug="my-api")

    # Option 1: Use instrument() method
    spotlight.instrument(app)

    # Option 2: Add middleware directly
    app.add_middleware(SpotlightMiddleware, spotlight=spotlight)
"""

from ..middleware import SpotlightMiddleware


# Re-export for consistency with other integrations
class FastAPIIntegration:
    """
    FastAPI integration wrapper.

    Note: You can also use spotlight.instrument(app) directly,
    or add SpotlightMiddleware to your app manually.
    """

    def __init__(self, spotlight):
        self.spotlight = spotlight
        self.middleware_class = SpotlightMiddleware

    def instrument(self, app):
        """Add Spotlight middleware to FastAPI app."""
        app.add_middleware(SpotlightMiddleware, spotlight=self.spotlight)


__all__ = ["FastAPIIntegration", "SpotlightMiddleware"]