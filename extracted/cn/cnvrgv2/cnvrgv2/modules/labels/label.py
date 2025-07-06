from cnvrgv2.config import routes
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.modules.base.dynamic_attributes import DynamicAttributes
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.modules.labels.utils import validate_labels_params
from cnvrgv2.utils.url_utils import urljoin


class Label(DynamicAttributes):
    available_attributes = {
        "id": str,
        "name": str,
        "kind": str,
        "color_name": str,
    }

    def __init__(self, context=None, name=None, kind=None, attributes=None):
        self._context = Context(context=context)

        if name and kind:
            self._context.set_scope(SCOPE.LABEL, {"name": name, "kind": kind})

        scope = self._context.get_scope(SCOPE.LABEL)

        self._proxy = Proxy(context=self._context)
        self._route = routes.LABELS_BASE.format(scope["organization"])
        self._attributes = attributes or {}

    def delete(self):
        """
        Deletes the current label
        @return: None
        """
        url = urljoin(self._route, self.id)
        self._proxy.call_api(route=url, http_method=HTTP.DELETE)

    def save(self):
        return self.update(name=self.name, color_name=self.color_name)

    def update(self, name=None, color_name=None):
        if name:
            self.name = name

        if color_name:
            self.color_name = color_name

        validate_labels_params(self.name, self.kind, self.color_name)
        attributes = {
            "id": self.id,
            "name": self.name,
            "kind": self.kind,
            "color_name": self.color_name,
        }

        self._proxy.call_api(
            route=self._route,
            http_method=HTTP.PUT,
            payload=JAF.serialize(type="label", attributes=attributes)
        )
        return self
