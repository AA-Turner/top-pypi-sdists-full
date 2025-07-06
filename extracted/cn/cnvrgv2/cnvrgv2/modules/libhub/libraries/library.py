from cnvrgv2.config import routes
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.modules.base.dynamic_attributes import DynamicAttributes
from cnvrgv2.modules.libhub.libraries.library_versions_client import LibraryVersionsClient
from cnvrgv2.proxy import Proxy


class Library(DynamicAttributes):
    available_attributes = {
        "public": bool,
        "name": str,
        "slug": str,
        "owner": str,
        "summary": str,
        "created": str,
        "downloads": int,
        "total_size": int,
        "tags": list
    }

    def __init__(self, context=None, slug=None, attributes=None):
        # Init data attributes
        super().__init__()

        self._context = Context(context=context)

        # Set current context scope to current library
        if slug:
            self._context.set_scope(SCOPE.LIBRARY, slug)

        scope = self._context.get_scope(SCOPE.LIBRARY)

        self._proxy = Proxy(context=self._context)
        self._route = routes.LIBRARY_BASE.format(scope["organization"], scope["library"])
        self._attributes = attributes or {}
        self.slug = scope["library"]

        self._init_clients()

    def _init_clients(self):
        self.versions = LibraryVersionsClient(self)
