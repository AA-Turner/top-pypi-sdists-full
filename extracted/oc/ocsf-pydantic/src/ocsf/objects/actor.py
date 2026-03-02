from .user import User


from .process import Process

from .authorization import AuthorizationResult
from .idp import IdentityProvider

from pydantic import BaseModel
from .session import Session


class Actor(BaseModel):
    """
    The Actor object contains details about the user, role, application, service, or
    process that initiated or performed a specific activity.
    """

    # Recommended:
    process: Process | None = None # The process that initiated the activity.
    user: User | None = None # The user that initiated the activity or the user context from which the
                             # activity was initiated.

    # Optional:
    app_name: str | None = None # The client application or service that initiated the activity. This
                                # can be in conjunction with the `user` if present.  Note
                                # that `app_name` is distinct from the `process`
                                # if present.
    app_uid: str | None = None # The unique identifier of the client application or service that
                               # initiated the activity. This can be in conjunction with the
                               # `user` if present. Note that `app_name` is
                               # distinct from the `process.pid` or `process.uid`
                               # if present.
    authorizations: list[AuthorizationResult] | None = None
    idp: IdentityProvider | None = None
    invoked_by: str | None = None
    session: Session | None = None # The user session from which the activity was initiated.
