import datetime
import modal._billing
import modal._workspace
import modal.client
import modal.object
import typing
import typing_extensions

class ProxyTokenInfo:
    """Metadata about a proxy token, not including the token secret."""

    token_id: str
    created_at: datetime.datetime
    scoped: bool

    def __init__(self, token_id: str, created_at: datetime.datetime, scoped: bool) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __repr__(self):
        """Return repr(self)."""
        ...

    def __eq__(self, other):
        """Return self==value."""
        ...

    def __setattr__(self, name, value):
        """Implement setattr(self, name, value)."""
        ...

    def __delattr__(self, name):
        """Implement delattr(self, name)."""
        ...

    def __hash__(self):
        """Return hash(self)."""
        ...

class TokenData:
    """A token ID / secret pair."""

    token_id: str
    token_secret: str

    def __init__(self, token_id: str, token_secret: str) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __repr__(self):
        """Return repr(self)."""
        ...

    def __eq__(self, other):
        """Return self==value."""
        ...

    def __setattr__(self, name, value):
        """Implement setattr(self, name, value)."""
        ...

    def __delattr__(self, name):
        """Implement delattr(self, name)."""
        ...

    def __hash__(self):
        """Return hash(self)."""
        ...

class WorkspaceMemberInfo:
    """Metadata about a Workspace member."""

    name: str
    email: str
    user_id: str
    role: typing.Literal["user", "manager", "owner"]
    joined_at: datetime.datetime
    last_active_at: typing.Optional[datetime.datetime]

    def __init__(
        self,
        name: str,
        email: str,
        user_id: str,
        role: typing.Literal["user", "manager", "owner"],
        joined_at: datetime.datetime,
        last_active_at: typing.Optional[datetime.datetime],
    ) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __repr__(self):
        """Return repr(self)."""
        ...

    def __eq__(self, other):
        """Return self==value."""
        ...

    def __setattr__(self, name, value):
        """Implement setattr(self, name, value)."""
        ...

    def __delattr__(self, name):
        """Implement delattr(self, name)."""
        ...

    def __hash__(self):
        """Return hash(self)."""
        ...

class Workspace(modal.object.Object):
    _name: typing.Optional[str]

    def __init__(self):
        """mdmd:hidden"""
        ...

    @property
    def name(self) -> typing.Optional[str]: ...
    @property
    def members(self) -> WorkspaceMembersManager: ...
    @staticmethod
    def from_context(*, client: typing.Optional[modal.client.Client] = None) -> Workspace:
        """Look up the Workspace associated with the current context.

        This returns the Workspace that the active Modal credentials authenticate against
        (i.e., your active profile or the `MODAL_TOKEN_ID` / `MODAL_TOKEN_SECRET` environment
        variables). If called inside a Modal container, it returns the Workspace that the
        container is running in.
        """
        ...

    @property
    def billing(self) -> WorkspaceBillingManager: ...
    @property
    def proxy_tokens(self) -> WorkspaceProxyTokenManager: ...

class WorkspaceMembersManager:
    """mdmd:namespace
    Namespace with methods for managing the membership of a Workspace.
    """
    def __init__(self, workspace: Workspace):
        """mdmd:hidden"""
        ...

    class __list_spec(typing_extensions.Protocol):
        def __call__(self, /) -> list[modal._workspace.WorkspaceMemberInfo]:
            """Return the members of the Workspace.

            **Examples:**

            ```python notest
            members = modal.Workspace.from_context().members.list()
            print([m.name for m in members])
            ```
            """
            ...

        async def aio(self, /) -> list[modal._workspace.WorkspaceMemberInfo]:
            """Return the members of the Workspace.

            **Examples:**

            ```python notest
            members = modal.Workspace.from_context().members.list()
            print([m.name for m in members])
            ```
            """
            ...

    list: __list_spec

class WorkspaceBillingManager:
    """mdmd:namespace
    Namespace for Workspace billing APIs.
    """
    def __init__(self, workspace: Workspace):
        """mdmd:hidden"""
        ...

    class __report_spec(typing_extensions.Protocol):
        def __call__(
            self,
            /,
            *,
            start: datetime.datetime,
            end: typing.Optional[datetime.datetime] = None,
            resolution: str = "d",
            tag_names: typing.Optional[list[str]] = None,
        ) -> list[modal._billing.BillingReportItem]:
            """Return a cost report for all Workspace usage, broken down by object and time.

            Args:
                start: Start of the report, inclusive and rounded to the beginning of the interval.
                    Must be in UTC or timezone-naive (interpreted as UTC).
                end: End of the report, exclusive. Must be in UTC or timezone-naive. Partial final
                    intervals will be excluded from the report.
                resolution: Resolution, e.g. "d" for daily or "h" for hourly.
                tag_names: List of tag names; each row will include the tag name and value in use
                    for that object during the relevant time interval. Pass `["*"]` to include all
                    tags in the report.

            Returns:
                A list of `BillingReportItem` dataclasses. Each item reports the cost attributed to
                a specific Modal object during a given time interval. Cost is further broken down by
                the resource type that generated it (e.g. CPU, Memory, specific GPU usage). Note that
                the specific resource types included in the breakdown are subject to change as Modal's
                billing model evolves.

            See also:
                - [`modal billing report`](https://modal.com/docs/cli/latest/billing#modal-billing-report):
                  A workspace report CLI that has convenience features around relative time range queries
                  and JSON/CSV output.
                - [`Environment.billing.report()`](https://modal.com/docs/sdk/py/latest/modal.Environment#billingreport):
                  An analogous report API that is scoped to a specific Environment.
            """
            ...

        async def aio(
            self,
            /,
            *,
            start: datetime.datetime,
            end: typing.Optional[datetime.datetime] = None,
            resolution: str = "d",
            tag_names: typing.Optional[list[str]] = None,
        ) -> list[modal._billing.BillingReportItem]:
            """Return a cost report for all Workspace usage, broken down by object and time.

            Args:
                start: Start of the report, inclusive and rounded to the beginning of the interval.
                    Must be in UTC or timezone-naive (interpreted as UTC).
                end: End of the report, exclusive. Must be in UTC or timezone-naive. Partial final
                    intervals will be excluded from the report.
                resolution: Resolution, e.g. "d" for daily or "h" for hourly.
                tag_names: List of tag names; each row will include the tag name and value in use
                    for that object during the relevant time interval. Pass `["*"]` to include all
                    tags in the report.

            Returns:
                A list of `BillingReportItem` dataclasses. Each item reports the cost attributed to
                a specific Modal object during a given time interval. Cost is further broken down by
                the resource type that generated it (e.g. CPU, Memory, specific GPU usage). Note that
                the specific resource types included in the breakdown are subject to change as Modal's
                billing model evolves.

            See also:
                - [`modal billing report`](https://modal.com/docs/cli/latest/billing#modal-billing-report):
                  A workspace report CLI that has convenience features around relative time range queries
                  and JSON/CSV output.
                - [`Environment.billing.report()`](https://modal.com/docs/sdk/py/latest/modal.Environment#billingreport):
                  An analogous report API that is scoped to a specific Environment.
            """
            ...

    report: __report_spec

class WorkspaceProxyTokenManager:
    """mdmd:namespace
    Namespace with methods for managing the proxy tokens in a Workspace.

    See [the guide](https://modal.com/docs/guide/webhook-proxy-auth) for more information on proxy tokens.
    """
    def __init__(self, workspace: Workspace):
        """mdmd:hidden"""
        ...

    class __create_spec(typing_extensions.Protocol):
        def __call__(self, /) -> modal._workspace.TokenData:
            """Create a new proxy token for the Workspace.

            Examples:
                ```python notest
                token = modal.Workspace.from_context().proxy_tokens.create()
                print(token.token_id, token.token_secret)
                ```
            """
            ...

        async def aio(self, /) -> modal._workspace.TokenData:
            """Create a new proxy token for the Workspace.

            Examples:
                ```python notest
                token = modal.Workspace.from_context().proxy_tokens.create()
                print(token.token_id, token.token_secret)
                ```
            """
            ...

    create: __create_spec

    class __list_spec(typing_extensions.Protocol):
        def __call__(self, /, environment_name: typing.Optional[str] = None) -> list[modal._workspace.ProxyTokenInfo]:
            """List proxy tokens in the Workspace.

            Args:
                environment_name: When provided, list only the tokens associated with this environment.

            Examples:
                ```python notest
                ws = modal.Workspace.from_context()

                # List all proxy tokens in the Workspace
                tokens = ws.proxy_tokens.list()
                print([t.token_id for t in tokens])

                # List only the proxy tokens associated with a specific Environment
                env_tokens = ws.proxy_tokens.list(environment_name="prod")
                ```
            """
            ...

        async def aio(self, /, environment_name: typing.Optional[str] = None) -> list[modal._workspace.ProxyTokenInfo]:
            """List proxy tokens in the Workspace.

            Args:
                environment_name: When provided, list only the tokens associated with this environment.

            Examples:
                ```python notest
                ws = modal.Workspace.from_context()

                # List all proxy tokens in the Workspace
                tokens = ws.proxy_tokens.list()
                print([t.token_id for t in tokens])

                # List only the proxy tokens associated with a specific Environment
                env_tokens = ws.proxy_tokens.list(environment_name="prod")
                ```
            """
            ...

    list: __list_spec

    class __allow_spec(typing_extensions.Protocol):
        def __call__(self, /, proxy_token_id: str, environment_name: str) -> None:
            """Allow a proxy token to authenticate requests to a given Environment.

            Args:
                proxy_token_id: The token ID (`wk-...`) to operate on.
                environment_name: The name of the environment to allow access to.

            Examples:
                ```python notest
                ws = modal.Workspace.from_context()
                token = ws.proxy_tokens.create()
                ws.proxy_tokens.allow(token.token_id, "prod")
                ```
            """
            ...

        async def aio(self, /, proxy_token_id: str, environment_name: str) -> None:
            """Allow a proxy token to authenticate requests to a given Environment.

            Args:
                proxy_token_id: The token ID (`wk-...`) to operate on.
                environment_name: The name of the environment to allow access to.

            Examples:
                ```python notest
                ws = modal.Workspace.from_context()
                token = ws.proxy_tokens.create()
                ws.proxy_tokens.allow(token.token_id, "prod")
                ```
            """
            ...

    allow: __allow_spec

    class __revoke_spec(typing_extensions.Protocol):
        def __call__(self, /, proxy_token_id: str, environment_name: str) -> None:
            """Revoke a proxy token's access to a given Environment.

            The proxy token is not deleted, and it will continue to authenticate requests to any
            other Environments it is associated with.

            Args:
                proxy_token_id: The token ID (`wk-...`) to operate on.
                environment_name: The name of the environment to revoke access from.

            Examples:
                ```python notest
                ws = modal.Workspace.from_context()
                ws.proxy_tokens.revoke(token_id, "prod")
                ```
            """
            ...

        async def aio(self, /, proxy_token_id: str, environment_name: str) -> None:
            """Revoke a proxy token's access to a given Environment.

            The proxy token is not deleted, and it will continue to authenticate requests to any
            other Environments it is associated with.

            Args:
                proxy_token_id: The token ID (`wk-...`) to operate on.
                environment_name: The name of the environment to revoke access from.

            Examples:
                ```python notest
                ws = modal.Workspace.from_context()
                ws.proxy_tokens.revoke(token_id, "prod")
                ```
            """
            ...

    revoke: __revoke_spec

    class __delete_spec(typing_extensions.Protocol):
        def __call__(self, /, proxy_token_id: str) -> None:
            """Delete a proxy token from the Workspace.

            This cannot be reverted. Any clients currently using the token will immediately
            lose access to associated resources.

            Args:
                proxy_token_id: The token ID (`wk-...`) to delete.

            Examples:
                ```python notest
                modal.Workspace.from_context().proxy_tokens.delete(token_id)
                ```
            """
            ...

        async def aio(self, /, proxy_token_id: str) -> None:
            """Delete a proxy token from the Workspace.

            This cannot be reverted. Any clients currently using the token will immediately
            lose access to associated resources.

            Args:
                proxy_token_id: The token ID (`wk-...`) to delete.

            Examples:
                ```python notest
                modal.Workspace.from_context().proxy_tokens.delete(token_id)
                ```
            """
            ...

    delete: __delete_spec

    class ___environment_id_spec(typing_extensions.Protocol):
        def __call__(self, /, environment_name: str) -> str: ...
        async def aio(self, /, environment_name: str) -> str: ...

    _environment_id: ___environment_id_spec
