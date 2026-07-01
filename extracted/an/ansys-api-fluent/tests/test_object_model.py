"""Tests for the Fluent ObjectModel gRPC service (v1).

All tests share the single Fluent session started by the ``grpc_channel_and_metadata``
session fixture in ``conftest.py``.
"""

import grpc
import pytest
from ansys.fluent.core import examples

from ansys.api.fluent.v1 import object_model_pb2, object_model_pb2_grpc, variant_pb2

_RULES = "meshing"
_VALID_SUBSCRIPTION_STATUSES = {
    object_model_pb2.SUBSCRIPTION_STATUS_UNSPECIFIED,
    object_model_pb2.SUBSCRIPTION_STATUS_SUBSCRIBED,
    object_model_pb2.SUBSCRIPTION_STATUS_UNSUBSCRIBED,
}


@pytest.fixture(scope="module")
def stub(grpc_channel_and_metadata_meshing):
    channel, _ = grpc_channel_and_metadata_meshing
    return object_model_pb2_grpc.ObjectModelStub(channel)

@pytest.fixture(scope="module")
def solver_stub(grpc_channel_and_metadata):
    channel, _ = grpc_channel_and_metadata
    return object_model_pb2_grpc.ObjectModelStub(channel)


def test_get_schema_returns_info(stub, grpc_channel_and_metadata_meshing):
    """GetSchema must return a Schema info object."""
    _, metadata = grpc_channel_and_metadata_meshing
    resp = stub.GetSchema(
        object_model_pb2.GetSchemaRequest(rules=_RULES),
        metadata=metadata,
    )
    assert hasattr(resp, "info")
    assert len(resp.info.singletons) > 0 or len(resp.info.named_objects) > 0


def test_get_state_known_path_returns_variant(stub, grpc_channel_and_metadata_meshing):
    """GetState on a known sub-path must return a Variant."""
    _, metadata = grpc_channel_and_metadata_meshing
    resp = stub.GetState(
        object_model_pb2.GetStateRequest(
            rules=_RULES, path="/GlobalSettings/EnableCleanCAD"
        ),
        metadata=metadata,
    )
    assert hasattr(resp, "state")
    assert resp.state.WhichOneof("as") is not None


def test_set_state_bool_roundtrip(stub, grpc_channel_and_metadata_meshing):
    """SetState followed by GetState must reflect the written value."""
    _, metadata = grpc_channel_and_metadata_meshing
    path = "/GlobalSettings/EnableCleanCAD"
    # Read original value.
    orig = stub.GetState(
        object_model_pb2.GetStateRequest(rules=_RULES, path=path),
        metadata=metadata,
    ).state.bool_state

    # Write the opposite value.
    stub.SetState(
        object_model_pb2.SetStateRequest(
            rules=_RULES,
            path=path,
            state=variant_pb2.Variant(bool_state=not orig),
            wait=True,
        ),
        metadata=metadata,
    )

    # Read back.
    new_val = stub.GetState(
        object_model_pb2.GetStateRequest(rules=_RULES, path=path),
        metadata=metadata,
    ).state.bool_state
    assert new_val == (not orig)

    # Restore.
    stub.SetState(
        object_model_pb2.SetStateRequest(
            rules=_RULES,
            path=path,
            state=variant_pb2.Variant(bool_state=orig),
            wait=True,
        ),
        metadata=metadata,
    )


def test_get_attribute_value_returns_result(stub, grpc_channel_and_metadata_meshing):
    """GetAttributeValue must return a result Variant."""
    _, metadata = grpc_channel_and_metadata_meshing
    resp = stub.GetAttributeValue(
        object_model_pb2.GetAttributeValueRequest(
            rules=_RULES,
            path="/GlobalSettings/EnableCleanCAD",
            attribute="default",
        ),
        metadata=metadata,
    )
    assert hasattr(resp, "result")
    assert resp.result.bool_state in (True, False)


def test_named_object_lifecycle(solver_stub, grpc_channel_and_metadata):
    """CreateObject followed by DeleteObject must succeed without error."""
    _, metadata = grpc_channel_and_metadata
    obj_path = "/Case/Results/Graphics/Contour"
    obj_name = "contour-1"
    create_resp = solver_stub.CreateObject(
        object_model_pb2.CreateObjectRequest(
            rules="flserver", path=obj_path, name=obj_name
        ),
        metadata=metadata,
    )
    assert hasattr(create_resp, "state")

    create_resp = solver_stub.CreateObject(
        object_model_pb2.CreateObjectRequest(
            rules="flserver", path=obj_path, name="contour-2"
        ),
        metadata=metadata,
    )
    assert hasattr(create_resp, "state")

    resp = solver_stub.GetObjectNames(
        object_model_pb2.GetObjectNamesRequest(rules="flserver", path="/Case/Results/Graphics/Contour"),
        metadata=metadata,
    )
    assert isinstance(list(resp.names), list)
    assert list(resp.names) == [obj_name, "contour-2"]

    new_name = "contour-renamed"
    resp = solver_stub.Rename(
            object_model_pb2.RenameRequest(
                rules="flserver",
                path=f"{obj_path}:{obj_name}",
                new_name=new_name,
            ),
            metadata=metadata,
        )
    assert hasattr(resp, "state")

    # resp = solver_stub.GetObjectNames(
    #     object_model_pb2.GetObjectNamesRequest(rules="flserver", path="/Case/Results/Graphics/Contour"),
    #     metadata=metadata,
    # )
    # assert isinstance(list(resp.names), list)
    # assert list(resp.names) == [new_name, "contour-2"]

    delete_resp = solver_stub.DeleteObject(
        object_model_pb2.DeleteObjectRequest(
            rules="flserver", path=f"{obj_path}:{new_name}", wait=True
        ),
        metadata=metadata,
    )
    assert hasattr(delete_resp, "state")

    resp = solver_stub.GetObjectNames(
        object_model_pb2.GetObjectNamesRequest(rules="flserver", path="/Case/Results/Graphics/Contour"),
        metadata=metadata,
    )
    assert isinstance(list(resp.names), list)
    assert list(resp.names) == ["contour-2"]

    # Clean -up
    delete_resp = solver_stub.DeleteObject(
        object_model_pb2.DeleteObjectRequest(
            rules="flserver", path=f"{obj_path}:contour-2", wait=True
        ),
        metadata=metadata,
    )
    assert hasattr(delete_resp, "state")

    resp = solver_stub.GetObjectNames(
        object_model_pb2.GetObjectNamesRequest(rules="flserver", path="/Case/Results/Graphics/Contour"),
        metadata=metadata,
    )
    assert isinstance(list(resp.names), list)
    assert list(resp.names) == []


def test_create_and_delete_command_arguments(stub, grpc_channel_and_metadata_meshing):
    """CreateCommandArguments must return a command_id; DeleteCommandArguments must clean it up."""
    _, metadata = grpc_channel_and_metadata_meshing
    create_resp = stub.CreateCommandArguments(
        object_model_pb2.CreateCommandArgumentsRequest(
            rules=_RULES, path="", command="ImportGeometry"
        ),
        metadata=metadata,
    )
    assert isinstance(create_resp.command_id, str)
    assert len(create_resp.command_id) > 0

    stub.DeleteCommandArguments(
        object_model_pb2.DeleteCommandArgumentsRequest(
            rules=_RULES,
            path="",
            command="ImportGeometry",
            command_id=create_resp.command_id,
        ),
        metadata=metadata,
    )


def test_execute_command_returns_response(stub, grpc_channel_and_metadata_meshing):
    """ExecuteCommand must return a response with result and state fields."""
    _, metadata = grpc_channel_and_metadata_meshing
    file_name = examples.download_file(
        file_name="mixing_elbow.pmdb", directory="pyfluent/mixing_elbow"
    )
    cmd_args = variant_pb2.Variant(
            variant_map_state=variant_pb2.VariantMap(
                item={
                    "FileName": variant_pb2.Variant(string_state=file_name),
                }
            )
        )
    resp = stub.ExecuteCommand(
        object_model_pb2.ExecuteCommandRequest(
            rules=_RULES,
            path="",
            command="ImportGeometry",
            wait=True,
            args=cmd_args,
        ),
        metadata=metadata,
    )
    assert hasattr(resp, "result")
    assert hasattr(resp, "state")


def test_subscribe_and_unsubscribe_events(stub, grpc_channel_and_metadata_meshing):
    """SubscribeEvents must return subscription tags; UnsubscribeEvents must remove them."""
    _, metadata = grpc_channel_and_metadata_meshing
    sub_resp = stub.SubscribeEvents(
        object_model_pb2.SubscribeEventsRequest(
            event_requests=[
                object_model_pb2.ObjectModelEventRequest(
                    rules=_RULES,
                    modified_event_request=object_model_pb2.ModifiedEventRequest(
                        path="/GlobalSettings/EnableCleanCAD"
                    ),
                )
            ]
        ),
        metadata=metadata,
    )
    assert len(sub_resp.responses) > 0
    tags = [r.tag for r in sub_resp.responses]
    assert all(len(t) > 0 for t in tags)
    for r in sub_resp.responses:
        assert r.status == object_model_pb2.SUBSCRIPTION_STATUS_SUBSCRIBED

    unsub_resp = stub.UnsubscribeEvents(
        object_model_pb2.UnsubscribeEventsRequest(tags=tags),
        metadata=metadata,
    )
    for r in unsub_resp.responses:
        assert r.status == object_model_pb2.SUBSCRIPTION_STATUS_UNSUBSCRIBED


def test_stream_events_can_be_cancelled(stub, grpc_channel_and_metadata_meshing):
    """StreamEvents stream must open without error and be cancellable."""
    _, metadata = grpc_channel_and_metadata_meshing
    # Subscribe first so there is at least one active subscription.
    sub_resp = stub.SubscribeEvents(
        object_model_pb2.SubscribeEventsRequest(
            event_requests=[
                object_model_pb2.ObjectModelEventRequest(
                    rules=_RULES,
                    modified_event_request=object_model_pb2.ModifiedEventRequest(
                        path="/GlobalSettings/EnableCleanCAD"
                    ),
                )
            ]
        ),
        metadata=metadata,
    )
    tags = [r.tag for r in sub_resp.responses]

    stream = stub.StreamEvents(
        object_model_pb2.StreamEventsRequest(), metadata=metadata
    )
    assert stream is not None
    stream.cancel()

    # Cleanup subscriptions.
    stub.UnsubscribeEvents(
        object_model_pb2.UnsubscribeEventsRequest(tags=tags),
        metadata=metadata,
    )


def test_stream_state_changes_returns_stream(stub, grpc_channel_and_metadata_meshing):
    """StreamStateChanges must open a server-streaming iterator."""
    _, metadata = grpc_channel_and_metadata_meshing
    stream = stub.StreamStateChanges(
        object_model_pb2.StreamStateChangesRequest(
            rules=_RULES,
            return_state_changes=True,
            diff_state=object_model_pb2.DIFF_STATE_FULL,
        ),
        metadata=metadata,
    )
    assert stream is not None
    stream.cancel()


def test_stream_state_changes_first_response_has_state(stub, grpc_channel_and_metadata_meshing):
    """The first StreamStateChanges response must include a state field."""
    _, metadata = grpc_channel_and_metadata_meshing
    try:
        stream = stub.StreamStateChanges(
            object_model_pb2.StreamStateChangesRequest(
                rules=_RULES,
                return_state_changes=True,
                diff_state=object_model_pb2.DIFF_STATE_NOCOMMANDS,
            ),
            metadata=metadata,
        )
        first = next(iter(stream))
        stream.cancel()
        assert hasattr(first, "state")
        assert isinstance(list(first.deleted_paths), list)
        assert isinstance(list(first.events), list)
    except StopIteration:
        pytest.fail("StreamStateChanges ended without sending any response")
