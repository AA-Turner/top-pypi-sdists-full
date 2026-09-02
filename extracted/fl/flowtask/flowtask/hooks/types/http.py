from navigator.views import BaseHandler
from navigator.libs.json import JSONContent
from navigator.types import WebApp
from .base import BaseTrigger


class HTTPHook(BaseTrigger, BaseHandler):
    """HTTPHook.

    Base Hook for all HTTP-based hooks.

    """
    methods: list = ["GET", "POST"]
    default_status: int = 202

    def __init__(self, *args, **kwargs):
        self.method: str = kwargs.pop('method', None)
        if self.method:
            self.methods = [self.method]
        super(HTTPHook, self).__init__(*args, **kwargs)
        trigger_url = kwargs.get('url', None)
        if trigger_url:
            self.url = trigger_url
        else:
            self._base_url = kwargs.get('base_url', '/api/v1/webhook/')
            self.url = f"{self._base_url}{self.trigger_id}"
        self._json = JSONContent()

    def setup(self, app: WebApp) -> None:
        super().setup(app)
        self._logger.notice(
            f"Set the unique URL Trigger to: {self.url}"
        )
        if hasattr(self, 'handle'):
            self.app.router.add_route(
                'POST',
                self.url,
                self.handle
            )
        else:
            # Class-based Views
            for method in self.methods:
                handler = getattr(self, method.lower(), None)
                if handler:
                    self.app.router.add_route(
                        method,
                        self.url,
                        handler
                    )
