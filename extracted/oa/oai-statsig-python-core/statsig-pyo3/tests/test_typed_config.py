from copy import deepcopy
from gc import collect
from queue import Queue
from threading import Barrier, Condition, Event, Thread
from types import SimpleNamespace
from weakref import ref

import pytest
from google.protobuf.descriptor_pb2 import FieldDescriptorProto
from google.protobuf.json_format import ParseError
from google.protobuf.struct_pb2 import Struct
from statsig_python_core import Statsig, StatsigUser, TypedDynamicConfig
from statsig_python_core.typed_config import (
    TypedConfigConversionError,
    TypedConfigUnavailableError,
    _TypedConfigs,
)


def selected(version, value=None, *, lcut=None, usable=True):
    return {
        "ruleID": "selected",
        "idType": "userID",
        "details": {
            "reason": "Network:Recognized",
            "lcut": lcut or version,
            "version": version,
            "received_at": 123,
        },
        "value": {"number": version} if value is None else value,
        "__typed_revision": version,
        "__typed_usable": usable,
    }


class Updates:
    def __init__(self):
        self.condition = Condition()
        self.pending = False
        self.closed = False
        self.paused = None
        self.resume = None

    def publish(self):
        with self.condition:
            self.pending = True
            self.condition.notify_all()

    def wait(self):
        with self.condition:
            self.condition.wait_for(lambda: self.pending or self.closed, timeout=1)
            if self.closed:
                return None
            changed = self.pending
            self.pending = False
        if changed and self.paused is not None:
            self.paused.set()
            assert self.resume.wait(5)
        return changed

    def close(self):
        with self.condition:
            self.closed = True
            self.condition.notify_all()


class NativeContext:
    def __init__(self, sdk, user):
        self.sdk = sdk
        self.user = SimpleNamespace(
            user_id=user.user_id,
            custom=deepcopy(user.custom),
            private_attributes=deepcopy(user.private_attributes),
        )

    def get_evaluation(self):
        return self.sdk.evaluate(self.user)


class FakeSDK:
    def __init__(self):
        self.raw = selected(1)
        self.updates = Updates()
        self.background_evaluated = Event()
        self._typed_configs = _TypedConfigs(self)
        observe = self._typed_configs._observe

        def observed(observer, *, baseline=False):
            try:
                observe(observer, baseline=baseline)
            finally:
                if not baseline:
                    self.background_evaluated.set()

        self._typed_configs._observe = observed
        self.user = StatsigUser("infrastructure", custom={"cluster": "staging"})
        self.initialized = True
        self.last_options = None
        self.request_reads = 0

    def is_initialized(self):
        return self.initialized

    def evaluate(self, user):
        return deepcopy(self.raw(user) if callable(self.raw) else self.raw)

    def _INTERNAL_get_typed_config(self, user, name, options):
        self.last_options = options
        self.request_reads += 1
        return self.evaluate(user)

    def _INTERNAL_typed_config_context(self, user, name):
        return NativeContext(self, user)

    def _INTERNAL_typed_config_updates(self):
        return self.updates

    def get(self, *, user=None, message_type=Struct, options=None):
        return self._typed_configs.get(
            "config", user or self.user, message_type, options
        )

    def register(self, callback, *, user=None, message_type=Struct):
        return self._typed_configs.register(
            "config", user or self.user, callback, message_type
        )

    def publish(self, raw):
        self.background_evaluated.clear()
        self.raw = raw
        self.updates.publish()

    def wait_for_observation(self):
        assert self.background_evaluated.wait(5)


@pytest.fixture
def sdk():
    instance = FakeSDK()
    try:
        yield instance
    finally:
        if instance.updates.resume is not None:
            instance.updates.resume.set()
        instance._typed_configs.close()


def test_each_read_uses_current_context_options_and_paired_metadata(sdk):
    sdk.raw = lambda user: selected(
        1 if user.custom["marker"] == "A" else 2,
        {"user": user.user_id, "marker": user.custom["marker"]},
    )
    first_user = StatsigUser("first", custom={"marker": "A"})
    second_user = StatsigUser("second", custom={"marker": "B"})
    options = object()
    results = [
        sdk.get(user=user, options=options)
        for user in (first_user, second_user, first_user)
    ]
    assert sdk.last_options is options
    assert [result.value["marker"] for result in results] == ["A", "B", "A"]
    assert [result.details.version for result in results] == [1, 2, 1]
    first_user.custom = {"marker": "B"}
    changed = sdk.get(user=first_user)
    assert changed.value == {"user": "first", "marker": "B"}
    assert changed.details.version == 2
    result = results[0]
    assert isinstance(result, TypedDynamicConfig)
    assert result.get_value() is result.value
    assert result.get_name() == "config"
    assert result.get_rule_id() == "selected" and result.get_id_type() == "userID"
    assert result.get_evaluation_details().to_dict() == {
        "reason": "Network:Recognized",
        "version": 1,
        "lcut": 1,
        "received_at": 123,
    }
    assert result.to_dict()["value"] is result.value
    assert sdk.request_reads == 4


def test_request_volume_retains_no_bindings_or_results(sdk):
    results = []
    for index in range(200):
        result = sdk.get(user=StatsigUser(str(index)))
        results.append(ref(result))
    del result
    assert all(reference() is None for reference in results)
    assert sdk._typed_configs.observers == []
    assert sdk._typed_configs._worker is None
    assert not hasattr(sdk._typed_configs, "bindings")


def test_unchanged_protobuf_reads_construct_fresh(sdk):
    results = [sdk.get(message_type=Struct) for _ in range(10)]
    assert all(result.value["number"] == 1 for result in results)
    assert len({id(result.value) for result in results}) == 10


def test_open_handle_retains_owner_without_retaining_it_in_coordinator():
    class Owner:
        pass

    owner = Owner()
    owner_ref = ref(owner)
    coordinator = _TypedConfigs(owner)
    handle = coordinator._ensure_open()
    assert handle is owner
    del owner
    assert owner_ref() is handle
    del handle
    collect()
    assert owner_ref() is None
    with pytest.raises(TypedConfigUnavailableError, match="shut down"):
        coordinator._ensure_open()


@pytest.mark.parametrize("operation", ["get", "register"])
@pytest.mark.parametrize("owner_state", ["collected", "closed"])
def test_missing_or_closed_owner_rejects_typed_operations(operation, owner_state):
    class Owner:
        pass

    owner = Owner()
    coordinator = _TypedConfigs(owner)
    if owner_state == "collected":
        del owner
        collect()
    else:
        coordinator.close()
    with pytest.raises(TypedConfigUnavailableError, match="shut down"):
        if operation == "get":
            coordinator.get("config", None, Struct, None)
        else:
            coordinator.register("config", None, lambda result: None, Struct)
    assert coordinator.observers == []


def test_open_handle_dereferences_owner_once():
    class Owner:
        pass

    owner = Owner()
    coordinator = _TypedConfigs(owner)
    calls = []

    def resolve_owner():
        calls.append(None)
        return owner if len(calls) == 1 else None

    coordinator._sdk = resolve_owner
    assert coordinator._ensure_open() is owner
    assert len(calls) == 1


@pytest.mark.parametrize(
    "payload_state", ["unusable", "cache_hit", "missing", "non_object"]
)
def test_unavailable_never_substitutes_previous_value(sdk, payload_state):
    previous = sdk.get()
    sdk.raw = selected(1, lcut=20)
    if payload_state == "unusable":
        sdk.raw["__typed_usable"] = False
    elif payload_state == "non_object":
        sdk.raw["value"] = []
    else:
        del sdk.raw["value"]
        if payload_state == "cache_hit":
            sdk.raw["__statsig_dynamic_returnable_cache_hit"] = True
    with pytest.raises(TypedConfigUnavailableError):
        sdk.get()
    assert previous.value == {"number": 1} and previous.details.lcut == 1
    sdk.raw = selected(2, {})
    assert sdk.get().value == {}


def test_conversion_failure_is_explicit_with_cause_for_each_user(sdk):
    sdk.get()
    sdk.raw = selected(2, {"number": "invalid"})
    for user in (sdk.user, StatsigUser("other")):
        with pytest.raises(TypedConfigConversionError) as caught:
            sdk.get(user=user, message_type=FieldDescriptorProto)
        assert isinstance(caught.value.__cause__, ParseError)
    assert sdk._typed_configs.observers == []


def test_explicit_contexts_are_captured_without_replay_or_getter_notifications(sdk):
    version = 1
    sdk.raw = lambda user: selected(version, {"marker": user.custom["marker"]})
    first_user = StatsigUser("first", custom={"marker": "A"})
    second_user = StatsigUser("second", custom={"marker": "B"})
    callbacks = Queue()
    assert sdk.register(callbacks.put, user=first_user) is None
    assert sdk.register(callbacks.put, user=second_user) is None
    first_user.custom = {"marker": "changed"}
    assert callbacks.empty()
    version = 2
    assert sdk.get(user=first_user).value == {"marker": "changed"}
    assert callbacks.empty()
    sdk.updates.publish()
    assert [callbacks.get(timeout=5).value for _ in range(2)] == [
        {"marker": "A"},
        {"marker": "B"},
    ]


def test_registration_replaces_stopped_worker_and_reuses_live_worker(sdk):
    stopped_worker = Thread()
    stopped_worker.start()
    stopped_worker.join(timeout=5)
    assert not stopped_worker.is_alive()
    sdk._typed_configs._worker = stopped_worker
    callbacks = Queue()

    sdk.register(callbacks.put)
    replacement = sdk._typed_configs._worker
    assert replacement is not stopped_worker and replacement.is_alive()
    sdk.register(callbacks.put)
    assert sdk._typed_configs._worker is replacement
    assert callbacks.empty()

    sdk.publish(selected(2))
    assert [callbacks.get(timeout=5).value["number"] for _ in range(2)] == [2, 2]


def test_no_replay_unrelated_lcut_equal_value_revision_and_rollback(sdk):
    callbacks = Queue()
    sdk.register(callbacks.put)
    assert callbacks.empty()
    sdk.publish(selected(1, lcut=20))
    sdk.wait_for_observation()
    assert callbacks.empty()
    for version in (2, 1):
        sdk.publish(selected(version, {"number": 1}, lcut=20 + version))
        result = callbacks.get(timeout=5)
        assert result.value["number"] == 1 and result.details.version == version
        result_ref = ref(result)
        del result
        sdk.wait_for_observation()
        assert result_ref() is None
    assert sdk._typed_configs.observers[0].revision == 1


def test_background_signal_coalesces_and_callback_getter_can_see_newer_state(sdk):
    callbacks = Queue()
    sdk.updates.paused, sdk.updates.resume = Event(), Event()

    def callback(result):
        sdk.raw = selected(4)
        latest = sdk.get()
        callbacks.put((result, latest))

    sdk.register(callback)
    sdk.publish(selected(2))
    assert sdk.updates.paused.wait(5)
    sdk.raw = selected(3)
    assert sdk.get().value == {"number": 3} and callbacks.empty()
    sdk.updates.resume.set()
    delivered, latest = callbacks.get(timeout=5)
    assert delivered.details.version == 3 and latest.details.version == 4
    assert delivered.value is not latest.value
    sdk.wait_for_observation()
    assert callbacks.empty()


@pytest.mark.parametrize("existing_worker", [False, True])
def test_publication_during_registration_baseline_is_not_lost(
    sdk, monkeypatch, existing_worker
):
    callbacks, entered, release = Queue(), Event(), Event()
    if existing_worker:
        sdk.register(lambda result: None)
    evaluate = sdk.evaluate

    def baseline(user):
        raw = evaluate(user)
        if user.user_id == "registering" and raw["__typed_revision"] == 1:
            entered.set()
            assert release.wait(5)
        return raw

    monkeypatch.setattr(sdk, "evaluate", baseline)
    registrar = Thread(
        target=lambda: sdk.register(callbacks.put, user=StatsigUser("registering")),
        daemon=True,
    )
    registrar.start()
    try:
        assert entered.wait(5)
        sdk.publish(selected(2))
        assert sdk.get().details.version == 2
    finally:
        release.set()
        registrar.join(5)
    assert not registrar.is_alive()
    assert callbacks.get(timeout=5).details.version == 2
    sdk.wait_for_observation()
    assert callbacks.empty()


def test_failed_baseline_and_observation_report_without_retained_values(sdk, caplog):
    callbacks = Queue()

    sdk.raw = selected(1, {"number": "private invalid payload"})
    sdk.register(callbacks.put, message_type=FieldDescriptorProto)
    assert sdk._typed_configs.observers[0].revision is None
    sdk.publish(selected(2))
    assert callbacks.get(timeout=5).details.version == 2
    sdk.wait_for_observation()
    sdk.publish(selected(3, {"number": "private invalid payload"}))
    sdk.wait_for_observation()
    assert callbacks.empty()
    assert sdk._typed_configs.observers[0].revision == 2
    sdk.publish(selected(4))
    assert callbacks.get(timeout=5).details.version == 4
    assert "TypedConfigConversionError" in caplog.text
    assert "private invalid payload" not in caplog.text


def test_callback_exception_isolation_and_callback_shutdown_fence(sdk, caplog):
    delivered = Queue()

    def broken(result):
        raise ValueError("private payload")

    def stop(result):
        sdk._typed_configs.close()
        delivered.put(result)

    sdk.register(broken)
    sdk.register(stop)
    sdk.register(lambda result: pytest.fail("delivery after shutdown"))
    sdk.publish(selected(2))
    assert delivered.get(timeout=5).details.version == 2
    sdk._typed_configs.close()
    assert not sdk._typed_configs._worker.is_alive()
    assert sdk._typed_configs.observers == []
    assert "ValueError" in caplog.text and "private payload" not in caplog.text
    with pytest.raises(TypedConfigUnavailableError):
        sdk.get()


def test_callback_failure_retries_only_on_later_publication(sdk):
    attempts = []

    def callback(result):
        attempts.append(result.details.version)
        if len(attempts) == 1:
            raise ValueError("first delivery rejected")

    sdk.register(callback)
    sdk.publish(selected(2))
    sdk.wait_for_observation()
    assert attempts == [2]
    assert sdk._typed_configs.observers[0].revision == 1
    sdk.get()
    assert attempts == [2]
    sdk.publish(selected(2, lcut=3))
    sdk.wait_for_observation()
    assert attempts == [2, 2]
    assert sdk._typed_configs.observers[0].revision == 2
    sdk.publish(selected(2, lcut=4))
    sdk.wait_for_observation()
    assert attempts == [2, 2]


@pytest.mark.parametrize("operation", ["get", "register"])
def test_shutdown_fences_inflight_evaluation_without_holding_state_lock(
    sdk, monkeypatch, operation
):
    sdk.register(lambda result: None)
    entered, release, outcomes = Event(), Event(), Queue()
    evaluate = sdk.evaluate

    def paused(user):
        raw = evaluate(user)
        entered.set()
        assert release.wait(5)
        return raw

    monkeypatch.setattr(sdk, "evaluate", paused)

    def invoke():
        try:
            if operation == "get":
                outcomes.put(sdk.get())
            else:
                outcomes.put(sdk.register(lambda result: None))
        except Exception as error:
            outcomes.put(error)

    caller = Thread(target=invoke, daemon=True)
    caller.start()
    try:
        assert entered.wait(5)
        if operation == "register":
            sdk.updates.publish()
        sdk._typed_configs.close()
    finally:
        release.set()
        caller.join(5)
    assert isinstance(outcomes.get(timeout=5), TypedConfigUnavailableError)
    assert not sdk._typed_configs._worker.is_alive()
    assert sdk._typed_configs.observers == []


def test_shutdown_waits_for_delivery_and_releases_registration_references(sdk):
    entered, release, closed = Event(), Event(), Event()

    def callback(result):
        entered.set()
        assert release.wait(5)

    callback_ref = ref(callback)
    sdk.register(callback)
    del callback
    sdk.publish(selected(2))
    assert entered.wait(5)

    def close():
        sdk._typed_configs.close()
        closed.set()

    closer = Thread(target=close)
    closer.start()
    try:
        assert not closed.wait(0.05)
    finally:
        release.set()
        closer.join(5)
    assert closed.is_set() and callback_ref() is None


def test_registration_requires_initialization_and_protobuf_arguments_are_local(sdk):
    sdk.initialized = False
    with pytest.raises(TypedConfigUnavailableError, match="Initialize"):
        sdk.register(lambda result: None)
    for message_type in (None, dict, Struct()):
        with pytest.raises(TypeError, match="Message"):
            sdk.get(message_type=message_type)
    with pytest.raises(TypeError, match="callable"):
        sdk.register(None)
    for method, arguments in (
        (Statsig.get_typed_config, (sdk, "config", sdk.user)),
        (Statsig.register_typed_config_callback, (sdk, "config", sdk.user, print)),
    ):
        with pytest.raises(TypeError, match="message_type"):
            method(*arguments)
        with pytest.raises(TypeError, match="decoder"):
            method(*arguments, message_type=Struct, decoder=dict)


def test_callbacks_can_register_without_replay_and_read_each_others_sdk():
    first, second = FakeSDK(), FakeSDK()
    entered, delivered, later = Barrier(2), Queue(), Queue()

    def callback(other):
        def receive(result):
            entered.wait(timeout=5)
            latest = other.get()
            other.register(later.put)
            delivered.put((result.details.version, latest.details.version))

        return receive

    first.register(callback(second))
    second.register(callback(first))
    try:
        first.publish(selected(2))
        second.publish(selected(2))
        assert [delivered.get(timeout=5) for _ in range(2)] == [(2, 2), (2, 2)]
        first.wait_for_observation()
        second.wait_for_observation()
        assert later.empty()
        first.publish(selected(3))
        second.publish(selected(3))
        assert [delivered.get(timeout=5) for _ in range(2)] == [(3, 3), (3, 3)]
        assert [later.get(timeout=5).details.version for _ in range(2)] == [3, 3]
    finally:
        closers = [
            Thread(target=sdk._typed_configs.close, daemon=True)
            for sdk in (first, second)
        ]
        for closer in closers:
            closer.start()
        for closer in closers:
            closer.join(5)
        assert all(not closer.is_alive() for closer in closers)
