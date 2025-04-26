"""
Cloud (and similarly its subclass CloudV2) is not intended as a user-facing API but rather is a helper
for implementing top-level user-facing functions.

* Cloud contains methods for our "v1" API (e.g. software environments)
* CloudV2 contains methods for our "v2" API (clusters, package sync)

A few methods in Cloud are reused by CloudV2, but not much. Ideally we would completely separate these classes
so there's no subclass relationship, or implement a tiny base class CloudBase with subclasses CloudV1 and CloudV2.

Some notes on async:

Because the distributed API can be used as either async and sync, Coiled can too. This is implemented with
leading-underscore async-only functions like "Cloud._create_software_environment", and then non-underscored
versions like "Cloud.create_software_environment", where the latter uses a helper method "cloud.sync" to do
the right thing depending on whether we're in a sync or async context.

When it comes to the Cluster class, this complexity is probably forced on us by distributed supporting sync and async.
But for our own stuff (e.g. create_software_environment) we could probably simplify to a simpler sync-only API
if we choose.
"""

from __future__ import annotations

import asyncio
import base64
import datetime
import json
import logging
import numbers
import os
import pathlib
import platform
import sys
import threading
import time
import warnings
import weakref
from contextlib import contextmanager
from dataclasses import dataclass
from hashlib import md5
from json.decoder import JSONDecodeError
from typing import (
    Any,
    Awaitable,
    BinaryIO,
    Callable,
    Coroutine,
    Dict,
    Generator,
    Generic,
    List,
    TextIO,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

import aiohttp
import backoff
import dask
import dask.config
import dask.distributed
import distributed
import httpx
import rich
from distributed.comm.addressing import parse_address
from distributed.utils import LoopRunner, sync
from importlib_metadata import PackageNotFoundError, version
from packaging.version import Version
from rich.console import Console
from rich.text import Text
from tornado.ioloop import IOLoop
from typing_extensions import Literal, ParamSpec, Protocol, TypeAlias

from coiled.exceptions import (
    AccountConflictError,
    ApiResponseStatusError,
    AWSCredentialsParameterError,
    BuildError,
    GCPCredentialsError,
    GCPCredentialsParameterError,
    NotFound,
    PermissionsError,
    RegistryParameterError,
    UnsupportedBackendError,
)
from coiled.scan import scan_prefix
from coiled.software import create_env_spec
from coiled.software_utils import (
    create_wheel,
    create_wheels_for_local_python,
    partition_ignored_packages,
    partition_local_packages,
    partition_local_python_code_packages,
)

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

from .compatibility import COILED_VERSION, PY_VERSION
from .context import COILED_SESSION_ID, TRACE_CONFIG, track_context
from .software_utils import get_index_urls
from .types import (
    ApproximatePackageRequest,
    ApproximatePackageResult,
    ArchitectureTypesEnum,
    CondaEnvSchema,
    PackageLevelEnum,
    SoftwareEnvironmentAlias,
    SoftwareEnvSpec,
)
from .utils import (
    ALLOWED_PROVIDERS,
    COILED_LOGGER_NAME,
    AsyncBytesIO,
    Spinner,
    VmType,
    error_info_for_tracking,
    experimental,
    get_auth_header_value,
    handle_api_exception,
    handle_credentials,
    in_async_call,
    parse_gcp_region_zone,
    parse_identifier,
    parse_requested_memory,
    rich_console,
    verify_aws_credentials_with_retry,
)
from .websockets import ConfigureBackendConnector

logger = logging.getLogger(COILED_LOGGER_NAME)
console = Console()
SUPPORTED_BACKENDS = {"aws", "gcp"}


class BackoffLogLevelKwargs(TypedDict, total=False):
    backoff_log_level: int


backoff_log_level_kwargs: BackoffLogLevelKwargs = (
    {"backoff_log_level": logging.DEBUG}
    if Version(getattr(backoff, "__version__", "0.0.0")) >= Version("1.11.0")
    else {}
)


class AWSSessionCredentials(TypedDict):
    AccessKeyId: str
    SecretAccessKey: str
    SessionToken: str | None
    Expiration: datetime.datetime | None
    DefaultRegion: str | None


def delete_docstring(func):
    delete_doc = """ Delete a {kind}

Parameters
---------
name
    Name of {kind} to delete.
"""
    func_name = func.__name__
    kind = " ".join(func_name.split("_")[1:])  # delete_software_environments -> software environments
    func.__doc__ = delete_doc.format(kind=kind)
    return func


def list_docstring(func):
    list_doc = """ List {kind}s

Parameters
---------
account
    Name of the Coiled account to list {kind}s.
    If not provided, will use the ``coiled.account`` configuration
    value.

Returns
-------
:
    Dictionary with information about each {kind} in the
    specified account. Keys in the dictionary are names of {kind}s,
    while the values contain information about the corresponding {kind}.
"""
    func_name = func.__name__
    kind = " ".join(func_name.split("_")[1:])
    kind = kind[:-1]  # drop trailing "s"
    func.__doc__ = list_doc.format(kind=kind)
    return func


# This lock helps avoid a race condition between cluster creation in the
# in process backend, which temporarily modify coiled's dask config values,
# and the creation of new Cloud objects, with load those same config values.
# This works, but is not ideal.
_cluster_creation_lock = threading.RLock()


# Generic TypeVar for return value from sync/async function.
_T = TypeVar("_T")


# A generic that can only be True/False, allowing us to type async/sync
# versions of coiled objects.
Async = Literal[True]
Sync = Literal[False]
IsAsynchronous = TypeVar("IsAsynchronous", Async, Sync)
CloudSyncAsync: TypeAlias = Union["Cloud[Async]", "Cloud[Sync]"]
SYNC_PARAMS = ParamSpec("SYNC_PARAMS")


# Short of writing type stubs for distributed or typing the underlying package,
# this is a useful cast.
class _SyncProtocol(Protocol):
    def __call__(
        self,
        loop: IOLoop,
        func: Callable[..., Awaitable[_T]],
        *args: Any,
        callback_timeout: numbers.Number | None,
        **kwargs: Any,
    ) -> _T: ...


sync = cast(_SyncProtocol, sync)


class Cloud(Generic[IsAsynchronous]):
    """Connect to Coiled

    Parameters
    ----------
    user
        Username for Coiled account. If not specified, will check the
        ``coiled.user`` configuration value.
    token
        Token for Coiled account. If not specified, will check the
        ``coiled.token`` configuration value.
    server
        Server to connect to. If not specified, will check the
        ``coiled.server`` configuration value.
    account
        **DEPRECATED**. Use ``workspace`` instead.
    workspace
        The Coiled workspace (previously "account") to use. If not specified,
        will check the ``coiled.workspace`` or ``coiled.account`` configuration values,
        or will use your default workspace if those aren't set.
    asynchronous
        Set to True if using this Cloud within ``async``/``await`` functions or
        within Tornado ``gen.coroutines``. Otherwise this should remain
        ``False`` for normal use. Default is ``False``.
    loop
        If given, this event loop will be re-used, otherwise an appropriate one
        will be looked up or created.
    default_cluster_timeout
        Default timeout in seconds to wait for cluster startup before raising ``TimeoutError``.
        Pass ``None`` to wait forever, otherwise the default is 20 minutes.
    """

    _recent_sync: List[weakref.ReferenceType[Cloud[Sync]]] = list()
    _recent_async: List[weakref.ReferenceType[Cloud[Async]]] = list()

    @overload
    def __init__(
        self: Cloud[Sync],
        user: str | None = None,
        token: str | None = None,
        server: str | None = None,
        account: str | None = None,
        workspace: str | None = None,
        asynchronous: Sync = False,
        loop: IOLoop | None = None,
        default_cluster_timeout: int = 20 * 60,
    ): ...

    @overload
    def __init__(
        self: Cloud[Async],
        user: str | None = None,
        token: str | None = None,
        server: str | None = None,
        account: str | None = None,
        workspace: str | None = None,
        asynchronous: Async = True,
        loop: IOLoop | None = None,
        default_cluster_timeout: int = 20 * 60,
    ): ...

    def __init__(
        self: CloudSyncAsync,
        user: str | None = None,
        token: str | None = None,
        server: str | None = None,
        account: str | None = None,
        workspace: str | None = None,
        asynchronous: bool = False,
        loop: IOLoop | None = None,
        default_cluster_timeout: int = 20 * 60,
    ):
        # TODO deprecation warning for account
        with _cluster_creation_lock:
            self.user = user or dask.config.get("coiled.user")
            self.token = token or dask.config.get("coiled.token")
            self.server = server or dask.config.get("coiled.server")
            if "://" not in self.server:
                self.server = "http://" + self.server
            self.server = self.server.rstrip("/")
            self._default_account = (
                workspace or account or dask.config.get("coiled.workspace", dask.config.get("coiled.account"))
            )
            self._default_backend_options = dask.config.get("coiled.backend-options", None) or {}
        self.session: aiohttp.ClientSession | None = None
        self.status = "init"
        self.cluster_id: int | None = None
        self._asynchronous = asynchronous
        self._loop_runner = LoopRunner(loop=loop, asynchronous=asynchronous)
        self._loop_runner.start()
        self.default_cluster_timeout = default_cluster_timeout

        if asynchronous:
            self._recent_async.append(weakref.ref(cast(Cloud[Async], self)))
        else:
            self._recent_sync.append(weakref.ref(cast(Cloud[Sync], self)))

        if not self.asynchronous:
            self._sync(self._start)

    def __repr__(self):
        return f"<Cloud: {self.user}@{self.server} - {self.status}>"

    def _repr_html_(self):
        text = (
            '<h3 style="text-align: left;">Cloud</h3>\n'
            '<ul style="text-align: left; list-style: none; margin: 0; padding: 0;">\n'
            f"  <li><b>User: </b>{self.user}</li>\n"
            f"  <li><b>Server: </b>{self.server}</li>\n"
            f"  <li><b>Workspace: </b>{self.default_workspace}</li>\n"
        )

        return text

    @property
    def loop(self) -> IOLoop:
        return self._loop_runner.loop

    @overload
    @classmethod
    def current(cls, asynchronous: Sync) -> Cloud[Sync]: ...

    @overload
    @classmethod
    def current(cls, asynchronous: Async) -> Cloud[Async]: ...

    @overload
    @classmethod
    def current(cls, asynchronous: bool) -> Cloud: ...

    @classmethod
    def current(cls: Type[Cloud], asynchronous: bool) -> Cloud:
        recent: List[weakref.ReferenceType[Cloud]]
        if asynchronous:
            recent = cls._recent_async
        else:
            recent = cls._recent_sync
        try:
            cloud = recent[-1]()
            while cloud is None or cloud.status != "running":
                recent.pop()
                cloud = recent[-1]()
        except IndexError:
            if asynchronous:
                return cls(asynchronous=True)
            else:
                return cls(asynchronous=False)
        else:
            return cloud

    @property
    def closed(self) -> bool:
        if self.session:
            return self.session.closed
        # If we haven't opened, we must be closed?
        return True

    @backoff.on_exception(
        backoff.expo,
        # `aiohttp.client_exceptions.ClientOSError` is the same as `aiohttp.ClientOSError`
        # except that pyright doesn't like the former
        aiohttp.ClientOSError,
        logger=logger,
        max_time=5 * 60,
        **backoff_log_level_kwargs,
    )
    async def _do_request_idempotent(self, *args, ensure_running: bool = True, **kwargs):
        """
        This method retries more aggressively than _do_request.

        We may retry with no knowledge of the state of the original request so this
        should only ever be used to make idempotent API calls (e.g. non-mutating calls).
        """
        return await self._do_request(*args, ensure_running=ensure_running, **kwargs)

    @backoff.on_predicate(
        backoff.expo,
        lambda resp: resp.status in [502, 503, 504, 429],
        logger=logger,
        max_time=5 * 60,
        max_value=15,
    )
    async def _do_request(self, *args, ensure_running: bool = True, **kwargs):
        """
        This wraps the session.request call and injects a per-call UUID.

        Most of the time we check that this is in a "running" state before making
        requests. However, we can disable that by passing in ensure_running=False
        """
        session = self._ensure_session(ensure_running)
        response = await session.request(*args, **kwargs)
        return response

    def _ensure_session(self, ensure_running=True) -> aiohttp.ClientSession:
        if self.session and (not ensure_running or self.status == "running"):
            return self.session
        else:
            raise RuntimeError("Cloud is not running, did you forget to await it?")

    @track_context
    async def _start(self):
        if self.status != "init":
            return self
        # Check that server and token are valid
        self.user, self.token, self.server, memberships = await handle_credentials(
            server=self.server, token=self.token, save=None if not self.token else False
        )

        self.session = aiohttp.ClientSession(
            trace_configs=[TRACE_CONFIG],
            headers={
                "Authorization": get_auth_header_value(self.token),
                "Client-Version": COILED_VERSION,
                "coiled-session-id": COILED_SESSION_ID,
            },
        )
        self.accounts = {d["account"]["slug"]: {**d["account"], "admin": d["is_admin"]} for d in memberships}

        # get default account set in database
        if not self._default_account:
            for d in memberships:
                if d["is_default_account"]:
                    self._default_account = d["account"]["slug"]
                    break

        if self._default_account:
            await self._verify_workspace(self._default_account)

        self.status = "running"

        return self

    @property
    def default_account(self):
        warnings.warn(
            "The `default_account` property is deprecated, use `default_workspace` instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.default_workspace

    @property
    def default_workspace(self) -> str:
        # "default" could be from kwarg, local config, or database (in that order)
        if self._default_account:
            return self._default_account
        # if there's a single account for user, then that's the only option
        elif len(self.accounts) == 1:
            return next(iter(self.accounts))
        # otherwise, pick the account that matches user
        # (even though likely to be wrong choice if they're a member of a company account)
        elif self.user in self.accounts:
            return self.user
        elif self.user.lower() in self.accounts:
            return self.user.lower()
        elif not self.accounts:
            raise ValueError("No workspace memberships found for user")
        else:
            raise ValueError(
                "No default workspace is set. Please specify one of the workspaces your user is in: "
                f"{', '.join(self.accounts.keys())}",
            )

    async def _close(self) -> None:
        if self.session:
            await self.session.close()
        self.status = "closed"

    @overload
    def close(self: Cloud[Sync]) -> None: ...

    @overload
    def close(self: Cloud[Async]) -> Awaitable[None]: ...

    def close(self: CloudSyncAsync) -> Awaitable[None] | None:
        """Close connection to Coiled"""
        result = self._sync(self._close)
        self._loop_runner.stop()
        return result

    def __await__(
        self: Cloud[Async],
    ) -> Generator[None, None, Cloud[Async]]:
        return self._start().__await__()

    async def __aenter__(self: Cloud[Async]) -> Cloud[Async]:
        return await self._start()

    async def __aexit__(self: Cloud[Async], typ, value, tb) -> None:
        await self._close()

    def __enter__(self: Cloud[Sync]) -> Cloud[Sync]:
        return self

    def __exit__(self: Cloud[Sync], typ, value, tb) -> None:
        self.close()

    @property
    def asynchronous(self) -> bool:
        """Are we running in the event loop?"""
        return in_async_call(self.loop, default=self._asynchronous)

    @overload
    def _sync(
        self: Cloud[Sync],
        func: Callable[SYNC_PARAMS, Coroutine[None, None, _T]],
        *args: SYNC_PARAMS.args,
        **kwargs: SYNC_PARAMS.kwargs,
    ) -> _T: ...

    @overload
    def _sync(
        self: Cloud[Async],
        func: Callable[SYNC_PARAMS, Coroutine[None, None, _T]],
        *args: SYNC_PARAMS.args,
        **kwargs: SYNC_PARAMS.kwargs,
    ) -> Coroutine[None, None, _T]: ...

    def _sync(
        self,
        func: Callable[SYNC_PARAMS, Coroutine[None, None, _T]],
        *args: SYNC_PARAMS.args,
        **kwargs: SYNC_PARAMS.kwargs,
    ) -> Union[_T, Coroutine[None, None, _T]]:
        asynchronous = self.asynchronous
        if asynchronous:
            future = func(*args, **kwargs)
            future = asyncio.wait_for(future, timeout=None)
            return future
        else:
            return cast(_T, sync(self.loop, func, *args, callback_timeout=None, **kwargs))

    async def _verify_workspace(self, workspace: str):
        """Perform sanity checks on workspace values

        In particular, this raises and informative error message if the
        workspace is not found, and provides a list of possible options.
        """
        workspace = workspace or self.default_workspace
        if workspace not in self.accounts:
            await self._close()
            if workspace:
                match_on_name = [
                    w.get("slug") for w in self.accounts.values() if w.get("name", "").lower() == workspace.lower()
                ]
                if match_on_name:
                    raise PermissionsError(
                        f"Please use the workspace slug '{match_on_name[0]}' instead of the name '{workspace}'."
                    )
            raise PermissionError(f"Workspace not found: {workspace!r}\nPossible workspaces: {sorted(self.accounts)}")

    def _verify_per_cluster_backend_options(self, backend_options: dict | None = None):
        """Validation for cluster- (vs account-) level specified options."""
        backend_options = backend_options or {}
        if "network" in backend_options:
            raise PermissionError(
                "Network options cannot be specified per cluster. Use coiled.set_backend_options() to set for account."
            )

    @overload
    def create_api_token(
        self: Cloud[Sync],
        *,
        label: str | None = None,
        days_to_expire: int | None = None,
    ) -> dict: ...

    @overload
    def create_api_token(
        self: Cloud[Async],
        *,
        label: str | None = None,
        days_to_expire: int | None = None,
    ) -> Awaitable[dict]: ...

    def create_api_token(
        self: Union[Cloud[Async], Cloud[Sync]],
        *,
        label: str | None = None,
        days_to_expire: int | None = None,
    ) -> Union[dict, Awaitable[dict]]:
        return self._sync(self._create_api_token, label=label, days_to_expire=days_to_expire)

    @overload
    def list_api_tokens(self: Cloud[Sync], include_inactive: bool = False) -> Dict[str, dict]: ...

    @overload
    def list_api_tokens(self: Cloud[Async], include_inactive: bool = False) -> Awaitable[Dict[str, dict]]: ...

    def list_api_tokens(
        self: Union[Cloud[Async], Cloud[Sync]], include_inactive: bool = False
    ) -> Union[Awaitable[Dict[str, dict]], Dict[str, dict]]:
        return self._sync(self._list_api_tokens, include_inactive=include_inactive)

    @overload
    def revoke_all_api_tokens(self: Cloud[Sync]) -> None: ...

    @overload
    def revoke_all_api_tokens(self: Cloud[Async]) -> Awaitable[None]: ...

    def revoke_all_api_tokens(self: CloudSyncAsync) -> Awaitable[None] | None:
        return self._sync(
            self._revoke_all_api_tokens,
        )

    async def _revoke_all_api_tokens(self) -> None:
        tokens = await self._list_api_tokens(include_inactive=True)
        logged_in_token_id = None
        # we could be more asyncy here by kicking off multiple revokes
        # at once but this seems fine
        for token_id in tokens:
            if self.token.startswith(token_id):
                # this is the current token! revoke it last
                logged_in_token_id = token_id
            else:
                await self._revoke_api_token(identifier=token_id)

        # after transitioning to new api tokens, we expect we would
        # find the in-use token in the tokens list
        # but in the meantime the in-use token might be an old-style one we can't revoke
        if logged_in_token_id is None:
            rich.print("Did not revoke the token you're logged in with now.")
        else:
            await self._revoke_api_token(identifier=logged_in_token_id)

    @overload
    def revoke_api_token(
        self: Cloud[Sync],
        *,
        identifier: str | None = None,
        label: str | None = None,
    ) -> None: ...

    @overload
    def revoke_api_token(
        self: Cloud[Async],
        *,
        identifier: str | None = None,
        label: str | None = None,
    ) -> Awaitable[None]: ...

    def revoke_api_token(
        self: CloudSyncAsync,
        *,
        identifier: str | None = None,
        label: str | None = None,
    ) -> Union[None, Awaitable[None]]:
        return self._sync(self._revoke_api_token, identifier=identifier, label=label)

    @track_context
    async def _create_senv_package(
        self,
        package_file: BinaryIO,
        contents_md5: str,
        workspace: str | None = None,
        region_name: str | None = None,
    ) -> int:
        package_name = pathlib.Path(package_file.name).name
        logger.debug(f"Starting upload for {package_name}")
        package_bytes = package_file.read()
        # s3 expects the md5 to be base64 encoded
        wheel_md5 = base64.b64encode(md5(package_bytes).digest()).decode("utf-8")
        workspace = workspace or self.default_workspace

        response = await self._do_request(
            "POST",
            self.server + f"/api/v2/software-environment/account/{workspace}/package-upload",
            json={
                "name": package_name,
                "md5": contents_md5,
                "wheel_md5": wheel_md5,
                "region_name": region_name,
            },
        )
        if response.status >= 400:
            await handle_api_exception(response)  # always raises exception, no return
        data = await response.json()
        if data["should_upload"]:
            num_bytes = len(package_bytes)
            await self._put_package(
                url=data["upload_url"],
                package_data=AsyncBytesIO(package_bytes),
                file_md5=wheel_md5,
                num_bytes=num_bytes,
            )
        else:
            logger.debug(f"{package_name} MD5 matches existing, skipping upload")
        return data["id"]

    @backoff.on_exception(
        backoff.expo,
        aiohttp.ClientResponseError,
        max_time=120,
        giveup=lambda error: cast(aiohttp.ClientResponseError, error).status < 500,
    )
    async def _put_package(self, url: str, package_data: AsyncBytesIO, file_md5: str, num_bytes: int):
        # can't use the default session as it has coiled auth headers
        async with httpx.AsyncClient(http2=True) as client:
            headers = {
                "Content-Type": "binary/octet-stream",
                "Content-Length": str(num_bytes),
                "content-md5": file_md5,
            }
            if "blob.core.windows.net" in url:
                headers["x-ms-blob-type"] = "BlockBlob"
            response = await client.put(
                url=url,
                # content must be set to an iterable of bytes, rather than a
                # bytes object (like file.read()) because files >2GB need
                # to be sent in chunks to avoid an OverflowError in the
                # Python stdlib ssl module, and httpx will not chunk up a
                # bytes object automatically.
                content=package_data,
                headers=headers,
                timeout=60,
            )
            response.raise_for_status()

    @overload
    def create_software_environment(
        self: Cloud[Sync],
        name: str | None = None,
        *,
        account: str | None = None,
        workspace: str | None = None,
        conda: Union[list, CondaEnvSchema, str, pathlib.Path] | None = None,
        pip: Union[list, str, pathlib.Path] | None = None,
        container: str | None = None,
        log_output=sys.stdout,
        force_rebuild: bool = False,
        use_entrypoint: bool = True,
        wait_build: bool = True,
        gpu_enabled: bool = False,
        architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
        arm: bool = False,
        region_name: str | None = None,
        include_local_code: bool = False,
        ignore_local_packages: List[str] | None = None,
        use_uv_installer: bool = True,
    ) -> SoftwareEnvironmentAlias | None: ...

    @overload
    def create_software_environment(
        self: Cloud[Async],
        name: str | None = None,
        *,
        account: str | None = None,
        workspace: str | None = None,
        conda: Union[list, CondaEnvSchema, str, pathlib.Path] | None = None,
        pip: Union[list, str, pathlib.Path] | None = None,
        container: str | None = None,
        log_output=sys.stdout,
        force_rebuild: bool = False,
        use_entrypoint: bool = True,
        wait_build: bool = True,
        gpu_enabled: bool = False,
        architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
        arm: bool = False,
        region_name: str | None = None,
        include_local_code: bool = False,
        ignore_local_packages: List[str] | None = None,
        use_uv_installer: bool = True,
    ) -> Awaitable[SoftwareEnvironmentAlias | None]: ...

    def create_software_environment(
        self: CloudSyncAsync,
        name: str | None = None,
        *,
        account: str | None = None,
        workspace: str | None = None,
        conda: Union[list, CondaEnvSchema, str, pathlib.Path] | None = None,
        pip: Union[list, str, pathlib.Path] | None = None,
        container: str | None = None,
        log_output=sys.stdout,
        force_rebuild: bool = False,
        use_entrypoint: bool = True,
        wait_build: bool = True,
        gpu_enabled: bool = False,
        architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
        arm: bool = False,
        region_name: str | None = None,
        include_local_code: bool = False,
        ignore_local_packages: List[str] | None = None,
        use_uv_installer: bool = True,
    ) -> Union[
        Awaitable[SoftwareEnvironmentAlias | None],
        SoftwareEnvironmentAlias | None,
    ]:
        return self._sync(
            self._create_software_environment,
            name=name,
            workspace=workspace or account,
            conda=conda,
            pip=pip,
            container=container,
            log_output=log_output,
            force_rebuild=force_rebuild,
            use_entrypoint=use_entrypoint,
            wait_build=wait_build,
            gpu_enabled=gpu_enabled,
            architecture=ArchitectureTypesEnum.ARM64 if arm else architecture,  # arm bool takes precedence
            region_name=region_name,
            include_local_code=include_local_code,
            ignore_local_packages=ignore_local_packages,
            use_uv_installer=use_uv_installer,
        )

    @track_context
    async def _create_software_environment(
        self,
        name: str | None = None,
        *,
        workspace: str | None = None,
        conda: Union[CondaEnvSchema, str, pathlib.Path, list, None] = None,
        pip: Union[List[str], str, pathlib.Path, None] = None,
        container: str | None = None,
        log_output=sys.stdout,
        force_rebuild: bool = False,
        use_entrypoint: bool = True,
        wait_build: bool = True,
        gpu_enabled: bool = False,
        architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
        region_name: str | None = None,
        include_local_code: bool = False,
        ignore_local_packages: List[str] | None = None,
        use_uv_installer: bool = True,
    ) -> SoftwareEnvironmentAlias | None:
        if name is None and conda is not None and isinstance(conda, dict) and "name" in conda:
            name = conda["name"]
        if ignore_local_packages is None:
            ignore_local_packages = []
        if name is None:
            raise ValueError("Must provide a name when creating a software environment")

        workspace, name = self._normalize_name(
            str(name),
            context_workspace=workspace,
            raise_on_account_conflict=True,
            property_name="software environment name",
        )

        if (pip or conda) and container:
            raise TypeError("The build backend does not support specifying both packages and a container")
        if container and include_local_code:
            raise TypeError("The build backend does not support including local code when using a container")
        if conda or pip:
            senv = await create_env_spec(conda=conda, pip=pip)
            if include_local_code:
                prefix = await scan_prefix()
                packages, _ = partition_ignored_packages(
                    prefix, {(k, "pip"): PackageLevelEnum.IGNORE for k in ignore_local_packages}
                )
                packages, local_packages = partition_local_python_code_packages(packages)
                _, editable_packages = partition_local_packages(packages)

                extra_packages = await create_wheels_for_local_python(local_packages)
                for package in editable_packages:
                    wheel_result = await create_wheel(
                        pkg_name=package["name"], version=package["version"], src=cast(str, package["wheel_target"])
                    )
                    if wheel_result["error"]:
                        raise BuildError(f"Failed to build wheel for {package['name']}: {package['wheel_target']}")
                    else:
                        extra_packages.append(wheel_result)

                for package in extra_packages:
                    if package["sdist"] and package["md5"]:
                        file_id = await self._create_senv_package(
                            package_file=package["sdist"],
                            contents_md5=package["md5"],
                            workspace=workspace,
                            region_name=region_name,
                        )
                        senv["packages"].append({
                            "name": package["name"],
                            "source": package["source"],
                            "channel": package["channel"],
                            "conda_name": package["conda_name"],
                            "specifier": package["specifier"],
                            "include": package["include"],
                            "client_version": package["client_version"],
                            "file": file_id,
                        })
        else:
            senv = None
        logger.info("Creating software environment")

        alias = await self._create_software_environment_v2(
            senv=senv,
            container=container,
            name=name,
            workspace=workspace,
            force_rebuild=force_rebuild,
            use_entrypoint=use_entrypoint,
            gpu_enabled=gpu_enabled,
            architecture=architecture,
            region_name=region_name,
            use_uv_installer=use_uv_installer,
        )
        if wait_build and alias:
            # pyright complains unless we nest like this
            # only tail software environments that have builds
            if alias.get("latest_spec"):
                assert alias["latest_spec"]
                spec = alias["latest_spec"]
                if spec.get("latest_build"):
                    assert spec["latest_build"]
                    build = spec["latest_build"]
                    if build["state"] == "built":
                        logger.info("Software environment already built")
                    else:
                        log_output.write("--- Logs from remote build follow ---\n")
                        final_state = await self._tail_software_build_logs(
                            build["id"], workspace=workspace, log_output=log_output
                        )
                        info_url = (
                            self.server + f"/software/alias/{alias['id']}"
                            f"/build/{build['id']}?account={workspace}&tab=logs"
                        )
                        log_output.write(f"--- Logs end, may be truncated, see {info_url} for full output ---\n")
                        if final_state == "error":
                            raise BuildError("The software environment failed to build")
            logger.info("Software environment created")
        return alias

    @track_context
    async def _approximate_packages(
        self,
        packages: List[ApproximatePackageRequest],
        architecture: ArchitectureTypesEnum,
        pip_check_errors: Dict[str, List[str]] | None = None,
        gpu_enabled: bool = False,
    ) -> List[ApproximatePackageResult]:
        response = await self._do_request(
            "POST",
            f"{self.server}/api/v2/software-environment/approximate-packages",
            json={
                "architecture": architecture,
                "packages": packages,
                "metadata": {
                    "base_prefix": sys.base_prefix,
                    "platform": platform.platform(),
                    "prefix": sys.prefix,
                    "sys_path": sys.path,
                },
                "index_urls": get_index_urls(),
                "pip_check_errors": pip_check_errors,
                "gpu_enabled": gpu_enabled,
            },
        )
        if response.status >= 400:
            await handle_api_exception(response)
        return await response.json()

    async def _tail_software_build_logs(
        self,
        senv_build_id: int,
        workspace: str | None = None,
        log_output: TextIO = sys.stdout,
    ) -> str:
        workspace = workspace or self.default_workspace
        build = await self._fetch_software_build(senv_build_id, workspace=workspace)
        page_token = None
        logs = await self._fetch_software_build_logs(senv_build_id, workspace=workspace, page_token=page_token)
        printed_logs = set()
        for log in logs["events"]:
            log_output.write(log["message"] + "\n")
            printed_logs.add(log["eventId"])
        page_token = logs["nextToken"]
        while build["state"] not in ["error", "built"]:
            logs = await self._fetch_software_build_logs(senv_build_id, workspace=workspace, page_token=page_token)
            if logs["nextToken"] != page_token:
                for log in logs["events"]:
                    if log["eventId"] not in printed_logs:
                        log_output.write(log["message"] + "\n")
                        printed_logs.add(log["eventId"])
            await asyncio.sleep(1)
            page_token = logs["nextToken"]
            build = await self._fetch_software_build(senv_build_id, workspace=workspace)
        if build["state"] == "error":
            logger.error(f"Build failed: {build['reason']}" + "\n")
        else:
            logger.info("Build successful" + "\n")
        return build["state"]

    async def _fetch_software_build(self, senv_build_id: int, workspace: str | None = None):
        workspace = workspace or self.default_workspace
        resp = await self._do_request(
            "GET",
            self.server + f"/api/v2/software-environment/account/{workspace}/build/{senv_build_id}",
        )
        return await resp.json()

    async def _fetch_software_build_logs(
        self,
        senv_build_id: int,
        workspace: str | None = None,
        page_token: str | None = None,
        limit: int = 500,
    ):
        workspace = workspace or self.default_workspace
        params: Dict[str, Union[int, str]] = {"limit": limit}
        if page_token:
            params["pageToken"] = page_token
        resp = await self._do_request(
            "GET",
            self.server + f"/api/v2/software-environment/account/{workspace}/build/logs/{senv_build_id}",
            params=params,
        )
        return await resp.json()

    async def _create_software_environment_v2(
        self,
        senv: SoftwareEnvSpec | None = None,
        container: str | None = None,
        workspace: str | None = None,
        name: str | None = None,
        force_rebuild: bool | None = False,
        use_entrypoint: bool | None = None,
        gpu_enabled: bool = False,
        architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
        region_name: str | None = None,
        use_uv_installer: bool = True,
    ) -> SoftwareEnvironmentAlias:
        workspace = workspace or self.default_workspace
        payload = {
            "name": name,
            "container": container,
            "force_rebuild": force_rebuild,
            "md5": md5(json.dumps(senv, sort_keys=True).encode("utf-8")).hexdigest(),
            "use_entrypoint": use_entrypoint,
            "gpu_enabled": gpu_enabled,
            "architecture": architecture,
            "region_name": region_name,
            "enable_experimental_installer": use_uv_installer,
        }
        if senv:
            payload["packages"] = senv["packages"]
            payload["raw_conda"] = senv["raw_conda"]
            payload["raw_pip"] = senv["raw_pip"]
        resp = await self._do_request(
            "POST",
            self.server + f"/api/v2/software-environment/account/{workspace}",
            json=payload,
        )
        if resp.status >= 400:
            await handle_api_exception(resp)  # always raises exception, no return
        data = await resp.json()
        return data

    @track_context
    async def _create_api_token(self, label: str | None = None, days_to_expire: int | None = None) -> dict:
        label_str = "no label" if label is None else f"label '{label}'"
        rich.print(f"Generating an API token with {label_str} expiring in {days_to_expire} days...")

        data = {}
        if label is not None:
            data["label"] = label
        if days_to_expire is not None:
            expiry = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=days_to_expire)
            data["expiry"] = expiry.isoformat()
        response = await self._do_request(
            "POST",
            self.server + "/api/v1/api-tokens/",
            json=data,
        )
        if response.status >= 400:
            await handle_api_exception(response)

        return await response.json()

    @track_context
    async def _list_api_tokens(self, include_inactive) -> Dict[str, dict]:
        tokens = await self._depaginate(self._list_api_tokens_page)
        if include_inactive:
            return tokens
        else:
            return {
                t_id: t_details
                for t_id, t_details in tokens.items()
                if not t_details["revoked"] and not t_details["expired"]
            }

    @track_context
    async def _list_api_tokens_page(self, page: int) -> Tuple[Dict[str, dict], str | None]:
        response = await self._do_request(
            "GET",
            self.server + "/api/v1/api-tokens/",
            params={"page": page},
        )
        if response.status >= 400:
            await handle_api_exception(response)
            return {}, None
        else:
            response_json = await response.json()
            results = {r["identifier"]: r for r in response_json["results"]}
            return results, response_json["next"]

    @track_context
    async def _revoke_api_token(self, *, identifier: str | None = None, label: str | None = None) -> None:
        if label is None and identifier is None:
            raise ValueError("We need a label or identifier to revoke a token.")

        if label is not None:
            if identifier is not None:
                raise ValueError("Only a label or identifier should be provided, but not both.")

            tokens = await self._list_api_tokens(include_inactive=False)
            identifiers_found = [token_id for token_id, details in tokens.items() if details["label"] == label]

            if len(identifiers_found) == 0:
                raise ValueError(f"Found no tokens with label '{label}'.")
            elif len(identifiers_found) > 1:
                raise ValueError(
                    f"Found multiple tokens with label '{label}'. Please revoke with the `identifier` instead."
                )

            else:
                [identifier] = identifiers_found

        rich.print(f"Revoking API token with identifier '{identifier}' ...")

        response = await self._do_request(
            "DELETE",
            self.server + f"/api/v1/api-tokens/{identifier}/revoke",
        )

        if response.status >= 400:
            if response.status == 404:
                raise ValueError(f"Could not find an API token with identifier {identifier}")
            await handle_api_exception(response)

    @staticmethod
    async def _depaginate(
        func: Callable[..., Awaitable[Tuple[dict, Union[bool, str] | None]]],
        *args,
        **kwargs,
    ) -> dict:
        results_all = {}
        page = 1
        while True:
            kwargs["page"] = page
            results, next = await func(*args, **kwargs)
            results_all.update(results)
            page += 1
            if (not results) or next is None:
                break
        return results_all

    @staticmethod
    async def _depaginate_v2(
        func: Callable[..., Awaitable[Tuple[dict, int]]],
        *args,
        **kwargs,
    ) -> dict:
        results_all = {}
        offset = 0
        while True:
            kwargs["offset"] = offset
            results, count = await func(*args, **kwargs)
            results_all.update(results)
            offset = len(results_all)
            if len(results_all) == count:
                break
        return results_all

    @track_context
    async def _list_software_environments(self, workspace: str | None = None) -> dict:
        return await self._depaginate_v2(self._list_software_environments_page_v2, workspace=workspace)

    @track_context
    async def _list_software_environments_page_v2(self, offset: int, workspace: str | None = None) -> Tuple[dict, int]:
        workspace = workspace or self.default_workspace
        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/software-environment/account/{workspace}/alias",
            params={"offset": offset},
        )
        if response.status >= 400:
            await handle_api_exception(response)
        response_json = await response.json()
        return {alias["name"]: alias for alias in response_json["items"]}, response_json["count"]

    @track_context
    async def _list_software_environments_page(
        self, page: int, workspace: str | None = None
    ) -> Tuple[dict, str | None]:
        workspace = workspace or self.default_workspace
        response = await self._do_request(
            "GET",
            self.server + f"/api/v1/{workspace}/software_environments/",
            params={"page": page},
        )
        if response.status >= 400:
            await handle_api_exception(response)
            return {}, None
        else:
            response_json = await response.json()
            results = {
                f"{format_account_output(r['account'])}/{r['name']}": format_software_environment_output(r)
                for r in response_json["results"]
            }

            return results, response_json["next"]

    @track_context
    async def _list_instance_types(
        self,
        backend: str | None = None,
        min_cores: int | None = None,
        min_gpus: int | None = None,
        min_memory: Union[int, str, float] | None = None,
        cores: Union[int, List[int]] | None = None,
        memory: Union[int, float, str, List[int], List[str], List[float]] | None = None,
        gpus: Union[int, List[int]] | None = None,
        arch: Literal["x86_64", "arm64"] | None = None,
    ) -> Dict[str, VmType]:
        if backend:
            user_provider = backend
        else:
            user_provider = await self.get_account_provider_name(account=self.default_workspace)

        if user_provider and user_provider not in ALLOWED_PROVIDERS:
            raise UnsupportedBackendError(
                (f"Unknown cloud provider provided - {user_provider} is not one of {ALLOWED_PROVIDERS}")
            )

        all_instance_types = await self._depaginate(
            self._list_instance_types_page,
            min_cores=min_cores,
            min_gpus=min_gpus,
            min_memory=min_memory,
            cores=cores,
            memory=memory,
            gpus=gpus,
            backend=user_provider.lower(),
            arch=arch,
        )

        return {f"{name}": i for name, i in all_instance_types.items()}

    @delete_docstring
    def set_gcp_credentials(
        self: CloudSyncAsync,
        gcp_credentials: dict,
        instance_service_account: str | None = None,
        account: str | None = None,
    ):
        return self._sync(
            self._set_gcp_credentials,
            account=account,
            gcp_credentials=gcp_credentials,
            instance_service_account=instance_service_account,
        )

    @track_context
    async def _set_gcp_credentials(
        self,
        gcp_credentials: dict,
        instance_service_account: str | None,
        account: str | None = None,
    ):
        account = account or self.default_workspace
        payload = {
            **gcp_credentials,
            "instance_service_account": instance_service_account,
        }
        response = await self._do_request(
            "POST",
            self.server + f"/api/v2/cloud-credentials/{account}/gcp",
            json=payload,
        )
        if not response.ok:
            logger.debug(f"Failed to update gcp creds {response.status}:{await response.text()}")

    @delete_docstring
    def unset_gcp_credentials(self: CloudSyncAsync, account: str | None = None):
        return self._sync(self._unset_gcp_credentials, account=account)

    @track_context
    async def _unset_gcp_credentials(self, account: str | None = None):
        account = account or self.default_workspace
        response = await self._do_request(
            "DELETE",
            self.server + f"/api/v2/cloud-credentials/{account}/gcp",
        )
        if not response.ok:
            logger.debug(f"Failed to delete gcp creds {response.status}:{await response.text()}")

    @delete_docstring
    def set_aws_credentials(self: CloudSyncAsync, aws_credentials: dict, account: str | None = None):
        return self._sync(self._set_aws_credentials, account=account, aws_credentials=aws_credentials)

    @track_context
    async def _set_aws_credentials(self, aws_credentials: dict, account: str | None = None):
        account = account or self.default_workspace
        response = await self._do_request(
            "POST",
            self.server + f"/api/v2/cloud-credentials/{account}/aws",
            json=aws_credentials,
        )
        if not response.ok:
            logger.debug(f"Failed to update aws creds {response.status}:{await response.text()}")

    @delete_docstring
    def unset_aws_credentials(self: CloudSyncAsync, account: str | None = None):
        return self._sync(self._unset_aws_credentials, account=account)

    @track_context
    async def _unset_aws_credentials(self, account: str | None = None):
        account = account or self.default_workspace
        response = await self._do_request(
            "DELETE",
            self.server + f"/api/v2/cloud-credentials/{account}/aws",
        )
        if not response.ok:
            logger.debug(f"Failed to delete aws creds {response.status}:{await response.text()}")

    @track_context
    async def _list_instance_types_page(
        self,
        page: int,
        min_cores: int | None = None,
        min_gpus: int | None = None,
        min_memory: Union[int, str, float] | None = None,
        cores: Union[int, List[int]] | None = None,
        memory: Union[int, str, float, List[int], List[str], List[float]] | None = None,
        gpus: Union[int, List[int]] | None = None,
        backend: str | None = None,
        arch: Literal["x86_64", "arm64"] | None = None,
    ) -> Tuple[dict, str | None]:
        parsed_memory = parse_requested_memory(memory, min_memory)
        params = {"page": page, **parsed_memory}

        # This isn't particularly pretty, but we are handling the case
        # where users specify a range for cores/memory/gpus or an exact
        # match
        if isinstance(cores, list):
            params["cores__gte"] = min(cores)
            params["cores__lte"] = max(cores)
        elif isinstance(cores, int):
            params["cores"] = cores

        if isinstance(gpus, list):
            params["gpus__gte"] = min(gpus)
            params["gpus__lte"] = max(gpus)
        elif isinstance(gpus, int):
            params["gpus"] = gpus

        if min_cores:
            params["cores__gte"] = min_cores

        if min_gpus:
            params["gpus__gte"] = min_gpus

        if backend:
            params["backend_type"] = backend if backend.startswith("vm_") else f"vm_{backend}"

        if arch:
            params["arch"] = arch

        response = await self._do_request(
            "GET",
            f"{self.server}/api/v1/vm-types/",
            params=params,
        )

        if response.status == 200:
            body = await response.json()

            results = {f"{r['name']}": r for r in body["results"]}
            return results, body["next"]

        else:
            msg = f"Coiled API responded with a {response.status} status code while fetching available instance types."
            raise ApiResponseStatusError(msg)

    @overload
    def list_software_environments(self: Cloud[Sync], account: str | None = None) -> dict: ...

    @overload
    def list_software_environments(
        self: Cloud[Async],
        account: str | None = None,
    ) -> Awaitable[dict]: ...

    @list_docstring
    def list_software_environments(
        self: CloudSyncAsync,
        account: str | None = None,
    ) -> Union[dict, Awaitable[dict]]:
        return self._sync(
            self._list_software_environments,
            workspace=account,
        )

    def _normalize_name(
        self,
        name: str,
        context_workspace: str | None = None,
        raise_on_account_conflict: bool = False,
        allow_uppercase: bool = False,
        property_name: str = "name",
    ) -> Tuple[str, str]:
        account, parsed_name, _ = parse_identifier(name, allow_uppercase=allow_uppercase, property_name=property_name)
        if (
            raise_on_account_conflict
            and context_workspace is not None
            and account is not None
            and context_workspace != account
        ):
            raise AccountConflictError(
                unparsed_name=name,
                account_from_name=account,
                account=context_workspace,
            )
        account = account or context_workspace or self.default_workspace
        return account, parsed_name

    @overload
    def delete_software_environment(
        self: Cloud[Sync],
        name: str,
        account: str | None = None,
    ) -> None: ...

    @overload
    def delete_software_environment(
        self: Cloud[Async],
        name: str,
        account: str | None = None,
    ) -> Awaitable[None]: ...

    @delete_docstring
    def delete_software_environment(
        self: CloudSyncAsync,
        name: str,
        account: str | None = None,
    ) -> Awaitable[None] | None:
        return self._sync(self._delete_software_environment, name, account)

    @track_context
    async def _delete_software_environment(self, name: str, workspace: str | None = None) -> None:
        workspace_kwarg = workspace
        workspace, name, tag = parse_identifier(name)
        workspace = workspace or workspace_kwarg or self.default_workspace

        if tag:
            name = ":".join([name, tag])
        response = await self._do_request(
            "DELETE",
            f"{self.server}/api/v2/software-environment/account/{workspace}/alias/name/{name}",
        )
        if response.status == 404:
            raise NotFound(
                f"Unable to find software environment with the name '{name}' in the workspace '{workspace}'."
            )
        elif response.status == 403:
            await handle_api_exception(response, exception_cls=PermissionsError)
        elif response.status >= 400:
            await handle_api_exception(response)
        else:
            rich.print("[green]Software environment deleted successfully.")

    @overload
    def set_backend_options(
        self: Cloud[Sync],
        backend_options: dict,
        account: str | None = None,
        workspace: str | None = None,
        log_output=sys.stdout,
    ) -> str: ...

    @overload
    def set_backend_options(
        self: Cloud[Async],
        backend_options: dict,
        account: str | None = None,
        workspace: str | None = None,
        log_output=sys.stdout,
    ) -> Awaitable[str]: ...

    def set_backend_options(
        self: CloudSyncAsync,
        backend_options: dict,
        account: str | None = None,
        workspace: str | None = None,
        log_output=sys.stdout,
    ) -> Union[str, Awaitable[str]]:
        return self._sync(
            self._set_backend_options,
            backend_options,
            account=account,
            workspace=workspace,
            log_output=log_output,
        )

    @track_context
    async def _set_backend_options(
        self,
        backend_options: dict,
        account: str | None = None,
        workspace: str | None = None,
        log_output=sys.stdout,
    ) -> str:
        session = self._ensure_session()
        workspace = workspace or account or self.default_workspace
        await self._verify_workspace(workspace)
        logging_context = {}
        default_configuration_message = {
            "type": "update_options",
            "logging_context": logging_context,
            "data": backend_options,
        }
        ws_server = self.server.replace("http", "ws", 1)
        ws = ConfigureBackendConnector(
            endpoint=f"{ws_server}/ws/api/v1/{workspace}/cluster-info/",
            session=session,
            log_output=log_output,
            connection_error_message=(
                "Unable to connect to server, do you have permissions to "
                f'edit backend_options in the "{workspace}" workspace?'
            ),
        )
        await ws.connect()
        await ws.send_json(default_configuration_message)
        with Spinner():
            await ws.stream_messages()
        return f"{self.server}/{workspace}/account"

    @overload
    def list_instance_types(
        self: Cloud[Sync],
        backend: str | None,
        min_cores: int | None,
        min_gpus: int | None,
        min_memory: Union[int, str, float] | None,
        cores: Union[int, List[int]] | None,
        memory: Union[int, str, float, List[int], List[str], List[float]] | None,
        gpus: Union[int, List[int]] | None,
        arch: Literal["x86_64", "arm64"] | None = None,
    ) -> Dict[str, VmType]: ...

    @overload
    def list_instance_types(
        self: Cloud[Async],
        backend: str | None,
        min_cores: int | None,
        min_gpus: int | None,
        min_memory: Union[int, str, float] | None,
        cores: Union[int, List[int]] | None,
        memory: Union[int, str, float, List[int], List[str], List[float]] | None,
        gpus: Union[int, List[int]] | None,
        arch: Literal["x86_64", "arm64"] | None = None,
    ) -> Awaitable[Dict[str, VmType]]: ...

    def list_instance_types(
        self: CloudSyncAsync,
        backend: str | None = None,
        min_cores: int | None = None,
        min_gpus: int | None = None,
        min_memory: Union[int, str, float] | None = None,
        cores: Union[int, List[int]] | None = None,
        memory: Union[int, str, float, List[int], List[str], List[float]] | None = None,
        gpus: Union[int, List[int]] | None = None,
        arch: Literal["x86_64", "arm64"] | None = None,
    ) -> Union[Awaitable[Dict[str, VmType]], Dict[str, VmType]]:
        return self._sync(
            self._list_instance_types,
            backend=backend,
            min_cores=min_cores,
            min_gpus=min_gpus,
            min_memory=min_memory,
            cores=cores,
            memory=memory,
            gpus=gpus,
            arch=arch,
        )

    @overload
    def list_gpu_types(self: Cloud[Sync]) -> dict: ...

    @overload
    def list_gpu_types(self: Cloud[Async]) -> Coroutine[None, None, dict]: ...

    def list_gpu_types(self: CloudSyncAsync):
        return self._sync(self._list_gpu_types)

    @track_context
    async def _list_gpu_types(self):
        title = "GCP GPU Types"
        allowed_gpus = "nvidia-tesla-t4"

        return {title: allowed_gpus}

    @track_context
    async def get_aws_credentials(self, account: str | None = None):
        """Return the logged in user's AWS credentials"""
        # this doesn't work, since aws credentials aren't (currently) returned by this endpoint
        backend_options = await self.get_backend_options(account)
        credentials = backend_options.get("options", {}).get("credentials", {})
        return credentials

    @track_context
    async def get_backend_options(self, account: str | None = None) -> dict:
        """Queries the API to get the backend options from account."""
        account = account or self.default_workspace
        response = await self._do_request(
            "GET",
            self.server + f"/api/v1/{account}/backend_options/",
        )
        if response.status >= 400:
            await handle_api_exception(response)

        backend_options = await response.json()
        return backend_options

    @track_context
    async def get_account_provider_name(self, account: str | None = None) -> str:
        """Get the provider name used by the account.

        Currently we are using this method only for the validation of instance
        types when users provide them. So we are handling the three clouds only
        otherwise we will return whatever is in the backend or an empty string.

        """
        backend_options = await self.get_backend_options(account)
        if backend_options.get("backend") == "vm":
            provider_name = backend_options.get("options", {}).get("provider_name", "")

        elif backend_options.get("backend") == "vm_aws":
            provider_name = "aws"
        elif backend_options.get("backend") == "vm_gcp":
            provider_name = "gcp"
        elif backend_options.get("backend") == "vm_azure":
            provider_name = "azure"
        else:
            provider_name = backend_options.get("backend", "")

        return provider_name

    @overload
    def get_software_info(
        self: Cloud[Sync],
        name: str,
        account: str | None = None,
    ) -> dict: ...

    @overload
    def get_software_info(
        self: Cloud[Async],
        name: str,
        account: str | None = None,
    ) -> Awaitable[dict]: ...

    def get_software_info(
        self: CloudSyncAsync,
        name: str,
        account: str | None = None,
    ) -> Union[dict, Awaitable[dict]]:
        return self._sync(
            self._get_software_info,
            name=name,
            workspace=account,
        )

    @track_context
    async def _get_software_info(self, name: str, workspace: str | None = None) -> dict:
        """Retrieve solved spec for a Coiled software environment

        Parameters
        ----------
        name
            Software environment name

        Returns
        -------
        results
            Coiled software environment information
        """
        workspace, name = self._normalize_name(name, context_workspace=workspace)
        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/software-environment/account/{workspace}/alias/name/{name}",
        )
        if response.status >= 400:
            await handle_api_exception(response)
        alias = await response.json()
        return await self._get_software_spec(alias["latest_spec"]["id"], workspace=workspace)

    async def _get_software_spec(self, pk: str, workspace: str | None = None) -> dict:
        workspace = workspace or self.default_workspace
        response = await self._do_request(
            "GET",
            self.server + f"/api/v2/software-environment/account/{workspace}/spec/{pk}",
        )
        if response.status >= 400:
            await handle_api_exception(response)
        return await response.json()

    @overload
    def list_core_usage(self: Cloud[Sync], account: str | None = None) -> dict: ...

    @overload
    def list_core_usage(self: Cloud[Async], account: str | None = None) -> Awaitable[dict]: ...

    def list_core_usage(self: CloudSyncAsync, account: str | None = None) -> Union[Awaitable[dict], dict]:
        return self._sync(self._list_core_usage, account=account)

    @track_context
    async def _list_core_usage(self, account: str | None = None) -> dict:
        account = account or self.default_workspace

        response = await self._do_request("GET", f"{self.server}/api/v1/{account}/usage/cores/")

        if response.status >= 400:
            await handle_api_exception(response)

        result = await response.json()

        return result

    async def _list_local_versions(self) -> dict:
        try:
            conda_version = version("conda")
        except PackageNotFoundError:
            conda_version = "None"
        try:
            pip_version = version("pip")
        except PackageNotFoundError:
            pip_version = "None"

        return {
            "operating_system": platform.platform(),
            "python": str(PY_VERSION),
            "pip": pip_version,
            "conda": conda_version,
            "coiled": COILED_VERSION,
            "dask": dask.__version__,
            "distributed": distributed.__version__,
        }

    @overload
    def list_local_versions(self: Cloud[Sync]) -> dict: ...

    @overload
    def list_local_versions(self: Cloud[Async]) -> Awaitable[dict]: ...

    def list_local_versions(
        self: CloudSyncAsync,
    ) -> Union[Awaitable[dict], dict]:
        return self._sync(self._list_local_versions)

    @track_context
    async def _noop_wait(self, duration: int):
        response = await self._do_request("GET", self.server + f"/api/v1/_noop_wait/{int(duration)}")

        result = await response.json()
        return result

    @track_context
    async def _upload_performance_report(
        self,
        content: str,
        account: str | None = None,
        filename: str | None = None,
        private: bool = False,
    ) -> Dict:
        account = account or self.default_workspace

        data = aiohttp.MultipartWriter("form-data")
        with open(content, "rb") as f:
            part = data.append(f)
            part.headers[aiohttp.hdrs.CONTENT_DISPOSITION] = (
                f'form-data; name="file"; filename="{filename}"; filename*="{filename}"'
            )

            upload_type = "private" if private else "public"
            response = await self._do_request(
                "POST",
                f"{self.server}/api/v1/{account}/performance_reports/{upload_type}/",
                data=data,
            )

        if response.status >= 400:
            await handle_api_exception(response)

        result = await response.json()
        return result

    @overload
    def upload_performance_report(
        self: Cloud[Sync],
        content: str,
        account: str | None = None,
        filename: str | None = None,
        private: bool = False,
    ) -> Dict: ...

    @overload
    def upload_performance_report(
        self: Cloud[Async],
        content: str,
        account: str | None = None,
        filename: str | None = None,
        private: bool = False,
    ) -> Awaitable[Dict]: ...

    def upload_performance_report(
        self: CloudSyncAsync,
        content: str,
        account: str | None = None,
        filename: str | None = None,
        private: bool = False,
    ) -> Union[Dict, Awaitable[Dict]]:
        return self._sync(
            self._upload_performance_report,
            content,
            filename=filename,
            account=account,
            private=private,
        )

    @track_context
    async def _list_performance_reports(
        self,
        account: str | None = None,
    ) -> List[Dict]:
        account = account or self.default_workspace
        response = await self._do_request(
            "GET",
            f"{self.server}/api/v1/{account}/performance_reports/all/",
        )
        if response.status >= 400:
            await handle_api_exception(response)

        result = await response.json()
        return result

    @overload
    def list_performance_reports(
        self: Cloud[Async],
        account: str | None = None,
    ) -> Awaitable[List[Dict]]: ...

    @overload
    def list_performance_reports(
        self: Cloud[Sync],
        account: str | None = None,
    ) -> List[Dict]: ...

    def list_performance_reports(
        self: CloudSyncAsync,
        account: str | None = None,
    ) -> Union[List[Dict], Awaitable[List[Dict]]]:
        return self._sync(
            self._list_performance_reports,
            account=account,
        )

    @overload
    def list_user_information(self: Cloud[Sync]) -> dict: ...

    @overload
    def list_user_information(self: Cloud[Async]) -> Awaitable[dict]: ...

    def list_user_information(self: CloudSyncAsync) -> Union[Awaitable[dict], dict]:
        return self._sync(self._list_user_information)

    @track_context
    async def _list_user_information(
        self,
    ) -> dict:
        response = await self._do_request("GET", self.server + "/api/v1/users/me/")
        if response.status >= 400:
            await handle_api_exception(response)
        result = await response.json()

        return result

    @track_context
    async def _health_check(self) -> dict:
        response = await self._do_request("GET", self.server + "/api/v1/health")
        if response.status >= 400:
            await handle_api_exception(response)

        result = await response.json()
        return result

    @overload
    def health_check(self: Cloud[Sync]) -> dict: ...

    @overload
    def health_check(self: Cloud[Async]) -> Awaitable[dict]: ...

    def health_check(self: CloudSyncAsync) -> Union[Awaitable[dict], dict]:
        return self._sync(self._health_check)

    @track_context
    async def _get_billing_activity(
        self,
        account: str | None = None,
        cluster: str | None = None,
        cluster_id: int | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        kind: str | None = None,
        page: int | None = None,
    ) -> Dict:
        account = account or self.default_workspace
        params = {}
        if start_time:
            params["event_after"] = start_time
        if end_time:
            params["event_before"] = end_time
        if kind:
            params["kind"] = kind
        if cluster:
            params["cluster"] = cluster
        if cluster_id:
            params["cluster_id"] = cluster_id
        if page:
            params["page"] = page
        response = await self._do_request(
            "GET",
            f"{self.server}/api/v1/{account}/billing-events/",
            params=params,
        )
        if response.status >= 400:
            await handle_api_exception(response)

        result = await response.json()
        return result

    @overload
    def get_billing_activity(
        self: Cloud[Async],
        account: str | None = None,
        cluster: str | None = None,
        cluster_id: int | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        kind: str | None = None,
        page: int | None = None,
    ) -> Awaitable[Dict]: ...

    @overload
    def get_billing_activity(
        self: Cloud[Sync],
        account: str | None = None,
        cluster: str | None = None,
        cluster_id: int | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        kind: str | None = None,
        page: int | None = None,
    ) -> Dict: ...

    def get_billing_activity(
        self: CloudSyncAsync,
        account: str | None = None,
        cluster: str | None = None,
        cluster_id: int | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        kind: str | None = None,
        page: int | None = None,
    ) -> Union[Dict, Awaitable[Dict]]:
        return self._sync(
            self._get_billing_activity,
            account=account,
            cluster=cluster,
            start_time=start_time,
            end_time=end_time,
            kind=kind,
            page=page,
        )

    @track_context
    async def _add_interation(
        self,
        action: str,
        success: bool,
        version: int = 1,
        coiled_version: str = COILED_VERSION,
        error_message: str | None = None,
        additional_text: str | None = None,
        additional_data: dict | None = None,
    ) -> None:
        data = {
            "action": action,
            "version": version,
            "success": success,
            "coiled_version": coiled_version[:30],  # dev version strings are long
            "error_message": error_message,
            "additional_text": additional_text,
            "additional_data": additional_data,
        }
        response = await self._do_request(
            "POST",
            f"{self.server}/api/v2/interactions/interaction",
            json=data,
        )
        if response.status >= 400:
            await handle_api_exception(response)

    @overload
    def add_interaction(
        self: Cloud[Async],
        action: str,
        success: bool,
        coiled_version: str = COILED_VERSION,
        version: int = 1,
        error_message: str | None = None,
        additional_text: str | None = None,
        additional_data: dict | None = None,
    ) -> Coroutine[None, None, None]: ...

    @overload
    def add_interaction(
        self: Cloud[Sync],
        action: str,
        success: bool,
        coiled_version: str = COILED_VERSION,
        version: int = 1,
        error_message: str | None = None,
        additional_text: str | None = None,
        additional_data: dict | None = None,
    ) -> None: ...

    def add_interaction(
        self: CloudSyncAsync,
        action: str,
        success: bool,
        coiled_version: str = COILED_VERSION,
        version: int = 1,
        error_message: str | None = None,
        additional_text: str | None = None,
        additional_data: dict | None = None,
    ) -> Union[None, Coroutine[None, None, None]]:
        return self._sync(
            self._add_interation,
            action=action,
            version=version,
            success=success,
            coiled_version=coiled_version,
            error_message=error_message,
            additional_text=additional_text,
            additional_data=additional_data,
        )


# Utility functions for formatting list_* endpoint responses to be more user-friendly


def format_security_output(data, cluster_id, server, token):
    d = data.copy()
    scheme, _ = parse_address(d["public_address"])
    if scheme.startswith("ws"):
        address = f"{server.replace('http', 'ws')}/cluster/{cluster_id}/"
        d["public_address"] = address
        d["extra_conn_args"] = {"headers": {"Authorization": get_auth_header_value(token)}}
        d["dashboard_address"] = f"{server}/dashboard/{cluster_id}/status"
        d.pop("tls_key")
        d.pop("tls_cert")
    else:
        # can delete after backend no longer sends extra_conn_args
        d.pop("extra_conn_args", None)
    return d


def format_account_output(d):
    return d["slug"]


def format_software_environment_output(d):
    exclude_list = [
        "id",
        "name",
        "content_hash",
        "builds",
    ]
    d = {k: v for k, v in d.items() if k not in exclude_list}
    d["account"] = format_account_output(d["account"])
    return d


def format_cluster_output(d, server):
    d = d.copy()
    for key in ["auth_token", "name", "last_seen"]:
        d.pop(key)
    d["account"] = format_account_output(d["account"])
    # Rename "public_address" to "address"
    address = d.pop("public_address")
    scheme, _ = parse_address(address)
    if scheme.startswith("ws"):
        address = f"{server.replace('http', 'ws')}/cluster/{d['id']}/"
    d["address"] = address
    # Use proxied dashboard address if we're in a hosted notebook
    # or proxying through websockets
    if dask.config.get("coiled.dashboard.proxy", False) or scheme.startswith("ws"):
        d["dashboard_address"] = f"{server}/dashboard/{d['id']}/status"
    return d


# Public API


def create_api_token(*, label: str | None = None, days_to_expire: int | None = None) -> dict:
    """Create a new API token.

    Parameters
    ---------
    label
        A label associated with the new API token, helpful for identifying it later.
    days_to_expire
        A number of days until the new API token expires.
    """
    with Cloud() as cloud:
        return cloud.create_api_token(
            label=label,
            days_to_expire=days_to_expire,
        )


def list_api_tokens(include_inactive=False) -> Dict[str, dict]:
    """List your API tokens.

    Note that this does not provide the actual key value, which is only available when creating the key.

    Returns
    -------
    Dictionary with information about each API token for your account. Keys in the dictionary are the API tokens'
    identifiers of {kind}s, while the values contain information about the corresponding API token.
    """
    with Cloud() as cloud:
        return cloud.list_api_tokens(include_inactive=include_inactive)


def revoke_api_token(*, identifier: str | None = None, label: str | None = None) -> None:
    """Revoke an API token. Note that this cannot be undone.

    Exactly one of ``identifier`` and ``label`` should be provided.

    Parameters
    ---------
    identifier
        The identifier of the API token.
    label
        The label of the API token(s) to revoke.
    """
    with Cloud() as cloud:
        return cloud.revoke_api_token(identifier=identifier, label=label)


def revoke_all_api_tokens() -> None:
    """Revoke all API tokens. Note that this cannot be undone."""
    with Cloud() as cloud:
        return cloud.revoke_all_api_tokens()


def create_software_environment(
    name: str | None = None,
    *,
    account: str | None = None,
    workspace: str | None = None,
    conda: Union[list, CondaEnvSchema, str, pathlib.Path] | None = None,
    pip: Union[list, str, pathlib.Path] | None = None,
    container: str | None = None,
    log_output=sys.stdout,
    force_rebuild: bool = False,
    use_entrypoint: bool = True,
    gpu_enabled: bool = False,
    arm: bool = False,
    architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
    region_name: str | None = None,
    include_local_code: bool = False,
    ignore_local_packages: List[str] | None = None,
    use_uv_installer: bool = True,
) -> SoftwareEnvironmentAlias | None:
    """Create a software environment

    .. seealso::

       By default, your local environment is automatically replicated in your
       cluster (see :doc:`software/index`).


    Parameters
    ----------
    name
        Name of software environment. Name can't contain uppercase letters.
    account
        **DEPRECATED**. Use ``workspace`` instead.
    workspace
        The workspace in which to create the software environment, if not given in the name.
    conda
        Specification for packages to install into the software environment using conda.
        Can be a list of packages, a dictionary, or a path to a conda environment YAML file.
        Can be used together with ``pip`` keyword argument, cannot be used together with ``container``.
    pip
        Packages to install into the software environment using pip.
        Can be a list of packages or a path to a pip requirements file.
        Can be used together with ``conda`` keyword argument, cannot be used together with ``container``.
    container
        Reference to a custom container image. For images in Docker Hub, you can reference by name,
        for example, ``daskdev/dask:latest``. For images in other registries, you need to reference by
        registry URL, for example, ``789111821368.dkr.ecr.us-east-2.amazonaws.com/prod/coiled``.
        Custom container image cannot be used together with ``conda`` or ``pip``.
    log_output
        Stream to output logs to. Defaults to ``sys.stdout``.
    force_rebuild
        By default, if an existing software environment with the same name and dependencies already
        exists, a rebuild is aborted. If this is set to ``True``, those checks are skipped and the
        environment will be rebuilt. Defaults to ``False``
    use_entrypoint
        Whether to use (or override) entrypoint set on container.
    gpu_enabled
        Set CUDA version for Conda
    arm
        Build software environment for ARM CPU architecture; defaults to ``False``;
        if ``True``, this takes precedence over ``architecture``.
    architecture
        CPU architecture of the software environment. Defaults to ``x86_64``;
        specify ``aarch64`` for ARM.
    region_name
        The AWS or GCP region name to use to store the software environment.
        If not provided, defaults to us-east-1 for AWS and us-east1 for GCP.
    include_local_code
        Whether to include local code in the software environment. Defaults to ``False``.
        Local code means any editable installs of packages, and any importable python files.
    ignore_local_packages:
        A list of package names to ignore when including local code. Defaults to ``None``.

    """
    error = False

    with Cloud() as cloud:
        try:
            return cloud.create_software_environment(
                name=name,
                account=account,
                workspace=workspace,
                conda=conda,
                pip=pip,
                container=container,
                log_output=log_output,
                force_rebuild=force_rebuild,
                use_entrypoint=use_entrypoint,
                gpu_enabled=gpu_enabled,
                arm=arm,
                architecture=architecture,
                region_name=region_name,
                include_local_code=include_local_code,
                ignore_local_packages=ignore_local_packages,
                use_uv_installer=use_uv_installer,
            )
        except Exception as e:
            error = e
            raise
        finally:
            data = {
                **(error_info_for_tracking(error) if error else {}),
                "name": str(name),
                "conda": bool(conda),
                "account": account,
                "pip": bool(pip),
                "container": container,
                "use_entrypoint": bool(use_entrypoint),
                "arm": arm,
                "architecture": str(architecture),
            }
            if error:
                cloud.add_interaction(
                    "create-software-environment",
                    success=False,
                    additional_data=data,
                )
            else:
                cloud.add_interaction(
                    "create-software-environment",
                    success=True,
                    additional_data=data,
                )


@list_docstring
def list_software_environments(account: str | None = None, workspace: str | None = None):
    with Cloud() as cloud:
        return cloud.list_software_environments(
            account=workspace or account,
        )


@delete_docstring
def delete_software_environment(name, account: str | None = None, workspace: str | None = None):
    with Cloud() as cloud:
        return cloud.delete_software_environment(
            name=name,
            account=workspace or account,
        )


def get_software_info(name: str, account: str | None = None, workspace: str | None = None) -> dict:
    """Retrieve solved spec for a Coiled software environment

    Parameters
    ----------
    name
        Software environment name
    workspace
        The workspace in which the software environment is located
    Returns
    -------
    results
        Coiled software environment information
    """
    with Cloud() as cloud:
        return cloud.get_software_info(name=name, account=account)


def list_core_usage(account: str | None = None) -> dict:
    """Get a list of used cores.

    Returns a table that shows the limit of cores that the user can use
    and a breakdown of the core usage split up between account, user and clusters.

    Parameters
    ----------
    account
        Name of the Coiled workspace (account) to list core usage. If not provided,
        will use the ``coiled.workspace`` or ``coiled.account`` configuration values.
    json
        If set to ``True``, it will return this list in json format instead of
        a table.
    """
    with Cloud() as cloud:
        return cloud.list_core_usage(account=account)


def list_local_versions() -> dict:
    """Get information about local versions.

    Returns the versions of Python, Coiled, Dask and Distributed that
    are installed locally. This information could be useful when
    troubleshooting issues.

    Parameters
    ----------
    json
        If set to ``True``, it will return this list in json format instead of a
        table.
    """
    with Cloud() as cloud:
        return cloud.list_local_versions()


def diagnostics(account: str | None = None) -> dict:
    """Run a diagnostic check aimed to help support with any issues.

    This command will call others to dump information that could help
    in troubleshooting issues. This command will return a json that will
    make it easier for you to share with the Coiled support team if needed.

    Parameters
    ----------
    account
        Name of the Coiled workspace (previously "account") to list core usage. If not provided,
        will use the ``coiled.workspace`` or ``coiled.account`` configuration values.
    """
    console = rich_console()
    with console.status("Gathering diagnostics..."):
        with Cloud() as cloud:
            data = {}

            health_check = cloud.health_check()
            status = health_check.get("status", "Issues found")

            data["health_check"] = health_check
            console.print(f"Performing health check.... Status: {status}")
            time.sleep(0.5)

            console.print("Gathering information about local environment...")
            local_versions = cloud.list_local_versions()
            data["local_versions"] = local_versions
            time.sleep(0.5)

            configuration = dask.config.config
            configuration["coiled"]["token"] = "hidden"
            data["coiled_configuration"] = configuration
            time.sleep(0.5)

            console.print("Getting user information...")
            user_info = cloud.list_user_information()
            data["user_information"] = user_info
            time.sleep(0.5)

            usage = cloud.list_core_usage(account=account)
            data["core_usage"] = usage
            time.sleep(0.5)

            return data


def list_user_information() -> dict:
    """List information about your user.

    This command will give you more information about your account,
    which teams you are part of and any limits that your account might
    have.
    """
    with Cloud() as cloud:
        cloud.list_user_information()
        return cloud.list_user_information()


def _upload_report(filename, private=False, account=None) -> dict:
    """Private method for uploading report to Coiled"""
    if not os.path.isfile(filename):
        raise ValueError("Report file does not exist.")

    statinfo = os.stat(filename)
    max_mb = 50
    if statinfo.st_size >= 1048576 * max_mb:
        raise ValueError(f"Report file size greater than {max_mb}mb limit")

    # At this point Dask has generated a local file with the performance report contents
    with Cloud() as cloud:
        result = cloud.upload_performance_report(filename, filename=filename, private=private, account=account)
        return result


@dataclass
class PerformanceReportURL:
    url: str | None


@experimental
@contextmanager
def performance_report(
    filename="dask-report.html",
    private=False,
    account=None,
) -> Generator[PerformanceReportURL, None, None]:
    """Generates a static performance report and saves it to Coiled Cloud

    This context manager lightly wraps Dask's performance_report. It generates a static performance
    report and uploads it to Coiled Cloud. After uploading, it prints out the url where the report is
    hosted. For a list of hosted performance reports, utilize coiled.list_performance_reports(). Note
    each user is limited to 5 hosted reports with each a maximum file size of 10mb.

    The context manager yields an object that will have the url as an attribute,
    though the URL is not available inside the context but only after (see example).

    Example::

        with coiled.performance_report("filename") as perf_url:
            dask.compute(...)

        assert isinstance(perf_url["url"], str)


    Parameters
    ----------

    filename
        The file name of the performance report file.
    private
        If set to ``True``, the uploaded performance report is only accessible to logged in Coiled users who
        are members of the current / default or specified account.
    account
        Name of the Coiled workspace (previously "account") to use.

    """
    perf_url = PerformanceReportURL(None)
    # stacklevel= is newer kwarg after version check below
    try:
        with dask.distributed.performance_report(filename=filename, stacklevel=3):
            yield perf_url
    finally:
        # by this point dask will have written local file as <filename>
        results = _upload_report(filename, private=private, account=account)
        console = Console()
        perf_url.url = results["url"]
        text = Text(
            f"Performance Report Available at: {results['url']}",
            style=f"link {results['url']}",
        )
        console.print(text)


@experimental
def list_performance_reports(account=None) -> List[Dict]:
    """List performance reports stored on Coiled Cloud

    Returns a list of dicts that contain information about Coiled Cloud hosted performance reports

    Parameters
    ----------

    account
        Name of the Coiled workspace (previously "account") from which to get report.
        If not specified, will use the current or default workspace.

    """
    with Cloud() as cloud:
        result = cloud.list_performance_reports(account=account)
        return result


def _parse_gcp_creds(gcp_service_creds_dict: Dict | None, gcp_service_creds_file: str | None) -> Dict:
    if not any([gcp_service_creds_dict, gcp_service_creds_file]):
        raise GCPCredentialsParameterError(
            "Parameter 'gcp_service_creds_file' or 'gcp_service_creds_dict' must be supplied"
        )

    if gcp_service_creds_file:
        if not os.path.isfile(gcp_service_creds_file):
            raise GCPCredentialsError("The parameter 'gcp_service_creds_file' must be a valid file")
        try:
            with open(gcp_service_creds_file, "r") as json_file:
                creds = json.load(json_file)

                required_keys = [
                    "type",
                    "project_id",
                    "private_key_id",
                    "private_key",
                    "client_email",
                    "client_id",
                    "auth_uri",
                    "token_uri",
                    "auth_provider_x509_cert_url",
                    "client_x509_cert_url",
                ]
                missing_keys = [key for key in required_keys if key not in creds]
                if missing_keys:
                    raise GCPCredentialsError(
                        message=(
                            f"The supplied file '{gcp_service_creds_file}' is missing the keys: "
                            f"{', '.join(missing_keys)}"
                        )
                    )

                return creds
        except JSONDecodeError:
            raise GCPCredentialsError(
                f"The supplied file '{gcp_service_creds_file}' is not a valid JSON file."
            ) from None
    if gcp_service_creds_dict and not gcp_service_creds_dict.get("project_id"):
        raise GCPCredentialsError(
            "Unable to find 'project_id' in 'gcp_service_creds_dict', make sure this key exists in the dictionary"
        )

    # Type checker doesn't know that this should no longer
    # be None.
    return cast(Dict, gcp_service_creds_dict)


def set_backend_options(
    account: str | None = None,
    workspace: str | None = None,
    backend: Literal["aws", "gcp"] = "aws",
    ingress: List[Dict] | None = None,
    firewall: Dict | None = None,
    network: Dict | None = None,
    aws_region: str = "us-east-1",
    aws_access_key_id: str | None = None,
    aws_secret_access_key: str | None = None,
    gcp_service_creds_file: str | None = None,
    gcp_service_creds_dict: dict | None = None,
    gcp_project_id: str | None = None,
    gcp_region: str | None = None,
    gcp_zone: str | None = None,
    instance_service_account: str | None = None,
    zone: str | None = None,
    registry_type: Literal["ecr", "docker_hub", "gar"] = "ecr",
    registry_namespace: str | None = None,
    registry_access_token: str | None = None,
    registry_uri: str = "docker.io",
    registry_username: str | None = None,
    log_output=sys.stdout,
    **kwargs,
):
    """Configure workspace-level settings for cloud provider and container registry.

    This method configures workspace-level backend settings for cloud providers, container registries,
    and setting up a workspace-level VPC for running clusters and other Coiled managed resources.


    Parameters
    ----------

    account
        **DEPRECATED**. Use ``workspace`` instead.

    workspace
        The Coiled workspace (previously "account") to configure. If not specified,
        will check the ``coiled.workspace`` or ``coiled.account`` configuration values,
        or will use your default workspace if those aren't set.

    backend
        Supported backends such as AWS VM (aws) and GCP VM (gcp).

    ingress
        Specification of the ingress rules the firewall/security group that Coiled creates for the cluster scheduler.
        This is a list of ingress rules, each rule is a dictionary with a list of ports and a CIDR block from which to
        allow ingress on those ports to the scheduler. For example,
        ``[{"ports" [8787], "cidr": "0.0.0.0/0"}, {"ports" [8786], "cidr": "10.2.0.0/16"}]``
        would allow the dashboard on 8787 to be accessed from any IP address, and the scheduler comm on 8786 to only
        be accessed from IP addresses in the 10.2.0.0/16 local network block.

    firewall
        A single ingress rule for the scheduler firewall/security group; this is deprecated and ingress rules should be
        specified with ``ingress`` instead.

    network
        Specification for your network/subnets, dictionary can take ID(s) for existing network and/or subnet(s).

    aws_region
        The region which Coiled cloud resources will be deployed to and where other resources
        such as the docker registry are located or where a specified VPC will be created.

    aws_access_key_id
        For AWS support backend, this argument is required to create or use an existing Coiled managed VPC.

    aws_secret_access_key
        For AWS support backend, this argument is required to create or use an existing Coiled managed VPC.

    use_scheduler_public_ip
        Determines if the client connects to the Dask scheduler using it's public or internal address.

    gcp_service_creds_file
        A string filepath to a Google Cloud Compute service account json credentials file used for creating and
        managing a Coiled VPC.

    gcp_service_creds_dict
        A dictionary of the contents of a Google Cloud Compute service account json credentials file used for
        creating a VPC to host Coiled Cloud related assets.

    gcp_project_id
        The Google Cloud Compute project id in which a VPC will be created to host Coiled Cloud related assets.

    gcp_region
        The Google Cloud Compute region name in which a VPC will be created.

    instance_service_account
        Email for optional service account to attach to cluster instances; using this is the best practice
        for granting access to your data stored in Google Cloud services. This
        should be a scoped service instance with only the permissions needed to run
        your computations.

    zone
        Optional; used to specify zone to use for clusters (for either AWS or GCP).

    registry_type
        Custom software environments are stored in a docker container registry. By default, container images will be
        stored in AWS ECR. Users are able to store contains on a private registry by providing additional
        configuration registry_* arguments and specifying registry_type='docker_hub'. To use
        Google Artifact Registry, pass registry_type='gar', gcp_project_id, gcp_region,
        and one of gcp_service_creds_dict or gcp_service_creds_file.

    registry_uri
        The container registry URI. Defaults to docker.io. Only required if
        registry_type='docker_hub'.

    registry_username
        A registry username (should be lowercased). Only required if
        registry_type='docker_hub'.

    registry_namespace
        A namespace for storing the container images. Defaults to username if not specified. More information
        about docker namespaces can be found here: https://docs.docker.com/docker-hub/repos/create/.
        Only required if registry_type='docker_hub'.

    registry_access_token
        A token to access registry images. More information about access tokens ca be found here:
        https://docs.docker.com/docker-hub/access-tokens/. Only required if registry_type='docker_hub'.

    """
    if firewall:
        if ingress:
            raise ValueError(
                "You specified both `firewall` and `ingress`. These are redundant; you should use `ingress`."
            )
        else:
            logger.warning(
                "The `firewall` keyword argument is deprecated; in the future you should use\n"
                f"  ingress=[{{ {firewall} }}]\n"
                "to specify your desired firewall ingress rules."
            )
            ingress = [firewall]
    firewall_spec = {"ingress": ingress} if ingress else {}

    # TODO - see if way to add default in BE to avoid re-versioning of this
    backend_options = {
        "backend": "vm_aws",
        "options": {
            "aws_region_name": aws_region,
            "account_role": "",
            "credentials": {"aws_access_key_id": "", "aws_secret_access_key": ""},
            "firewall": {},
            "firewall_spec": firewall_spec,
            "network": network or {},
            "zone": zone,
        },
        "registry": {"type": "ecr", "credentials": {}, "public_ecr": False},
    }

    # override gcp_zone with zone, if set
    if zone and gcp_project_id:
        gcp_zone = zone

    output_msg = ""
    # Used to print warnings to the user
    console = Console()

    if backend not in SUPPORTED_BACKENDS:
        raise UnsupportedBackendError(f"Supplied backend: {backend} not in supported types: {SUPPORTED_BACKENDS}")

    if aws_access_key_id and aws_secret_access_key:
        # verify that these are valid credentials
        verify_aws_credentials_with_retry(aws_access_key_id, aws_secret_access_key)

    parsed_gcp_credentials: Dict | None = None

    # Parse GCP region/zones or return default region/zone
    gcp_region, gcp_zone = parse_gcp_region_zone(region=gcp_region, zone=gcp_zone)

    if backend == "aws":
        backend_options["backend"] = "vm"
        backend_options["options"]["aws_region_name"] = aws_region
        if aws_access_key_id and aws_secret_access_key:
            backend_options["options"]["credentials"] = {
                "aws_access_key": aws_access_key_id,
                "aws_secret_key": aws_secret_access_key,
            }

            backend_options["options"]["provider_name"] = "aws"
            backend_options["options"]["type"] = "aws_cloudbridge_backend_options"
            output_msg = "Successfully set your backend options to Coiled Customer Hosted on AWS VM."
        else:
            raise AWSCredentialsParameterError(
                "Setting up AWS backend requires both: aws_access_key_id and aws_secret_access_key."
            )
    elif backend == "gcp":
        parsed_gcp_credentials = _parse_gcp_creds(
            gcp_service_creds_dict=gcp_service_creds_dict,
            gcp_service_creds_file=gcp_service_creds_file,
        )
        if not gcp_project_id:
            gcp_project_id = parsed_gcp_credentials.get("project_id", "")
        backend_options["options"]["gcp_service_creds_dict"] = parsed_gcp_credentials

        backend_options["backend"] = "vm"

        backend_options["options"]["provider_name"] = "gcp"
        backend_options["options"]["type"] = "gcp_cloudbridge_backend_options"

        backend_options["options"]["gcp_project_name"] = gcp_project_id
        backend_options["options"]["gcp_region_name"] = gcp_region
        backend_options["options"]["gcp_zone_name"] = gcp_zone
        backend_options["options"]["instance_service_account"] = instance_service_account

        output_msg = "Successfully set your backend options to Coiled Customer Hosted on GCP VM."

    ### container registry
    if registry_type == "ecr":
        # TODO add aws credentials in here for VPCs
        backend_options["registry"]["region"] = aws_region
        if aws_access_key_id and aws_secret_access_key:
            backend_options["registry"]["credentials"]["aws_access_key_id"] = aws_access_key_id
            backend_options["registry"]["credentials"]["aws_secret_access_key"] = aws_secret_access_key

    elif registry_type == "docker_hub":
        registry = {
            "account": registry_namespace or registry_username,
            "password": registry_access_token,
            "type": registry_type,
            "uri": registry_uri,
            "username": registry_username,
        }

        # any missing values
        empty_registry_values = [f"registry_{k}" for k, v in registry.items() if not v]
        if any(empty_registry_values):
            raise RegistryParameterError(
                f"For setting your registry credentials, these fields cannot be empty: {empty_registry_values}"
            )

        # docker username /// account name cannot be uppercase
        if registry_username and any(ele.isupper() for ele in registry_username) is True:
            raise RegistryParameterError("Your dockerhub [registry_username] must be lowercase")

        backend_options["registry"] = registry
    elif registry_type == "gar":
        if parsed_gcp_credentials is None:
            parsed_gcp_credentials = _parse_gcp_creds(
                gcp_service_creds_dict=gcp_service_creds_dict,
                gcp_service_creds_file=gcp_service_creds_file,
            )
        if not gcp_project_id:
            gcp_project_id = parsed_gcp_credentials.get("project_id", "")
        gar_required_kwargs = {
            "gcp_region_name": gcp_region,
            "gcp_project_name": gcp_project_id,
            "one of gcp_service_creds_dict / gcp_service_creds_file": parsed_gcp_credentials,
        }
        missing_gar_kwargs = ", ".join([kw for kw, val in gar_required_kwargs.items() if not val])
        if missing_gar_kwargs:
            raise RegistryParameterError(f"Missing required args for Google Artifact Registry: {missing_gar_kwargs}")
        backend_options["registry"] = {
            "type": registry_type,
            "location": gcp_region,
            "project_id": gcp_project_id,
            "credentials": parsed_gcp_credentials,
        }

    with Cloud(workspace=workspace or account) as cloud:
        account_options_url = cloud.set_backend_options(
            backend_options,
            workspace=workspace or account,
            log_output=log_output,
        )
        text = Text()
        text.append(output_msg, style="green")
        text.append("\n\n")
        text.append(
            f"You can view your workspace backend options here: {account_options_url}",
            style=f"link {account_options_url}",
        )
        console.print(text)


def list_instance_types(
    backend: str | None = None,
    min_cores: int | None = None,
    min_gpus: int | None = None,
    min_memory: Union[int, str, float] | None = None,
    cores: Union[int, List[int]] | None = None,
    memory: Union[int, str, float, List[int], List[str], List[float]] | None = None,
    gpus: Union[int, List[int]] | None = None,
    arch: Literal["x86_64", "arm64"] | None = None,
) -> Dict[str, VmType]:
    """List allowed instance types for the cloud provider configured on your account.

    This command allows you to get all instance types available for a backend or a filtered
    list of instance types that match your requirements by using the available keyword
    arguments. Please refer to :doc:`clusters/size-and-type` for more information.

    Parameters
    ----------
    backend:
        Relevant cloud provider (aws or gcp) to get a list of allowed instance types. If
        not provided the list will show the instances for your account cloud provider.
    min_cores
        Filter results on the minimum number of required cores
    min_gpus
        Filter results on the minimum number of required GPUs
    min_memory
        Filter results on the minimum amount of memory
    cores:
        The exact number of cores to filter for example ``cores=1`` or a list containg the
        minimum and maximum amount of cores to filter instances by, for example ``cores=[2,8]``.
    memory:
        The exact amount of memory or a list containing the minimum and maximum
        amount of memory to filter instances by.
    gpus
        The exact number of gpus to filter or a list containing the minimum and maximum number
        of GPUS to filter instances by.
    arch
        CPU architecture, defaults to x86_64. There's no way to get both x86_64 and arm64
        instances in a single call.
    """
    with Cloud() as cloud:
        return cloud.list_instance_types(
            backend=backend,
            min_cores=min_cores,
            min_gpus=min_gpus,
            min_memory=min_memory,
            cores=cores,
            memory=memory,
            gpus=gpus,
            arch=arch,
        )


def list_gpu_types() -> Dict:
    """List allowed GPU Types.

    For AWS the GPU types are tied to the instance type, but for GCP you can
    add different GPU types to GPU enabled instances. Please refer to
    :doc:`clusters/gpu` for more information.

    Parameters
    ----------
    json
        if set to ``True``, it will return this list in json format instead of a table.

    """
    with Cloud() as cloud:
        return cloud.list_gpu_types()


BillingEventKind = Literal[
    "instance",
    "monthly_grant",
    "manual_adjustment",
    "payg_payment",
]


def get_billing_activity(
    account: str | None = None,
    cluster: str | None = None,
    cluster_id: int | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    kind: BillingEventKind | None = None,
    page: int | None = None,
) -> Dict:
    """Retrieve Billing information.

    Parameters
    ----------
    account
        The workspace (previously "account") to retrieve billing information from.
        If not specified, will use the current or default workspace.

    cluster
        Cluster name. Filter billing events to this cluster. Defaults to ``None``.

    cluster_id
        Cluster id. Filter billing events to this cluster by id. Defaults to ``None``.

    start_time
        Filter events after this datetime (isoformat). Defaults to ``None``.

    end_time
        Filter events before this datetime (isoformat). Defaults to ``None``.

    kind
        Filter events to this kind of event. Defaults to ``None``.

    page
       Grab events from this page. Defaults to ``None``.
    """
    with Cloud() as cloud:
        return cloud.get_billing_activity(
            account=account,
            cluster=cluster,
            cluster_id=cluster_id,
            start_time=start_time,
            end_time=end_time,
            kind=kind,
            page=page,
        )


def add_interaction(
    action: str,
    *,
    success: bool,
    error_message: str | None = None,
    additional_text: str | None = None,
    **kwargs,
):
    with Cloud() as cloud:
        return cloud.add_interaction(
            action=action,
            success=success,
            error_message=error_message,
            additional_text=additional_text,
            additional_data=kwargs or None,
        )
