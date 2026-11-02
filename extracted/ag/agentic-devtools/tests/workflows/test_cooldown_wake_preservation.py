"""Cooldown and dispatcher wake persistence share one loss-resistant document."""

import hashlib
import json
from unittest.mock import MagicMock, patch

from agentic_devtools.cli.ci.cooldown import persist_cooldown
from agentic_devtools.cli.ci.dispatcher_wake_store import DispatcherWakeStore
from agentic_devtools.cli.shared.retry import ProviderRateLimitError


def test_cooldown_retry_preserves_wakes_and_unknown_metadata():
    provider = MagicMock()
    stored = json.dumps(
        {
            "version": 8,
            "provider_cooldowns": {"future": {"version": 9}, "github:GH_TOKEN": {"custom": True}},
        }
    )
    writes = 0
    lose_next = False

    def read(_name, *, use_writer_token=False):
        assert use_writer_token
        return stored

    def write(_name, value):
        nonlocal stored, writes, lose_next
        writes += 1
        stored = "{}" if lose_next else value
        lose_next = False

    provider.get_variable.side_effect = read
    provider.set_variable.side_effect = write
    store = DispatcherWakeStore(provider)
    assert store.enqueue(42, "abc", "synchronize", 200, now=100)
    key, entry = next(iter(store.entries(now=100).items()))
    assert store.acknowledge(key, entry, now=110)
    original_wakes = json.loads(stored)["dispatcher_wakes"]
    before = writes
    lose_next = True
    error = ProviderRateLimitError(provider="github", credential_identity="GH_TOKEN")
    assert persist_cooldown(provider, error, now=120) is not None
    assert writes == before + 2
    actual = json.loads(stored)
    assert actual["version"] == 8
    assert actual["dispatcher_wakes"] == original_wakes
    assert actual["provider_cooldowns"]["future"] == {"version": 9}
    assert actual["provider_cooldowns"]["github:GH_TOKEN"]["custom"] is True
    assert store.entries(now=120) == {}
    assert store.enqueue(42, "abc", "synchronize", 300, now=130)
    assert store.entries(now=130) == {}


def test_cooldown_retry_refuses_a_65_entry_union_without_evicting_wakes():
    provider = MagicMock()

    def wake(number):
        key = hashlib.sha256(json.dumps([number, "abc", "opened"], separators=(",", ":")).encode()).hexdigest()
        return key, {
            "version": 1,
            "identity": str(number),
            "pr_number": number,
            "head_sha": "abc",
            "event": "opened",
            "created_at": 100,
            "expires_at": 86500,
            "resume_at": 200,
            "status": "pending",
        }

    shared = dict(wake(number) for number in range(1, 64))
    first = {"dispatcher_wakes": {"version": 1, "entries": shared | dict([wake(64)])}}
    competing = {"dispatcher_wakes": {"version": 1, "entries": shared | dict([wake(65)])}}
    stored = json.dumps(first)
    writes = []

    def read(_name, *, use_writer_token=False):
        assert use_writer_token
        return stored

    def write(_name, value):
        nonlocal stored
        document = json.loads(value)
        writes.append(document)
        raced = dict(competing, provider_cooldowns=document["provider_cooldowns"])
        stored = json.dumps(raced)

    provider.get_variable.side_effect = read
    provider.set_variable.side_effect = write
    error = ProviderRateLimitError(provider="github", credential_identity="GH_TOKEN")
    with patch("agentic_devtools.cli.ci.cooldown.time.sleep"):
        assert persist_cooldown(provider, error, now=120) is None
    assert len(writes) == 1
    assert all(len(document["dispatcher_wakes"]["entries"]) == 64 for document in writes)
    assert len(json.loads(stored)["dispatcher_wakes"]["entries"]) == 64
    assert len(DispatcherWakeStore(provider).entries(now=120)) == 64
