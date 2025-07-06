from cnvrgv2 import cnvrg
from cnvrgv2.config import error_messages, routes
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.libhub.libraries.library import Library
from cnvrgv2.proxy import Proxy
from cnvrgv2.utils.api_list_generator import api_list_generator


class LibrariesClient:
    def __init__(self, organization):
        if type(organization) is not cnvrg.Cnvrg:
            raise CnvrgArgumentsError(error_messages.ARGUMENT_BAD_TYPE.format(cnvrg.Cnvrg, type(organization)))
        self._context = Context(context=organization._context)
        scope = self._context.get_scope(SCOPE.ORGANIZATION)

        self._proxy = Proxy(context=self._context)
        self._route = routes.LIBRARIES_BASE.format(scope["organization"])

    def list(self, sort="-id"):
        """
        List all library in a specific organization
        @param sort: key to sort the list by (-key -> DESC | key -> ASC)
        @raise: HttpError
        @return: Generator that yields project objects
        """
        return api_list_generator(
            context=self._context,
            route=self._route,
            object=Library,
            sort=sort,
            pagination_type=None
        )

    def get(self, slug):
        """
        Retrieves a project by the given slug
        @param slug: The slug of the requested project
        @return: Project object
        """
        if not slug or not isinstance(slug, str):
            raise CnvrgArgumentsError(error_messages.LIBRARY_GET_FAULTY_SLUG)

        return Library(context=self._context, slug=slug)

    # TODO: Need to implement in the future
