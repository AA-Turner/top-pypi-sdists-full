from __future__ import annotations

import json
import os
import re
import textwrap
import warnings
from dataclasses import dataclass
from typing import Dict, Optional, List

import pytz
import requests
from dateutil.tz import tz

from seeq import spy, sdk
from seeq.sdk import *
from seeq.sdk.configuration import ClientConfiguration
from seeq.spy import _url, _common, _datalab, _errors, _version
from seeq.spy._datalab import is_datalab_functions_project
from seeq.spy._errors import *

SEEQ_SDK_RETRY_TIMEOUT_IN_SECONDS_ENV_VAR_NAME = 'SEEQ_SDK_RETRY_TIMEOUT_IN_SECONDS'
DEFAULT_REQUESTS_TIMEOUT = 90
SAAS_AUTH_DATASOURCES = ['Seeq Saas Admin']


@dataclass(repr=False)
class Session:
    """
    Used to segregate Seeq Server logins and allows for multi-server /
    multi-user concurrent logins. This object encapsulates all server-
    specific state, SPy options and API client configuration.

    Examples
    --------
    Log in to two different servers at the same time:

    >>> session1 = Session()
    >>> session2 = Session()
    >>> spy.login(url='https://server1.seeq.site', username='mark', password='markpassword', session=session1)
    >>> spy.login(url='https://server2.seeq.site', username='alex', password='alexpassword', session=session2)
    """
    _options: Options = None
    client_configuration: ClientConfiguration = None
    _client: Optional[ApiClient] = None
    _user: Optional[UserOutputV1] = None
    _user_tz: Optional[str] = None
    _public_url: Optional[str] = None
    _private_url: Optional[str] = None
    _server_version: Optional[str] = None
    _datasources: Optional[Dict[str, DatasourceOutputV1]] = None
    _user_folders: Optional[Dict[str, FolderOutputV1]] = None
    supported_units: Optional[set] = None
    corporate_folder: Optional[FolderOutputV1] = None
    my_folder: Optional[FolderOutputV1] = None
    _directories: Optional[Dict[str, DatasourceOutputV1]] = None
    auth_providers: Optional[List[DatasourceOutputV1]] = None
    https_verify_ssl: bool = True
    https_key_file: Optional[str] = None
    https_cert_file: Optional[str] = None

    def __init__(self, options: Options = None, client_configuration: ClientConfiguration = None):
        self.client_configuration = client_configuration if client_configuration is not None else ClientConfiguration()
        self.options = options if options is not None else Options(self.client_configuration)
        self._datasources = dict()

        # We have this mechanism so that test_run_notebooks() is able to increase the timeout for the child kernels
        if Session.get_global_sdk_retry_timeout_in_seconds() is not None:
            self.options.retry_timeout_in_seconds = Session.get_global_sdk_retry_timeout_in_seconds()

    def __repr__(self):
        return self.get_info()

    def __hash__(self):
        # Added so that the lru_cache can be used when Session is an argument
        return id(self)

    def __getstate__(self):
        # We can only pickle certain members. This has to mirror __setstate__().
        return self.options

    def __setstate__(self, state):
        self.options = state

    def get_info(self, *, html: bool = False) -> str:
        if self.client:
            url_part = self.public_url
            if self.private_url != self.public_url:
                url_part += f' ({self.private_url})'
            info = f'Logged in to <strong>{url_part}</strong> as <strong>{self.user_string}</strong>.\n'
            info += f'Seeq Server Version: <strong>{spy.server_version}</strong>\n'
        else:
            info = 'Not logged in.\n'

        info += (f'Seeq SDK Module Version: <strong>{sdk.__version__}</strong> @ {os.path.dirname(sdk.__file__)}\n'
                 f'Seeq SPy Module Version: <strong>{spy.__version__}</strong> @ {os.path.dirname(spy.__file__)}')

        if not html:
            info = re.sub(r'<[^>]*?>', '', info)

        return info

    @property
    def user_string(self) -> str:
        if self.user is None:
            return 'Not logged in.'

        user_string = self.user.username
        user_profile = ''
        if self.user.first_name:
            user_profile = self.user.first_name
        if self.user.last_name:
            user_profile += ' ' + self.user.last_name
        if self.user.is_admin:
            user_profile += ' [Admin]'
        if len(user_profile) > 0:
            user_string += ' (%s)' % user_profile.strip()

        return user_string

    @staticmethod
    def validate(session):
        return spy.session if session is None else session

    @staticmethod
    def set_global_sdk_retry_timeout_in_seconds(timeout: Optional[int]):
        """
        This is used to set the SDK's retry timeout (see
        "retry_timeout_in_seconds" in api_client.py) for all
        child Python kernels, such as those spawned by executing
        notebooks via nbformat is in test_run_notebook().
        :param timeout: Timeout (in seconds)

        :meta private:
        """
        if timeout is None and SEEQ_SDK_RETRY_TIMEOUT_IN_SECONDS_ENV_VAR_NAME in os.environ:
            del os.environ[SEEQ_SDK_RETRY_TIMEOUT_IN_SECONDS_ENV_VAR_NAME]
        else:
            os.environ[SEEQ_SDK_RETRY_TIMEOUT_IN_SECONDS_ENV_VAR_NAME] = str(timeout)

    @staticmethod
    def get_global_sdk_retry_timeout_in_seconds() -> Optional[int]:
        """
        See set_global_sdk_retry_timeout_in_seconds()
        :return: Timeout (in seconds)

        :meta private:
        """
        if SEEQ_SDK_RETRY_TIMEOUT_IN_SECONDS_ENV_VAR_NAME in os.environ:
            return int(os.environ[SEEQ_SDK_RETRY_TIMEOUT_IN_SECONDS_ENV_VAR_NAME])
        else:
            return None

    def populate_directories(self, client: ApiClient):
        auth_api = AuthApi(client)
        try:
            auth_providers_output = auth_api.get_auth_providers(include_auth_provider_ids=SAAS_AUTH_DATASOURCES)
        except TypeError:
            # Older versions of Seeq SDK don't have the "include_auth_provider_ids" parameter
            auth_providers_output = auth_api.get_auth_providers()
        self.auth_providers = auth_providers_output.auth_providers
        self._directories = {ds.name: ds for ds in self.auth_providers}

    @property
    def directories(self) -> Optional[Dict[str, DatasourceOutputV1]]:
        if self._directories is None and self._client is not None:
            self.populate_directories(self._client)
        return self._directories

    def clear(self):
        """
        Re-initializes the object to a "logged out" state. Note that this
        function does NOT reset API client configuration or SPy options.
        """
        self.client = None
        self.user = None
        self.public_url = None
        self.private_url = None
        self.server_version = None
        self.supported_units = None
        self.corporate_folder = None
        self.my_folder = None
        self._directories = None
        self.auth_providers = None
        self.https_verify_ssl = True
        self.https_key_file = None
        self.https_cert_file = None
        self._datasources = dict()
        self._user_folders = None
        self._user_tz = None

    # Prior to the advent of Session objects, the spy.client, spy.user and spy.server_version module-level variables
    # were exposed to end-users as a convenience. The setters below copy those (now) Session variables to those
    # legacy module-level locations for backward compatibility purposes. (Only if this Session object is the default
    # Session.)
    @property
    def client(self) -> Optional[ApiClient]:
        """
        Get the API client object for this session
        """
        return self._client

    @client.setter
    def client(self, value):
        self._client = value
        if self._client is not None:
            self._client.user_agent = f'Seeq-Python-SPy/{spy.__version__}/python'
        if self is spy.session:
            spy.client = self._client

    @property
    def user(self) -> Optional[UserOutputV1]:
        """
        Get the user that is logged into this session
        """
        return self._user

    @user.setter
    def user(self, value):
        self._user = value
        self._user_tz = None
        if self is spy.session:
            spy.user = self._user

    @property
    def server_version(self) -> Optional[str]:
        """
        Get the version of the Seeq server
        this session is logged into
        """
        return self._server_version

    @server_version.setter
    def server_version(self, value):
        self._server_version = value
        if self is spy.session:
            spy.server_version = self._server_version

    @property
    def public_url(self):
        return self._public_url

    @public_url.setter
    def public_url(self, value):
        self._public_url = _url.cleanse_url(value)

    @property
    def private_url(self):
        return self._private_url

    @private_url.setter
    def private_url(self, value):
        self._private_url = _url.cleanse_url(value)

    def get_api_url(self):
        """
        Returns the URL to use for API calls, which ends up being the
        private URL (if specified) or the public URL.

        :meta private:
        """
        return f'{self.private_url}/api'

    @property
    def options(self):
        """
        Assign a new value to the following variables if you would like to adjust them.

        ``spy.options.compatibility`` (default: None)

            The major version of SPy to emulate from a compatibility standpoint. This
            is important to set if you would like to minimize the chance that your
            script or add-on "breaks" when SPy is upgraded. Set it to the major version
            of SPy that you have tested against. E.g.: spy.options.compatibility = 184

        ``spy.options.search_page_size`` (default: 1000)

            The number of items retrieved on each round-trip to the Seeq Server during
            a spy.search() call. If you have a fast system and fast connection, you can
            make this higher.

        ``spy.options.pull_page_size`` (default: 1000000)

            The number of samples/capsules retrieved on each round-trip to the Seeq
            Server during a spy.pull() call. If you have a slow system or slow
            connection, you may wish to make this lower. It is not recommended to
            exceed 1000000.

        ``spy.options.push_page_size`` (default: 100000)

            The number of samples/capsules uploaded during each round-trip to the Seeq
            Server during a spy.push() call. If you have a slow system or slow
            connection, you may wish to make this lower. It is not recommended to
            exceed 1000000.

        ``spy.options.metadata_push_batch_size`` (default: 1000)

            The number of items uploaded during each round-trip to the Seeq
            Server during a spy.push(metadata) call. If you have a low-memory system
            you may wish to make this lower. It is not recommended to exceed 10000.

        ``spy.options.max_display_items`` (default: 10)

            The maximum number of items automatically added to the display pane of a
            worksheet by spy.push(). If pushing more than ten items you may wish to
            increase this. Setting this option to None adds all items to the display.

        ``spy.options.max_concurrent_requests`` (default: 8)

            The maximum number of simultaneous requests made to the Seeq Server during
            spy.pull() and spy.push() calls. The higher the number, the more you can
            monopolize the Seeq Server. If you keep it low, then other users are less
            likely to be impacted by your activity.

        ``spy.options.retry_timeout_in_seconds`` (default: 5)

            The amount of time to spend retrying a failed Seeq Server API call in an
            attempt to overcome network flakiness.

        ``spy.options.request_timeout_in_seconds`` (default: None)

            The amount of time to wait for a single request to complete, after which
            the http client will consider it is taking too long and give up on it.
            The default of None indicates there is no limit (infinite timeout).

        ``spy.options.clear_content_cache_before_render`` (default: False)

            When using spy.workbooks.pull(include_rendered_content=True), always
            re-render the content even if it had been previously rendered and cached.

        ``spy.options.force_calculated_scalars`` (default: False)

            During spy.push(metadata), always push CalculatedScalars even if
            LiteralScalars would normally apply. (Ignored in R60 and earlier.)

        ``spy.options.allow_version_mismatch`` (default: False)

            Allow a major version mismatch between SPy and Seeq Server. (Normally,
            a mismatch raises a RuntimeError.)

        ``spy.options.friendly_exceptions`` (default: True if running in Data Lab, otherwise False)

            If True, exceptions raised in a Jupyter notebook will be displayed in a
            friendlier format. Stack traces will not be shown by default for most
            errors; error messages will precede the stack trace; and internal SPy
            code will be omitted from the stack trace.

        ``spy.options.default_timezone`` (default: None)

            If set to a timezone, this will be understood as the intended timezone
            for all naive datetimes passed as input to SPy. This will not override
            the timezone of any timezone-aware datetime. If set to None, naive
            datetimes will be interpreted as being in the logged-in user's preferred
            timezone. Timezone can be specified as str, pytz.timezone or dateutil.tzinfo.

        ``spy.options.include_push_method`` (default: False)

            If True, a Push Method column will be added to the metadata push result DataFrame
            that indicates whether an item was pushed via the (fast) ``batch`` REST APIs or had
            to resort to the (slower) ``single`` REST APIs.
        """
        return self._options

    @options.setter
    def options(self, value):
        self._options = value

    @property
    def requests(self):
        return SqAuthRequests(self)

    @property
    def request_origin_label(self) -> str:
        """
        Used for tracking Data Consumption. If supplied, this label will be added as a header to all requests from
        the logged in user. Data Lab will automatically provide a default that you can choose to override.
        """
        return self.client.default_headers.get('x-sq-origin-label')

    @request_origin_label.setter
    def request_origin_label(self, value: str):
        if self.client is None:
            raise RuntimeError("Cannot set request_origin_label before logging in")

        if value is None:
            if 'x-sq-origin-label' in self.client.default_headers:
                del self.client.default_headers['x-sq-origin-label']
            return

        if is_datalab_functions_project() and not value.startswith("[Data Lab Functions]"):
            value = f"[Data Lab Functions] {value}"
        self.client.set_default_header('x-sq-origin-label', value)

    @property
    def request_origin_url(self) -> str:
        """
        Used for tracking Data Consumption. If supplied, this label will be added as a header to all requests from
        the logged in user. Data Lab will automatically provide a default that you can choose to override. If NOT in
        Data Lab, supply a full URL that leads to the tool/plugin that is consuming data, if applicable.
        """
        return self.client.default_headers.get('x-sq-origin-url')

    @request_origin_url.setter
    def request_origin_url(self, value: str):
        if self.client is None:
            raise RuntimeError("Cannot set request_origin_url before logging in")

        if value is None:
            if 'x-sq-origin-url' in self.client.default_headers:
                del self.client.default_headers['x-sq-origin-url']
            return

        self.client.set_default_header('x-sq-origin-url', value)
        self.client.set_default_header('Referer', value)

    def clear_datasource_cache(self):
        self._datasources = dict()

    def get_datasource(self, _id: str) -> DatasourceOutputV1:
        if not self.client:
            raise SPyRuntimeError('get_datasource() requires logged in session')

        if _id not in self._datasources:
            datasources_api = DatasourcesApi(self.client)
            self._datasources[_id] = datasources_api.get_datasource(id=_id)

        return self._datasources[_id]

    def clear_user_folder_cache(self):
        self._user_folders = None

    def get_user_folder(self, user_id: str) -> FolderOutputV1:
        """
        Get the specified user's home folder. Requires admin permissions.
        """
        if not self.user.is_admin:
            raise SPyRuntimeError('get_user_folders() requires admin permissions')

        if not self.client:
            raise SPyRuntimeError('get_user_folders() requires logged in session')

        if self._user_folders is not None:
            return self._user_folders.get(user_id)

        folders_api = FoldersApi(self.client)
        offset = 0
        limit = self.options.search_page_size
        self._user_folders = dict()
        candidates = dict()
        while True:
            folders_output = folders_api.get_folders(filter='Users', folder_id='users', limit=limit, offset=offset)
            for content in folders_output.content:
                if content.type != 'Folder' or not getattr(content, 'is_unmodifiable', False):
                    # Non-Home Folders (e.g., Data Lab Projects) can appear under /users (CRAB-60205)
                    continue

                if content.owner is not None:
                    candidates.setdefault(content.owner.id, list()).append(content)

            if len(folders_output.content) < limit:
                break

            offset += limit

        for owner_id, folder_list in candidates.items():
            if len(folder_list) > 1 and owner_id == user_id:
                folder_str = '\n'.join(f'"{c.name}" ({c.id})' for c in folder_list)
                raise SPyRuntimeError(f'Multiple candidate folders found when trying to find home folder for user '
                                      f'{owner_id}. Contact Seeq Support to remediate. Folders found:\n{folder_str}')

            if len(folder_list) == 1:
                self._user_folders[owner_id] = folder_list[0]

        return self._user_folders.get(user_id)

    def get_user_timezone(self, default_tz: str = 'UTC') -> str:
        """
        Returns the preferred timezone of the user currently logged in, or default_tz if there is no user currently
        logged in.

        :param: session: The login session (necessary to fulfill this call).
        :param: default_tz: The default timezone to return if no user is logged in.
        :return: The user's preferred timezone, in IANA Time Zone Database format (e.g., 'America/New York')
        :rtype: str
        """
        if self._user_tz is not None:
            return self._user_tz

        try:
            workbench_dict = json.loads(self.user.workbench)
            _tz = workbench_dict['state']['stores']['sqWorkbenchStore']['userTimeZone']
        except (AttributeError, KeyError, TypeError):
            # This can happen if the user has never logged in interactively (e.g., agent_api_key)
            _common.validate_timezone_arg(default_tz)
            _tz = default_tz

        self._user_tz = _tz
        return _tz

    def get_session_timezone(self):
        """
        Gets the timezone to interpret a datetime as if none is specified. This is the
        spy.options.default_timezone timezone if it exists, else the user's preferred timezone.
        :return: The session timezone, in IANA Time Zone Database format (e.g., 'America/New York')
        :rtype: str
        """
        return self.options.default_timezone if self.options.default_timezone else self.get_user_timezone()

    # The list of units that come back from system_api.get_supported_units() is a curated set of compound units that are
    # meant to be human-friendly in Formula tool help. But it's the only thing available in the API to figure out what
    # base units are supported, so we have to split the compound unit string into its components. I.e., S/cm³ gets split
    # into S and cm so that we can add those two "base" units to the set we use to determine validity.
    UNITS_SPLIT_REGEX = r'[/*²³·]'

    def is_valid_unit(self, unit):
        """
        Returns True if the supplied unit will be recognized by the Seeq calculation engine. This can be an important
        function to use if you are attempting to supply a "Value Unit Of Measure" property on a Signal or a "Unit Of
        Measure" property on a Scalar.

        :param: session: The login session (necessary to execute this call)
        :param: unit: The unit of measure for which to assess validity
        :return: True if unit is valid, False if not
        """
        if not self.supported_units:
            system_api = SystemApi(self.client)
            support_units_output = system_api.get_supported_units()  # type: SupportedUnitsOutputV1

            self.supported_units = set()
            for supported_unit_family in support_units_output.units.values():
                for supported_unit in supported_unit_family:
                    unit_parts = re.split(self.UNITS_SPLIT_REGEX, supported_unit)
                    self.supported_units.update([u for u in unit_parts if len(u) > 0])

        unit_parts = re.split(self.UNITS_SPLIT_REGEX, unit)
        for unit_part in [u for u in unit_parts if len(u) > 0]:
            if unit_part not in self.supported_units:
                return False

        return True


class Options:
    _DEFAULT_SEARCH_PAGE_SIZE = 1_000
    _DEFAULT_PULL_PAGE_SIZE = 1_000_000
    _DEFAULT_TABLE_PULL_PAGE_SIZE = 10_000
    _DEFAULT_PUSH_PAGE_SIZE = 100_000
    _DEFAULT_METADATA_PUSH_BATCH_SIZE = 1_000
    _DEFAULT_MAX_DISPLAY_ITEMS = 10
    _DEFAULT_MAX_CONCURRENT_REQUESTS = 8
    _DEFAULT_CLEAR_CONTENT_CACHE_BEFORE_RENDER = False
    _DEFAULT_FORCE_CALCULATED_SCALARS = True
    _DEFAULT_ALLOW_VERSION_MISMATCH = False
    _DEFAULT_FRIENDLY_EXCEPTIONS = _datalab.is_datalab()
    _DEFAULT_TIMEZONE = None
    _DEFAULT_COMPATIBILITY = None
    _DEFAULT_MIN_COMPATIBILITY = 188
    _DEFAULT_INCLUDE_PUSH_METHOD = False
    _DEFAULT_STATUS_WARNING_LIMIT = 20

    def __init__(self, client_configuration: ClientConfiguration):
        self.client_configuration = client_configuration
        self.search_page_size = self._DEFAULT_SEARCH_PAGE_SIZE
        self.pull_page_size = self._DEFAULT_PULL_PAGE_SIZE
        self.table_pull_page_size = self._DEFAULT_TABLE_PULL_PAGE_SIZE
        self.push_page_size = self._DEFAULT_PUSH_PAGE_SIZE
        self.metadata_push_batch_size = self._DEFAULT_METADATA_PUSH_BATCH_SIZE
        self._max_display_items = self._DEFAULT_MAX_DISPLAY_ITEMS
        self.max_concurrent_requests = self._DEFAULT_MAX_CONCURRENT_REQUESTS
        self.clear_content_cache_before_render = self._DEFAULT_CLEAR_CONTENT_CACHE_BEFORE_RENDER
        self.force_calculated_scalars = self._DEFAULT_FORCE_CALCULATED_SCALARS
        self.allow_version_mismatch = self._DEFAULT_ALLOW_VERSION_MISMATCH
        self.default_timezone = self._DEFAULT_TIMEZONE
        self._compatibility = self._DEFAULT_COMPATIBILITY
        self.include_push_method = self._DEFAULT_INCLUDE_PUSH_METHOD
        self.status_warning_limit = self._DEFAULT_STATUS_WARNING_LIMIT
        try:
            self.friendly_exceptions = self._DEFAULT_FRIENDLY_EXCEPTIONS
        except RuntimeError:
            pass

    @property
    def compatibility(self):
        return self._compatibility

    @compatibility.setter
    def compatibility(self, value: Optional[int]):
        _common.validate_argument_types([
            (value, 'compatibility', (int, float)),
        ])
        if value is None:
            self._compatibility = None
            return
        if isinstance(value, float):
            # Users may try to provide a point fix compatibility, but our compatibility flag is on Major only.
            # Drop the decimal values here. Floats don't work like version numbers anyway (190.1 vs 190.10).
            value = int(value)
        max_compatibility, _ = _version.get_spy_module_version_tuple()
        if value < self._DEFAULT_MIN_COMPATIBILITY:
            warnings.warn(f"Compatibility value {value} is below the minimum value {self._DEFAULT_MIN_COMPATIBILITY}. "
                          f"Defaulting to the minimum value.")
            self._compatibility = self._DEFAULT_MIN_COMPATIBILITY
        elif value > max_compatibility:
            warnings.warn(f"Compatibility value {value} is above the maximum value {max_compatibility}. Defaulting to "
                          f"the maximum value.")
            self._compatibility = max_compatibility
        else:
            self._compatibility = value

    @property
    def max_display_items(self):
        return self._max_display_items

    @max_display_items.setter
    def max_display_items(self, value: Optional[int]):
        if value is None:
            self._max_display_items = None
            return

        # Check if it's a numeric type
        if not isinstance(value, (int, float)):
            raise SPyValueError(
                "max_display_items must be a positive integer or None. "
                f"Got {type(value).__name__}: {value}"
            )

        # Convert float to int if it's a whole number, otherwise reject
        if isinstance(value, float):
            if value.is_integer():
                value = int(value)
            else:
                raise SPyValueError(
                    "max_display_items must be a positive integer or None. "
                    f"Got float with decimal: {value}"
                )

        # Check that it's positive
        if value <= 0:
            raise SPyValueError(
                "max_display_items must be a positive integer or None. "
                f"Got non-positive value: {value}"
            )

        # Check that it doesn't exceed the absolute maximum to prevent browser issues
        from seeq.spy._push import _ABSOLUTE_MAX_DISPLAY_ITEMS
        if value > _ABSOLUTE_MAX_DISPLAY_ITEMS:
            raise SPyValueError(
                f"max_display_items must be set to {_ABSOLUTE_MAX_DISPLAY_ITEMS} or less to maintain browser responsiveness. "
                f"Got value: {value}"
            )

        self._max_display_items = value

    def __str__(self):
        return '\n'.join([f"{k}: {v}" for k, v in self.__dict__.items()])

    def __getstate__(self):
        # We can only pickle certain members. This has to mirror __setstate__().
        return (self.compatibility,
                self.search_page_size,
                self.pull_page_size,
                self.push_page_size,
                self.metadata_push_batch_size,
                self.max_concurrent_requests,
                self.clear_content_cache_before_render,
                self.force_calculated_scalars,
                self.allow_version_mismatch,
                self.table_pull_page_size,
                self._max_display_items)

    def __setstate__(self, state):
        def get(i, default=None):
            return state[i] if i < len(state) else default

        # Accessing by index with a default allows us to maintain compatibility with previously-pickled Status
        # DataFrames
        self.compatibility = get(0, self._DEFAULT_COMPATIBILITY)
        self.search_page_size = get(1, self._DEFAULT_SEARCH_PAGE_SIZE)
        self.pull_page_size = get(2, self._DEFAULT_PULL_PAGE_SIZE)
        self.push_page_size = get(3, self._DEFAULT_PUSH_PAGE_SIZE)
        self.metadata_push_batch_size = get(4, self._DEFAULT_METADATA_PUSH_BATCH_SIZE)
        self.max_concurrent_requests = get(5, self._DEFAULT_MAX_CONCURRENT_REQUESTS)
        self.clear_content_cache_before_render = get(6, self._DEFAULT_CLEAR_CONTENT_CACHE_BEFORE_RENDER)
        self.force_calculated_scalars = get(7, self._DEFAULT_FORCE_CALCULATED_SCALARS)
        self.allow_version_mismatch = get(8, self._DEFAULT_ALLOW_VERSION_MISMATCH)
        self.table_pull_page_size = get(9, self._DEFAULT_TABLE_PULL_PAGE_SIZE)
        self._max_display_items = get(10, self._DEFAULT_MAX_DISPLAY_ITEMS)

    @property
    def friendly_exceptions(self):
        return self._friendly_exceptions

    @friendly_exceptions.setter
    def friendly_exceptions(self, value):
        if value:
            try:
                _errors.add_spy_exception_handler()
                self._friendly_exceptions = True
            except RuntimeError:
                self._friendly_exceptions = False
                raise

        else:
            _errors.remove_spy_exception_handler()
            self._friendly_exceptions = False

    @property
    def default_timezone(self):
        return self._default_timezone

    @default_timezone.setter
    def default_timezone(self, value):
        if value is None:
            self._default_timezone = None
        elif isinstance(value, str):
            try:
                pytz.timezone(value)
                self._default_timezone = value
            except pytz.UnknownTimeZoneError:
                raise
        elif isinstance(value, pytz.BaseTzInfo) or isinstance(value, tz.tzoffset):
            self._default_timezone = value
        else:
            raise SPyTypeError(f"Default timezone can't be type {type(value).__name__}")

    @property
    def retry_timeout_in_seconds(self):
        return self.client_configuration.retry_timeout_in_seconds

    @retry_timeout_in_seconds.setter
    def retry_timeout_in_seconds(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise SPyValueError("retry_timeout_in_seconds must be a positive, non-zero integer or float number.")

        if self.request_timeout_in_seconds is not None and value > self.request_timeout_in_seconds:
            raise SPyValueError("retry_timeout_in_seconds cannot be more than request_timeout_in_seconds. Set "
                                "request_timeout_in_seconds to an equal or greater value first (or None so that it is "
                                "infinite.")

        self.client_configuration.retry_timeout_in_seconds = value

    @property
    def request_timeout_in_seconds(self):
        # We need to check here because SPy can be used with older versions of Seeq, which do not have this attribute
        if hasattr(self.client_configuration, 'request_timeout_in_seconds'):
            return self.client_configuration.request_timeout_in_seconds
        return None

    @request_timeout_in_seconds.setter
    def request_timeout_in_seconds(self, value):
        if value is not None and (not isinstance(value, (int, float)) or value <= 0):
            raise SPyValueError("request_timeout_in_seconds must be a positive, non-zero integer or float number "
                                "OR None to indicate infinite.")

        if value is not None and value < self.client_configuration.retry_timeout_in_seconds:
            raise SPyValueError("request_timeout_in_seconds cannot be less than retry_timeout_in_seconds. Set "
                                "retry_timeout_in_seconds to an equal or lower value first.")

        # We need to check here because SPy can be used with older versions of Seeq, which do not have this attribute
        if hasattr(self.client_configuration, 'request_timeout_in_seconds'):
            self.client_configuration.request_timeout_in_seconds = value
        else:
            warnings.warn("The request_timeout_in_seconds option is not available in the current version of the "
                          "seeq Python package. Please upgrade to the latest version of the seeq package that "
                          "corresponds to the version of your Seeq service.")

    def print(self):
        _common.print_output(str(self))

    def help(self):
        help_string = f"""\
            Assign a new value to the following variables if you would like to adjust them.

            E.g.:
               spy.options.max_concurrent_requests = 3

            Available Options
            -----------------

            spy.options.compatibility (default: {self._DEFAULT_COMPATIBILITY})

                The major version of SPy to emulate from a compatibility standpoint. This
                is important to set if you would like to minimize the chance that your
                script or add-on "breaks" when SPy is upgraded. Set it to the major version
                of SPy that you have tested against. E.g.: spy.options.compatibility = 184

            spy.options.search_page_size (default: {self._DEFAULT_SEARCH_PAGE_SIZE})

                The number of items retrieved on each round-trip to the Seeq Server during
                a spy.search() call. If you have a fast system and fast connection, you can
                make this higher.

            spy.options.pull_page_size (default: {self._DEFAULT_PULL_PAGE_SIZE})

                The number of samples/capsules retrieved on each round-trip to the Seeq
                Server during a spy.pull() call. If you have a slow system or slow
                connection, you may wish to make this lower. It is not recommended to
                exceed 1000000.

            spy.options.table_pull_page_size (default: {self._DEFAULT_TABLE_PULL_PAGE_SIZE})

                The number of rows retrieved on each round-trip to the Seeq Server
                during a spy.pull() call where a Vantage Room is being pulled. If
                you have a slow system or slow connection, you may wish to make this
                lower. It is not recommended to exceed 10_000.

            spy.options.push_page_size (default: {self._DEFAULT_PUSH_PAGE_SIZE})

                The number of samples/capsules uploaded during each round-trip to the Seeq
                Server during a spy.push() call. If you have a slow system or slow
                connection, you may wish to make this lower. It is not recommended to
                exceed 1000000.

            spy.options.metadata_push_batch_size (default: {self._DEFAULT_METADATA_PUSH_BATCH_SIZE})

                The number of items uploaded during each round-trip to the Seeq
                Server during a spy.push(metadata) call. If you have a low-memory system
                you may wish to make this lower. It is not recommended to exceed 10000.

            spy.options.max_display_items (default: {self._DEFAULT_MAX_DISPLAY_ITEMS})

                The maximum number of items automatically added to the display pane of a
                worksheet by spy.push(). If pushing more than ten signals you may wish to
                increase this. Setting this option to None adds all items to the display.

            spy.options.max_concurrent_requests (default: {self._DEFAULT_MAX_CONCURRENT_REQUESTS})

                The maximum number of simultaneous requests made to the Seeq Server during
                spy.pull() and spy.push() calls. The higher the number, the more you can
                monopolize the Seeq Server. If you keep it low, then other users are less
                likely to be impacted by your activity.

            spy.options.retry_timeout_in_seconds (default: {ClientConfiguration.DEFAULT_RETRY_TIMEOUT_IN_SECONDS})

                The amount of time to spend retrying a failed Seeq Server API call in an
                attempt to overcome network flakiness.

            spy.options.request_timeout_in_seconds (default: None)

                The amount of time to wait for a single request to complete, after which
                the http client will consider it is taking too long and give up on it.
                The default of None indicates there is no limit (infinite timeout).

                This option may require an upgrade of the `seeq` Python package to
                function - a warning will be provided if so.

            spy.options.clear_content_cache_before_render (default: {str(self._DEFAULT_CLEAR_CONTENT_CACHE_BEFORE_RENDER)})

                When using spy.workbooks.pull(include_rendered_content=True), always
                re-render the content even if it had been previously rendered and cached.

            spy.options.force_calculated_scalars (default: {self._DEFAULT_FORCE_CALCULATED_SCALARS})

                During spy.push(metadata), always push CalculatedScalars even if
                LiteralScalars would normally apply. (Ignored in R60 and earlier.)

            spy.options.allow_version_mismatch (default: {self._DEFAULT_ALLOW_VERSION_MISMATCH})

                Allow a major version mismatch between SPy and Seeq Server. (Normally,
                a mismatch raises a RuntimeError.)

            spy.options.friendly_exceptions (default: True if running in Data Lab, otherwise False)

                If True, exceptions raised in a Jupyter notebook will be displayed in a
                friendlier format. Stack traces will not be shown by default for most
                errors; error messages will precede the stack trace; and internal SPy
                code will be omitted from the stack trace.

            spy.options.default_timezone (default: {self._DEFAULT_TIMEZONE})

                If set to a timezone, this will be understood as the intended timezone
                for all naive datetimes passed as input to SPy. This will not override
                the timezone of any timezone-aware datetime. If set to None, naive
                datetimes will be interpreted as being in the logged-in user's preferred
                timezone. Timezone can be specified as str, pytz.timezone or dateutil.tzinfo.

            spy.options.include_push_method (default: {self._DEFAULT_INCLUDE_PUSH_METHOD})

                If True, a Push Method column will be added to the metadata push result DataFrame
                that indicates whether an item was pushed via the (fast) ``batch`` REST APIs or had
                to resort to the (slower) ``single`` REST APIs.

            spy.options.status_warning_limit (default: {self._DEFAULT_STATUS_WARNING_LIMIT})
                The number of warnings to display in the status output before truncating.
                If the number of warnings exceeds this limit, a message will be displayed
                indicating how many warnings were truncated.
        """

        _common.print_output(textwrap.dedent(help_string))

    def wants_compatibility_with(self, major_version):
        return self.compatibility is not None and self.compatibility <= major_version


@dataclass(repr=False)
class SqAuthRequests:
    session: Session

    def add_request_kwargs(self, d):
        if 'cookies' not in d:
            d['cookies'] = dict()
        d['cookies']['sq-auth'] = self.session.client.auth_token
        if 'headers' not in d:
            d['headers'] = dict()
        d['headers']['x-sq-auth'] = self.session.client.auth_token
        d['verify'] = self.session.https_verify_ssl
        if 'timeout' not in d:
            d['timeout'] = DEFAULT_REQUESTS_TIMEOUT

    def get(self, *args, **kwargs) -> requests.Response:
        self.add_request_kwargs(kwargs)
        return requests.get(*args, **kwargs)

    def patch(self, *args, **kwargs) -> requests.Response:
        self.add_request_kwargs(kwargs)
        return requests.patch(*args, **kwargs)

    def post(self, *args, **kwargs) -> requests.Response:
        self.add_request_kwargs(kwargs)
        return requests.post(*args, **kwargs)

    def put(self, *args, **kwargs) -> requests.Response:
        self.add_request_kwargs(kwargs)
        return requests.put(*args, **kwargs)

    def delete(self, *args, **kwargs) -> requests.Response:
        self.add_request_kwargs(kwargs)
        return requests.delete(*args, **kwargs)
