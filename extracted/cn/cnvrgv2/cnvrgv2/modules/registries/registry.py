from cnvrgv2.config import routes
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.modules.images.image import Image
from cnvrgv2.modules.registries.utils import validate_registry_params
from cnvrgv2.modules.base.dynamic_attributes import DynamicAttributes
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.utils.json_api_format import JAF


class Registry(DynamicAttributes):
    available_attributes = {
        "url": str,
        "title": str,
        "private": bool,
        "username": str,
        "registry_type": str,
    }

    def __init__(self, context=None, slug=None, attributes=None):
        self._context = Context(context=context)

        # Set current context scope to current project
        if slug:
            self._context.set_scope(SCOPE.REGISTRY, slug)

        scope = self._context.get_scope(SCOPE.REGISTRY)

        self.slug = scope["registry"]
        self._proxy = Proxy(context=self._context)
        self._route = routes.REGISTRY_BASE.format(scope["organization"], self.slug)
        self._attributes = attributes or {}

    @property
    def images(self):
        """
        Returns the registry images
        @return: [List] of Image objects
        """

        # TODO: Convert to pagination
        response = self._proxy.call_api(route="{}/images".format(self._route), http_method=HTTP.GET)
        items = response.items

        images = []
        for item in items:
            slug = item.attributes["slug"]
            object_instance = Image(context=self._context, slug=slug, attributes=item.attributes)
            images.append(object_instance)

        return images

    def update(self, title=None, url=None, username=None, password=None):
        """
        Updates the current registry
        @param title: [String] The registry name
        @param url: [String] The registry url
        @param username: [String] The username with which to connect to the registry
        @param password: [String] The password with which to connect to the registry
        @return: Registry object
        """

        validate_registry_params(title=title, url=url, username=username, password=password)

        # Take only the attributes we want to update (remove None values)
        attributes = {"title": title, "url": url, "username": username, "password": password}
        attributes = {k: v for k, v in attributes.items() if v is not None}

        response = self._proxy.call_api(
            route=self._route,
            http_method=HTTP.PUT,
            payload=JAF.serialize(type="registry", attributes=attributes)
        )

        self._attributes = response.attributes
        return self

    def delete(self):
        """
        Deletes the current image
        @return: None
        """
        self._proxy.call_api(route=self._route, http_method=HTTP.DELETE)
