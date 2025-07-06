from cnvrgv2.config import error_messages, routes
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.registries.registry import Registry
from cnvrgv2.modules.registries.utils import RegistryTypes, validate_registry_params
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.utils.api_list_generator import api_list_generator
from cnvrgv2.utils.json_api_format import JAF


class RegistriesClient:
    def __init__(self, organization):
        self._context = Context(context=organization._context)
        scope = self._context.get_scope(SCOPE.ORGANIZATION)

        self._proxy = Proxy(context=self._context)
        self._route = routes.REGISTRIES_BASE.format(scope["organization"])

    def list(self, sort="-id"):
        """
        List all registries in a specific organization
        @param sort: key to sort the list by (-key -> DESC | key -> ASC)
        @raise: HttpError
        @return: Generator that yields registry objects
        """
        return api_list_generator(
            context=self._context,
            route=self._route,
            object=Registry,
            sort=sort
        )

    def create(self, title, url, type=RegistryTypes.OTHER, username=None, password=None):
        """
        Create a new registry
        @param title: [String] The registry name
        @param url: [String] The registry url
        @param type: [String] The registry type
        @param username: [String] The username with which to connect to the registry
        @param password: [String] The password with which to connect to the registry
        @return: [Registry object] The newly created registry
        """

        validate_registry_params(title=title, url=url, username=username, password=password)
        if (password or username) and not all([username, password]):
            raise CnvrgArgumentsError(error_messages.REGISTRY_USERNAME_AND_PASSWORD)
        if not RegistryTypes.validate_type(type):
            raise CnvrgArgumentsError(error_messages.REGISTRY_BAD_TYPE)

        attributes = {
            "url": url,
            "title": title,
            "registry_type": type,
            "username": username,
            "password": password,
        }
        response = self._proxy.call_api(
            route=self._route,
            http_method=HTTP.POST,
            payload=JAF.serialize(type="registry", attributes=attributes)
        )

        slug = response.attributes['slug']
        return Registry(context=self._context, slug=slug)

    def get(self, slug):
        """
        Retrieves a registry by the given slug
        @param slug: [String] The slug of the requested image
        @return: Registry object
        """

        return Registry(context=self._context, slug=slug)

    def delete(self, slug):
        """
        Delete a registry by its slug
        @param slug: [String] Registry slug
        @return: None
        """

        Registry(context=self._context, slug=slug).delete()
