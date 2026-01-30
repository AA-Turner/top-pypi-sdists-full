import os
from typing import Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

import frogml_storage
from frogml_storage.logging import logger


class HTTPClient:

    def __init__(
        self, auth: Tuple[str, str], session: Optional[requests.Session] = None
    ):
        self.auth = auth
        # add default headers
        if session is None:
            self.session = self._create_session()
        self._add_default_headers()
        self.timeout = os.getenv("JFML_TIMEOUT", default=30)

    @staticmethod
    def _create_session():
        session = requests.Session()
        adapter = HTTPAdapter(
            max_retries=RetryWithLog(
                total=5, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504]
            )
        )
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def post(self, url, data=None, params=None):
        return self.session.post(
            url, auth=self.auth, timeout=self.timeout, data=data, params=params
        )

    def get(self, url, params=None, stream=False):
        return self.session.get(url, auth=self.auth, params=params, stream=stream)

    def put(self, url, payload=None, files=None, stream=False, headers=None, json=None):
        return self.session.request(
            method="PUT",
            url=url,
            data=payload,
            auth=self.auth,
            files=files,
            stream=stream,
            timeout=self.timeout,
            headers=headers,
            json=json,
        )

    def delete(self, url):
        return self.session.request(
            method="DELETE",
            url=url,
            auth=self.auth,
            timeout=self.timeout,
        )

    def head(self, url, params=None, stream=False):
        return self.session.head(url, auth=self.auth, params=params, stream=stream)

    def _add_default_headers(self):
        self.session.headers.update(
            {"User-Agent": "frogml-sdk-python/{}".format(frogml_storage.__version__)}
        )


class RetryWithLog(Retry):
    """
    Adding extra logs before making a retry request
    """

    def __init__(self, *args, **kwargs):
        history = kwargs.get("history")
        if history is not None:
            logger.debug(f"Error: ${history[-1].error}\nretrying...")
        super().__init__(*args, **kwargs)
