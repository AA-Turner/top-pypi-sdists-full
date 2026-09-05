import json
from time import sleep
from typing import Optional
import pytest

from statsig_python_core import (
    DataStore,
    StatsigOptions,
    StatsigUser,
    Statsig,
    DataStoreResponse,
    DataStoreBytesResponse,
    DataStoreGetBytesRequest,
)
from pytest_httpserver import HTTPServer
from utils import get_test_data_resource, get_test_data_resource_bytes

known_lcut = 1767981029384

dcs_content = get_test_data_resource("eval_proj_dcs.json")
json_data = json.loads(dcs_content)
eval_proj_protobuf = get_test_data_resource_bytes("eval_proj_dcs.pb.br")

del json_data["checksum"]
NO_UPDATE_BYTES_RESPONSE = json.dumps({"has_updates": False}).encode()

updated_dcs_json_data = json_data.copy()
if "time" in updated_dcs_json_data:
    updated_dcs_json_data["time"] += 10


class MockDataStore(DataStore):
    VERBOSE = False

    def __init__(self, test_param: str = ""):
        super().__init__()
        self.test_param = test_param
        self.init_called = False
        self.content_set = None
        self.get_called_count = 0
        self.should_poll = False
        self.initialize_fn = self.initialize
        self.shutdown_fn = self.shutdown
        self.get_fn = self.get
        self.set_fn = self.set
        self.support_polling_updates_for_fn = self.support_polling_updates_for
        self.get_bytes_fn = None
        self.set_bytes_fn = None

    def initialize(self):
        self.init_called = True
        self._log("Initializing MockDataStore")

    def shutdown(self):
        self._log("Shutting down MockDataStore")

    def get(self, key: str) -> Optional[DataStoreResponse]:
        self._log(f"Getting value for key: {key}")
        self.get_called_count += 1
        return DataStoreResponse(result=dcs_content, time=1234567890)

    def set(self, key: str, value: str, time: Optional[int] = None):
        self.content_set = value
        self._log(f"Setting value for key: {key}")

    def support_polling_updates_for(self, key: str) -> bool:
        self._log(
            f"Checking if polling updates are supported for key: {key}: should_poll={self.should_poll}"
        )
        return self.should_poll

    def _log(self, message: str):
        if self.VERBOSE:
            print(message)


class MockBytesDataStore(DataStore):
    VERBOSE = False

    def __init__(self, test_param: str = ""):
        super().__init__()
        self.test_param = test_param
        self.init_called = False
        self.content_set = None
        self.stored_time = 1767981029384
        self.stored_checksum = "8506699639233708000"
        self.get_called_count = 0
        self.get_bytes_called_count = 0
        self.get_bytes_requests = []
        self.set_called_count = 0
        self.set_bytes_called_count = 0
        self.returned_no_update = False
        self.should_poll = False
        self.initialize_fn = self.initialize
        self.shutdown_fn = self.shutdown
        self.get_fn = self.get
        self.set_fn = self.set
        self.get_bytes_fn = self.get_bytes
        self.set_bytes_fn = self.set_bytes
        self.support_polling_updates_for_fn = self.support_polling_updates_for

    def initialize(self):
        self.init_called = True
        self._log("Initializing MockBytesDataStore")

    def shutdown(self):
        self._log("Shutting down MockBytesDataStore")

    def get(self, key: str) -> Optional[DataStoreResponse]:
        self.get_called_count += 1
        return None

    def set(self, key: str, value: str, time: Optional[int] = None):
        self.set_called_count += 1
        self._log(f"Setting value for key via string path: {key}")

    def get_bytes(
        self,
        key: str,
        request: Optional[DataStoreGetBytesRequest] = None,
    ) -> Optional[DataStoreBytesResponse]:
        self._log(f"Getting bytes for key: {key}")
        self.get_bytes_called_count += 1
        self.get_bytes_requests.append(request)
        if request is not None and request.checksum is not None and request.checksum == self.stored_checksum:
            self.returned_no_update = True
            return DataStoreBytesResponse(
                result=NO_UPDATE_BYTES_RESPONSE,
                time=request.since_time,
                checksum=request.checksum,
                has_updates=False,
            )
        return DataStoreBytesResponse(result=eval_proj_protobuf, time=1234567890, checksum=self.stored_checksum)

    def set_bytes(
        self,
        key: str,
        value: bytes,
        time: Optional[int] = None,
        checksum: Optional[str] = None,
    ):
        self.content_set = value
        self.stored_time = time
        self.stored_checksum = checksum
        self.set_bytes_called_count += 1
        self._log(f"Setting bytes for key: {key}")

    def support_polling_updates_for(self, key: str) -> bool:
        self._log(
            f"Checking if polling updates are supported for key: {key}: should_poll={self.should_poll}"
        )
        return self.should_poll

    def _log(self, message: str):
        if self.VERBOSE:
            print(message)


@pytest.fixture
def statsig_setup(httpserver: HTTPServer):
    data_store = MockDataStore(test_param="test_param")

    httpserver.expect_request(
        "/v2/download_config_specs"
    ).respond_with_json(updated_dcs_json_data)
    httpserver.expect_request("/v1/log_event").respond_with_json({"success": True})

    options = StatsigOptions(
        specs_url=httpserver.url_for("/v2/download_config_specs"),
        log_event_url=httpserver.url_for("/v1/log_event"),
        data_store=data_store,
        specs_sync_interval_ms=1,
    )

    statsig = Statsig("secret-key", options)
    user = StatsigUser(user_id="test_user_id")

    yield statsig, data_store, user

    statsig.shutdown().wait()


@pytest.fixture
def statsig_bytes_setup(httpserver: HTTPServer):
    data_store = MockBytesDataStore(test_param="test_param")

    httpserver.expect_request(
        "/v2/download_config_specs"
    ).respond_with_json(updated_dcs_json_data)
    httpserver.expect_request("/v1/log_event").respond_with_json({"success": True})

    options = StatsigOptions(
        specs_url=httpserver.url_for("/v2/download_config_specs"),
        log_event_url=httpserver.url_for("/v1/log_event"),
        data_store=data_store,
        specs_sync_interval_ms=1,
    )

    statsig = Statsig("secret-key", options)
    user = StatsigUser(user_id="test_user_id")

    yield statsig, data_store, user

    statsig.shutdown().wait()


def test_data_store_usage_get_with_test_param():
    data_store = MockDataStore(test_param="test_param")
    assert data_store.test_param == "test_param"


def test_data_store_usage_get(statsig_setup):
    statsig, data_store, user = statsig_setup
    data_store.should_poll = True
    statsig.initialize().wait()

    gate = statsig.get_feature_gate(user, "test_public")

    statsig.flush_events().wait()

    assert data_store.init_called
    assert gate.details.reason == "Adapter(DataStore):Recognized"
    assert gate.value == True
    assert gate.details.lcut == known_lcut

    for _ in range(100):
        if data_store.get_called_count >= 2:
            break
        sleep(0.05)

    assert data_store.get_called_count > 1


def test_data_store_usage_set(statsig_setup):
    statsig, data_store, user = statsig_setup
    data_store.should_poll = False
    statsig.initialize().wait()

    gate = statsig.get_feature_gate(user, "test_public")

    assert data_store.init_called
    assert gate.details.reason == "Adapter(DataStore):Recognized"
    sleep(1)

    gate_after = statsig.get_feature_gate(user, "test_public")
    statsig.flush_events().wait()

    assert gate_after.value == True
    assert gate_after.details.lcut == known_lcut + 10
    assert data_store.get_called_count == 1
    assert data_store.content_set is not None
    assert json.loads(data_store.content_set) == updated_dcs_json_data


def test_data_store_usage_get_bytes(statsig_bytes_setup):
    statsig, data_store, user = statsig_bytes_setup
    statsig.initialize().wait()

    gate = statsig.get_feature_gate(user, "test_public")

    statsig.flush_events().wait()

    assert data_store.init_called
    assert gate.details.reason == "Adapter(DataStore):Recognized"
    assert gate.value == True
    assert gate.details.lcut == known_lcut

    for _ in range(5):
        if data_store.set_bytes_called_count > 0:
            break
        sleep(0.05)

    assert data_store.get_bytes_called_count >= 1
    assert data_store.get_called_count == 0
    assert data_store.set_bytes_called_count > 0


def test_data_store_usage_get_bytes_request_has_since_time_after_initial_poll(statsig_bytes_setup):
    statsig, data_store, user = statsig_bytes_setup
    data_store.should_poll = True
    statsig.initialize().wait()

    gate = statsig.get_feature_gate(user, "test_public")
    assert gate.details.reason == "Adapter(DataStore):Recognized"

    for _ in range(100):
        if data_store.get_bytes_called_count >= 2:
            break
        sleep(0.05)

    assert data_store.get_bytes_called_count >= 2

    first_request = data_store.get_bytes_requests[0]
    second_request = data_store.get_bytes_requests[1]

    assert isinstance(first_request, DataStoreGetBytesRequest)
    assert first_request.since_time is None
    assert first_request.checksum is None
    assert isinstance(second_request, DataStoreGetBytesRequest)
    assert second_request.since_time is not None


def test_data_store_usage_get_bytes_request_checksum_match_returns_no_update(statsig_bytes_setup):
    statsig, data_store, user = statsig_bytes_setup
    data_store.should_poll = True
    statsig.initialize().wait()

    gate = statsig.get_feature_gate(user, "test_public")
    assert gate.details.reason == "Adapter(DataStore):Recognized"

    for _ in range(100):
        if data_store.get_bytes_called_count >= 2:
            break
        sleep(0.05)

    assert data_store.get_bytes_called_count >= 2
    assert data_store.returned_no_update

    request_with_checksum = next(
        request
        for request in data_store.get_bytes_requests
        if request is not None and request.checksum is not None
    )
    assert request_with_checksum.checksum == data_store.stored_checksum
    assert request_with_checksum.since_time == data_store.stored_time

    # no second write should occur when server responds with {"has_updates": false}
    for _ in range(100):
        if data_store.get_bytes_called_count > 2:
            break
        sleep(0.05)



def test_data_store_usage_set_bytes(statsig_bytes_setup):
    statsig, data_store, user = statsig_bytes_setup
    data_store.should_poll = False
    statsig.initialize().wait()

    gate = statsig.get_feature_gate(user, "test_public")

    assert data_store.init_called
    assert gate.details.reason == "Adapter(DataStore):Recognized"
    sleep(1)

    gate_after = statsig.get_feature_gate(user, "test_public")
    statsig.flush_events().wait()

    assert gate_after.value == True
    assert gate_after.details.lcut == known_lcut + 10
    assert data_store.get_bytes_called_count == 1
    assert data_store.set_bytes_called_count > 0
    assert data_store.content_set is not None
    assert json.loads(data_store.content_set) == updated_dcs_json_data
