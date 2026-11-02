"""Calls to a pool of warm verifier servers, as samples are produced, from any process of the worker."""

import http.client
import itertools
import json
import threading
import time
from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import cast
from urllib.parse import urlsplit

from labqoat.json_document import JsonValue


@dataclass
class VerifierClient:
    """Send one JSON document per sample to the next server and return its JSON answer.

    It holds only addresses, so it can be handed to another process, such as a trainer's reward worker. Each
    thread keeps one connection per server. A server that cannot be reached is skipped for the next one; the
    request fails only when none answers. ``stats`` tells how many checks were made and how long they took.
    """

    urls: Sequence[str]
    path: str = "/"
    timeout: float = 120.0
    _turn: "itertools.count[int]" = field(default_factory=itertools.count, init=False, repr=False)
    _local: threading.local = field(default_factory=threading.local, init=False, repr=False)
    _requests: int = field(default=0, init=False)
    _seconds: float = field(default=0.0, init=False)

    def __getstate__(self) -> dict[str, object]:
        """Send only the addresses to another process."""
        return {"urls": tuple(self.urls), "path": self.path, "timeout": self.timeout}

    def __setstate__(self, state: dict[str, object]) -> None:
        """Start afresh in the receiving process."""
        self.__init__(**state)  # type: ignore[misc]

    def check(self, document: JsonValue) -> JsonValue:
        """Verify one sample; the first server that answers decides."""
        started = time.monotonic()
        first = next(self._turn)
        failure: Exception | None = None
        for offset in range(len(self.urls)):
            try:
                answer = self._post(self.urls[(first + offset) % len(self.urls)], document)
            except (OSError, http.client.HTTPException) as error:
                failure = error
                continue
            self._requests += 1
            self._seconds += time.monotonic() - started
            return answer
        raise ConnectionError(f"No verifier answered: {failure}")

    def stats(self) -> dict[str, float]:
        """Checks made from this process and the mean time each took, waiting included."""
        mean = self._seconds / self._requests if self._requests else 0.0
        return {"requests": self._requests, "mean_seconds": mean}

    def _post(self, url: str, document: JsonValue) -> JsonValue:
        """One request on this thread's connection to `url`, opened again if it was dropped."""
        connections: dict[str, http.client.HTTPConnection] = self._local.__dict__.setdefault("connections", {})
        connection = connections.get(url)
        if connection is None:
            address = urlsplit(url)
            connection = http.client.HTTPConnection(address.hostname or "", address.port, timeout=self.timeout)
            connections[url] = connection
        body = json.dumps(document).encode()
        try:
            connection.request("POST", self.path, body, {"Content-Type": "application/json"})
            response = connection.getresponse()
            content = response.read()
        except (OSError, http.client.HTTPException):
            connection.close()
            connections.pop(url, None)
            raise
        if response.status != 200:
            raise http.client.HTTPException(f"verifier answered HTTP {response.status}")
        return cast(JsonValue, json.loads(content))
