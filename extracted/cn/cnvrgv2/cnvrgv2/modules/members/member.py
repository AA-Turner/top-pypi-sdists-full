from cnvrgv2.config import routes
from cnvrgv2.config.error_messages import FAULTY_VALUE
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.base.dynamic_attributes import DynamicAttributes
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.utils.validators import validate_user_role


class ROLES:
    ADMIN = 'admin'
    MANAGER = 'manager'
    MEMBER = 'member'
    REVIEWER = 'reviewer'
    ALL_ROLES = [ADMIN, MANAGER, MEMBER, REVIEWER]


class Member(DynamicAttributes):
    available_attributes = {
        "username": str,
        "role": str,
        "access_level": str,
        "email": str,
        "last_seen_at": str,
    }

    def __init__(self, context=None, attributes=None, email=None):
        self._context = Context(context=context)

        if attributes:
            self._email = attributes["email"]

        if email:
            self._email = email

        if self._email:
            self._context.set_scope(SCOPE.MEMBER, self._email)

        scope = self._context.get_scope(SCOPE.MEMBER)

        self._proxy = Proxy(context=self._context)
        self._route = routes.MEMBER_BASE.format(scope["organization"], scope["member"])
        self._attributes = attributes or {}

    @property
    def email(self):
        return self._email

    def revoke(self):
        """
        Delete the membership profile
        """

        self._proxy.call_api(route=self._route, http_method=HTTP.DELETE)

    def update(self, role):
        """
        Update the membership profile
        """

        if not validate_user_role(role):
            raise CnvrgArgumentsError(FAULTY_VALUE.format(role))

        self._proxy.call_api(
            route=self._route,
            http_method=HTTP.PUT,
            payload=JAF.serialize(type="users", attributes={"role": role})
        )
