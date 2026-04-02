"""Encode JWT tokens with Atlassian Connect `qsh` claim.

This module provides an `encode_token` function that can be used to encode a
JWT including the query string hash claim.
"""

from time import time

import jwt as jwt

from .url_utils import hash_url


def encode_token(http_method, url, clientKey, sharedSecret,
                 timeout_secs=60 * 60, payload_kwargs=None, **ignored):
    """Encode a JWT token including the `qsh` claim.

    Args:
        http_method (string): HTTP method used for the ensuing request.
        url (string): URL to sign. Must be relative to the host base URL found
            in the tenant information.
        clientKey (string): client key from tenant information used as `aud`
            claim in token. camel case to allow JSON tenant information (from
            installed lifecycle callback) to be passed in directly.
        sharedSecret (string): key used to encrypt the token. camel case to
            allow tenant information to be passed in directly.
        timeout_secs (Optional[int]): timeout for the generated token in
            seconds. Defaults to one hour.
        payload_kwargs (Optional[dict]): allows for setting specific payload
            options.
        ignored (dict): allows tenant information to be passed in directly.

    Returns:
        string: the encoded JWT token
    """
    if payload_kwargs is None:
        payload_kwargs = {}
    now = int(time())
    payload = {
        'aud': clientKey,
        'exp': now + timeout_secs,
        'iat': now,
        'iss': clientKey,
        'qsh': hash_url(http_method, url),
    }
    payload.update(payload_kwargs)
    token = jwt.encode(key=sharedSecret, algorithm='HS256', payload=payload)
    if isinstance(token, bytes):
        token = token.decode('utf8')
    return token
