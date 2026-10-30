from typing import Optional, Sequence

from botocore.exceptions import ClientError


class AWSClientException(ClientError):
    """
    An exception class that translates a ClientError from botocore to reveal
    ResponseMetadata when the stack trace is printed. Maintains backward compatibility with
    botocore.exceptions.ClientError
    """

    def __init__(self, client_error: ClientError):
        self._client_error = client_error
        self.response = client_error.response
        self._response_metadata = self.response.get("ResponseMetadata", {})
        super().__init__(self.response, client_error.operation_name)

    def __str__(self):
        return f"{str(self._client_error)}\nResponseMetadata: {self._response_metadata}"


class StudioContextError(Exception):
    """
    Base class for failures caused by the runtime the SDK is in, not by an AWS call.

    On an AWS Notebook local kernel the SDK resolves connections and their
    credentials through the app's local API; everywhere else it behaves as it always has.
    Errors in this hierarchy mean "what you asked for is not available where you are", so a
    kernel or UI can catch this one type and render an actionable message instead of a stack
    trace.
    """


class UnsupportedInModeError(StudioContextError, RuntimeError):
    """
    A feature was requested that the current runtime mode cannot provide.

    Args:
        feature: What was asked for, in user terms (e.g. ``"project S3 paths"``).
        mode: The mode the SDK is in (a :class:`~sagemaker_studio.local_kernel.RuntimeMode`).
        required: The mode that provides the feature.
        detail: Optional extra guidance appended to the message.

    Subclasses :class:`RuntimeError` because the legacy code raised ``RuntimeError`` (for
    example ``"Project is not initialized."``) on these paths and callers may catch it.
    """

    def __init__(self, feature: str, mode, required, detail: str = ""):
        self.feature = feature
        self.mode = mode
        self.required = required
        message = (
            f"{feature} is not available in {_mode_label(mode)} mode; "
            f"it requires {_mode_label(required)} mode."
        )
        if detail:
            message = f"{message} {detail}"
        super().__init__(message)


class CredentialsUnavailableError(StudioContextError, RuntimeError):
    """
    A connection's credentials are needed and the AWS Notebook app vends none: the user is
    signed out, or the app refused this connection's credentials.

    Raised before any AWS call, with the app's own reason, so the message tells the user what
    to do instead of an access-denied error from inside a query.

    Args:
        feature: What needs the credentials (``"Connection 'warehouse'"``).
        detail: The app's reason, when it gave one.
        guidance: What the user should do; the sign-in hint unless the case calls for another.
    """

    GUIDANCE = "Sign in to AWS in the AWS Notebook app and run the cell again."

    def __init__(self, feature: str, detail: str = "", guidance: Optional[str] = None):
        self.feature = feature
        self.detail = detail
        self.guidance = self.GUIDANCE if guidance is None else guidance
        message = f"{feature} has no AWS credentials. {self.guidance}".strip()
        if detail:
            message = f"{message} ({detail})"
        super().__init__(message)


class CredentialsExpiredError(StudioContextError, RuntimeError):
    """
    A connection's credentials were refused by AWS or have expired, and asking the AWS Notebook
    app again did not yield usable ones.
    """

    def __init__(self, detail: str = ""):
        message = (
            "The AWS credentials for this connection have expired. "
            "Sign in to AWS in the AWS Notebook app again."
        )
        super().__init__(f"{message} {detail}".strip())


class AccessDeniedError(StudioContextError, RuntimeError):
    """
    AWS refused a read made as the identity the AWS Notebook app is signed in with (DuckDB's
    credential-chain secret), or as the access role a connection names (assumed for the catalogs
    attached for that connection): that identity may not access the location.

    Distinct from :class:`CredentialsExpiredError`: nothing is stale. For the signed-in identity,
    signing in again as the same identity will not help; switching to a profile that may read the
    location will. For a role, its permissions, or the connection's access role, are what to change.

    Args:
        location: What was being read (``"s3://bucket/key"``, or ``"catalog 'alias'"``), when known.
        account: The AWS account the app is signed in to, when the caller knows it; the SDK's own
            reads name none.
        detail: The error AWS answered with.
        role: The access role the read was made as, when the statement ran against catalogs
            attached with one.
        connections: The connection(s) naming that role.
    """

    def __init__(
        self,
        location: str = "",
        account: Optional[str] = None,
        detail: str = "",
        role: Optional[str] = None,
        connections: Sequence[str] = (),
    ):
        self.location = location
        self.account = account
        self.detail = detail
        self.role = role
        self.connections = list(connections)
        what = f"Reading {location}" if location else "This read"
        if role:
            names = [repr(name) for name in self.connections]
            whose = ""
            if len(names) == 1:
                whose = f" for connection {names[0]}"
            elif names:
                whose = f" for connections {' and '.join(names)}"
            who = f"the role {role}, which the AWS Notebook app assumes{whose}"
            guidance = (
                "Give the role access to it, or change the connection's access role in the AWS "
                "Notebook app, and run the cell again."
            )
        else:
            who = (
                f"the AWS account the app is signed in to ({account})"
                if account
                else "the identity the app is signed in with"
            )
            guidance = "Switch to a profile that may access it in the AWS Notebook app and run the cell again."
        super().__init__(f"{what} was denied to {who}. {guidance} {detail}".strip())


class LocalAppError(StudioContextError, RuntimeError):
    """
    The AWS Notebook app's local API answered an error envelope ``{"error": {"code", "message"}}``.

    Attributes:
        code: The app's error code (``"ResourceNotFoundException"``, ``"ValidationException"`` ...).
        status: The HTTP status the app answered with.
        detail: The app's message.
    """

    def __init__(self, code: str, detail: str, status: int = 0, operation: str = ""):
        self.code = code
        self.status = status
        self.detail = detail
        self.operation = operation
        where = f" ({operation})" if operation else ""
        super().__init__(f"The AWS Notebook app refused the request{where}: {code}: {detail}")


class LocalAppUnavailableError(StudioContextError, RuntimeError):
    """
    The AWS Notebook app's local API could not be reached, or answered something unreadable.

    The kernel was started by the app, so this usually means the app has quit or the
    ``AWS_NOTEBOOK_APP_URL`` the kernel was given is wrong.
    """


class CatalogUnavailableError(StudioContextError, LookupError):
    """
    A DuckDB cell was to run in a catalog (``catalog_name``, and ``schema_name``) that the kernel's
    DuckDB cannot put on its ``search_path``: not attached, no such schema, or no default schema when
    none was named. Raised before the cell's statements run, with the attach's own error when the
    SDK recorded one, so the message says what to do instead of a binder error from inside the query.

    Args:
        catalog: The catalog asked for.
        schema: The schema asked for, when one was.
        detail: Why it is not available.
        guidance: What the user should do.
    """

    def __init__(
        self, catalog: str, schema: Optional[str] = None, detail: str = "", guidance: str = ""
    ):
        self.catalog = catalog
        self.schema = schema
        self.detail = detail
        self.guidance = guidance
        what = f"Catalog {catalog!r}" + (f", schema {schema!r}," if schema else "")
        message = f"{what} is not available on the kernel's DuckDB"
        if detail:
            message = f"{message}: {detail}"
        super().__init__(f"{message}. {guidance}".strip() if guidance else f"{message}.")


def _mode_label(mode) -> str:
    """Render a RuntimeMode (or anything else) for messages without importing local_kernel."""
    name = getattr(mode, "name", None)
    value = getattr(mode, "value", None)
    if name is not None and value is not None:
        return f"{name} ({value})"
    return str(mode)


class ConnectionConfigurationError(ValueError):
    """
    A connection's record lacks something a feature needs from it, such as an AWS region, so the
    feature can't use that connection until the connection is fixed.

    Args:
        connection: The connection's name (or id).
        missing: What the record lacks, in user terms (``"AWS region"``).
        feature: What couldn't be done without it.

    Subclasses :class:`ValueError`, which these paths raised before.
    """

    def __init__(self, connection: str, missing: str, feature: str):
        self.connection = connection
        self.missing = missing
        self.feature = feature
        super().__init__(
            f"Connection {connection!r} has no {missing}, so {feature}. "
            f"Set its {missing} and run the cell again."
        )
