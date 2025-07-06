import re
import uuid
from typing import List, Generator

from locust import SequentialTaskSet, TaskSet
from requests import JSONDecodeError

from .utilities import logger
from .feature_flag import FeatureFlag
from .utilities import DEFAULT_CONFIG_PATH
from .utilities.url_provider import UrlProvider, URL_PROVIDER_V0, URL_PROVIDER_V1
from .appian_client import AppianClient
from ._feature_toggle_helper import override_default_feature_flags

log = logger.getLogger(__name__)


class AppianTaskSet(TaskSet):
    def __init__(self, parent: TaskSet) -> None:
        """
        Locust performance tests with a TaskSet should set AppianTaskSet as their base class to have access to various functionality.
        This class handles creation of basic objects like ``self.appian`` and actions like ``login`` and ``logout``
        """

        super().__init__(parent)

        self.host = self.parent.host

        # A set of datatypes cached. Used to populate "X-Appian-Cached-Datatypes" header field
        self.cached_datatype: set = set()
        self.url_provider = None

    def on_start(self, portals_mode: bool = False, config_path: str = DEFAULT_CONFIG_PATH, is_mobile_client: bool = False) -> None:
        """
        Overloaded function of Locust's default on_start.

        It will create object self.appian and logs in to Appian

        Args:
            portals_mode (bool): set to True if connecting to portals site
            config_path (str): path to configuration file
            is_mobile_client (bool): set to True if client should act as mobile
        """
        self.portals_mode = portals_mode
        self.workerId = str(uuid.uuid4())
        base_path_override = self.parent.base_path_override \
            if hasattr(self.parent, "base_path_override") else ""
        self._appian = AppianClient(self.client, self.host, base_path_override=base_path_override,
                                    portals_mode=portals_mode, config_path=config_path, is_mobile_client=is_mobile_client)
        if not portals_mode:
            self.auth = self._determine_auth()
            self.appian.login(self.auth)
            resp = self.appian._interactor.get_page(self.host + '/suite/rest/a/sites/latest/locust-templates', check_login=False)
            if not resp.ok:
                resp = self.appian._interactor.get_page(uri=self.host + "/suite/tempo/news")
                test = r'\\\\\\/suite\\\\\\/rest\\\\\\/a\\\\\\/sites\\\\\\/latest\\\\\\/D6JMim\\\\\\/page\\\\\\/(.+)\\\\\\'
                m = re.search(test, resp.text)
                if m is None or m.group(1) == 'news':
                    # old way
                    self.appian._interactor.set_url_provider(URL_PROVIDER_V0)
                elif m.group(1) == 'p.news':
                    # new way
                    self.appian._interactor.set_url_provider(URL_PROVIDER_V1)
                else:
                    log.warning("appian-locust could not determine appian interaction url pattern.  Defaulting to v1.  If errors persist, you may explicitly try v0.")
                    self.appian._interactor.set_url_provider(URL_PROVIDER_V1)
            else:
                try:
                    self.appian._interactor.set_url_provider(UrlProvider(resp.json()))
                except (JSONDecodeError, ValueError):
                    log.warning("appian-locust could not determine appian interaction url pattern.  Defaulting to v1.  If errors persist, you may explicitly try v0.")
                    log.warning(f"content of the url pattern response: {resp.text}")
                    self.appian._interactor.set_url_provider(URL_PROVIDER_V1)

        self.appian.get_client_feature_toggles()

    def _determine_auth(self) -> List[str]:
        """
        Determines what Appian username/password will be used on simulated logins. Auth will be determined
        using the following rules:

        If only "auth" key exists in config file, use the corresponding username and password for every login

        If only "credentials" key exists, pop one pair of credentials per Locust user until there's only one pair left.
        Then use the last pair of credentials for all remaining logins

        If both of the above keys exist, first use up all pairs in the "credentials" key, then use the pair in "auth"
        repeatedly for all remaining logings.

        In distributed mode, if only "credentials" key exists, each load driver will use last pair of credentials in the subset
        assigned to it via the setup_distributed_creds method.

        For example, if there are 3 pairs of credentials and 5 users per driver:
            Load driver 1 user 1 will take credential pair 1
            Load driver 2 users 1-5 will take credential pair 2
            Load driver 1 user 2-5 (and all after) will take credential pair 3

        Args:
            None

        Returns:
            auth: 2-entry list formatted as follows: ["username", "password"]

        """
        auth = self.parent.auth
        if hasattr(self.parent, 'credentials') and \
                isinstance(self.parent.credentials, list) and \
                self.parent.credentials:
            if len(self.parent.credentials) > 1 or (len(self.parent.credentials) == 1 and auth):
                auth = self.parent.credentials.pop(0)
            else:
                auth = self.parent.credentials[0]
        return auth

    def on_stop(self) -> None:
        """
        Overloaded function of Locust's default on_stop.

        It logs out the client from Appian.
        """
        if not self.portals_mode:
            self.appian.logout()

    @property
    def appian(self) -> AppianClient:
        """
        A wrapper around the generated AppianClient
        """
        return self._appian

    def override_default_flags(self, flags_to_override: List[FeatureFlag]) -> None:
        """
        `override_default_flags` gets the flag mask to set all of the flags to true given
        a list of flag enums and overrides the current feature flag extended value to set
        these flags to true.
        """
        def flags_to_override_generator() -> Generator[FeatureFlag, None, None]:
            yield from flags_to_override
        override_default_feature_flags(self.appian._interactor, flags_to_override_generator)


class AppianTaskSequence(SequentialTaskSet, AppianTaskSet):
    """
    Appian Locust SequentialTaskSet. Provides functionality of Locust's SequentialTaskSet and Handles creation of basic
    objects like``self.appian`` and actions like ``login`` and ``logout``
    """

    def __init__(self, parent: SequentialTaskSet) -> None:
        super(AppianTaskSequence, self).__init__(parent)
