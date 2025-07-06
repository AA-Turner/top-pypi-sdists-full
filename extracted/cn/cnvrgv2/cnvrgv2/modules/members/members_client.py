from cnvrgv2 import cnvrg
from cnvrgv2.config import error_messages, routes
from cnvrgv2.config.error_messages import FAULTY_VALUE
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.members import Member
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.utils.api_list_generator import api_list_generator
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.utils.validators import validate_email, validate_user_role


class MembersClient:
    def __init__(self, organization):
        if type(organization) is not cnvrg.Cnvrg:
            raise CnvrgArgumentsError(error_messages.ARGUMENT_BAD_TYPE.format(cnvrg.Cnvrg, type(organization)))

        self._context = Context(context=organization._context)
        scope = self._context.get_scope(SCOPE.ORGANIZATION)

        self._scope = scope
        self._proxy = Proxy(context=self._context)
        self._list_route = routes.MEMBERS_ALL_BASE.format(scope["organization"])
        self._route = routes.MEMBERS_BASE.format(scope["organization"])

    def add(self, email, role):
        """
        Add a new member to the organization
        @param email: User email
        @param role: Role to add
        """

        if not validate_user_role(role):
            raise CnvrgArgumentsError(FAULTY_VALUE.format(role))

        if not validate_email(email):
            raise CnvrgArgumentsError(FAULTY_VALUE.format(email))

        self._proxy.call_api(
            route=self._route,
            http_method=HTTP.POST,
            payload=JAF.serialize(type="users", attributes={"members": [{"email": email, "role": role}]})
        )

    def get(self, email):
        """
        Retrieves a project by the given slug
        @param email: The slug of the requested project
        @return: Project object
        """
        if not email or not isinstance(email, str):
            raise CnvrgArgumentsError(error_messages.INVALID_EMAIL)

        return Member(context=self._context, email=email)

    def list(self, filter=None, sort="-id"):
        """
        List all members in a specific organization
        @param sort: key to sort the list by (-key -> DESC | key -> ASC)
        @param filter: Filter json
        @raise: HttpError
        @return: Generator that yields dataset objects
        """

        context = self._context

        def member_builder(item):
            return Member(context, attributes=item.attributes)

        return api_list_generator(
            context=self._context,
            route=self._list_route,
            object_builder=member_builder,
            identifier="username",
            sort=sort,
            filter=filter
        )
