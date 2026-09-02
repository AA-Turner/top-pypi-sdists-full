"""Component Documentation Extension.

Extension for registering the Component Documentation API routes.
"""
from navigator.types import WebApp
from .abstract import BaseExtension
from ..handlers.component import FlowtaskComponentHandler


class ComponentDocumentation(BaseExtension):
    """Extension for Component Documentation API.

    Registers routes for serving pre-generated component documentation:
        GET /api/v1/flowtask/components - List all documented components
        GET /api/v1/flowtask/components/{component_name} - Get component documentation

    Usage:
        In your application setup:

        ```python
        from flowtask.extensions.component_docs import ComponentDocumentation

        # During app setup
        component_docs = ComponentDocumentation()
        component_docs.setup(app)
        ```
    """

    def setup(self, app: WebApp) -> WebApp:
        """Set up the extension and register routes.

        Args:
            app: The aiohttp web application instance

        Returns:
            The configured application instance
        """
        app = super().setup(app)

        # Register component documentation routes
        self.app.router.add_view(
            "/api/v1/flowtask/components",
            FlowtaskComponentHandler
        )
        self.app.router.add_view(
            "/api/v1/flowtask/components/{component_name}",
            FlowtaskComponentHandler
        )

        self.logger.info(
            "Component Documentation API registered at /api/v1/flowtask/components"
        )

        return self.app
