"""Repository-backed initial-delivery claims and staged escalation reservations."""

from __future__ import annotations

import base64
import json
import re
from datetime import UTC, datetime, timedelta
from typing import Any, cast

from agentic_devtools.cli.ci.reconciliation.queue_store import (
    GitHubVariableBackingStore,
    _is_conflict_error,
    _is_not_found_error,
)
from agentic_devtools.cli.ci.retry import retry_with_backoff
from agentic_devtools.cli.shared.retry import RetryableError

_ESCALATION_RESERVATION_TTL = timedelta(minutes=15)


class InitialDeliveryClaims:
    """One shared claim per original delivery and purpose.

    Recovery and delivery claims are immutable. Escalation reservations use the
    GitHub contents blob SHA for owner-checked compare-and-swap stage changes.
    Never delete claims or retry an ambiguous create. The existing
    ``ai-pr-loop-state`` branch must already be initialized.
    """

    def __init__(self, repo: str) -> None:
        if (
            not isinstance(repo, str)
            or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*", repo) is None
        ):
            raise ValueError("repo must be a canonical owner/name")
        self._repo = repo

    @staticmethod
    @retry_with_backoff(max_retries=0)
    def _api(endpoint: str, *, method: str = "GET", body: dict[str, Any] | None = None) -> str:
        """Use the existing repository-state credential boundary without retries."""
        return GitHubVariableBackingStore._api(endpoint, method=method, body=body)

    def _endpoint(self, pr: int, key: str, purpose: str) -> str:
        if (
            isinstance(pr, bool)
            or not isinstance(pr, int)
            or pr <= 0
            or not isinstance(key, str)
            or re.fullmatch(r"[0-9a-f]{64}", key) is None
            or purpose not in {"recovery", "escalation", "delivered"}
        ):
            raise ValueError("invalid initial-delivery claim identity")
        return f"/repos/{self._repo}/contents/.agdt/initial-delivery/{pr}/{key}/{purpose}.json"

    def _read_versioned(self, pr: int, key: str, purpose: str) -> tuple[dict[str, Any], str] | None:
        """Read a claim and its blob SHA for narrowly scoped compare-and-swap updates."""
        try:
            raw = self._api(f"{self._endpoint(pr, key, purpose)}?ref=ai-pr-loop-state")
        except RuntimeError as exc:
            if _is_not_found_error(exc):
                return None
            raise
        metadata = json.loads(raw)
        content = base64.b64decode(metadata["content"].replace("\n", ""), validate=True)
        if len(content) > 16_000:
            raise ValueError("initial-delivery claim exceeds bounded size")
        record = json.loads(content)
        if not isinstance(record, dict) or not isinstance(record.get("created_at"), str):
            raise ValueError("malformed initial-delivery claim")
        now = datetime.now(UTC)
        created = datetime.fromisoformat(record["created_at"])
        if created.tzinfo is None or created > now:
            raise ValueError("invalid initial-delivery claim timestamp")
        if "updated_at" in record:
            updated_at = record["updated_at"]
            if not isinstance(updated_at, str):
                raise ValueError("invalid initial-delivery claim timestamp")
            updated = datetime.fromisoformat(updated_at)
            if updated.tzinfo is None or updated < created or updated > now:
                raise ValueError("invalid initial-delivery claim timestamp")
        sha = metadata.get("sha")
        if not isinstance(sha, str) or not sha:
            raise ValueError("malformed initial-delivery claim")
        return record, sha

    def read(self, pr: int, key: str, purpose: str) -> dict[str, Any] | None:
        """Read a claim; malformed/unavailable data is never treated as absence."""
        versioned = self._read_versioned(pr, key, purpose)
        return versioned[0] if versioned is not None else None

    def claim(self, pr: int, key: str, purpose: str, evidence: dict[str, Any]) -> bool:
        """Create once before mutation; only a confirmed create authorizes work."""
        endpoint = self._endpoint(pr, key, purpose)
        record = {**evidence, "created_at": datetime.now(UTC).isoformat()}
        content = json.dumps(record).encode()
        if len(content) > 16_000:
            raise ValueError("initial-delivery claim exceeds bounded size")
        try:
            self._api(
                endpoint,
                method="PUT",
                body={
                    "branch": "ai-pr-loop-state",
                    "message": f"chore(#{pr}): claim initial-delivery {purpose}\n\n#{pr}",
                    "content": base64.b64encode(content).decode("ascii"),
                },
            )
        except RuntimeError, RetryableError:
            if self.read(pr, key, purpose) is not None:
                return False
            raise
        return True

    def _reserve_escalation(self, pr: int, key: str, evidence: dict[str, Any], owner_token: str) -> bool:
        """Create or CAS-acquire one owner's escalation reservation."""
        if not isinstance(owner_token, str) or re.fullmatch(r"[0-9a-f]{32}", owner_token) is None:
            raise ValueError("invalid escalation reservation owner")
        reservation = {**evidence, "stage": "reserved", "owner_token": owner_token}
        if self.claim(pr, key, "escalation", reservation):
            return True
        existing = self._read_versioned(pr, key, "escalation")
        if existing is None:
            return False
        record, _sha = existing
        if record.get("stage") == "reserved" and record.get("owner_token") == owner_token:
            return True
        if record.get("stage") == "reserved":
            acquired = datetime.fromisoformat(record.get("updated_at", record["created_at"]))
            if datetime.now(UTC) - acquired < _ESCALATION_RESERVATION_TTL:
                return False
            current_owner = record.get("owner_token")
            if not isinstance(current_owner, str) or re.fullmatch(r"[0-9a-f]{32}", current_owner) is None:
                return False
            return self._transition_escalation(
                pr,
                key,
                current_owner,
                "reserved",
                "reserved",
                next_owner_token=owner_token,
            )
        if record.get("stage") != "retryable":
            return False
        current_owner = record.get("owner_token")
        if not isinstance(current_owner, str) or re.fullmatch(r"[0-9a-f]{32}", current_owner) is None:
            return False
        return self._transition_escalation(
            pr,
            key,
            current_owner,
            "retryable",
            "reserved",
            next_owner_token=owner_token,
        )

    def _transition_escalation(
        self,
        pr: int,
        key: str,
        owner_token: str,
        expected_stage: str,
        next_stage: str,
        *,
        next_owner_token: str | None = None,
    ) -> bool:
        """CAS an escalation stage; ambiguous writes require exact read-back verification."""
        allowed = {
            ("reserved", "retryable"),
            ("reserved", "reserved"),
            ("retryable", "reserved"),
            ("reserved", "attempted"),
        }
        if (
            (expected_stage, next_stage) not in allowed
            or not isinstance(owner_token, str)
            or re.fullmatch(r"[0-9a-f]{32}", owner_token) is None
            or (
                next_owner_token is not None
                and (not isinstance(next_owner_token, str) or re.fullmatch(r"[0-9a-f]{32}", next_owner_token) is None)
            )
            or (
                (expected_stage, next_stage) in {("retryable", "reserved"), ("reserved", "reserved")}
                and next_owner_token is None
            )
            or (
                (expected_stage, next_stage) not in {("retryable", "reserved"), ("reserved", "reserved")}
                and next_owner_token is not None
            )
        ):
            raise ValueError("invalid escalation reservation transition")
        versioned = self._read_versioned(pr, key, "escalation")
        if versioned is None:
            return False
        record, sha = versioned
        if record.get("stage") != expected_stage or record.get("owner_token") != owner_token:
            return False
        updated = dict(record)
        updated["stage"] = next_stage
        if next_owner_token is not None:
            updated["owner_token"] = next_owner_token
        updated["updated_at"] = datetime.now(UTC).isoformat()
        content = json.dumps(updated).encode()
        if len(content) > 16_000:
            raise ValueError("initial-delivery claim exceeds bounded size")
        try:
            self._api(
                self._endpoint(pr, key, "escalation"),
                method="PUT",
                body={
                    "branch": "ai-pr-loop-state",
                    "message": f"chore(#{pr}): advance initial-delivery escalation\n\n#{pr}",
                    "content": base64.b64encode(content).decode("ascii"),
                    "sha": sha,
                },
            )
        except (RuntimeError, RetryableError) as exc:
            if _is_conflict_error(cast(RuntimeError, exc)):
                return False
            observed = self._read_versioned(pr, key, "escalation")
            if observed is not None and observed[0] == updated:
                return True
            if observed is not None and observed[0] == record:
                return False
            raise
        return True
