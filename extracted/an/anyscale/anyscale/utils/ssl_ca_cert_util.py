import os
from typing import Optional


# ANYSCALE_SSL_CA_CERT is checked first: an explicit override must win over
# an ambient REQUESTS_CA_BUNDLE/CURL_CA_BUNDLE/SSL_CERT_FILE set by some
# other tool.
#
# Only the generated REST clients (authenticate.py, login_commands.py,
# sdk/anyscale_client/sdk.py) read this. Bare `requests` calls elsewhere in
# the CLI (e.g. working_dir uploads) keep honoring their own native env vars
# (REQUESTS_CA_BUNDLE etc.) directly and do not see ANYSCALE_SSL_CA_CERT.
_CA_CERT_ENV_VARS = (
    "ANYSCALE_SSL_CA_CERT",
    "REQUESTS_CA_BUNDLE",
    "CURL_CA_BUNDLE",
    "SSL_CERT_FILE",
)


def get_ssl_ca_cert_from_env() -> Optional[str]:
    for env_var in _CA_CERT_ENV_VARS:
        value = os.environ.get(env_var)
        # `requests` accepts a directory (e.g. c_rehash'd) for these vars,
        # but urllib3's ca_certs expects a single bundle file -- skip a
        # directory rather than pass it through and break the TLS handshake.
        if value and not os.path.isdir(value):
            return value
    return None
