"""Create-only GitHub contents claims remain consumed across workers."""

import base64
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime, timedelta
from threading import Lock
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.initial_delivery_claims import _ESCALATION_RESERVATION_TTL, InitialDeliveryClaims
from agentic_devtools.cli.shared.retry import ProviderRateLimitError, RetryableError

MODULE = "agentic_devtools.cli.ci.initial_delivery_claims"
KEY = "a" * 64


class TestInitialDeliveryClaims:
    def test_concurrent_and_restarted_workers_have_exactly_one_winner(self):
        documents = {}
        lock = Lock()

        def api(endpoint, *, method="GET", body=None, **kwargs):
            path = endpoint.split("?")[0]
            with lock:
                if method == "PUT":
                    current = documents.get(path)
                    if current is not None and body.get("sha") != hashlib.sha256(current.encode()).hexdigest():
                        raise RuntimeError("HTTP 409 blob SHA conflict")
                    if current is None and body.get("sha") is not None:
                        raise RuntimeError("HTTP 409 blob SHA conflict")
                    documents[path] = body["content"]
                    return "{}"
                if path not in documents:
                    raise RuntimeError("HTTP 404")
                return json.dumps(
                    {
                        "content": documents[path],
                        "sha": hashlib.sha256(documents[path].encode()).hexdigest(),
                    }
                )

        with patch(f"{MODULE}.InitialDeliveryClaims._api", side_effect=api):
            with ThreadPoolExecutor(max_workers=8) as pool:
                results = list(
                    pool.map(
                        lambda _: InitialDeliveryClaims("org/repo").claim(12, KEY, "recovery", {"head": "initial"}),
                        range(12),
                    )
                )
            assert sum(results) == 1
            restarted = InitialDeliveryClaims("org/repo")
            assert restarted.claim(12, KEY, "recovery", {}) is False
            assert restarted.read(12, KEY, "recovery")["head"] == "initial"
            assert restarted.claim(12, KEY, "escalation", {"reason": "unknown"}) is True

    def test_escalation_reservations_are_owner_safe_across_cas_contenders(self):
        documents = {}
        lock = Lock()

        def api(endpoint, *, method="GET", body=None):
            path = endpoint.split("?")[0]
            with lock:
                current = documents.get(path)
                if method == "PUT":
                    current_sha = hashlib.sha256(current.encode()).hexdigest() if current is not None else None
                    if body.get("sha") != current_sha:
                        raise RuntimeError("HTTP 409 blob SHA conflict")
                    documents[path] = body["content"]
                    return "{}"
                if current is None:
                    raise RuntimeError("HTTP 404")
                return json.dumps({"content": current, "sha": hashlib.sha256(current.encode()).hexdigest()})

        store = InitialDeliveryClaims("org/repo")
        owner_a, owner_b, owner_c = "a" * 32, "b" * 32, "c" * 32
        with patch(f"{MODULE}.InitialDeliveryClaims._api", side_effect=api):
            assert store._reserve_escalation(12, KEY, {}, owner_a)
            assert store._transition_escalation(12, KEY, owner_a, "reserved", "retryable")
            with ThreadPoolExecutor(max_workers=2) as pool:
                results = list(
                    pool.map(
                        lambda owner: store._reserve_escalation(12, KEY, {}, owner),
                        (owner_b, owner_c),
                    )
                )
            assert sum(results) == 1
            winner = owner_b if results[0] else owner_c
            assert not store._transition_escalation(12, KEY, owner_a, "reserved", "retryable")
            assert store._transition_escalation(12, KEY, winner, "reserved", "attempted")
            assert not store._reserve_escalation(12, KEY, {}, owner_a)
            assert store.read(12, KEY, "escalation")["stage"] == "attempted"

    def test_only_expired_reserved_escalations_can_be_reclaimed_by_one_owner(self):
        documents = {}
        lock = Lock()

        def api(endpoint, *, method="GET", body=None):
            path = endpoint.split("?")[0]
            with lock:
                current = documents.get(path)
                if method == "PUT":
                    current_sha = hashlib.sha256(current.encode()).hexdigest() if current is not None else None
                    if body.get("sha") != current_sha:
                        raise RuntimeError("HTTP 409 blob SHA conflict")
                    documents[path] = body["content"]
                    return "{}"
                if current is None:
                    raise RuntimeError("HTTP 404")
                return json.dumps({"content": current, "sha": hashlib.sha256(current.encode()).hexdigest()})

        store = InitialDeliveryClaims("org/repo")
        old_owner = "a" * 32
        contenders = [f"{value:032x}" for value in range(1, 9)]
        path = store._endpoint(12, KEY, "escalation")

        def replace_record(**updates):
            record = json.loads(base64.b64decode(documents[path]))
            record.update(updates)
            documents[path] = base64.b64encode(json.dumps(record).encode()).decode()

        with patch(f"{MODULE}.InitialDeliveryClaims._api", side_effect=api):
            assert store._reserve_escalation(12, KEY, {}, old_owner)
            replace_record(
                created_at=(datetime.now(UTC) - _ESCALATION_RESERVATION_TTL - timedelta(seconds=1)).isoformat(),
                updated_at=datetime.now(UTC).isoformat(),
            )
            assert not store._reserve_escalation(12, KEY, {}, contenders[0])
            replace_record(
                updated_at=(datetime.now(UTC) - _ESCALATION_RESERVATION_TTL - timedelta(seconds=1)).isoformat()
            )

            with ThreadPoolExecutor(max_workers=len(contenders)) as pool:
                results = list(pool.map(lambda owner: store._reserve_escalation(12, KEY, {}, owner), contenders))

            assert sum(results) == 1
            winner = contenders[results.index(True)]
            assert not store._transition_escalation(12, KEY, old_owner, "reserved", "attempted")
            for owner in contenders:
                if owner != winner:
                    assert not store._transition_escalation(12, KEY, owner, "reserved", "attempted")
            assert store._transition_escalation(12, KEY, winner, "reserved", "attempted")
            replace_record(
                updated_at=(datetime.now(UTC) - _ESCALATION_RESERVATION_TTL - timedelta(seconds=1)).isoformat()
            )
            assert not store._reserve_escalation(12, KEY, {}, old_owner)
            assert store.read(12, KEY, "escalation")["stage"] == "attempted"

    def test_escalation_reservation_reuses_its_owner_and_fails_closed_on_missing_state(self):
        store = InitialDeliveryClaims("org/repo")
        owner = "a" * 32
        with (
            patch.object(store, "claim", return_value=False),
            patch.object(store, "_read_versioned", return_value=({"stage": "reserved", "owner_token": owner}, "sha")),
        ):
            assert store._reserve_escalation(12, KEY, {}, owner)
        with (
            patch.object(store, "claim", return_value=False),
            patch.object(store, "_read_versioned", return_value=None),
        ):
            assert not store._reserve_escalation(12, KEY, {}, owner)
        with (
            patch.object(store, "claim", return_value=False),
            patch.object(
                store, "_read_versioned", return_value=({"stage": "retryable", "owner_token": "invalid"}, "sha")
            ),
        ):
            assert not store._reserve_escalation(12, KEY, {}, owner)
        with (
            patch.object(store, "claim", return_value=False),
            patch.object(
                store,
                "_read_versioned",
                return_value=(
                    {
                        "stage": "reserved",
                        "owner_token": "invalid",
                        "created_at": (
                            datetime.now(UTC) - _ESCALATION_RESERVATION_TTL - timedelta(seconds=1)
                        ).isoformat(),
                    },
                    "sha",
                ),
            ),
        ):
            assert not store._reserve_escalation(12, KEY, {}, owner)

    @pytest.mark.parametrize("owner", ["", "A" * 32, None])
    def test_escalation_reservation_rejects_invalid_owner(self, owner):
        with pytest.raises(ValueError, match="owner"):
            InitialDeliveryClaims("org/repo")._reserve_escalation(12, KEY, {}, owner)

    @pytest.mark.parametrize(
        ("expected", "next_stage", "owner", "next_owner"),
        [
            ("attempted", "retryable", "a" * 32, None),
            ("reserved", "attempted", "invalid", None),
            ("reserved", "reserved", "a" * 32, None),
            ("retryable", "reserved", "a" * 32, None),
            ("reserved", "retryable", "a" * 32, "b" * 32),
            ("retryable", "reserved", "a" * 32, "invalid"),
        ],
    )
    def test_escalation_transition_rejects_invalid_stage_or_ownership(self, expected, next_stage, owner, next_owner):
        with pytest.raises(ValueError, match="transition"):
            InitialDeliveryClaims("org/repo")._transition_escalation(
                12, KEY, owner, expected, next_stage, next_owner_token=next_owner
            )

    def test_escalation_transition_fails_closed_on_missing_or_changed_state(self):
        store = InitialDeliveryClaims("org/repo")
        with patch.object(store, "_read_versioned", return_value=None):
            assert not store._transition_escalation(12, KEY, "a" * 32, "reserved", "attempted")

    @pytest.mark.parametrize("error", [RuntimeError("response lost"), RetryableError("response lost")])
    def test_escalation_transition_accepts_exact_readback_after_lost_response(self, error):
        store = InitialDeliveryClaims("org/repo")
        record = {
            "created_at": "2026-01-01T00:00:00+00:00",
            "stage": "reserved",
            "owner_token": "a" * 32,
        }
        observed = {}
        reads = 0
        writes = []

        def read_versioned(*_args):
            nonlocal reads
            reads += 1
            return (record, "sha") if reads == 1 else (observed["record"], "sha")

        def api(_endpoint, *, method, body):
            writes.append(method)
            observed["record"] = json.loads(base64.b64decode(body["content"]))
            raise error

        with (
            patch.object(store, "_read_versioned", side_effect=read_versioned),
            patch.object(store, "_api", side_effect=api),
        ):
            assert store._transition_escalation(12, KEY, "a" * 32, "reserved", "attempted")
        assert writes == ["PUT"]
        assert reads == 2
        with patch.object(
            store, "_read_versioned", return_value=({"stage": "reserved", "owner_token": "b" * 32}, "sha")
        ):
            assert not store._transition_escalation(12, KEY, "a" * 32, "reserved", "attempted")

    def test_escalation_transition_fails_closed_when_retryable_readback_is_unknown(self):
        store = InitialDeliveryClaims("org/repo")
        record = {"created_at": "2026-01-01T00:00:00+00:00", "stage": "reserved", "owner_token": "a" * 32}
        reads = 0

        def read_versioned(*_args):
            nonlocal reads
            reads += 1
            if reads == 1:
                return record, "sha"
            raise RetryableError("readback unavailable")

        with (
            patch.object(store, "_read_versioned", side_effect=read_versioned),
            patch.object(store, "_api", side_effect=RuntimeError("response lost")) as api,
            pytest.raises(RetryableError, match="readback unavailable"),
        ):
            store._transition_escalation(12, KEY, "a" * 32, "reserved", "attempted")

        assert reads == 2
        api.assert_called_once()

    def test_escalation_transition_does_not_read_back_a_rate_limit(self):
        store = InitialDeliveryClaims("org/repo")
        record = {"created_at": "2026-01-01T00:00:00+00:00", "stage": "reserved", "owner_token": "a" * 32}
        error = ProviderRateLimitError(is_rate_limit=True)
        with (
            patch.object(store, "_read_versioned", return_value=(record, "sha")) as readback,
            patch.object(store, "_api", side_effect=error),
            pytest.raises(ProviderRateLimitError) as exc_info,
        ):
            store._transition_escalation(12, KEY, "a" * 32, "reserved", "attempted")

        assert exc_info.value is error
        readback.assert_called_once()

    def test_escalation_transition_rejects_an_oversized_updated_record(self):
        store = InitialDeliveryClaims("org/repo")
        record = {"created_at": "2026-01-01T00:00:00+00:00", "stage": "reserved", "owner_token": "a" * 32}
        while len(json.dumps(record).encode()) < 15_990:
            record["notice"] = record.get("notice", "") + "x"
        with patch.object(store, "_read_versioned", return_value=(record, "sha")):
            with pytest.raises(ValueError, match="bounded size"):
                store._transition_escalation(12, KEY, "a" * 32, "reserved", "attempted")

    @pytest.mark.parametrize("failure", ["conflict", "unchanged", "changed", "unknown"])
    def test_escalation_transition_handles_uncertain_cas_responses(self, failure):
        store = InitialDeliveryClaims("org/repo")
        record = {
            "created_at": "2026-01-01T00:00:00+00:00",
            "stage": "reserved",
            "owner_token": "a" * 32,
        }
        if failure == "conflict":
            error = RuntimeError("HTTP 409 blob SHA conflict")
            readbacks = [record]
        elif failure == "unchanged":
            error = RuntimeError("response lost")
            readbacks = [record, record]
        elif failure == "changed":
            error = RuntimeError("response lost")
            readbacks = [{"stage": "attempted", "owner_token": "b" * 32}]
        else:
            error = RuntimeError("response lost")
            readbacks = [RuntimeError("read unavailable")]
        with (
            patch.object(
                store,
                "_read_versioned",
                side_effect=[
                    (record, "sha"),
                    *[
                        value if isinstance(value, Exception) else (value, "sha") if value else None
                        for value in readbacks
                    ],
                ],
            ),
            patch.object(store, "_api", side_effect=error),
        ):
            if failure in {"changed", "unknown"}:
                error_message = "response lost" if failure == "changed" else "read unavailable"
                with pytest.raises(RuntimeError, match=error_message):
                    store._transition_escalation(12, KEY, "a" * 32, "reserved", "attempted")
            else:
                assert not store._transition_escalation(12, KEY, "a" * 32, "reserved", "attempted")

    def test_uncertain_create_is_not_retried(self):
        store = InitialDeliveryClaims("org/repo")
        with patch.object(store, "_api", side_effect=TimeoutError("lost response")) as api:
            with pytest.raises(TimeoutError):
                store.claim(12, KEY, "recovery", {})
            assert api.call_count == 1

    def test_reservation_reconciles_its_own_ambiguous_retryable_create_once(self):
        store = InitialDeliveryClaims("org/repo")
        documents = {}
        writes = 0
        owner = "a" * 32

        def api(endpoint, *, method="GET", body=None):
            nonlocal writes
            path = endpoint.split("?")[0]
            if method == "PUT":
                writes += 1
                documents[path] = body["content"]
                raise RetryableError("reservation response lost")
            content = documents[path]
            return json.dumps({"content": content, "sha": hashlib.sha256(content.encode()).hexdigest()})

        with patch.object(store, "_api", side_effect=api):
            assert store._reserve_escalation(12, KEY, {"reason": "verified"}, owner)
            record = store.read(12, KEY, "escalation")
        assert writes == 1
        assert record["stage"] == "reserved"
        assert record["owner_token"] == owner

    def test_reservation_create_propagates_rate_limit_without_readback(self):
        store = InitialDeliveryClaims("org/repo")
        error = ProviderRateLimitError(is_rate_limit=True)
        with (
            patch.object(store, "_api", side_effect=error) as api,
            patch.object(store, "read") as readback,
            pytest.raises(ProviderRateLimitError) as exc_info,
        ):
            store._reserve_escalation(12, KEY, {}, "a" * 32)

        assert exc_info.value is error
        api.assert_called_once()
        readback.assert_not_called()

    @pytest.mark.parametrize("error", [RuntimeError("provider rejected"), RetryableError("write uncertain")])
    def test_claim_create_rethrows_when_readback_confirms_absence(self, error):
        store = InitialDeliveryClaims("org/repo")
        with (
            patch.object(store, "_api", side_effect=error) as api,
            patch.object(store, "read", return_value=None) as readback,
            pytest.raises(type(error)) as exc_info,
        ):
            store.claim(12, KEY, "escalation", {})

        assert exc_info.value is error
        api.assert_called_once()
        readback.assert_called_once_with(12, KEY, "escalation")

    @pytest.mark.parametrize("repo", ["", "../repo", "org/repo/extra"])
    def test_rejects_unsafe_repository(self, repo):
        with pytest.raises(ValueError):
            InitialDeliveryClaims(repo)

    @pytest.mark.parametrize(
        "pr,key,purpose",
        [(0, KEY, "recovery"), (True, KEY, "recovery"), (12, "../key", "recovery"), (12, KEY, "arbitrary")],
    )
    def test_rejects_invalid_claim_identity(self, pr, key, purpose):
        with pytest.raises(ValueError), patch(f"{MODULE}.InitialDeliveryClaims._api") as api:
            InitialDeliveryClaims("org/repo").claim(pr, key, purpose, {})
        api.assert_not_called()

    def test_read_absent_and_propagate_unavailable(self):
        store = InitialDeliveryClaims("org/repo")
        with patch.object(store, "_api", side_effect=RuntimeError("HTTP 404")):
            assert store.read(12, KEY, "recovery") is None
        with patch.object(store, "_api", side_effect=RuntimeError("HTTP 403")):
            with pytest.raises(RuntimeError):
                store.read(12, KEY, "recovery")

    @pytest.mark.parametrize(
        "content", ["!", base64.b64encode(b"[]").decode(), base64.b64encode(b'{"created_at":"not-a-date"}').decode()]
    )
    def test_malformed_claim_never_looks_absent(self, content):
        with patch(f"{MODULE}.InitialDeliveryClaims._api", return_value=json.dumps({"content": content})):
            with pytest.raises(ValueError):
                InitialDeliveryClaims("org/repo").read(12, KEY, "recovery")

    def test_malformed_claim_without_blob_sha_never_looks_absent(self):
        content = base64.b64encode(json.dumps({"created_at": "2026-01-01T00:00:00+00:00"}).encode()).decode()
        with patch(f"{MODULE}.InitialDeliveryClaims._api", return_value=json.dumps({"content": content})):
            with pytest.raises(ValueError, match="malformed"):
                InitialDeliveryClaims("org/repo").read(12, KEY, "recovery")

    def test_uses_existing_repository_state_credential_boundary(self):
        with patch(f"{MODULE}.GitHubVariableBackingStore._api", return_value="result") as api:
            assert InitialDeliveryClaims._api("/test", method="PUT", body={"value": 1}) == "result"
        api.assert_called_once_with("/test", method="PUT", body={"value": 1})

    def test_api_converts_rate_limit_without_replaying_write(self):
        error = RetryableError(
            "rate limited",
            retry_after=30,
            provider="github",
            credential_identity="test-credential",
            is_rate_limit=True,
        )
        with (
            patch(f"{MODULE}.GitHubVariableBackingStore._api", side_effect=error) as api,
            pytest.raises(ProviderRateLimitError) as exc_info,
        ):
            InitialDeliveryClaims._api("/test", method="PUT", body={"value": 1})

        api.assert_called_once_with("/test", method="PUT", body={"value": 1})
        assert exc_info.value.is_rate_limit is True
        assert exc_info.value.retry_after_seconds == 30
        assert exc_info.value.provider == "github"
        assert exc_info.value.credential_identity == "test-credential"

    @pytest.mark.parametrize(
        "record",
        [
            {"created_at": "2026-01-01T00:00:00"},
            {"created_at": "9999-01-01T00:00:00+00:00"},
            {
                "created_at": datetime.now(UTC).isoformat(),
                "updated_at": "2026-01-01T00:00:00",
            },
            {
                "created_at": datetime.now(UTC).isoformat(),
                "updated_at": "9999-01-01T00:00:00+00:00",
            },
            {
                "created_at": datetime.now(UTC).isoformat(),
                "updated_at": 123,
            },
            {
                "created_at": datetime.now(UTC).isoformat(),
                "updated_at": None,
            },
        ],
    )
    def test_invalid_timestamp_fails_closed(self, record):
        content = base64.b64encode(json.dumps(record).encode()).decode()
        with patch(f"{MODULE}.InitialDeliveryClaims._api", return_value=json.dumps({"content": content})):
            with pytest.raises(ValueError, match="timestamp"):
                InitialDeliveryClaims("org/repo").read(12, KEY, "recovery")

    def test_oversized_claims_are_rejected_on_read_and_create(self):
        store = InitialDeliveryClaims("org/repo")
        with pytest.raises(ValueError, match="bounded size"):
            store.claim(12, KEY, "recovery", {"notice": "x" * 16_000})
        content = base64.b64encode(b"x" * 16_001).decode()
        with patch.object(store, "_api", return_value=json.dumps({"content": content})):
            with pytest.raises(ValueError, match="bounded size"):
                store.read(12, KEY, "recovery")

    def test_create_error_without_an_existing_claim_propagates(self):
        store = InitialDeliveryClaims("org/repo")
        with patch.object(store, "_api", side_effect=RuntimeError("HTTP 404")):
            with pytest.raises(RuntimeError):
                store.claim(12, KEY, "recovery", {})
