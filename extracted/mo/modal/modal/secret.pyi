import datetime
import google.protobuf.message
import modal._object
import modal.client
import modal.object
import modal_proto.api_pb2
import typing
import typing_extensions

class SecretInfo:
    """Information about the Secret object."""

    name: typing.Optional[str]
    created_at: datetime.datetime
    created_by: typing.Optional[str]

    def __init__(
        self, name: typing.Optional[str], created_at: datetime.datetime, created_by: typing.Optional[str]
    ) -> None:
        """Initialize self.  See help(type(self)) for accurate signature."""
        ...

    def __repr__(self):
        """Return repr(self)."""
        ...

    def __eq__(self, other):
        """Return self==value."""
        ...

class _Secret(modal._object._Object):
    """Secrets provide a dictionary of environment variables for images.

    Secrets are a secure way to add credentials and other sensitive information
    to the containers your functions run in. You can create and edit secrets on
    [the dashboard](https://modal.com/secrets), or programmatically from Python code.

    See [the secrets guide page](https://modal.com/docs/guide/secrets) for more information.
    """

    _metadata: typing.Optional[modal_proto.api_pb2.SecretMetadata]

    @property
    def name(self) -> typing.Optional[str]: ...
    def _hydrate_metadata(self, metadata: typing.Optional[google.protobuf.message.Message]): ...
    def _get_metadata(self) -> modal_proto.api_pb2.SecretMetadata: ...
    @staticmethod
    def from_dict(env_dict: dict[str, typing.Optional[str]] = {}) -> _Secret:
        """Create a secret from a str-str dictionary. Values can also be `None`, which is ignored.

        Usage:
        ```python
        @app.function(secrets=[modal.Secret.from_dict({"FOO": "bar"})])
        def run():
            print(os.environ["FOO"])
        ```
        """
        ...

    @staticmethod
    def from_local_environ(env_keys: list[str]) -> _Secret:
        """Create secrets from local environment variables automatically."""
        ...

    @staticmethod
    def from_dotenv(path=None, *, filename=".env") -> _Secret:
        """Create secrets from a .env file automatically.

        If no argument is provided, it will use the current working directory as the starting
        point for finding a `.env` file. Note that it does not use the location of the module
        calling `Secret.from_dotenv`.

        If called with an argument, it will use that as a starting point for finding `.env` files.
        In particular, you can call it like this:
        ```python
        @app.function(secrets=[modal.Secret.from_dotenv(__file__)])
        def run():
            print(os.environ["USERNAME"])  # Assumes USERNAME is defined in your .env file
        ```

        This will use the location of the script calling `modal.Secret.from_dotenv` as a
        starting point for finding the `.env` file.

        A file named `.env` is expected by default, but this can be overridden with the `filename`
        keyword argument:

        ```python
        @app.function(secrets=[modal.Secret.from_dotenv(filename=".env-dev")])
        def run():
            ...
        ```
        """
        ...

    @staticmethod
    def from_name(
        name: str, *, namespace=None, environment_name: typing.Optional[str] = None, required_keys: list[str] = []
    ) -> _Secret:
        """Reference a Secret by its name.

        In contrast to most other Modal objects, named Secrets must be provisioned
        from the Dashboard. See other methods for alternate ways of creating a new
        Secret from code.

        ```python
        secret = modal.Secret.from_name("my-secret")

        @app.function(secrets=[secret])
        def run():
           ...
        ```
        """
        ...

    @staticmethod
    async def lookup(
        name: str,
        namespace=None,
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
        required_keys: list[str] = [],
    ) -> _Secret:
        """mdmd:hidden"""
        ...

    @staticmethod
    async def create_deployed(
        deployment_name: str,
        env_dict: dict[str, str],
        namespace=None,
        client: typing.Optional[modal.client._Client] = None,
        environment_name: typing.Optional[str] = None,
        overwrite: bool = False,
    ) -> str:
        """mdmd:hidden"""
        ...

    async def info(self) -> SecretInfo:
        """Return information about the Secret object."""
        ...

SUPERSELF = typing.TypeVar("SUPERSELF", covariant=True)

class Secret(modal.object.Object):
    """Secrets provide a dictionary of environment variables for images.

    Secrets are a secure way to add credentials and other sensitive information
    to the containers your functions run in. You can create and edit secrets on
    [the dashboard](https://modal.com/secrets), or programmatically from Python code.

    See [the secrets guide page](https://modal.com/docs/guide/secrets) for more information.
    """

    _metadata: typing.Optional[modal_proto.api_pb2.SecretMetadata]

    def __init__(self, *args, **kwargs):
        """mdmd:hidden"""
        ...

    @property
    def name(self) -> typing.Optional[str]: ...
    def _hydrate_metadata(self, metadata: typing.Optional[google.protobuf.message.Message]): ...
    def _get_metadata(self) -> modal_proto.api_pb2.SecretMetadata: ...
    @staticmethod
    def from_dict(env_dict: dict[str, typing.Optional[str]] = {}) -> Secret:
        """Create a secret from a str-str dictionary. Values can also be `None`, which is ignored.

        Usage:
        ```python
        @app.function(secrets=[modal.Secret.from_dict({"FOO": "bar"})])
        def run():
            print(os.environ["FOO"])
        ```
        """
        ...

    @staticmethod
    def from_local_environ(env_keys: list[str]) -> Secret:
        """Create secrets from local environment variables automatically."""
        ...

    @staticmethod
    def from_dotenv(path=None, *, filename=".env") -> Secret:
        """Create secrets from a .env file automatically.

        If no argument is provided, it will use the current working directory as the starting
        point for finding a `.env` file. Note that it does not use the location of the module
        calling `Secret.from_dotenv`.

        If called with an argument, it will use that as a starting point for finding `.env` files.
        In particular, you can call it like this:
        ```python
        @app.function(secrets=[modal.Secret.from_dotenv(__file__)])
        def run():
            print(os.environ["USERNAME"])  # Assumes USERNAME is defined in your .env file
        ```

        This will use the location of the script calling `modal.Secret.from_dotenv` as a
        starting point for finding the `.env` file.

        A file named `.env` is expected by default, but this can be overridden with the `filename`
        keyword argument:

        ```python
        @app.function(secrets=[modal.Secret.from_dotenv(filename=".env-dev")])
        def run():
            ...
        ```
        """
        ...

    @staticmethod
    def from_name(
        name: str, *, namespace=None, environment_name: typing.Optional[str] = None, required_keys: list[str] = []
    ) -> Secret:
        """Reference a Secret by its name.

        In contrast to most other Modal objects, named Secrets must be provisioned
        from the Dashboard. See other methods for alternate ways of creating a new
        Secret from code.

        ```python
        secret = modal.Secret.from_name("my-secret")

        @app.function(secrets=[secret])
        def run():
           ...
        ```
        """
        ...

    class __lookup_spec(typing_extensions.Protocol):
        def __call__(
            self,
            /,
            name: str,
            namespace=None,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            required_keys: list[str] = [],
        ) -> Secret:
            """mdmd:hidden"""
            ...

        async def aio(
            self,
            /,
            name: str,
            namespace=None,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            required_keys: list[str] = [],
        ) -> Secret:
            """mdmd:hidden"""
            ...

    lookup: __lookup_spec

    class __create_deployed_spec(typing_extensions.Protocol):
        def __call__(
            self,
            /,
            deployment_name: str,
            env_dict: dict[str, str],
            namespace=None,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            overwrite: bool = False,
        ) -> str:
            """mdmd:hidden"""
            ...

        async def aio(
            self,
            /,
            deployment_name: str,
            env_dict: dict[str, str],
            namespace=None,
            client: typing.Optional[modal.client.Client] = None,
            environment_name: typing.Optional[str] = None,
            overwrite: bool = False,
        ) -> str:
            """mdmd:hidden"""
            ...

    create_deployed: __create_deployed_spec

    class __info_spec(typing_extensions.Protocol[SUPERSELF]):
        def __call__(self, /) -> SecretInfo:
            """Return information about the Secret object."""
            ...

        async def aio(self, /) -> SecretInfo:
            """Return information about the Secret object."""
            ...

    info: __info_spec[typing_extensions.Self]
