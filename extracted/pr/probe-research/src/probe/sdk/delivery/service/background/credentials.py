"""HeldCredentials: in-code keys a training process handed over (`credentials.hold`, plan D21), in this
service's memory only, for the drains of their credential queues (`<outbox>/credential-v1/<fp>/`)."""

from __future__ import annotations

import collections
import os
import threading

#: Keys held at once, at most; the oldest goes first.
MAX_HELD = 64
#: The folder credential queues live in (`ops.CREDENTIAL_NAMESPACE`, held equal by a test).
CREDENTIAL_NAMESPACE = "credential-v1"


class HeldCredentials:
    """fingerprint -> the environment that sends with it (`PROBE_TOKEN`, `PROBE_INGEST_TOKEN`,
    `PROBE_BASE_URL`). Never written anywhere; gone with the service."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._held: collections.OrderedDict[str, dict] = collections.OrderedDict()

    def hold(self, fingerprint: str, env: dict) -> None:
        with self._lock:
            self._held.pop(fingerprint, None)
            self._held[fingerprint] = dict(env)
            while len(self._held) > MAX_HELD:
                self._held.popitem(last=False)

    def get_env_for(self, directory: str) -> dict:
        """The held environment for a credential queue's folder, else {}."""
        parent, name = os.path.split(os.path.normpath(directory))
        if os.path.basename(parent) != CREDENTIAL_NAMESPACE:
            return {}
        with self._lock:
            return dict(self._held.get(name) or {})

    def count(self) -> int:
        with self._lock:
            return len(self._held)


def need_credentials(parameters: dict) -> tuple[str, dict]:
    """`credentials.hold`'s `(fingerprint, env)`: `env` holds `PROBE_TOKEN` and/or
    `PROBE_INGEST_TOKEN` (and may name `PROBE_BASE_URL`), and `fingerprint` must be theirs
    (`credential_fingerprint`), so a caller can only fill the queue its own key names."""
    from probe.foundation.service_api.wire import invalid_params
    from probe.sdk.delivery.outbox.drain.credentials import credential_fingerprint

    env = parameters.get("env")
    allowed = {"PROBE_TOKEN", "PROBE_INGEST_TOKEN", "PROBE_BASE_URL"}
    if not isinstance(env, dict) or not env or not set(env) <= allowed:
        raise invalid_params(f"env must hold only {sorted(allowed)}")
    if not all(isinstance(value, str) and 0 < len(value) <= 8192 and "\0" not in value for value in env.values()):
        raise invalid_params("env values must be non-empty strings of at most 8192 characters")
    fingerprint = credential_fingerprint(env.get("PROBE_TOKEN"), env.get("PROBE_INGEST_TOKEN"))
    if fingerprint is None or parameters.get("fingerprint") != fingerprint:
        raise invalid_params("fingerprint must be the one of env's token")
    return fingerprint, dict(env)
