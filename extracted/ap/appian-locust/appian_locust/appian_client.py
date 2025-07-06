import greenlet
import os
import urllib.parse
from typing import Tuple, Optional

from locust.clients import HttpSession
from requests import Response

from .utilities import logger
from .utilities import loadDriverUtils, DEFAULT_CONFIG_PATH
from ._feature_toggle_helper import get_client_feature_toggles
from ._interactor import _Interactor
from ._actions import _Actions
from ._news import _News
from ._records import _Records
from ._reports import _Reports
from ._sites import _Sites
from ._tasks import _Tasks
from .visitor import Visitor
from .system_operator import SystemOperator
from .info import ActionsInfo, NewsInfo, RecordsInfo, ReportsInfo, SitesInfo, TasksInfo

log = logger.getLogger(__name__)


class AppianClient:
    def __init__(self, session: HttpSession, host: str, base_path_override: Optional[str] = None, portals_mode: bool = False,
                 config_path: str = DEFAULT_CONFIG_PATH, is_mobile_client: bool = False) -> None:
        """
        Appian client class contains all the required functions to interact with Tempo.

        Note: This class will be called inside ``AppianTaskSet`` so it is not necessary to call this explicitly in a test.
        ``self.appian`` can be used directly in a test.

        Args:
            session: Locust session/client object
            host (str): Host URL
            base_path_override (str): override for sites where /suite is not the base path
            config_path (str): path to configuration file
            is_mobile_client(bool): set to True if client should act as mobile

        """
        self.client = session
        self.portals_mode = portals_mode
        self.host = _trim_trailing_slash(host)

        timeout = 300
        if os.path.exists(config_path):
            config_timeout = loadDriverUtils().load_config(config_path).get('request_timeout', None)
            if config_timeout:
                log.info(f"Overriding default timeout to {config_timeout}s")
                timeout = config_timeout

        self._interactor = _Interactor(self.client, self.host, portals_mode=portals_mode, request_timeout=timeout)
        self._news = _News(self._interactor)
        self._actions = _Actions(self._interactor)
        self._tasks = _Tasks(self._interactor)
        self._reports = _Reports(self._interactor)
        self._records = _Records(self._interactor, is_mobile_client=is_mobile_client)
        self._sites = _Sites(self._interactor)

        self._visitor = Visitor(self._interactor,
                                self._tasks,
                                self._reports,
                                self._actions,
                                self._records,
                                self._sites)
        self._system_operator = SystemOperator(self._interactor, self._actions)

        # Adding a few session specific attributes to self.client to that it can be carried and handled by session
        # in case of having multiple sessions in the future.
        setattr(self.client, "feature_flag", "")
        setattr(self.client, "feature_flag_extended", "")

        # Used for sites where /suite is not in the URL, i.e. local builds
        setattr(self.client, "base_path_override", base_path_override)

    @property
    def actions_info(self) -> ActionsInfo:
        """
        Navigate to actions and gather information about available actions
        """
        return ActionsInfo(self._actions)

    @property
    def news_info(self) -> NewsInfo:
        """
        Navigate to news and fetch information on news entries
        """
        return NewsInfo(self._news)

    @property
    def records_info(self) -> RecordsInfo:
        """
        Navigate to records and gather information about available records
        """
        return RecordsInfo(self._records)

    @property
    def reports_info(self) -> ReportsInfo:
        """
        Navigate to reports and gather information about available reports
        """
        return ReportsInfo(self._reports)

    @property
    def sites_info(self) -> SitesInfo:
        """
        Get Site metadata object
        """
        return SitesInfo(self._sites)

    @property
    def tasks_info(self) -> TasksInfo:
        """
        Navigate to tasks and gather information about available tasks
        """
        return TasksInfo(self._tasks)

    @property
    def visitor(self) -> Visitor:
        """
        Visitor that can be used to navigate to different types of pages in an Appian instance
        """
        return self._visitor

    @property
    def system_operator(self) -> SystemOperator:
        """
        Abstraction used for system operation that do not require a UI
        """
        return self._system_operator

    def login(self, auth: Optional[list] = None, check_login: bool = True) -> Tuple[HttpSession, Response]:
        return self._interactor.login(auth, raise_error=check_login)

    def logout(self) -> None:
        """
        Logout from Appian
        """
        logout_uri = (
            self.host
            + "/suite/logout?targetUrl="
            + urllib.parse.quote(self.host + "/suite/tempo/")
        )

        headers = self._interactor.setup_request_headers(logout_uri)
        if hasattr(greenlet.getcurrent(), "minimal_ident"):
            log.info(f"Logging out user {self._interactor.auth[0]} from greenlet id {greenlet.getcurrent().minimal_ident}")
        else:
            log.info(f"Logging out user {self._interactor.auth[0]} from {greenlet.getcurrent()}")
        self._interactor.post_page(logout_uri, headers=headers, label="Logout.LoadUi", raise_error=False, check_login=False)
        self.client.cookies.clear()

    def get_client_feature_toggles(self) -> None:
        self.client.feature_flag, self.client.feature_flag_extended = ("7ffceebc", "1bff7f49dc1fffceebc") if self.portals_mode else (
            get_client_feature_toggles(self._interactor, self.client)
        )


class _NoOpEvents():
    def fire(self, *args: str, **kwargs: int) -> None:
        pass

    def context(self, *args: str, **kwargs: int) -> dict:
        return {}


def _trim_trailing_slash(host: str) -> str:
    return host[:-1] if host and host.endswith('/') else host


def appian_client_without_locust(host: str, record_mode: bool = False,
                                 base_path_override: Optional[str] = None) -> 'AppianClient':
    """
    Returns an AppianClient that can be used without locust to make requests against a host, e.g.

    >>> appian_client_without_locust()
    >>> client.login(auth=('username', 'password'))
    >>> client.get_client_feature_toggles()

    This can be used for debugging/ making CLI style requests, instead of load testing
    You MUST call client.get_client_feature_toggles() to correctly finish initializing the client.

    Returns:
        AppianClient: an Appian client that can be used
    """
    inner_client = HttpSession(_trim_trailing_slash(host), _NoOpEvents(), _NoOpEvents())
    if record_mode:
        setattr(inner_client, 'record_mode', True)
    return AppianClient(inner_client, host=host, base_path_override=base_path_override)
