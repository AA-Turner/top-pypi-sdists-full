"""Storage PUTs through explicit short-lived grants, without platform credentials."""

import http.client
import sys
from collections.abc import Mapping
from pathlib import Path
from urllib.parse import urlsplit

from labqoat.worker.scoped_api import ScopedApi
from labqoat.net.transport_trust import TransportTrust


class DirectAssetUpload:
    """Send a staged file straight to storage; the grant's signed headers admit only the registered bytes."""

    @staticmethod
    def send(grant: Mapping[str, object], source: Path) -> bool:
        """Report whether storage kept the file; any refusal leaves the authenticated upload to the caller."""
        url, headers = grant.get("url"), grant.get("headers")
        if not isinstance(url, str) or not isinstance(headers, dict):
            return False
        parsed = urlsplit(url)
        ScopedApi(parsed._replace(path="", query="", fragment="").geturl(), {}, "/")
        host, megabyte = str(parsed.hostname), 1024 * 1024
        connection = TransportTrust.connection(parsed.scheme, host, parsed.port, timeout=180, blocksize=megabyte)
        try:
            with source.open("rb") as body:
                connection.request("PUT", f"{parsed.path}?{parsed.query}", body=body, headers=headers)
                response = connection.getresponse()
                response.read()
            return DirectAssetUpload._kept(parsed.hostname, f"HTTP {response.status}", response.status == 200)
        except (OSError, http.client.HTTPException) as error:
            return DirectAssetUpload._kept(parsed.hostname, type(error).__name__, False)
        finally:
            connection.close()

    @staticmethod
    def _kept(host: str | None, outcome: str, kept: bool) -> bool:
        """Name the storage host and outcome of a refused transfer, never text that could echo the signed grant."""
        if not kept:
            message = f"Direct storage upload was not accepted ({host}: {outcome}); sending through the API instead."
            print(message, file=sys.stderr, flush=True)
        return kept
