from urllib.parse import urlparse

import requests
import time
import random
import os
import sys


def read_mf_config():
    # this should be overridden with the resolved remote config here:
    # obp-python-packages/ob-metaflow-extensions/metaflow_extensions/outerbounds/__init__.py
    from metaflow.metaflow_config_funcs import METAFLOW_CONFIG

    return METAFLOW_CONFIG


def get_token_url_and_headers(url_path):
    from metaflow.metaflow_config import (
        SERVICE_HEADERS,
        SERVICE_URL,
    )
    from metaflow.metaflow_config import SERVICE_HEADERS, SERVICE_URL

    # Infer auth host from metadata service URL, unless it has been
    # specified explicitly. Take the MDS host and replace first part of
    # the domain name with `auth.`. All our deployments follow this scheme
    # anyways.
    #
    auth_host = "auth." + urlparse(SERVICE_URL).hostname.split(".", 1)[1]

    authServer = read_mf_config().get("OBP_AUTH_SERVER", auth_host)
    assert url_path.startswith("/")
    url = "https://" + authServer + url_path
    headers = SERVICE_HEADERS
    return url, headers


def get_token(url_path):
    from metaflow.exception import MetaflowException

    retry_delay = 1
    max_retries = os.environ.get("METAFLOW_EXT_HTTP_MAX_RETRIES", "10")
    attempt = 0
    while attempt < int(max_retries):
        attempt = attempt + 1
        try:
            url, headers = get_token_url_and_headers(url_path)
            r = requests.get(url, headers=headers)
            r.raise_for_status()
            token_info = r.json()
            return token_info
        except requests.exceptions.HTTPError as e:
            raise MetaflowException(repr(e))
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ReadTimeout,
        ) as e:
            # ConnectionErrors are generally temporary errors like DNS resolution failures,
            # timeouts etc.
            time.sleep(retry_delay)
            retry_delay *= 2  # Double the delay for the next attempt
            retry_delay += random.uniform(0, 1)  # Add jitter
            retry_delay = min(retry_delay, 10)

    raise MetaflowException("error connecting to Outerbounds")
