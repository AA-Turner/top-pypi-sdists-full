"""Behavioral tests for the shared-variable wake store."""

import json
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.cli.ci.cooldown import COOLDOWN_VARIABLE
from agentic_devtools.cli.ci.dispatcher_wake_store import DispatcherWakeStore
from agentic_devtools.cli.ci.exceptions import VariableWriteError
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


@pytest.fixture
def provider():
    """Model repository variables without any external provider calls."""
    mock = MagicMock()
    mock.payload = "{}"

    def read(name, *, use_writer_token=False):
        assert name == COOLDOWN_VARIABLE
        assert use_writer_token
        return mock.payload

    def write(name, value):
        assert name == COOLDOWN_VARIABLE
        mock.payload = value

    mock.get_variable.side_effect = read
    mock.set_variable.side_effect = write
    return mock


class TestDispatcherWakeStore:
    @pytest.mark.parametrize("operation", ["enqueue", "acknowledge", "postpone"])
    def test_refusal_is_read_only_and_resets_on_mutation(self, provider, operation):
        store = DispatcherWakeStore(provider)
        assert store.last_refusal is None
        with pytest.raises(AttributeError):
            store.last_refusal = "changed"
        assert store.enqueue(1, "a", "opened", 200, now=100)
        key, entry = next(iter(store.entries(now=100).items()))
        assert not store.enqueue(2, "b", "opened", 100 + store.TTL_SECONDS, now=100)
        args = (1, "a", "opened", 200) if operation == "enqueue" else (key, entry)
        if operation == "postpone":
            args += (300,)
        with pytest.raises(ValueError):
            getattr(store, operation)(*args, now=-1)
        assert store.last_refusal is None
        assert getattr(store, operation)(*args, now=100)
        assert store.last_refusal is None

    @pytest.mark.parametrize("stage", ["read", "write", "verify-read"])
    @pytest.mark.parametrize("outcome", ["failure", "success", "mismatch"])
    def test_attempt_scoped_refusal(self, provider, stage, outcome):
        store = DispatcherWakeStore(provider)
        original_read, original_write = provider.get_variable.side_effect, provider.set_variable.side_effect

        def read(name, **kwargs):
            count = provider.get_variable.call_count
            if stage == "read" or (stage == "verify-read" and count % 2 == 0):
                if outcome == "failure" or count == (1 if stage == "read" else 2):
                    raise RuntimeError("private diagnostic payload")
            return "{}" if outcome == "mismatch" else original_read(name, **kwargs)

        def write(name, value):
            if stage == "write" and (outcome == "failure" or provider.set_variable.call_count == 1):
                raise RuntimeError("private diagnostic payload")
            original_write(name, value)

        provider.get_variable.side_effect, provider.set_variable.side_effect = read, write
        assert store.enqueue(1, "a", "opened", 200, now=100) == (outcome == "success")
        expected = f"{stage}-error:RuntimeError" if outcome == "failure" else "verification-failed"
        assert store.last_refusal == (None if outcome == "success" else expected)

    def test_whole_document_retry_merge_keeps_invalid_cooldown_deadline(self, provider):
        original = {"github:TOKEN": {"resume_at": 1e300, "custom": True}}
        provider.payload = json.dumps({"provider_cooldowns": original})
        writes = 0

        def race(name, value):
            nonlocal writes
            writes += 1
            document = json.loads(value)
            if writes == 1:
                document["provider_cooldowns"]["github:TOKEN"]["resume_at"] = 200
            provider.payload = json.dumps(document)

        provider.set_variable.side_effect = race
        assert DispatcherWakeStore(provider).enqueue(1, "a", "opened", 200, now=100)
        assert writes == 2
        assert json.loads(provider.payload)["provider_cooldowns"] == original

    @pytest.mark.parametrize("operation", ["acknowledge", "postpone"])
    def test_lost_existing_mutation_never_reports_success(self, provider, operation):
        store = DispatcherWakeStore(provider)
        assert store.enqueue(1, "a", "opened", 200, now=100)
        key, entry = next(iter(store.entries(now=100).items()))
        provider.set_variable.reset_mock()
        provider.set_variable.side_effect = lambda name, value: None

        if operation == "acknowledge":
            assert not store.acknowledge(key, entry, now=110)
        else:
            assert not store.postpone(key, entry, 300, now=110)
        assert store.last_refusal == "verification-failed"
        assert provider.set_variable.call_count == 3
        assert store.entries(now=110)[key] == entry

    @pytest.mark.parametrize("operation", ["acknowledge", "postpone"])
    def test_changed_same_identity_snapshot_never_verifies_mutation(self, provider, operation):
        store = DispatcherWakeStore(provider)
        assert store.enqueue(1, "a", "opened", 200, now=100)
        key, entry = next(iter(store.entries(now=100).items()))

        def change_envelope(name, value):
            document = json.loads(value)
            document["dispatcher_wakes"]["entries"][key]["created_at"] += 1
            provider.payload = json.dumps(document)

        provider.set_variable.side_effect = change_envelope
        if operation == "acknowledge":
            assert not store.acknowledge(key, entry, now=110)
        else:
            assert not store.postpone(key, entry, 300, now=110)

    @pytest.mark.parametrize("operation", ["acknowledge", "postpone"])
    def test_verified_other_generation_does_not_claim_snapshot_mutation(self, provider, operation):
        store = DispatcherWakeStore(provider)
        assert store.enqueue(1, "a", "opened", 200, now=100)
        key, entry = next(iter(store.entries(now=100).items()))

        def replace_identity(name, value):
            document = json.loads(value)
            document["dispatcher_wakes"]["entries"][key]["identity"] = "z" * 32
            provider.payload = json.dumps(document)

        provider.set_variable.side_effect = replace_identity
        if operation == "acknowledge":
            assert not store.acknowledge(key, entry, now=110)
        else:
            assert not store.postpone(key, entry, 300, now=110)

    def test_invalid_verified_target_is_never_reported_as_persisted(self, provider):
        store = DispatcherWakeStore(provider)

        def corrupt(name, value):
            document = json.loads(value)
            target = next(iter(document["dispatcher_wakes"]["entries"].values()))
            target["expires_at"] += 10
            provider.payload = json.dumps(document)

        provider.set_variable.side_effect = corrupt
        assert not store.enqueue(1, "a", "opened", 200, now=100)
        assert store.last_refusal == "invalid-existing"
        assert store.entries(now=100) == {}

    def test_entries_propagates_provider_read_failure(self, provider):
        store = DispatcherWakeStore(provider)
        error = RuntimeError("HTTP 503 service unavailable")
        provider.get_variable.side_effect = error

        with pytest.raises(RuntimeError, match="HTTP 503"):
            store.entries(now=100)

    def test_concurrent_enqueue_generations_cannot_verify_an_invalid_ttl(self, provider):
        store = DispatcherWakeStore(provider)
        assert store.enqueue(1, "a", "opened", 300, now=100)
        older = json.loads(provider.payload)
        older_key = next(iter(store.entries(now=100)))
        provider.payload = "{}"
        assert store.enqueue(1, "a", "opened", 200, now=110)
        newer = json.loads(provider.payload)
        calls = 0

        def race_read(name, *, use_writer_token=False):
            nonlocal calls
            calls += 1
            if calls == 1:
                return json.dumps(newer)
            if calls == 2:
                return json.dumps(older)
            return provider.payload

        provider.get_variable.side_effect = race_read
        assert store.enqueue(2, "b", "opened", 400, now=120)
        recovered = store.entries(now=120)[older_key]
        assert recovered["resume_at"] == 300
        assert recovered["identity"] == older["dispatcher_wakes"]["entries"][older_key]["identity"]
        assert recovered["expires_at"] - recovered["created_at"] == store.TTL_SECONDS

    def test_enqueue_is_idempotent_monotonic_and_preserves_metadata(self, provider):
        provider.payload = json.dumps({"legacy": {"a": 1}, "provider_cooldowns": {"unknown": {"x": 2}}})
        store = DispatcherWakeStore(provider)
        assert store.enqueue(42, "abc", "synchronize", 200, now=100)
        key, entry = next(iter(store.entries(now=100).items()))
        assert entry["pr_number"] == 42
        assert entry["status"] == "pending"
        assert store.enqueue(42, "abc", "synchronize", 150, now=110)
        assert store.entries(now=110)[key]["resume_at"] == 200
        assert store.enqueue(42, "abc", "synchronize", 300, now=110)
        assert store.entries(now=110)[key]["resume_at"] == 300
        assert json.loads(provider.payload)["legacy"] == {"a": 1}
        assert json.loads(provider.payload)["provider_cooldowns"] == {"unknown": {"x": 2}}

    def test_acknowledgement_requires_current_snapshot_and_retains_tombstone(self, provider):
        store = DispatcherWakeStore(provider)
        assert store.enqueue(42, "abc", "synchronize", 200, now=100)
        key, entry = next(iter(store.entries(now=100).items()))
        assert store.postpone(key, entry, 300, now=110)
        assert not store.acknowledge(key, entry, now=110)
        assert store.last_refusal == "snapshot-mismatch"
        current = store.entries(now=110)[key]
        assert store.acknowledge(key, current, now=120)
        assert store.entries(now=120) == {}
        assert store.enqueue(42, "abc", "synchronize", 400, now=130)
        assert store.entries(now=130) == {}
        assert not store.postpone(key, current, 500, now=130)

    def test_expiration_releases_capacity_without_dropping_pending(self, provider):
        store = DispatcherWakeStore(provider)
        with patch.object(DispatcherWakeStore, "MAX_ENTRIES", 2):
            assert store.enqueue(1, "a", "opened", 200, now=100)
            assert store.enqueue(2, "b", "opened", 200, now=100)
            assert not store.enqueue(3, "c", "opened", 200, now=100)
            assert store.last_refusal == "entry-capacity"
            assert len(store.entries(now=100)) == 2
            assert store.last_refusal == "entry-capacity"
            assert store.entries(now=100 + store.TTL_SECONDS) == {}
            assert store.enqueue(3, "c", "opened", 100000, now=90000)

    def test_observed_oversized_queue_is_not_rewritten(self, provider):
        store = DispatcherWakeStore(provider)
        assert store.enqueue(1, "a", "opened", 200, now=100)
        assert store.enqueue(2, "b", "opened", 200, now=100)
        provider.set_variable.reset_mock()
        with patch.object(DispatcherWakeStore, "MAX_ENTRIES", 1):
            assert not store.enqueue(1, "a", "opened", 300, now=110)
        provider.set_variable.assert_not_called()

    def test_unknown_records_are_preserved_and_unknown_schema_refuses_write(self, provider):
        provider.payload = json.dumps({"dispatcher_wakes": {"version": 1, "entries": {"future": {"version": 9}}}})
        store = DispatcherWakeStore(provider)
        assert store.entries(now=100) == {}
        assert store.enqueue(1, "a", "opened", 200, now=100)
        assert json.loads(provider.payload)["dispatcher_wakes"]["entries"]["future"] == {"version": 9}
        provider.payload = '{"dispatcher_wakes":{"version":9,"entries":[]}}'
        assert not store.enqueue(2, "b", "opened", 200, now=100)
        assert json.loads(provider.payload)["dispatcher_wakes"]["version"] == 9

    @pytest.mark.parametrize("raw", ["{", "[]", "null", '{"dispatcher_wakes":[]}'])
    def test_malformed_state_is_not_overwritten(self, provider, raw):
        provider.payload = raw
        store = DispatcherWakeStore(provider)
        assert store.entries(now=100) == {}
        assert not store.enqueue(1, "a", "opened", 200, now=100)
        provider.set_variable.assert_not_called()

    def test_failures_are_not_reported_as_persisted(self, provider):
        store = DispatcherWakeStore(provider)
        provider.set_variable.side_effect = RuntimeError("unavailable")
        assert not store.enqueue(1, "a", "opened", 200, now=100)
        assert store.last_refusal == "write-error:RuntimeError"
        assert provider.set_variable.call_count == 3
        provider.get_variable.side_effect = RuntimeError("read failed")
        with pytest.raises(RuntimeError, match="read failed"):
            store.entries(now=100)
        assert not store.enqueue(1, "a", "opened", 200, now=100)

    def test_lost_writes_are_retried_without_claiming_delivery(self, provider):
        store = DispatcherWakeStore(provider)
        provider.set_variable.side_effect = lambda name, value: None
        assert not store.enqueue(1, "a", "opened", 200, now=100)
        assert store.last_refusal == "verification-failed"
        assert provider.set_variable.call_count == 3

    def test_acknowledgement_write_failure_retains_pending(self, provider):
        store = DispatcherWakeStore(provider)
        assert store.enqueue(1, "a", "opened", 200, now=100)
        key, entry = next(iter(store.entries(now=100).items()))
        provider.set_variable.side_effect = RuntimeError("failed")
        assert not store.acknowledge(key, entry, now=110)
        assert store.entries(now=110)[key] == entry

    def test_retries_union_concurrent_intents_and_tombstones(self, provider):
        store = DispatcherWakeStore(provider)
        assert store.enqueue(1, "a", "opened", 200, now=100)
        first_key, first = next(iter(store.entries(now=100).items()))
        assert store.enqueue(2, "b", "opened", 200, now=100)
        original = json.loads(provider.payload)
        first_write = True

        def race(name, value):
            nonlocal first_write
            if first_write:
                first_write = False
                raced = json.loads(json.dumps(original))
                raced["dispatcher_wakes"]["entries"][first_key]["status"] = "delivered"
                raced["legacy"] = {"concurrent": True}
                provider.payload = json.dumps(raced)
            else:
                provider.payload = value

        provider.set_variable.side_effect = race
        assert store.enqueue(3, "c", "opened", 300, now=110)
        assert len(store.entries(now=110)) == 2
        assert first_key not in store.entries(now=110)
        assert json.loads(provider.payload)["legacy"] == {"concurrent": True}
        assert not store.acknowledge(first_key, first, now=110)

    def test_retry_does_not_acknowledge_a_changed_snapshot(self, provider):
        store = DispatcherWakeStore(provider)
        assert store.enqueue(1, "a", "opened", 200, now=100)
        key, entry = next(iter(store.entries(now=100).items()))

        def race(name, value):
            raced = json.loads(provider.payload)
            raced["dispatcher_wakes"]["entries"][key]["resume_at"] = 300
            provider.payload = json.dumps(raced)

        provider.set_variable.side_effect = race
        assert not store.acknowledge(key, entry, now=110)
        assert store.last_refusal == "snapshot-mismatch"
        assert store.entries(now=110)[key]["resume_at"] == 300

    def test_unrelated_lost_data_retries_acknowledgement_safely(self, provider):
        store = DispatcherWakeStore(provider)
        assert store.enqueue(1, "a", "opened", 200, now=100)
        key, entry = next(iter(store.entries(now=100).items()))
        payload = json.loads(provider.payload)
        payload["legacy"] = True
        provider.payload = json.dumps(payload)
        writes = 0

        def race(name, value):
            nonlocal writes
            writes += 1
            document = json.loads(value)
            if writes == 1:
                document.pop("legacy")
            provider.payload = json.dumps(document)

        provider.set_variable.side_effect = race
        assert store.acknowledge(key, entry, now=110)
        assert writes == 2
        assert json.loads(provider.payload)["legacy"] is True
        assert store.entries(now=110) == {}

    def test_bounds_deadlines_and_encoded_size(self, provider):
        store = DispatcherWakeStore(provider)
        assert not store.enqueue(1, "a", "opened", 100 + store.TTL_SECONDS + 1, now=100)
        assert not store.enqueue(1, "a", "opened", 100 + store.TTL_SECONDS, now=100)
        assert store.last_refusal == "deadline-beyond-ttl"
        assert not store.enqueue(1, "a", "opened", 200, now=1e30)
        assert store.last_refusal == "invalid-entry"
        with patch.object(DispatcherWakeStore, "MAX_BYTES", 10):
            assert not store.enqueue(1, "a", "opened", 200, now=100)
            assert store.last_refusal == "byte-capacity"
        assert store.enqueue(1, "a", "opened", 200, now=100)
        key, entry = next(iter(store.entries(now=100).items()))
        assert not store.postpone(key, entry, entry["expires_at"] + 1, now=110)
        assert not store.postpone(key, entry, entry["expires_at"], now=110)
        assert store.last_refusal == "deadline-beyond-expiry"
        assert not store.enqueue(1, "a", "opened", entry["expires_at"] + 1, now=110)
        assert store.last_refusal == "deadline-beyond-expiry"
        assert store.postpone(key, entry, 150, now=110)
        assert store.entries(now=110)[key]["resume_at"] == 200

    def test_invalid_and_expired_snapshots_are_not_mutated(self, provider):
        store = DispatcherWakeStore(provider)
        assert not store.acknowledge("missing", {}, now=100)
        assert store.enqueue(1, "a", "opened", 200, now=100)
        key, entry = next(iter(store.entries(now=100).items()))
        assert not store.acknowledge(key, entry, now=entry["expires_at"])
        assert store.last_refusal == "invalid-entry"
        assert not store.acknowledge("different", entry, now=100)

    @pytest.mark.parametrize(
        "overrides",
        [
            {"version": True},
            {"pr_number": 0},
            {"resume_at": None},
            {"resume_at": 10**400},
            {"created_at": 100000},
            {"expires_at": 1000000},
            {"resume_at": 1000000},
            {"status": "unknown"},
            {"identity": None},
            {"identity": ""},
        ],
    )
    def test_malformed_records_are_ignored_but_retained(self, provider, overrides):
        store = DispatcherWakeStore(provider)
        assert store.enqueue(1, "a", "opened", 200, now=100)
        key = next(iter(store.entries(now=100)))
        document = json.loads(provider.payload)
        document["dispatcher_wakes"]["entries"][key].update(overrides)
        provider.payload = json.dumps(document)
        assert store.entries(now=100) == {}
        assert not store.enqueue(1, "a", "opened", 200, now=100)
        assert store.last_refusal == "invalid-existing"
        assert json.loads(provider.payload) == document

    def test_unknown_extension_version_types_and_entries_are_not_overwritten(self, provider):
        store = DispatcherWakeStore(provider)
        for extension in [
            {"version": True, "entries": {}},
            {"version": 1, "entries": []},
            {"entries": {}},
        ]:
            provider.payload = json.dumps({"dispatcher_wakes": extension})
            assert not store.enqueue(1, "a", "opened", 200, now=100)
            assert store.entries(now=100) == {}

    def test_default_clock_is_used(self, provider):
        store = DispatcherWakeStore(provider)
        with patch("agentic_devtools.cli.ci.dispatcher_wake_store.time.time", return_value=100):
            assert store.enqueue(1, "a", "opened", 200)
            key, entry = next(iter(store.entries().items()))
            assert store.postpone(key, entry, 300)
            assert store.acknowledge(key, store.entries()[key])

    def test_writer_credential_never_falls_back_to_default(self, monkeypatch):
        monkeypatch.delenv("REPO_VARIABLE_WRITER_PAT", raising=False)
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "default-must-not-be-used")
        monkeypatch.setenv("GH_TOKEN", "primary-must-not-be-used")
        with patch("agentic_devtools.cli.ci.github_provider._gh_api") as api:
            store = DispatcherWakeStore(GitHubActionsProvider("owner/repo"))
            assert not store.enqueue(1, "a", "opened", 200, now=100)
            with pytest.raises(VariableWriteError, match="REPO_VARIABLE_WRITER_PAT"):
                store.entries(now=100)
        api.assert_not_called()

    def test_all_provider_reads_and_writes_use_independent_writer(self, monkeypatch):
        monkeypatch.setenv("REPO_VARIABLE_WRITER_PAT", "writer-for-test")
        monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "default-for-test")
        monkeypatch.setenv("GH_TOKEN", "limited-primary-for-test")
        stored = None

        def api(path, *, token=None, method="GET", body=None):
            nonlocal stored
            assert token == "writer-for-test"
            if method == "PATCH":
                stored = body["value"]
                return ""
            return json.dumps({"value": stored})

        with patch("agentic_devtools.cli.ci.github_provider._gh_api", side_effect=api):
            store = DispatcherWakeStore(GitHubActionsProvider("owner/repo"))
            assert store.enqueue(1, "a", "opened", 200, now=100)
            assert len(store.entries(now=100)) == 1

    @pytest.mark.parametrize(
        "args",
        [
            (0, "a", "opened", 200),
            (True, "a", "opened", 200),
            (1, "", "opened", 200),
            (1, "a", "", 200),
            (1, "a", "opened", float("nan")),
            (1, "a", "opened", -1),
            ("1", "a", "opened", 200),
            (1, None, "opened", 200),
            (1, "a" * 129, "opened", 200),
            (1, "a", None, 200),
            (1, "a", "e" * 129, 200),
            (1, "a", "opened", True),
            (1, "a", "opened", 10**400),
        ],
    )
    def test_invalid_enqueue_input_is_rejected(self, provider, args):
        with pytest.raises(ValueError):
            DispatcherWakeStore(provider).enqueue(*args, now=100)
