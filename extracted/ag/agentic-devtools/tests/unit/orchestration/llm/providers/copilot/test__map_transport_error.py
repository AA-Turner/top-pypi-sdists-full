"""Tests for _map_transport_error()."""

from types import SimpleNamespace

from agentic_devtools.orchestration.llm.errors import AuthenticationError
from agentic_devtools.orchestration.llm.providers.copilot import _map_transport_error, _StatusError


def test_preserves_authentication_error_identity():
    auth = AuthenticationError("auth", provider_type="copilot")
    assert _map_transport_error(auth) is auth


def test_maps_401_and_403_to_authentication_error():
    assert _map_transport_error(SimpleNamespace(status_code=401)).provider_type == "copilot"
    assert _map_transport_error(SimpleNamespace(status_code=403)).provider_type == "copilot"


def test_maps_timeout_error_to_504():
    assert _map_transport_error(TimeoutError()).status_code == 504


def test_preserves_status_error_code():
    assert _map_transport_error(_StatusError("rate", 429)).status_code == 429
    assert _map_transport_error(_StatusError("bad", 418)).status_code == 418


def test_attaches_model_to_not_found_error():
    assert _map_transport_error(_StatusError("bad", 404), model="missing").model == "missing"
