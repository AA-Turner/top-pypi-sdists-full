import json
import os
import warnings
from io import BytesIO
from operator import attrgetter
from urllib.parse import urlsplit
from zipfile import ZipFile

import jsonref
import requests
from requests.adapters import HTTPAdapter
from requests_cache import NEVER_EXPIRE, CachedSession

from ocdsextensionregistry.exceptions import UnknownLatestVersion

# For example: "file:///C|/tmp" or "file:///tmp"
FILE_URI_OFFSET = 8 if os.name == "nt" else 7

DEFAULT_MINOR_VERSION = "1.1"

# https://requests-cache.readthedocs.io/en/stable/user_guide/troubleshooting.html#common-error-messages
# https://docs.python.org/3/library/socket.html#constants
warnings.filterwarnings(
    "ignore",
    category=ResourceWarning,
    message=r"^unclosed <ssl\.SSLSocket fd=\d+, family=AddressFamily\.AF_INET6?, type=SocketKind\.SOCK_STREAM, ",
)

# https://2.python-requests.org/projects/3/api/#requests.adapters.HTTPAdapter
# https://urllib3.readthedocs.io/en/latest/advanced-usage.html#customizing-pool-behavior
adapter = HTTPAdapter(max_retries=3, pool_maxsize=int(os.getenv("REQUESTS_POOL_MAXSIZE", "10")))
session = CachedSession(backend="memory", expire_after=os.getenv("REQUESTS_CACHE_EXPIRE_AFTER", NEVER_EXPIRE))
session.headers.update(
    {"User-Agent": "ocdsextensionregistry (+http://www.open-contracting.org; data@open-contracting.org)"}
)
session.mount("https://", adapter)
session.mount("http://", adapter)


def json_dump(data, io):
    """Dump JSON to a file-like object."""
    json.dump(data, io, ensure_ascii=False, indent=2)


def get_latest_version(versions):
    """
    Return the identifier of the latest version from a list of versions of the same extension.

    :raises UnknownLatestVersion: if the latest version of the extension can't be determined
    """
    if len(versions) == 1:
        return versions[0]

    version_numbers = {version.version: version for version in versions}
    if "master" in version_numbers:
        return version_numbers["master"]
    if DEFAULT_MINOR_VERSION in version_numbers:
        return version_numbers[DEFAULT_MINOR_VERSION]

    dated = [version for version in versions if version.date]
    if dated:
        return max(dated, key=attrgetter("date"))

    raise UnknownLatestVersion


# jsonref's default jsonloader has no timeout and supports file, FTP and data URLs.
def loader(url, **kwargs):
    if urlsplit(url).scheme in {"http", "https"}:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json(**kwargs)
    raise NotImplementedError


def replace_refs(schema, *, keep_defs=False, proxies=False, **kwargs):
    deref = jsonref.replace_refs(
        schema,
        # Using one of `merge_props=True` or `proxies=True` preserves "deprecated" in a schema with "$ref".
        # `lazy_load=True` has an effect only if `proxies=True`. `lazy_load=False` forces references errors early.
        **({"proxies": proxies, "merge_props": not proxies, "loader": loader, "lazy_load": False} | kwargs),
    )
    if not keep_defs:
        for keyword in ("definitions", "$defs"):
            deref.pop(keyword, None)
    return deref


def remove_nulls(schema):
    if isinstance(schema, dict):
        for key in list(schema):
            subschema = schema[key]
            if subschema is None:
                del schema[key]
            else:
                remove_nulls(subschema)
    elif isinstance(schema, list):
        for subschema in schema:
            remove_nulls(subschema)


def _resolve(data_or_url):
    parsed = urlsplit(data_or_url)

    if parsed.scheme:
        if parsed.scheme == "file":
            with open(data_or_url[FILE_URI_OFFSET:]) as f:
                return f.read()

        response = session.get(data_or_url)
        response.raise_for_status()
        return response.text

    return data_or_url


def _resolve_zip(url, base=""):
    if isinstance(url, bytes):
        return ZipFile(BytesIO(url))

    parsed = urlsplit(url)

    if parsed.scheme == "file":
        if url.endswith(".zip"):
            with open(url[FILE_URI_OFFSET:], "rb") as f:
                io = BytesIO(f.read())
        else:
            io = BytesIO()
            with ZipFile(io, "w") as zipfile:
                zipfile.write(url[FILE_URI_OFFSET:], arcname="zip/")
                for root, dirs, files in os.walk(os.path.join(url[FILE_URI_OFFSET:], base)):
                    for directory in dirs:
                        if directory == "__pycache__":
                            dirs.remove(directory)
                    for file in sorted(files):
                        zipfile.write(os.path.join(root, file), arcname=f"zip/{file}")
    else:
        response = session.get(url, allow_redirects=True)
        response.raise_for_status()
        io = BytesIO(response.content)

    return ZipFile(io)
