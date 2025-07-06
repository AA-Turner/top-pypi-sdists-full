from cnvrgv2.config import routes
from cnvrgv2.modules.base.dynamic_attributes import DynamicAttributes
from cnvrgv2.proxy import Proxy, HTTP
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.utils.json_api_format import JAF

STATUS_MAP = {
    "init": "Initializing",
    "created": "Created",
    "up": "Available",
    "removed": "Removed",
    "error": "Error",
    "in_use": "In Use"
}
IN_USE = "in_use"

READ_WRITE_MANY = "Read Write Many"
READ_WRITE_ONCE = "Read Write Once"


class Volume(DynamicAttributes):
    available_attributes = {
        "slug": str,
        "title": str,
        "total_space": int,
        "used_space": int,
        "host_path": str,
        "host_ip": str,
        "read_only": bool,
        "hide": bool,
        "volume_type": str,
        "mount_path": str,
        "claim_name": str,
        "status": str,
        "in_use": bool,
        "using_jobs": list,
        "storage_class_slug": str,
        "access_mode": str
    }

    def __init__(self, context=None, slug=None, attributes=None):
        self._context = Context(context=context)

        # Set current context scope to current volume
        if slug:
            self._context.set_scope(SCOPE.VOLUME, slug)

        scope = self._context.get_scope(SCOPE.VOLUME)

        self._proxy = Proxy(context=self._context)
        self._route = routes.VOLUME_BASE.format(scope["organization"], scope["volume"])
        self._attributes = attributes or {}
        self.slug = scope["volume"]
        self.status = self.get_status()
        self.access_mode = self.get_access_mode()

    def delete(self):
        """
        Deletes the current volume
        @return: None
        """
        delete_route = self._route + "?delete_from_cluster=true"
        self._proxy.call_api(route=delete_route, http_method=HTTP.DELETE)

    def disconnect(self):
        """
        Disconnect the current volume
        @return: None
        """
        self._proxy.call_api(route=self._route, http_method=HTTP.DELETE,
                             payload=JAF.serialize(type="volume", attributes={}))

    def get_access_mode(self):
        return READ_WRITE_ONCE if self.read_only is False else READ_WRITE_MANY

    def get_status(self):
        if self.read_only and self.in_use:
            return STATUS_MAP[IN_USE]
        return STATUS_MAP[self.status]
