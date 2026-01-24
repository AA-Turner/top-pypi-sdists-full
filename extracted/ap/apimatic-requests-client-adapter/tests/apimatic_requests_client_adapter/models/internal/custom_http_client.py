from apimatic_core_interfaces.client.http_client_provider import HttpClientProvider
from cachecontrol import CacheControl
from requests import Session, session
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class CustomHttpClient(HttpClientProvider):

    def __init__(self,
                 timeout=60,
                 cache=False,
                 max_retries=None,
                 backoff_factor=None,
                 retry_statuses=None,
                 retry_methods=None,
                 verify=True):

        self._timeout = timeout
        self._session = session()

        if cache:
            self._session = CacheControl(self._session)

        retry_strategy = Retry(total=max_retries, backoff_factor=backoff_factor, status_forcelist=retry_statuses,
                               allowed_methods=retry_methods, raise_on_status=False, raise_on_redirect=False)
        self._session.mount('http://', HTTPAdapter(max_retries=retry_strategy))
        self._session.mount('https://', HTTPAdapter(max_retries=retry_strategy))
        self._session.verify = verify

    @property
    def timeout(self) -> float:
        return self._timeout

    @property
    def session(self) -> Session:
        return self._session