import threading
import time
from typing import Callable, Dict, Optional, Set

from abstra_internals.cloud_api import save_editor_auth_token_to_file
from abstra_internals.logger import AbstraLogger

# Renew whenever less than 6 of the token's 7 days remain — in practice, on
# the first request of each day of use. An idle gap longer than the full 7
# days cannot be renewed (cloud-api only renews still-valid tokens) and falls
# back to the console redirect in _guard().
RENEW_THRESHOLD_SECONDS = 6 * 24 * 60 * 60
RENEW_RETRY_INTERVAL_SECONDS = 60


class EditorAuthRenewer:
    """Sliding renewal of web editor session tokens.

    Renewal happens in a background thread so no user request ever blocks on
    the cloud-api round trip: `maybe_renew` kicks off the renewal, and once it
    completes, `fresh_token_for` returns the replacement so the caller can
    re-set the cookie on a later response.

    `renew_fn` is typically `EditorAuthRepository.renew_token`.
    """

    def __init__(self, renew_fn: Callable[[str], Optional[str]]):
        self._renew_fn = renew_fn
        self._lock = threading.Lock()
        self._renewed: Dict[str, str] = {}
        self._in_flight: Set[str] = set()
        self._last_attempt: Dict[str, float] = {}

    def fresh_token_for(self, token: str) -> Optional[str]:
        with self._lock:
            return self._renewed.get(token)

    def maybe_renew(self, token: str, exp: float) -> None:
        remaining = exp - time.time()
        if remaining <= 0 or remaining > RENEW_THRESHOLD_SECONDS:
            return

        with self._lock:
            if token in self._renewed or token in self._in_flight:
                return
            last_attempt = self._last_attempt.get(token, 0.0)
            if time.time() - last_attempt < RENEW_RETRY_INTERVAL_SECONDS:
                return
            self._last_attempt[token] = time.time()
            self._in_flight.add(token)

        threading.Thread(
            target=self._renew,
            args=(token,),
            daemon=True,
            name="EditorAuthRenewer",
        ).start()

    def _renew(self, token: str) -> None:
        try:
            new_token = self._renew_fn(token)
            if not new_token:
                return
            # Keep the tunnel path (which reads the token from this file) on
            # the freshest token too.
            save_editor_auth_token_to_file(new_token)
            with self._lock:
                self._renewed[token] = new_token
        except Exception as e:
            AbstraLogger.capture_exception(e)
        finally:
            with self._lock:
                self._in_flight.discard(token)
