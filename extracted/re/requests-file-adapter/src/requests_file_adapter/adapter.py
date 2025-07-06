#!/usr/bin/env python3
"""
File adapter for the requests library.
"""

import datetime
import errno
import io
import logging
import mimetypes
import os
import pathlib

from requests import Response, codes
from requests.adapters import BaseAdapter
from requests.compat import urlparse

from .ip import is_localhost


LOGGER = logging.getLogger(__name__)


class FileAdapter(BaseAdapter):
    """
    File adapter for the requests package.
    """

    ERROR_MAP = {
        # pylint: disable=no-member
        errno.EACCES: codes.forbidden,
        errno.ENOENT: codes.not_found,
    }

    def send(
        self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None
    ):  # pylint: disable=too-many-arguments
        """
        Send a file via a requests.Response object.

        Args:
            request:
                The sent request.

            stream:
                If True, stream the file content.

            timeout:
                Ignored.

            verify:
                Ignored

            cert:
                Ignored.

            proxies: Ignored.
        """
        supported_methods = ("GET", "HEAD")
        if request.method not in supported_methods:
            raise ValueError(
                f"Unsupported request method: {request.method} "
                f"[supported methods: {', '.join(supported_methods)}]"
            )

        parsed_url = urlparse(request.url)

        if parsed_url.netloc and not is_localhost(parsed_url.netloc):
            raise ValueError(
                f'The host "{parsed_url.netloc}" ' "does not resolve to localhost."
            )

        path = pathlib.Path(parsed_url.path)
        if not path.is_absolute():
            raise ValueError("Only absolute paths are supported.")

        LOGGER.debug("Responding to request for file %s", path)

        resp = Response()
        resp.request = request

        try:
            if request.method == "GET":
                resp.raw = path.open("rb")  # pylint: disable=consider-using-with
                resp.raw.release_conn = resp.raw.close
            elif not path.exists():
                raise FileNotFoundError(
                    errno.ENOENT, os.strerror(errno.ENOENT), str(path)
                )
            elif not os.access(path, os.R_OK):
                raise PermissionError(
                    errno.EACCES, os.strerror(errno.EACCES), str(path)
                )
            resp.status_code = codes.ok  # pylint: disable=no-member
            resp.url = request.url
            if path.is_file():
                self._set_file_headers(resp, path)

        except OSError as err:
            resp.status_code = self.ERROR_MAP.get(
                err.errno, codes.bad_request  # pylint: disable=no-member
            )
            err_msg = str(err).encode("utf-8")
            resp.raw = io.BytesIO(err_msg)
            resp.headers.update(
                {
                    "Content-Length": len(err_msg),
                    "Content-Type": "text/plain; charset=UTF-8",
                }
            )

        return resp

    @staticmethod
    def _set_file_headers(resp, path):
        """
        Set applicable HTTP headers for the given file.

        Args:
            resp:
                The requests.Response object.

            path:
                The path to the file as a pathlib.Path object.
        """
        stat = path.stat()
        mtime = datetime.datetime.fromtimestamp(stat.st_mtime, datetime.UTC)
        resp.headers.update(
            {
                "Content-Length": stat.st_size,
                "Last-Modified": mtime.strftime("%a, %d %b %Y %H:%M:%S GMT"),
            }
        )
        media_type, encoding = mimetypes.guess_type(path)
        if media_type:
            resp.headers["Content-Type"] = media_type
        if encoding:
            resp.headers["Content-Encoding"] = encoding

    def close(self):
        pass
