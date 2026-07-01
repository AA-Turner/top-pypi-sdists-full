"""Tests for the Fluent Settings gRPC service (v1).

All tests share the single Fluent solver session started by the
``grpc_channel_and_metadata`` session fixture in ``conftest.py``.

A mixing-elbow case (mixing_elbow.cas.h5) is assumed to be loaded.
"""

import grpc
import pytest

from ansys.api.fluent.v1 import settings_pb2, settings_pb2_grpc

_ROOT = "fluent"

# ---------------------------------------------------------------------------
# Stub fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def stub(grpc_channel_and_metadata):
    channel, _ = grpc_channel_and_metadata
    return settings_pb2_grpc.SettingsStub(channel)


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _path(path: str) -> settings_pb2.PathInfo:
    return settings_pb2.PathInfo(root=_ROOT, path=path)


def value_to_python(v):
    """Unpack a settings Value to the corresponding Python object."""
    kind = v.WhichOneof("value")
    if kind == "boolean":
        return v.boolean
    if kind == "integer":
        return v.integer
    if kind == "real":
        return v.real
    if kind == "string":
        return v.string
    if kind == "value_list":
        return [value_to_python(item) for item in v.value_list.lsts]
    if kind == "value_map":
        return {k: value_to_python(val) for k, val in v.value_map.m.items()}
    return None


def test_get_schema_root_returns_info(stub, grpc_channel_and_metadata):
    """GetSchema at the root must return a Schema with a non-empty type."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetSchema(
        settings_pb2.GetSchemaRequest(root=_ROOT),
        metadata=metadata,
    )
    assert hasattr(resp, "info")
    assert len(resp.info.type) > 0


def test_get_schema_has_children(stub, grpc_channel_and_metadata):
    """Root schema must expose at least one child entry."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetSchema(
        settings_pb2.GetSchemaRequest(root=_ROOT),
        metadata=metadata,
    )
    assert len(resp.info.children) > 0


def test_get_schema_setup_path(stub, grpc_channel_and_metadata):
    """GetSchema for the 'setup' sub-tree must return a non-empty type."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetSchema(
        settings_pb2.GetSchemaRequest(root=_ROOT, optional_attrs=["type"]),
        metadata=metadata,
    )
    assert resp.info is not None


def test_get_state_returns_value(stub, grpc_channel_and_metadata):
    """GetState on a known scalar path must return a Value."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetState(
        settings_pb2.GetStateRequest(
            path_info=_path("/setup/general/operating-conditions/operating-pressure")
        ),
        metadata=metadata,
    )
    assert resp.value.WhichOneof("value") is not None


def test_get_state_energy_model(stub, grpc_channel_and_metadata):
    """GetState on the energy model path must return a boolean or map value."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetState(
        settings_pb2.GetStateRequest(
            path_info=_path("/setup/models/energy")
        ),
        metadata=metadata,
    )
    assert resp.value.WhichOneof("value") is not None


def test_get_state_value_is_typed(stub, grpc_channel_and_metadata):
    """The Value returned by GetState must be one of the defined oneof types."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetState(
        settings_pb2.GetStateRequest(
            path_info=_path("/setup/general/operating-conditions/operating-pressure")
        ),
        metadata=metadata,
    )
    valid_kinds = {"boolean", "integer", "real", "string", "value_list", "value_map"}
    assert resp.value.WhichOneof("value") in valid_kinds


def test_set_state_integer_roundtrip(stub, grpc_channel_and_metadata):
    """SetState must persist a new integer value that is confirmed by GetState."""
    _, metadata = grpc_channel_and_metadata
    path_info = _path("/setup/general/operating-conditions/operating-pressure")

    # Read original.
    orig_resp = stub.GetState(
        settings_pb2.GetStateRequest(path_info=path_info),
        metadata=metadata,
    )
    orig_val = orig_resp.value

    # Write a different value.
    new_int = 101000
    stub.SetState(
        settings_pb2.SetStateRequest(
            path_info=path_info,
            value=settings_pb2.Value(integer=new_int),
        ),
        metadata=metadata,
    )

    # Read back and verify.
    check_resp = stub.GetState(
        settings_pb2.GetStateRequest(path_info=path_info),
        metadata=metadata,
    )
    kind = check_resp.value.WhichOneof("value")
    assert kind in ("integer", "real"), f"Unexpected kind after SetState: {kind}"
    readback = check_resp.value.integer if kind == "integer" else int(check_resp.value.real)
    assert readback == new_int, f"Expected {new_int}, got {readback}"

    # Restore original.
    stub.SetState(
        settings_pb2.SetStateRequest(path_info=path_info, value=orig_val),
        metadata=metadata,
    )


def test_get_object_names_returns_list(stub, grpc_channel_and_metadata):
    """GetObjectNames must return a (possibly empty) list of strings."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetObjectNames(
        settings_pb2.GetObjectNamesRequest(
            path_info=_path("/setup/boundary-conditions/wall")
        ),
        metadata=metadata,
    )
    assert isinstance(list(resp.names), list)


def test_get_object_names_contour_returns_list(stub, grpc_channel_and_metadata):
    """GetObjectNames on results/graphics/contour must return a list."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetObjectNames(
        settings_pb2.GetObjectNamesRequest(
            path_info=_path("/results/graphics/contour")
        ),
        metadata=metadata,
    )
    assert isinstance(list(resp.names), list)


def test_get_list_size_returns_non_negative(stub, grpc_channel_and_metadata):
    """GetListSize must return a non-negative integer."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetListSize(
        settings_pb2.GetListSizeRequest(
            path_info=_path("/results/graphics/lighting/lights")
        ),
        metadata=metadata,
    )
    assert isinstance(resp.size, int)
    assert resp.size >= 0


def test_create_and_delete_contour_lifecycle(stub, grpc_channel_and_metadata):
    """CreateObject must add an entry visible via GetObjectNames; DeleteObject removes it."""
    _, metadata = grpc_channel_and_metadata
    path_info = _path("/results/graphics/contour")
    obj_name = "test-contour-ci"

    stub.CreateObject(
        settings_pb2.CreateObjectRequest(path_info=path_info, name=obj_name),
        metadata=metadata,
    )

    names_resp = stub.GetObjectNames(
        settings_pb2.GetObjectNamesRequest(path_info=path_info),
        metadata=metadata,
    )
    assert obj_name in names_resp.names, (
        f"Created object '{obj_name}' not found in names: {list(names_resp.names)}"
    )

    stub.DeleteObject(
        settings_pb2.DeleteObjectRequest(path_info=path_info, name=obj_name),
        metadata=metadata,
    )

    names_after = stub.GetObjectNames(
        settings_pb2.GetObjectNamesRequest(path_info=path_info),
        metadata=metadata,
    )
    assert obj_name not in names_after.names, (
        f"Deleted object '{obj_name}' still present in names"
    )


def test_rename_object_lifecycle(stub, grpc_channel_and_metadata):
    """Create → Rename → Delete: the renamed object must appear under its new name."""
    _, metadata = grpc_channel_and_metadata
    path_info = _path("/results/graphics/contour")
    original_name = "rename-src-ci"
    new_name = "rename-dst-ci"

    stub.CreateObject(
        settings_pb2.CreateObjectRequest(path_info=path_info, name=original_name),
        metadata=metadata,
    )

    stub.Rename(
        settings_pb2.RenameRequest(
            path_info=path_info,
            old_name=original_name,
            new_name=new_name,
        ),
        metadata=metadata,
    )

    names_resp = stub.GetObjectNames(
        settings_pb2.GetObjectNamesRequest(path_info=path_info),
        metadata=metadata,
    )
    assert new_name in names_resp.names, (
        f"Renamed object '{new_name}' not found after Rename"
    )
    assert original_name not in names_resp.names, (
        f"Original name '{original_name}' still present after Rename"
    )

    stub.DeleteObject(
        settings_pb2.DeleteObjectRequest(path_info=path_info, name=new_name),
        metadata=metadata,
    )


def test_execute_command_returns_reply(stub, grpc_channel_and_metadata):
    """ExecuteCommand must return an ExecuteCommandResponse with a reply field."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.ExecuteCommand(
        settings_pb2.ExecuteCommandRequest(
            path_info=_path("/solution/run-calculation"),
            command="iterate",
            args=settings_pb2.Value(value_map=settings_pb2.Value.ValueMap(
                m={"number-of-iterations": settings_pb2.Value(integer=0)}
            )),
        ),
        metadata=metadata,
    )
    assert hasattr(resp, "reply")


def test_execute_query_returns_reply(stub, grpc_channel_and_metadata):
    """ExecuteQuery must return an ExecuteQueryResponse with a reply field."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.ExecuteQuery(
        settings_pb2.ExecuteQueryRequest(
            path_info=_path("/setup/models/system-coupling"),
            query="get-tensor-type",
            args=settings_pb2.Value(),
        ),
        metadata=metadata,
    )
    assert hasattr(resp, "reply")


def test_execute_query_reply_is_typed(stub, grpc_channel_and_metadata):
    """The reply from ExecuteQuery must carry a recognised Value oneof type."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.ExecuteQuery(
        settings_pb2.ExecuteQueryRequest(
            path_info=_path("/setup/models/system-coupling"),
            query="get-tensor-type",
            args=settings_pb2.Value(),
        ),
        metadata=metadata,
    )
    valid_kinds = {"boolean", "integer", "real", "string", "value_list", "value_map", None}
    assert resp.reply.WhichOneof("value") in valid_kinds


def test_get_attrs_returns_values(stub, grpc_channel_and_metadata):
    """GetAttrs must return a GetAttrsResponse with a values field."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetAttrs(
        settings_pb2.GetAttrsRequest(
            path_info=_path("/setup/models/energy"),
            attrs=["type", "active?", "read-only?"],
            recursive=False,
        ),
        metadata=metadata,
    )
    assert hasattr(resp, "values")


def test_get_attrs_value_map_has_keys(stub, grpc_channel_and_metadata):
    """GetAttrs response values must be a value_map containing the requested attrs."""
    _, metadata = grpc_channel_and_metadata
    requested = ["type", "active?", "read-only?"]
    resp = stub.GetAttrs(
        settings_pb2.GetAttrsRequest(
            path_info=_path("/setup/models/energy"),
            attrs=requested,
            recursive=False,
        ),
        metadata=metadata,
    )
    assert resp.values.WhichOneof("value") == "value_map"
    returned_keys = set(resp.values.value_map.m.keys())
    for attr in requested:
        assert attr in returned_keys, f"Attribute '{attr}' missing from GetAttrs response"


def test_get_attrs_recursive_has_group_children(stub, grpc_channel_and_metadata):
    """GetAttrs with recursive=True must populate group_children."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetAttrs(
        settings_pb2.GetAttrsRequest(
            path_info=_path("/setup/models"),
            attrs=["type"],
            recursive=True,
        ),
        metadata=metadata,
    )
    assert hasattr(resp, "group_children")
    assert len(resp.group_children) > 0


def test_is_wildcard_star_returns_true(stub, grpc_channel_and_metadata):
    """'*' is universally recognised as a wildcard."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.IsWildcard(
        settings_pb2.IsWildcardRequest(input="*"),
        metadata=metadata,
    )
    assert resp.is_wildcard is True


def test_is_wildcard_plain_string_returns_false(stub, grpc_channel_and_metadata):
    """A plain alphanumeric string must not be treated as a wildcard."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.IsWildcard(
        settings_pb2.IsWildcardRequest(input="cold-inlet"),
        metadata=metadata,
    )
    assert resp.is_wildcard is False


def test_is_wildcard_question_mark(stub, grpc_channel_and_metadata):
    """'?' is a common wildcard character; is_wildcard must be a bool."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.IsWildcard(
        settings_pb2.IsWildcardRequest(input="?"),
        metadata=metadata,
    )
    assert isinstance(resp.is_wildcard, bool)


def test_is_wildcard_empty_string(stub, grpc_channel_and_metadata):
    """An empty string must return a bool response without error."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.IsWildcard(
        settings_pb2.IsWildcardRequest(input=""),
        metadata=metadata,
    )
    assert isinstance(resp.is_wildcard, bool)
