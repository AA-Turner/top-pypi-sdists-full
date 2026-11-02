"""CredentialsMixin, Client's methods: which credential this client writes with -- queue name, stamp,
account identity, refresh and staleness."""

from __future__ import annotations
import os
import threading
import time
from typing import Any
from ..settings import settings as config_module
from ...foundation.safe_warn import safe_warn as _diagnostics
from ..session_marker import WIZARD_HINT
from ..delivery.outbox.drain.credentials import (
    CredentialSource,
    credential_fingerprint)


def _failure_kind(exc: BaseException) -> str:
    """An exception's type and HTTP status, never its text: a request error can
    carry the Authorization header (a non-ASCII token), and warnings reach the
    run's uploaded stderr."""
    status = getattr(exc, "status", None)
    return f"{type(exc).__name__}{f' {status}' if status else ''}"


class CredentialsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def _credential_queue_name(self, stamp: dict) -> str:
        """Which credential queue this client writes to: named by the key its
        ENVIRONMENT holds, so a kick from a shell with that environment finds
        it (`outbox_worker._env_fingerprints`). An ingest-only job
        (`PROBE_INGEST_TOKEN`, its personal token from the stored login) goes
        by its ingest token's fingerprint (#2041 round 4); otherwise the
        stamp's fingerprint."""
        token, ingest = self.settings.token, self.settings.ingest_token
        if (
            ingest
            and ingest == os.environ.get(config_module.INGEST_TOKEN_ENV)
            and not (token and token == os.environ.get(config_module.TOKEN_ENV))
        ):
            return credential_fingerprint(None, ingest) or stamp["fingerprint"]
        return stamp["fingerprint"]

    def _is_the_stored_login(self, context_name: str | None) -> bool:
        """Whether this client's credential IS the context's stored login, by
        value, however it arrived (a `PROBE_TOKEN` set to the same token, say),
        for the same server. Its writes then stay in the shared queue: every
        drainer, older ones included, sends them with that same token, and
        they keep their order against the stored login's own writes -- a close
        queued there cannot overtake them (#2041 round 3). They are stamped as
        the login (`_credential_stamp`) and this client re-reads the login
        after a refusal (`_credential_source`), so a re-login carries them on.
        The one test all three ask, so they cannot disagree."""
        try:
            stored = config_module.load_context(context_name)
        except Exception:  # noqa: BLE001 -- an unreadable config stores nothing
            return False
        return self._matches_login(stored, same_server=True)

    def _is_the_login(self, context_name: str | None) -> bool:
        """`_is_the_stored_login`, or a copy of it that a client of this process
        found when it started: after a re-login the copy no longer equals the
        login, and a later client of the same job (`probe.init()` in a sweep)
        must not then take it for a token of its own (`outbox_worker._COPIED_LOGINS`).
        Records the copy -- token and ingest token -- when it is one, so the
        workers this process starts never inherit it."""
        from ..delivery import outbox as outbox_worker

        token, ingest = self.settings.token, self.settings.ingest_token
        if self._is_the_stored_login(context_name):
            for fingerprint, var, value in (
                (credential_fingerprint(token, None), config_module.TOKEN_ENV, token),
                (credential_fingerprint(None, ingest), config_module.INGEST_TOKEN_ENV, ingest),
            ):
                if value and os.environ.get(var) == value:
                    outbox_worker.note_copied_login(fingerprint)
            return True
        if not token:
            return False
        fingerprint = credential_fingerprint(token, None)
        here = (self.settings.base_url or "").rstrip("/")
        if outbox_worker.is_copied_login(fingerprint):
            try:  # a copy of THIS server's login
                stored = config_module.load_context(context_name)
            except Exception:  # noqa: BLE001
                return False
            base = (stored.get(config_module.BASE_URL_KEY) or config_module.DEFAULT_BASE_URL).rstrip("/")
            return base == here
        # Another process of the job, after the re-login: this machine
        # recorded the token as its stored login for this server
        # (`journal.record_account`'s ``login_of``) AND as the account the
        # login stored now is -- never another context's or another person's.
        from ..delivery.outbox.drain.accounts import was_login

        try:
            identity = config_module.load_context(context_name).get("identity") or {}
        except Exception:  # noqa: BLE001
            identity = {}
        account = (identity.get("customer_id"), identity.get("user_id"))
        if all(account) and was_login(fingerprint, here, account=account):
            outbox_worker.note_copied_login(fingerprint)
            return True
        return False

    def _matches_login(self, stored: dict, *, same_server: bool) -> bool:
        token, ingest = self.settings.token, self.settings.ingest_token
        if not (token or ingest):
            return False
        if same_server:
            base = (stored.get(config_module.BASE_URL_KEY) or config_module.DEFAULT_BASE_URL).rstrip("/")
            if base != (self.settings.base_url or "").rstrip("/"):
                return False
        return (not token or token == stored.get("token")) and (
            not ingest or ingest == stored.get("ingest_token")
        )

    def _credential_stamp(self, context_name: str | None) -> dict | None:
        """What every op this client queues records about its credential:
        where it came from and a fingerprint of it, never the token (#2035).

        Told apart by VALUE, not by which argument carried it: a token equal to
        this context's stored login is that login, a `PROBE_TOKEN` copied from
        it included (a job told to export `config.json`'s token: its writes
        were stamped env and stranded by the next re-login, a customer's
        9,000 writes on 2026-10-23); any other token equal to this
        environment's ``PROBE_TOKEN`` is an env credential however it got here.
        Only a stored-login op may later go out with a NEW login of its context
        (a re-login); see `journal._settings_for_op`.
        """
        token, ingest = self.settings.token, self.settings.ingest_token
        fingerprint = credential_fingerprint(token, ingest)
        if fingerprint is None:
            return None
        env = {k: os.environ.get(k) for k in (config_module.TOKEN_ENV, config_module.INGEST_TOKEN_ENV)}
        try:
            stored = config_module.load_context(context_name)
        except Exception:  # noqa: BLE001 -- an unreadable config stores nothing
            stored = {}
        from_env = (token and token == env[config_module.TOKEN_ENV]) or (
            ingest and ingest == env[config_module.INGEST_TOKEN_ENV]
        )
        if from_env and not self._is_the_login(context_name):
            source = CredentialSource.ENV
        elif from_env or self._matches_login(stored, same_server=False):
            source = CredentialSource.CONFIG
        else:
            source = CredentialSource.CODE
        stamp = {"source": source.value, "fingerprint": fingerprint}
        # `/ingest` writes go out with the ingest token: named apart (#2041
        # re-review), so a drainer holding another ingest token cannot match.
        ingest_fingerprint = credential_fingerprint(None, ingest)
        if ingest_fingerprint:
            stamp["ingest_fingerprint"] = ingest_fingerprint
        # The account behind a stored login, as the sign-in recorded it -- only
        # when recorded for THIS token. A drainer may send a stored-login write
        # with a LATER login of the context only if that login is the same
        # account (`journal._settings_for_op`), and this is what it compares.
        recorded = stored.get("identity") if source == CredentialSource.CONFIG else None
        if (
            isinstance(recorded, dict)
            and recorded.get("fingerprint") == fingerprint
            and recorded.get("customer_id")
            and recorded.get("user_id")
        ):
            stamp["customer_id"] = str(recorded["customer_id"])
            stamp["user_id"] = str(recorded["user_id"])
        return stamp

    def _stamp_account(self, token: str | None, who: tuple[str, str], *, adopt: bool = False) -> None:
        """Record in this client's credential stamp which account ``token``
        belongs to, so the writes it queues from now on carry it (#2041 review).

        ``adopt`` is a refresh (plan 2.7) that verified ``token`` as the same
        account: the stamp moves to the new token's fingerprint. Otherwise the
        stamp must already name ``token``; a stamp for another credential is
        left alone. Replaces the stamp dict whole, never mutates it: an append
        on another thread may be serialising the old one."""
        context = self.journal.context
        stamp = context.get("principal") if isinstance(context, dict) else None
        if not isinstance(stamp, dict):
            return
        fingerprint = credential_fingerprint(token, self.settings.ingest_token)
        if fingerprint is None:
            return
        if adopt:
            self._credential_fingerprints.add(fingerprint)
        elif stamp.get("fingerprint") != fingerprint:
            return
        context["principal"] = {
            **stamp,
            "fingerprint": fingerprint,
            "customer_id": who[0],
            "user_id": who[1],
        }

    def _outbox_client_factory(self):
        """client_factory for ``journal.drain`` -- shared by ``flush()`` and
        the in-process exporter (F2).

        Ops pinned to THIS client's endpoint (or unpinned) replay over this
        client -- that keeps fake-transport tests and custom transports
        working. Ops pinned elsewhere resolve their own client from the named
        context, tokens fresh (5A): a context switch between enqueue and flush
        must never deliver to the wrong tenant.

        An op that records which credential queued it replays here only if
        that credential is this client's (#2035): the journal is shared by
        every process on the machine, and another job's op must go out as
        that job, never as whoever happens to flush.
        """

        def factory(context: dict | None):
            base = (context or {}).get("base_url")
            name = (context or {}).get("name")
            mine = (self.journal.context or {}).get("name")
            stamp = (context or {}).get("principal")
            if isinstance(stamp, dict):
                # The key the op's route is sent with (journal.op_credential).
                if (context or {}).get("route") == "ingest":
                    if stamp.get("ingest_fingerprint") not in self._ingest_fingerprints:
                        return None
                elif stamp.get("fingerprint") not in self._credential_fingerprints:
                    return None  # journal.drain looks for the credential that queued it
            # BOTH the endpoint and the context name must match before an op
            # replays over this client's credential: tenants can share one API
            # URL, and an op pinned to another context must resolve its own
            # stored token (red team: base_url alone re-opened wrong-principal
            # replay through the flush path).
            if (not base or base == self.settings.base_url) and (name is None or name == mine):
                return self
            return None  # journal.drain builds one from the pinned context

        return factory

    def refresh_credentials(self, *, refused: str | None = None) -> bool:
        """Re-read this client's API token after the API refused it (plan 2.7).

        A re-login on the box (the wizard's sign-in) revokes the old token, and a
        running job keeps the one it was built with: its heartbeat was refused
        from then on, the refusal was swallowed, and 15 minutes later the
        reaper marked a live run `crashed` (a false crash email for a 3h+ run).

        Only for an AMBIENT client, built from the environment or the stored
        login (`probe.init()`, a bare `Client()`): a token the caller passed is
        never second-guessed. It looks again ONLY where the token came from --
        `PROBE_TOKEN` for an environment token, this context's stored login
        for a stored one -- because the stored login on a shared box may be
        another person's. And it adopts a new token only after `GET /v1/me`
        with it names the SAME team and user as the credential this client
        started with; a login as anyone else is refused, with a warning, and
        the old token is kept.

        At most one re-read per 30 s, under a lock; no network unless the token
        actually changed. One warning when a new token is picked up; one, until
        the next success, when it cannot be.

        ``refused`` is the token the failed request carried: if another thread
        already swapped it, this answers True without reading anything.

        Returns True when a different token is now in use (retry once).
        """
        if not getattr(self, "_ambient_credentials", False):
            return False
        with self._credential_lock:
            if refused is not None and self.settings.token and self.settings.token != refused:
                return True
            now = time.monotonic()
            if now - self._credential_checked_at < self._CREDENTIAL_REFRESH_SECONDS:
                return False
            self._credential_checked_at = now
            candidate, why_not = self._reread_credential()
            if candidate is None or candidate == self.settings.token:
                self._warn_credential_stale(why_not or "there is no newer credential to read")
                return False
            if candidate == self._credential_rejected:
                return False  # already refused as another account's; said so then
            mismatch = self._different_account(candidate)
            if mismatch is not None:
                self._warn_credential_stale(mismatch)
                return False
            self.settings.token = candidate
            self._credential_stale_warned = False
            if self._credential_identity is not None:
                # Same account, verified above: later writes carry the new
                # token's fingerprint, and this client may replay the old one's.
                self._stamp_account(candidate, self._credential_identity, adopt=True)
        _diagnostics.warn(
            "probe: the API refused this process's credential (a re-login revokes the "
            "old one); picked up the new login for the same account and carried on"
        )
        return True

    def _reread_credential(self) -> tuple[str | None, str | None]:
        """(token, None), or (None, why) -- from the token's own source only."""
        if self._credential_source == "env":
            token = os.environ.get(config_module.TOKEN_ENV) or None
            if token is None or token == self.settings.token:
                return None, (
                    "its token comes from PROBE_TOKEN, which cannot change while the "
                    "process runs (a Kubernetes secret or an exported variable); restart "
                    "the job with a valid token"
                )
            return token, None
        if self._credential_source == "config":
            name = (self.journal.context or {}).get("name")
            try:
                stored = config_module.load_context(name)
            except Exception as exc:  # noqa: BLE001 -- an unreadable config is "nothing new"
                return None, f"the stored login could not be read ({_failure_kind(exc)})"
            base = (stored.get(config_module.BASE_URL_KEY) or config_module.DEFAULT_BASE_URL).rstrip("/")
            if base != self.settings.base_url.rstrip("/"):
                return None, f"the stored login is for {base}, not {self.settings.base_url}"
            token = stored.get("token") or None
            if token is None or token == self.settings.token:
                return None, f"there is no newer login to read; {WIZARD_HINT}"
            return token, None
        return None, None

    def _learn_identity(self) -> None:
        """Start the one background lookup of who this client's credential
        belongs to, if a refresh could ever be asked of it. Idempotent; called
        when a heartbeat or the exporter starts, never at construction."""
        if self._credential_source is None:
            return
        with self._credential_lock:
            if self._credential_identity_started:
                return
            self._credential_identity_started = True
        threading.Thread(
            target=self._remember_identity, name="probe-credential-identity", daemon=True
        ).start()

    def _remember_identity(self) -> None:
        """Record who the starting credential belongs to. Never raises."""
        self._credential_identity_started = True
        try:
            token = self.settings.token
            seen: dict = {}
            who = self._whoami(token, seen=seen)
            if who is not None:
                self._credential_identity = who
                self._stamp_account(token, who)
                from ..delivery.outbox.drain.credentials import _login_base_of
                from ..delivery.outbox.drain.accounts import record_account

                record_account(
                    credential_fingerprint(token, None),
                    who,
                    scopes=seen.get("scopes"),  # [] stays [] (no scope), absent stays None
                    # A login (stored, or copied into PROBE_TOKEN): any later
                    # process holding the copy is taken for the login too.
                    login_of=(
                        _login_base_of(self.journal.context, self.settings.base_url)
                        if self._credential_source == "config"
                        else None
                    ),
                )
        except Exception:  # noqa: BLE001 -- unknown stays None; a thread traceback would reach stderr
            pass
        finally:
            self._credential_identity_ready.set()

    def _whoami(self, token: str | None, *, seen: dict | None = None) -> tuple[str, str] | None:
        """(customer_id, user_id) that ``token`` belongs to: ONE attempt with a
        5 s timeout and no retries (the flush() or beat waiting on it must not
        sit through the transport's full retry budget). None when unknown.
        ``seen``, when given, gets the token's ``scopes`` when `/v1/me` named
        them (an empty list included). Raises what the request raised."""
        import copy

        probe_transport = copy.copy(self.transport)
        probe_transport.settings = copy.copy(self.settings)
        probe_transport.settings.token = token
        probe_transport.max_retries = 0
        response = probe_transport.request("GET", "/v1/me", idempotent=True, timeout=5.0)
        who = response.json() if response.content else {}
        if seen is not None and isinstance(who.get("scopes"), list):
            seen["scopes"] = [str(s) for s in who["scopes"]]
        if who.get("customer_id") and who.get("user_id"):
            return str(who["customer_id"]), str(who["user_id"])
        return None

    def _different_account(self, candidate: str) -> str | None:
        """None when ``candidate`` belongs to the account this client started
        with, else why it may not be adopted. Asks `/v1/me` WITH the candidate."""
        started_as = None
        if self._credential_identity_started:
            self._credential_identity_ready.wait(timeout=5.0)
            started_as = self._credential_identity
        if started_as is None:
            # Looked up too late (the token was already dead), or never: what
            # this machine recorded for the token when it still worked -- one
            # token is one account (`journal.record_account`).
            from ..delivery.outbox.drain.accounts import recorded_account

            started_as = recorded_account(credential_fingerprint(self.settings.token, None))
        if started_as is None:
            return "the account the process started as is unknown, so a new login cannot be matched to it"
        try:
            now_as = self._whoami(candidate)
        except Exception as exc:  # noqa: BLE001 -- unverifiable is refused
            return f"the new login could not be verified ({_failure_kind(exc)})"
        if now_as != started_as:
            if now_as is not None:
                self._credential_rejected = candidate
            return (
                "the new login on this machine belongs to a different account; this "
                "process keeps writing as the one it started with"
            )
        return None

    def _own_credential_refusal(self, report: Any) -> bool:
        """Did a drain stop because THIS client's credential was refused?

        Not a 403 naming a missing scope (the key still works), and not an op
        pinned to another context in the shared outbox (not our key at all)."""
        from ..settings.key_refusal import credential_refused

        if not getattr(report, "auth_blocked", False):
            return False
        refusals = getattr(report, "auth_refusals", None) or [
            {
                "status": getattr(report, "auth_status", None),
                "message": getattr(report, "auth_message", None),
                "context": getattr(report, "auth_context", None),
            }
        ]
        mine = (self.journal.context or {}).get("name")
        for refusal in refusals:
            if not credential_refused(refusal.get("status"), refusal.get("message")):
                continue
            context = refusal.get("context") or {}
            stamp = context.get("principal")
            if isinstance(stamp, dict) and stamp.get("fingerprint"):
                # The write names the credential that queued it (#2041): ours
                # only if it is one this client has written with. Another
                # login's 401 on a shared machine is not our key being refused.
                refused = refusal.get("fingerprint") or stamp["fingerprint"]
                if refused in self._credential_fingerprints | self._ingest_fingerprints:
                    return True
                continue
            base = context.get("base_url")
            name = context.get("name")
            if (not base or base == self.settings.base_url) and (name is None or name == mine):
                return True
        return False

    def _warn_credential_stale(self, why: str) -> None:
        if self._credential_stale_warned:
            return
        self._credential_stale_warned = True
        _diagnostics.warn(
            f"probe: the API refused this process's credential and {why}. Heartbeats "
            "and delivery stay refused; the run is marked crashed if this lasts 15 minutes."
        )
