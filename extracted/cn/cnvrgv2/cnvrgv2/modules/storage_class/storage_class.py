from cnvrgv2.config import routes
from cnvrgv2.modules.base.dynamic_attributes import DynamicAttributes
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.utils.json_api_format import JAF


class StorageClass(DynamicAttributes):
    available_attributes = {
        "slug": str,
        "title": str,
        "host_path": str,
        "host_ip": str,
        "connection_type": str,
        "status": str,
    }

    def __init__(self, context=None, slug=None, attributes=None):
        super().__init__()
        self._context = Context(context=context)
        if slug:
            self._context.set_scope(SCOPE.STORAGE_CLASS, slug)

        scope = self._context.get_scope(SCOPE.STORAGE_CLASS)

        self._proxy = Proxy(context=self._context)
        self._route = routes.STORAGE_CLASS_BASE.format(scope["organization"], slug)
        self._attributes = attributes or {}
        self.slug = scope["storage_class"]

    def delete(self):
        """
        Deletes the current storage class
        @return: None
        """
        query_param = "?delete_from_cluster=true"
        delete_route = self._route + query_param
        self._proxy.call_api(route=delete_route, http_method=HTTP.DELETE)

    def disconnect(self):
        """
        Disconnect the current storage class
        @return: None
        """
        self._proxy.call_api(route=self._route, http_method=HTTP.DELETE,
                             payload=JAF.serialize(type="storageClass", attributes={}))
