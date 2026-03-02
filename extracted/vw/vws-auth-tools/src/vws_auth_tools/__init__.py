"""Authorization helpers."""

import base64
import email.utils
import hashlib
import hmac


def _compute_hmac_base64(key: bytes, data: bytes) -> bytes:
    """Return the Base64 encoded HMAC-SHA1 hash of `data` using the `key`."""
    hashed = hmac.new(key=key, msg=None, digestmod=hashlib.sha1)
    hashed.update(msg=data)
    return base64.b64encode(s=hashed.digest())


def rfc_1123_date() -> str:
    """Return the date formatted as per RFC 2616, section 3.3.1, rfc1123-date.

    This is the date needed by the VWS API, as described in
    https://developer.vuforia.com/library/web-api/vuforia-web-api-authentication.
    """
    return email.utils.formatdate(None, localtime=False, usegmt=True)


def authorization_header(
    access_key: str,
    secret_key: str,
    method: str,
    content: str | bytes | None,
    content_type: str,
    date: str,
    request_path: str,
) -> str:
    """Get an `Authentication` header for the VWS API.

    This can be used for a request made to the VWS API with the given
    attributes.

    See https://developer.vuforia.com/library/web-api/vuforia-web-api-authentication.

    Args:
        access_key: A VWS server or client access key.
        secret_key: A VWS server or client secret key.
        method: The HTTP method which will be used in the request.
        content: The request body which will be used in the request.
        content_type: The `Content-Type` header which is expected by
            endpoint. This does not necessarily have to match the
            `Content-Type` sent in the headers. In particular, for the query
            API, this must be set to `multipart/form-data` but the header must
            include the boundary.
        date: The current date which must exactly match the date sent in the
            `Date` header.
        request_path: The path to the endpoint which will be used in the
            request.

    Returns:
        An `Authorization` header which can be used for a request made
        to the VWS API with the given attributes.
    """
    # Ignore a warning that MD5 is insecure - VWS requires it.
    hashed = hashlib.md5()  # noqa: S324

    if content is None:
        content = b""

    if isinstance(content, str):
        content = content.encode(encoding="utf-8")

    hashed.update(content)
    content_md5_hex = hashed.hexdigest()

    components_to_sign = [
        method,
        content_md5_hex,
        content_type,
        date,
        request_path,
    ]
    string_to_sign = "\n".join(components_to_sign)
    signature = _compute_hmac_base64(
        key=secret_key.encode(),
        data=bytes(
            string_to_sign,
            encoding="utf-8",
        ),
    )
    return f"VWS {access_key}:{signature.decode()}"
