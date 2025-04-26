import functools
import os

import requests


@functools.lru_cache(maxsize=None)
def session() -> requests.Session:
    """A requests Session to use for all HTTP Requests from the SDK.

    This session is pre-configured with global settings such as client certificates where required.
    Tecton-backend-specific stuff should _not_ be added here, because we also use this session for requests to e.g.
    AWS and Okta.
    """
    s = requests.Session()
    # Allow settings HTTP client certificates from environment variables. This is useful for making requests through
    # the Teleport proxy.
    if "TECTON_CLIENT_CERT" in os.environ:
        s.cert = (os.environ["TECTON_CLIENT_CERT"], os.environ["TECTON_CLIENT_KEY"])
    return s
