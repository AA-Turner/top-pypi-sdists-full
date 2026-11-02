"""Per-run selection of validated GitHub credentials for read-only API calls."""

from __future__ import annotations

import json
import logging
import re
import time
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from math import isfinite
from typing import Any

from agentic_devtools.cli.ci.cooldown import CooldownRecord
from agentic_devtools.cli.ci.retry import RetryableError
from agentic_devtools.cli.shared.retry import (
    DEFAULT_RATE_LIMIT_FALLBACK_DELAY,
    DEFAULT_RATE_LIMIT_MAX_DELAY,
    DEFAULT_RATE_LIMIT_SAFETY_MARGIN,
    calculate_rate_limit_delay,
)

logger = logging.getLogger(__name__)

_POOL_SECRET_SUFFIX = "_SWICA_CLASSIC_REPO_WORKFLOW_PAT"
_HTTP_STATUS_RE = re.compile(r"\bHTTP\s+(\d{3})\b", re.IGNORECASE)


class _ReadTokenPoolDeadlineExceeded(RuntimeError):
    """Private signal that an inventory-scoped request exhausted its deadline."""


@dataclass(frozen=True)
class ReadCredential:
    """A validated read credential identified only by its Actions secret name."""

    secret_name: str
    token: str
    login: str


class ReadTokenPool:
    """Discover, validate, and select per-run credentials for GitHub reads."""

    def __init__(
        self,
        *,
        repo: str,
        secrets_json: str | None,
        default_token: str = "",
        default_identity: str = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
        request: Callable[[str, str, str], tuple[str, int | None]],
        active_cooldowns: Iterable[str] | Mapping[str, float | None] = (),
        on_rate_limit: Callable[[str, RetryableError], float | None],
    ) -> None:
        if not isinstance(repo, str) or len(repo.split("/")) != 2 or not all(repo.split("/")):
            raise ValueError("repo must be in owner/repo form")
        if not isinstance(default_identity, str) or not default_identity.strip():
            raise ValueError("default_identity must be a non-empty logical identity")
        self.repo = repo
        self.default_token = default_token.strip() if isinstance(default_token, str) else ""
        self.default_identity = default_identity.strip()
        self._request = request
        self._on_rate_limit = on_rate_limit
        self._active_cooldowns: set[str] = set()
        self._cooldown_deadlines: dict[str, float] = {}
        self._current_run_cooldowns: dict[str, CooldownRecord] = {}
        if isinstance(active_cooldowns, Mapping):
            for name, deadline in active_cooldowns.items():
                if not isinstance(name, str):
                    continue
                self._active_cooldowns.add(name)
                if isinstance(deadline, (int, float)) and not isinstance(deadline, bool) and isfinite(deadline):
                    self._cooldown_deadlines[name] = float(deadline)
        else:
            self._active_cooldowns = {name for name in active_cooldowns if isinstance(name, str)}
        self._rate_limited: set[str] = set()
        self._budgets: dict[str, dict[str, int | None]] = {}
        self._logins_by_token: dict[str, str] = {}
        self._default_login: str | None = None
        self._default_login_attempted = False
        self._candidates: list[ReadCredential] = []
        self._configured_pool_identities: set[str] = set()
        self._excluded_pool_identities: set[str] = set()
        self._tie_cursor = {"rest": 0, "graphql": 0}
        self._sampled_unknown_budgets: dict[str, set[str]] = {"rest": set(), "graphql": set()}
        self._secret_entries_list = self._secret_entries(secrets_json)
        self._configured_pool_identities = {name for name, _ in self._secret_entries_list}
        self._load_candidates(self._secret_entries_list)

    @property
    def candidate_names(self) -> tuple[str, ...]:
        """Return the validated pool identities in deterministic order."""
        self._expire_cooldowns()
        return tuple(credential.secret_name for credential in self._candidates)

    @property
    def has_available_credentials(self) -> bool:
        """Return whether at least one validated identity is outside cooldown."""
        self._expire_cooldowns()
        return any(
            credential.secret_name not in self._active_cooldowns and credential.secret_name not in self._rate_limited
            for credential in self._candidates
        )

    @property
    def blocking_cooldown_identities(self) -> tuple[str, ...]:
        """Return identities whose active cooldown must stop loop scheduling."""
        self._expire_cooldowns()
        if self.default_is_active:
            return (self.default_identity,)
        if self.default_token:
            return ()
        eligible = self._configured_pool_identities - self._excluded_pool_identities
        if eligible and eligible <= self._active_cooldowns:
            return tuple(sorted(eligible))
        return ()

    @property
    def default_is_active(self) -> bool:
        """Return whether DEFAULT has a persisted or current-run rate-limit cooldown."""
        self._expire_cooldowns()
        return self.default_identity in self._active_cooldowns or self.default_identity in self._rate_limited

    def active_cooldown_for(
        self,
        identities: Iterable[str],
        *,
        now: float | None = None,
    ) -> tuple[str, CooldownRecord] | None:
        """Return the longest active cooldown recorded in this process for selected identities."""
        self._expire_cooldowns()
        current = time.time() if now is None else now
        active = [
            (f"github:{identity}", record)
            for identity in identities
            if isinstance(identity, str)
            and (record := self._current_run_cooldowns.get(identity)) is not None
            and record.resume_at > current
        ]
        return max(active, key=lambda item: item[1].resume_at, default=None)

    def recognizes_token(self, token: str | None) -> bool:
        """Return whether a token belongs to the validated alternate pool."""
        return isinstance(token, str) and any(credential.token == token for credential in self._candidates)

    def select(
        self,
        resource: str,
        *,
        excluded: Iterable[str] = (),
    ) -> ReadCredential | None:
        """Sample unmeasured budgets before selecting the highest known budget."""
        self._expire_cooldowns()
        self._validate_resource(resource)
        excluded_names = {name for name in excluded if isinstance(name, str)}
        available = [
            credential
            for credential in self._candidates
            if credential.secret_name not in self._active_cooldowns
            and credential.secret_name not in self._rate_limited
            and credential.secret_name not in excluded_names
        ]
        if not available:
            return None

        untried = [
            credential
            for credential in available
            if self._budgets[credential.secret_name][resource] is None
            and credential.secret_name not in self._sampled_unknown_budgets[resource]
        ]
        if untried:
            tied = untried
        else:
            known: list[int] = []
            for credential in available:
                budget = self._budgets[credential.secret_name][resource]
                if budget is not None:
                    known.append(budget)
            if not known:
                tied = available
            else:
                highest = max(known)
                tied = [
                    credential for credential in available if self._budgets[credential.secret_name][resource] == highest
                ]
        selected = self._next_tied(resource, tied)
        if self._budgets[selected.secret_name][resource] is None:
            self._sampled_unknown_budgets[resource].add(selected.secret_name)
        return selected

    def record_remaining(self, identity: str, resource: str, remaining: int | None) -> None:
        """Update one resource's last-known budget without erasing it on missing headers."""
        self._validate_resource(resource)
        budgets = self._budgets.setdefault(identity, {"rest": None, "graphql": None})
        if remaining is None:
            return
        if not isinstance(remaining, int) or isinstance(remaining, bool) or remaining < 0:
            return
        budgets[resource] = remaining

    def mark_rate_limited(self, identity: str, error: RetryableError) -> None:
        """Exclude a rate-limited identity for this run and persist its cooldown."""
        self._rate_limited.add(identity)
        self._active_cooldowns.add(identity)
        now = time.time()
        delay = calculate_rate_limit_delay(
            retry_after_seconds=error.retry_after,
            reset_timestamp=error.reset_timestamp,
            now=now,
            fallback_delay=DEFAULT_RATE_LIMIT_FALLBACK_DELAY,
            safety_margin=DEFAULT_RATE_LIMIT_SAFETY_MARGIN,
            max_delay=DEFAULT_RATE_LIMIT_MAX_DELAY,
        )
        record = CooldownRecord(resume_at=delay.resume_at, source=delay.source, updated_at=now)
        self._current_run_cooldowns[identity] = record
        self._cooldown_deadlines[identity] = record.resume_at
        deadline = self._on_rate_limit(identity, error)
        if isinstance(deadline, (int, float)) and not isinstance(deadline, bool) and isfinite(deadline):
            effective_deadline = float(deadline)
            self._cooldown_deadlines[identity] = effective_deadline
            self._current_run_cooldowns[identity] = CooldownRecord(
                resume_at=effective_deadline,
                source=record.source,
                updated_at=now,
            )

    def _secret_entries(self, secrets_json: str | None) -> list[tuple[str, str]]:
        if not secrets_json:
            return []
        try:
            secrets: Any = json.loads(secrets_json)
        except TypeError, json.JSONDecodeError:
            logger.warning("Ignoring malformed GitHub Actions secrets JSON for read-token discovery")
            return []
        if not isinstance(secrets, dict):
            logger.warning("Ignoring non-object GitHub Actions secrets JSON for read-token discovery")
            return []
        entries = [
            (name, value.strip())
            for name, value in secrets.items()
            if isinstance(name, str) and name.endswith(_POOL_SECRET_SUFFIX) and isinstance(value, str) and value.strip()
        ]
        return sorted(entries)

    def _load_candidates(self, entries: list[tuple[str, str]]) -> None:
        if not entries:
            return
        default_login = self._resolve_default_login()
        seen_logins = {credential.login.casefold() for credential in self._candidates}
        if default_login:
            seen_logins.add(default_login.casefold())
        for secret_name, token in entries:
            if (
                secret_name in self._active_cooldowns
                or secret_name in self._rate_limited
                or secret_name in self._excluded_pool_identities
                or any(credential.secret_name == secret_name for credential in self._candidates)
            ):
                continue
            if token == self.default_token and self.default_token:
                self._excluded_pool_identities.add(secret_name)
                logger.info("Read credential %s matches DEFAULT's token; excluding it", secret_name)
                continue
            if self.default_token and not default_login:
                logger.warning(
                    "Read credential %s is unavailable because DEFAULT identity could not be verified",
                    secret_name,
                )
                continue
            try:
                login = self._resolve_login(token, secret_name)
            except RetryableError as exc:
                if exc.is_rate_limit:
                    self._record_validation_rate_limit(secret_name, exc, "identity lookup")
                else:
                    self._warn_candidate_failure(secret_name, "identity lookup", exc)
                    self._excluded_pool_identities.add(secret_name)
                continue
            except Exception as exc:
                self._warn_candidate_failure(secret_name, "identity lookup", exc)
                self._excluded_pool_identities.add(secret_name)
                continue
            normalized_login = login.casefold()
            if normalized_login in seen_logins:
                logger.info("Read credential %s duplicates an existing GitHub identity; excluding it", secret_name)
                self._excluded_pool_identities.add(secret_name)
                continue
            try:
                _, remaining = self._request(f"/repos/{self.repo}", token, secret_name)
            except RetryableError as exc:
                if exc.is_rate_limit:
                    seen_logins.add(normalized_login)
                    self._record_validation_rate_limit(secret_name, exc, "repository access validation")
                else:
                    self._warn_candidate_failure(secret_name, "repository access validation", exc)
                    self._excluded_pool_identities.add(secret_name)
                continue
            except Exception as exc:
                self._warn_candidate_failure(secret_name, "repository access validation", exc)
                self._excluded_pool_identities.add(secret_name)
                continue
            self.record_remaining(secret_name, "rest", remaining)
            seen_logins.add(normalized_login)
            self._candidates.append(ReadCredential(secret_name, token, login))
        self._candidates.sort(key=lambda credential: credential.secret_name)

    def _resolve_default_login(self) -> str:
        if not self.default_token or self.default_identity in self._active_cooldowns:
            return ""
        if self._default_login_attempted:
            return self._default_login or ""
        self._default_login_attempted = True
        try:
            self._default_login = self._resolve_login(self.default_token, self.default_identity)
        except RetryableError as exc:
            self._record_validation_rate_limit(self.default_identity, exc, "identity lookup")
        except Exception as exc:
            self._warn_candidate_failure(self.default_identity, "identity lookup", exc)
        return self._default_login or ""

    def _expire_cooldowns(self) -> None:
        now = time.time()
        expired = {identity for identity, deadline in self._cooldown_deadlines.items() if deadline <= now}
        if not expired:
            return
        expired_deadlines = {identity: self._cooldown_deadlines[identity] for identity in expired}
        expired_rate_limited = expired & self._rate_limited
        for identity in expired:
            self._cooldown_deadlines.pop(identity, None)
            self._current_run_cooldowns.pop(identity, None)
            self._active_cooldowns.discard(identity)
            self._rate_limited.discard(identity)
            self._budgets[identity] = {"rest": None, "graphql": None}
            for sampled in self._sampled_unknown_budgets.values():
                sampled.discard(identity)
        if self.default_identity in expired:
            self._default_login = None
            self._default_login_attempted = False
            expired_entries = self._secret_entries_list
        else:
            expired_entries = [(name, token) for name, token in self._secret_entries_list if name in expired]
        try:
            self._load_candidates(expired_entries)
        except _ReadTokenPoolDeadlineExceeded:
            for identity, deadline in expired_deadlines.items():
                self._cooldown_deadlines.setdefault(identity, deadline)
            self._active_cooldowns.update(expired)
            self._rate_limited.update(expired_rate_limited)
            raise

    def _resolve_login(self, token: str, identity: str) -> str:
        if token in self._logins_by_token:
            return self._logins_by_token[token]
        response, remaining = self._request("/user", token, identity)
        self.record_remaining(identity, "rest", remaining)
        try:
            payload: Any = json.loads(response)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ValueError("GitHub identity response was not valid JSON") from exc
        if not isinstance(payload, dict):
            raise ValueError("GitHub identity response was not an object")
        login = payload.get("login")
        if not isinstance(login, str) or not login.strip():
            raise ValueError("GitHub identity response did not contain a login")
        normalized_login = login.strip()
        self._logins_by_token[token] = normalized_login
        return normalized_login

    def _record_validation_rate_limit(self, identity: str, error: RetryableError, stage: str) -> None:
        if error.is_rate_limit:
            self.mark_rate_limited(identity, error)
        else:
            self._warn_candidate_failure(identity, stage, error)

    def _warn_candidate_failure(self, identity: str, stage: str, error: Exception) -> None:
        if isinstance(error, _ReadTokenPoolDeadlineExceeded):
            raise error.with_traceback(error.__traceback__)
        status = self._http_status(str(error))
        if status in {401, 403, 404}:
            logger.warning("Read credential %s failed %s (HTTP %d); excluding it", identity, stage, status)
            return
        logger.warning("Read credential %s failed %s (%s); excluding it", identity, stage, type(error).__name__)

    def _next_tied(self, resource: str, tied: list[ReadCredential]) -> ReadCredential:
        ordered_names = [credential.secret_name for credential in self._candidates]
        start = self._tie_cursor[resource]
        for offset in range(len(ordered_names)):
            index = (start + offset) % len(ordered_names)
            name = ordered_names[index]
            for credential in tied:
                if credential.secret_name == name:
                    self._tie_cursor[resource] = (index + 1) % len(ordered_names)
                    return credential
        return tied[0]

    @staticmethod
    def _http_status(message: str) -> int | None:
        match = _HTTP_STATUS_RE.search(message)
        return int(match.group(1)) if match else None

    @staticmethod
    def _validate_resource(resource: str) -> None:
        if resource not in {"rest", "graphql"}:
            raise ValueError("resource must be 'rest' or 'graphql'")
