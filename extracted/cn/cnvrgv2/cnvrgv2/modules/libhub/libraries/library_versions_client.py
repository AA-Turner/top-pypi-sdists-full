from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.config import error_messages, routes
from cnvrgv2.utils.api_list_generator import api_list_generator
from cnvrgv2.modules.libhub.libraries.library_version import LibraryVersion


class LibraryVersionsClient:
    def __init__(self, library):

        self._context = Context(context=library._context)

        scope = self._context.get_scope(SCOPE.LIBRARY)
        self.library = library
        self._route = routes.LIBRARY_VERSIONS_BASE.format(scope["organization"], scope["library"])

    def list(self, sort="-id"):
        """
        List all projects in a specific organization
        @param sort: key to sort the list by (-key -> DESC | key -> ASC)
        @raise: HttpError
        @return: Generator that yields project objects
        """
        return api_list_generator(
            context=self._context,
            route=self._route,
            object=LibraryVersion,
            sort=sort
        )

    def get(self, version):
        """
        Retrieves a project by the given slug
        @param slug: The slug of the requested project
        @return: Project object
        """
        if not version or not isinstance(version, str):
            raise CnvrgArgumentsError(error_messages.PROJECT_GET_FAULTY_SLUG)

        return LibraryVersion(context=self._context, version=version)

    @property
    def latest(self):
        return self.get(version="latest")
