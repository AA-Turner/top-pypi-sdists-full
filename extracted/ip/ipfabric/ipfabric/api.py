import logging
import re
from functools import cached_property, wraps
from pathlib import Path
from ssl import SSLContext
from typing import Optional, Any, Union, Literal, Mapping, OrderedDict, Iterator, Generator

from dotenv import find_dotenv
from httpx import Client, BaseTransport, URL, Response
from httpx._client import EventHook
from httpx._types import CertTypes
from pydantic import ConfigDict, Field, InstanceOf, FilePath, BaseModel
from pydantic_settings.sources import DotenvType

from ipfabric.auth import Setup, ProxyTypes, TimeoutTypes
from ipfabric.models import Snapshot, OAS, Endpoint, Snapshots, Methods, User, create_snapshot
from ipfabric.models.snapshot import ScheduledSnapshot
from ipfabric.models.discovery import SeedList, Networks
from ipfabric.models.authentication import CredentialList, PrivilegeList
from ipfabric.tools.configuration import trigger_backup
from ipfabric.tools.shared import VALID_REFS, raise_for_status, VALID_IP

logger = logging.getLogger("ipfabric")

LAST_ID, PREV_ID, LASTLOCKED_ID = VALID_REFS
RE_PATH = re.compile(r"^/?(api/)?v\d(\.\d+)?/")


def check_deprecated(http_method: str = None):
    def decorator_check_deprecated(func):
        @wraps(func)
        def wrapper_check_deprecated(self: "IPFabricAPI", *f_args, **f_kwargs):
            if method := http_method:
                url = f_kwargs.get("url", f_args[0])
            else:
                method = f_kwargs.get("method", f_args[0])
                url = f_kwargs.get("url", f_args[1])
            url = self._check_url(url)
            method = method if not url[:6].startswith("tables") else "post"
            _: Endpoint = getattr(getattr(self, "oas", {}).get(url, Methods(full_api_endpoint="")), method, None)
            if _ and _.deprecated:
                logger.warning(
                    f"API endpoint '{method.upper()} /{_.api_endpoint}' is marked deprecated in OpenAPI specification."
                )
            return func(self, *f_args, **f_kwargs)

        return wrapper_check_deprecated

    return decorator_check_deprecated


class IPFabricAPI(BaseModel):
    """Initializes the IP Fabric Client.

    Args:
        base_url: IP Fabric instance provided in 'base_url' parameter, or the 'IPF_URL' environment variable
        api_version: [Optional] Version of IP Fabric API
        snapshot_id: IP Fabric snapshot ID to use by default for database actions - defaults to '$last'
        auth: API token, tuple (username, password), or custom Auth to pass to httpx
        unloaded: True to load metadata from unloaded snapshots
        env_file: Path to .env file to load
        streaming: Default True to use streaming instead of paging.
        verify: httpx.Client - Default True to verify IPF SSL certificate.
        timeout: httpx.Client - Default 5
        proxy: httpx.Client
        mounts: httpx.Client
        cert: httpx.Client
        event_hooks: httpx.Client
        local_oas: Default True, False mainly for development purposes
        local_oas_file: Default True, False mainly for development purposes
        debug: Enable Debug.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    base_url: Optional[Union[str, InstanceOf[URL]]] = Field(
        None, description="Base URL of the IPF instance", examples=["https://demo.ipfabric.io"]
    )
    auth: Optional[Any] = Field(default=None, exclude=True)
    snapshot_id: Optional[str] = Field(None, description="Defaults to '$last'.")
    env_file: Optional[DotenvType] = Field(default=None, exclude=True)
    unloaded: bool = Field(False, description="Default False, do not load unloaded snapshot metadata.")
    streaming: bool = Field(True, description="Default True; use streaming results instead of pagination.")

    # HTTPX Options:
    verify: Optional[Union[SSLContext, str, bool]] = Field(default=None, exclude=True)
    timeout: Optional[Union[TimeoutTypes, Literal["DEFAULT"]]] = Field(default="DEFAULT", exclude=True)
    proxy: Optional[ProxyTypes] = Field(default=None, exclude=True)
    mounts: Optional[Mapping[str, Optional[BaseTransport]]] = Field(default=None, exclude=True)
    cert: Optional[CertTypes] = Field(default=None, exclude=True)
    event_hooks: Optional[Mapping[str, list[EventHook]]] = Field(default=None, exclude=True)
    http2: Optional[bool] = Field(default=True, exclude=True)

    # Debug/Other less used
    nvd_api_key: Optional[str] = None
    debug: bool = False
    api_version: Optional[str] = Field(None, description="Defaults to SDK or API version.")
    local_oas: bool = Field(True, description="Default True, use local minified OAS file instead of servers.")
    local_oas_file: Optional[FilePath] = None
    _os_version: Optional[str] = None
    _os_api_version: Optional[str] = None
    _client: Client = None
    _prev_snapshot_id: Optional[str] = None
    _attribute_filters: Optional[dict] = None
    _no_loaded_snapshots: bool = False
    _oas: Optional[OAS] = None
    _user: Optional[User] = None
    _snapshots: Optional[Snapshots] = None

    def model_post_init(self, __context: Any) -> None:
        env_file = (
            self.env_file if self.env_file else find_dotenv(usecwd=True) or Path("~").expanduser().joinpath(".env")
        )
        logger.info(f"Using .env file located at {env_file}.")
        setup = Setup(
            base_url=self.base_url,
            api_version=self.api_version,
            auth=self.auth,
            _env_file=env_file,
            snapshot_id=self.snapshot_id,
            verify=self.verify,
            timeout=self.timeout,
            proxy=self.proxy,
            mounts=self.mounts,
            cert=self.cert,
            event_hooks=self.event_hooks,
            debug=self.debug,
            http2=self.http2,
        )
        self._client = setup.client
        [setattr(self, k, v) for k, v in setup.update_attrs.items()]

        self._oas = OAS(client=self, local_oas=self.local_oas, local_oas_file=self.local_oas_file)
        self._user = self.get_user()
        self._snapshots = Snapshots(client=self)
        self.snapshot_id = setup.snapshot_id
        logger.debug(
            f"Successfully connected to '{self.base_url.host}' IPF version '{self.os_version}' "
            f"as user '{self.user.username}'"
        )

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "timeout":
            self._client.timeout = value
        elif name == "snapshot_id":
            value = self._switch_snapshot(value)
        super().__setattr__(name, value)

    def _switch_snapshot(self, snapshot_id: str) -> Union[str, None]:
        """Verify snapshot ID is valid."""
        if not self.loaded_snapshots:
            logger.warning("No Snapshots are currently loaded.  Please load a snapshot before querying any data.")
            self._no_loaded_snapshots = True
            return None
        if snapshot_id in self.snapshots:
            self._prev_snapshot_id = self.snapshot_id
            if self.snapshots[snapshot_id].running:
                logger.warning(f"Snapshot {self.snapshot_id} is running; some methods may not be available.")
            return self.snapshots[snapshot_id].snapshot_id
        raise ValueError(f"Incorrect Snapshot ID: '{snapshot_id}'")

    @check_deprecated("get")
    def get(self, url, *args, params=None, **kwargs) -> Response:
        return self._client.get(url, *args, params=params, **kwargs)

    @check_deprecated("post")
    def post(self, url, *args, json=None, **kwargs) -> Response:
        return self._client.post(url, *args, json=json, **kwargs)

    @check_deprecated("put")
    def put(self, url, *args, json=None, **kwargs) -> Response:
        return self._client.put(url, *args, json=json, **kwargs)

    @check_deprecated("patch")
    def patch(self, url, *args, json=None, **kwargs) -> Response:
        return self._client.patch(url, *args, json=json, **kwargs)

    def request(self, method, url, *args, json=None, **kwargs) -> Response:
        return self._client.request(method, url, *args, json=json, **kwargs)

    @check_deprecated("delete")
    def delete(self, url, *args, **kwargs) -> Response:
        return self._client.delete(url, *args, **kwargs)

    def stream(self, method, url, *args, **kwargs) -> Iterator[Response]:
        return self._client.stream(method, url, *args, **kwargs)

    def _check_url(self, url) -> str:
        """Optimized URL processing with compiled regex and early returns"""

        path = URL(url).path
        if not path.startswith("/"):
            path = "/" + url

        # Early return for known web-to-api mappings
        if self._oas and path in self.web_to_api:
            return self.web_to_api[path].api_endpoint

        # Single regex match instead of multiple operations
        if match := RE_PATH.search(path):
            return path[match.end() :].lstrip("/")  # noqa: E203
        return path.lstrip("/")

    @cached_property
    def os_version(self):
        return self._os_version

    @cached_property
    def os_api_version(self):
        return self._os_api_version

    @cached_property
    def user(self) -> User:
        return self._user

    @cached_property
    def _api_insuf_rights(self):
        msg = f'API_INSUFFICIENT_RIGHTS for user "{self._user.username}" '
        if self._user.token:
            msg += f'token "{self._user.token.description}" '
        return msg

    @cached_property
    def hostname(self) -> str:
        resp = self.get("/os/hostname")
        if resp.status_code == 200:
            return resp.json()["hostname"]
        else:
            logger.critical(self._api_insuf_rights + 'on GET "/os/hostname"; Using URL host.')
            return str(self.base_url.host)

    @cached_property
    def oas(self) -> dict[str, Methods]:
        return self._oas.oas

    @cached_property
    def web_to_api(self) -> dict[str, Endpoint]:
        return self._oas.web_to_api

    @cached_property
    def scope_to_api(self) -> dict[str, Endpoint]:
        return self._oas.scope_to_api

    @property
    def attribute_filters(self):
        return self._attribute_filters

    @attribute_filters.setter
    def attribute_filters(self, attribute_filters: Union[dict[str, list[str]], None]):
        if attribute_filters:
            logger.warning(
                "Setting Global Attribute Filter for all tables/diagrams until explicitly unset to `None` or "
                f"overwritten in the method.\nFilter: {attribute_filters}"
            )
        self._attribute_filters = attribute_filters

    @property
    def snapshots(self) -> OrderedDict[str, Snapshot]:
        return self._snapshots.snapshots

    @property
    def snapshot(self) -> Snapshot:
        return self.snapshots[self.snapshot_id]

    @property
    def loaded_snapshots(self) -> OrderedDict[str, Snapshot]:
        """get only loaded snapshots"""
        return self._snapshots.loaded_snapshots

    @property
    def unloaded_snapshots(self) -> OrderedDict[str, Snapshot]:
        return self._snapshots.unloaded_snapshots

    @property
    def loading_snapshot(self) -> Union[Snapshot, None]:
        """Return Loading Snapshot or None"""
        return self._snapshots.loading_snapshot

    @property
    def running_snapshot(self) -> Union[Snapshot, None]:
        """Return Running Snapshot"""
        return self._snapshots.running_snapshot

    def get_snapshot(self, snapshot_id: str) -> Snapshot:
        return self._snapshots.get_snapshot(snapshot_id)

    def get_snapshot_id(self, snapshot: Union[Snapshot, str]) -> str:
        return self._snapshots.get_snapshot_id(snapshot)

    def get_snapshots(self) -> OrderedDict[str, Snapshot]:
        return self._snapshots.get_snapshots()

    @property
    def prev_snapshot_id(self) -> str:
        """get previous snapshot Id"""
        return self._prev_snapshot_id

    def get_user(self) -> User:
        """Gets current logged in user information.

        Returns:
            User: User model of logged in user
        """
        resp = raise_for_status(self.get("users/me"))
        user = User(**resp.json())
        if not (user.is_admin and user.token):  # TODO: NIM-14008: Implement logic after obtaining scopes for tokens
            resp = raise_for_status(self.get("users/me/scopes/api"))
            user.scopes = resp.json()["data"]
        return user

    def _ipf_pager(
        self,
        url: str,
        payload: dict,
        limit: int = 1000,
        start: int = 0,
    ) -> Generator:
        """
        Loops through and collects all the data from the tables
        :param url: str: Full URL to post to
        :param payload: dict: Data to submit to IP Fabric
        :param start: int: Where to start for the data
        :return: Generator: List of dictionaries
        """
        payload.setdefault("pagination", {})
        payload["pagination"]["limit"] = limit

        while True:
            payload["pagination"]["start"] = start
            response = raise_for_status(self.post(url, json=payload))
            chunk = response.json()["data"]

            if not chunk:
                break

            yield from chunk

            if len(chunk) < limit:
                break

            start += limit

    def trigger_backup(self, sn: str = None, ip: str = None):
        return trigger_backup(self, sn=sn, ip=ip)

    def create_snapshot(
        self,
        snapshot_name: str = "",
        snapshot_note: str = "",
        networks: Optional[Union[Networks, dict[str, list[Union[str, VALID_IP]]]]] = None,
        seeds: Optional[Union[SeedList, list[Union[str, VALID_IP]]]] = None,
        credentials: Optional[Union[CredentialList, list[dict]]] = None,
        privileges: Optional[Union[PrivilegeList, list[dict]]] = None,
        disabled_assurance_jobs: Optional[list[Literal["graphCache", "historicalData", "intentVerification"]]] = None,
        fail_if_running_snapshot: bool = True,
        **kwargs,
    ) -> ScheduledSnapshot:
        return create_snapshot(
            self,
            snapshot_name=snapshot_name,
            snapshot_note=snapshot_note,
            networks=networks,
            seeds=seeds,
            credentials=credentials,
            privileges=privileges,
            disabled_assurance_jobs=disabled_assurance_jobs,
            fail_if_running_snapshot=fail_if_running_snapshot,
            **kwargs,
        )
