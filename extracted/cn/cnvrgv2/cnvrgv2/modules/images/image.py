from cnvrgv2.config import error_messages, routes
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.base.dynamic_attributes import DynamicAttributes
from cnvrgv2.modules.images.utils import ImageLogos
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.utils.json_api_format import JAF


class Image(DynamicAttributes):
    available_attributes = {
        "name": str,
        "tag": str,
        "logo": str,
        "status": str,
        "readme": str,
        "registry_url": str,
        "registry_slug": str,
        "created_by": str,
        "created_at": str,
    }

    def __init__(self, context=None, slug=None, attributes=None):
        self._context = Context(context=context)

        # Set current context scope to current project
        if slug:
            self._context.set_scope(SCOPE.IMAGE, slug)

        scope = self._context.get_scope(SCOPE.IMAGE)

        self.slug = scope["image"]
        self._proxy = Proxy(context=self._context)
        self._route = routes.IMAGE_BASE.format(scope["organization"], self.slug)
        self._attributes = attributes or {}
        self._dockerfile = None

    @property
    def dockerfile(self, refresh=False):
        """
        Returns the image dockerfile
        @param refresh: Force refresh the dockerfile value
        @return: [String] The dockerfile of the image
        """
        if self._dockerfile is None or refresh:
            response = self._proxy.call_api(route="{}/dockerfile".format(self._route), http_method=HTTP.GET)
            self._dockerfile = response.attributes["dockerfile"]

        return self._dockerfile

    def update(self, logo=None, readme=None):
        """
        Updates the current image
        @param logo: [String] The image logo (to be displayed in the UI)
        @param readme: [String] Image readme (will be displayed in the UI)
        @return: Image object
        """

        if not ImageLogos.validate_icon(logo):
            raise CnvrgArgumentsError(error_messages.IMAGE_BAD_LOGO)

        # Take only the attributes we want to update (remove None values)
        attributes = {"logo": logo, "readme": readme}
        attributes = {k: v for k, v in attributes.items() if v is not None}

        response = self._proxy.call_api(
            route=self._route,
            http_method=HTTP.PUT,
            payload=JAF.serialize(type="image", attributes=attributes)
        )

        self._attributes = response.attributes
        return self

    def delete(self):
        """
        Deletes the current image
        @return: None
        """
        self._proxy.call_api(route=self._route, http_method=HTTP.DELETE)
