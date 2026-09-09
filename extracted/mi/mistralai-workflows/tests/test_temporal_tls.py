import pytest
from temporalio.service import TLSConfig

from mistralai.workflows.core.temporal.temporal_client import _resolve_temporal_tls
from mistralai.workflows.exceptions import ErrorCode, WorkflowsException


@pytest.mark.parametrize("tls", [False, True])
def test_resolve_returns_plain_flag_without_pinned_ca(tls):
    assert _resolve_temporal_tls(tls, None) is tls


def test_resolve_pins_configured_ca(ca_file, ca_pem):
    resolved = _resolve_temporal_tls(True, ca_file())

    assert isinstance(resolved, TLSConfig)
    assert resolved.server_root_ca_cert == ca_pem


def test_resolve_raises_when_tls_is_off(ca_file):
    # A pinned CA that is quietly dropped would connect in the clear to the endpoint it was
    # meant to pin, so the mismatch is fatal rather than a warning.
    with pytest.raises(WorkflowsException) as excinfo:
        _resolve_temporal_tls(False, ca_file())
    assert excinfo.value.code == ErrorCode.TEMPORAL_CONNECTION_ERROR


def test_resolve_raises_when_ca_file_missing(ca_file):
    # Must not silently fall back to the default roots when a CA was explicitly pinned.
    with pytest.raises(WorkflowsException) as excinfo:
        _resolve_temporal_tls(True, ca_file(write=False))
    assert excinfo.value.code == ErrorCode.TEMPORAL_CONNECTION_ERROR


def test_resolve_raises_when_ca_file_empty(ca_file):
    with pytest.raises(WorkflowsException) as excinfo:
        _resolve_temporal_tls(True, ca_file(b"   \n"))
    assert excinfo.value.code == ErrorCode.TEMPORAL_CONNECTION_ERROR


def test_resolve_raises_when_ca_file_is_not_pem(ca_file):
    with pytest.raises(WorkflowsException) as excinfo:
        _resolve_temporal_tls(True, ca_file(b'{"not": "a certificate"}'))
    assert excinfo.value.code == ErrorCode.TEMPORAL_CONNECTION_ERROR


def test_resolve_raises_when_pem_envelope_holds_garbage(ca_file):
    # The envelope alone is not proof of a usable CA; Temporal's Rust core would only report this
    # as an opaque connection error.
    contents = b"-----BEGIN CERTIFICATE-----\nnot-a-real-cert\n-----END CERTIFICATE-----\n"
    with pytest.raises(WorkflowsException) as excinfo:
        _resolve_temporal_tls(True, ca_file(contents))
    assert excinfo.value.code == ErrorCode.TEMPORAL_CONNECTION_ERROR


def test_resolve_raises_when_ca_path_is_not_a_valid_path():
    # A NUL byte makes read_bytes() raise ValueError, not OSError.
    with pytest.raises(WorkflowsException) as excinfo:
        _resolve_temporal_tls(True, "/tmp/ca\0.crt")
    assert excinfo.value.code == ErrorCode.TEMPORAL_CONNECTION_ERROR
