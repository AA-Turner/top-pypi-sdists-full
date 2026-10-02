"""Helpers to handle the WSGI environment variables"""
from typing import Mapping, Any, TYPE_CHECKING
from urllib.parse import urlencode
import base64
import io
import sys
import logging

from libadvian.binpackers import ensure_utf8

from .utilities import clean_path_string

if TYPE_CHECKING:
    from aws_lambda_powertools.utilities.typing import LambdaContext


LOGGER = logging.getLogger(__name__)

# FIXME: define the types the return keys can be
def environ(event: Mapping[str, Any], context: "LambdaContext") -> Mapping[str, Any]:
    """Prepare the WSGI environment from the Lambda event+context"""
    # Check if format version is in v2, used for determining where to retrieve http method and path
    is_v2 = "2.0" in event.get("version", {})

    body = event.get("body", "") or ""  # Outside things can set the value to None

    if event.get("isBase64Encoded", False):
        body = base64.b64decode(body)
    # FIXME: Flag the encoding in the headers <- this is old note, IDK what it is supposed to mean
    body = ensure_utf8(body)

    # Use get() to access queryStringParameter field without throwing error if it doesn't exist
    query_string = event.get("queryStringParameters", {}) or {}  # Outside things can set the value to None
    if "multiValueQueryStringParameters" in event and event["multiValueQueryStringParameters"]:
        query_string = []
        for key in event["multiValueQueryStringParameters"]:
            for value in event["multiValueQueryStringParameters"][key]:
                query_string.append((key, value))

    use_environ = {
        # Get http method from within requestContext.http field in V2 format
        "REQUEST_METHOD": event["requestContext"]["http"]["method"] if is_v2 else event["httpMethod"],
        "SCRIPT_NAME": "",
        "SERVER_NAME": "",
        "SERVER_PORT": "",
        "PATH_INFO": clean_path_string(event["requestContext"]["http"]["path"] if is_v2 else event["path"]),
        "QUERY_STRING": urlencode(query_string),
        "REMOTE_ADDR": "127.0.0.1",
        "CONTENT_LENGTH": str(len(body)),
        "HTTP": "on",
        "SERVER_PROTOCOL": "HTTP/1.1",
        "wsgi.version": (1, 0),
        "wsgi.input": io.BytesIO(body),
        "wsgi.errors": sys.stderr,  # PONDER: is there a smarter stream we can use ? some logging facility ?
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": False,
        "wsgi.url_scheme": "",
        "awsgi.event": event,
        "awsgi.context": context,
    }
    headers = event.get("headers", {}) or {}  # Outside things can set the value to None
    for key, val in headers.items():
        key = key.upper().replace("-", "_")

        if key == "CONTENT_TYPE":
            use_environ["CONTENT_TYPE"] = val
        elif key == "HOST":
            use_environ["SERVER_NAME"] = val
        elif key == "X_FORWARDED_FOR":
            use_environ["REMOTE_ADDR"] = val.split(", ")[0]
        elif key == "X_FORWARDED_PROTO":
            use_environ["wsgi.url_scheme"] = val
        elif key == "X_FORWARDED_PORT":
            use_environ["SERVER_PORT"] = val

        use_environ["HTTP_" + key] = val

    return use_environ
