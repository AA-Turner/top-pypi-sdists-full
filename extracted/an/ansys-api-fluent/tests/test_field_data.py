"""Tests for the Fluent FieldData gRPC service (v1).

All tests share the single Fluent solver session started by the
``grpc_channel_and_metadata`` session fixture in ``conftest.py``.

The mixing-elbow case (mixing_elbow.cas.h5) is assumed to be loaded in the
solver session.  Surface zone names and cell zone names match that case.
"""

import grpc
import pytest

from ansys.api.fluent.v1 import field_data_pb2, field_data_pb2_grpc


# ---------------------------------------------------------------------------
# Stub fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def stub(grpc_channel_and_metadata):
    channel, _ = grpc_channel_and_metadata
    return field_data_pb2_grpc.FieldDataStub(channel)


def _first_chunk(stream):
    """Return the first chunk from a server-streaming call, then cancel."""
    try:
        chunk = next(iter(stream))
        stream.cancel()
        return chunk
    except StopIteration:
        return None


# ---------------------------------------------------------------------------
# Discovery fixtures — module-scoped so results are reused across tests
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def surfaces_info(stub, grpc_channel_and_metadata):
    """Return list[SurfaceInfo] from GetSurfacesInfo (may be empty)."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetSurfacesInfo(
        field_data_pb2.GetSurfacesInfoRequest(), metadata=metadata
    )
    return list(resp.surface_info)


@pytest.fixture(scope="module")
def fields_info(stub, grpc_channel_and_metadata):
    """Return list[FieldInfo] from GetFieldsInfo (may be empty)."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetFieldsInfo(
        field_data_pb2.GetFieldsInfoRequest(), metadata=metadata
    )
    return list(resp.field_info)


@pytest.fixture(scope="module")
def vector_fields_info(stub, grpc_channel_and_metadata):
    """Return list[VectorFieldInfo] from GetVectorFieldsInfo (may be empty)."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetVectorFieldsInfo(
        field_data_pb2.GetVectorFieldsInfoRequest(), metadata=metadata
    )
    return list(resp.vector_field_info)


def test_is_data_available_returns_bool(stub, grpc_channel_and_metadata):
    """IsDataAvailable must return a bool response without error."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.IsDataAvailable(
        field_data_pb2.IsDataAvailableRequest(), metadata=metadata
    )
    assert isinstance(resp.is_data_available, bool)
    assert resp.is_data_available is True  # since data was read in the fixture


def test_is_boundary_values_enabled_returns_bool(stub, grpc_channel_and_metadata):
    """IsBoundaryValuesEnabled must return a bool response without error."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.IsBoundaryValuesEnabled(
        field_data_pb2.IsBoundaryValuesEnabledRequest(), metadata=metadata
        )
    assert isinstance(resp.is_boundary_values_enabled, bool)


def test_get_surfaces_info_returns_list(stub, grpc_channel_and_metadata):
    """GetSurfacesInfo must return a list of SurfaceInfo entries."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetSurfacesInfo(
        field_data_pb2.GetSurfacesInfoRequest(), metadata=metadata
    )
    assert hasattr(resp, "surface_info")
    assert isinstance(list(resp.surface_info), list)


def test_get_surfaces_info_entries_have_name(stub, grpc_channel_and_metadata, surfaces_info):
    """Each SurfaceInfo entry must have a non-empty surface_name."""
    for info in surfaces_info:
        assert len(info.surface_name) > 0


def test_get_surfaces_info_entries_have_surface_ids(stub, grpc_channel_and_metadata, surfaces_info):
    """Each SurfaceInfo entry must expose at least one surface id."""
    for info in surfaces_info:
        assert len(info.surface_ids) > 0


def test_get_fields_info_returns_list(stub, grpc_channel_and_metadata):
    """GetFieldsInfo must return a list of FieldInfo entries."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetFieldsInfo(
        field_data_pb2.GetFieldsInfoRequest(), metadata=metadata
    )
    assert hasattr(resp, "field_info")
    assert isinstance(list(resp.field_info), list)


def test_get_fields_info_entries_have_solver_name(stub, grpc_channel_and_metadata, fields_info):
    """Each FieldInfo entry must have a non-empty solver_name."""
    for fi in fields_info:
        assert len(fi.solver_name) > 0


def test_get_vector_fields_info_returns_list(stub, grpc_channel_and_metadata):
    """GetVectorFieldsInfo must return a list of VectorFieldInfo entries."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetVectorFieldsInfo(
        field_data_pb2.GetVectorFieldsInfoRequest(), metadata=metadata
    )
    assert hasattr(resp, "vector_field_info")
    assert isinstance(list(resp.vector_field_info), list)


def test_get_vector_fields_info_entries_have_display_name(
    stub, grpc_channel_and_metadata, vector_fields_info
):
    """Each VectorFieldInfo entry must have a non-empty display_name."""
    for vfi in vector_fields_info:
        assert len(vfi.display_name) > 0


def test_get_range_returns_min_max(stub, grpc_channel_and_metadata, fields_info, surfaces_info):
    """GetRange must return minimum <= maximum for a known scalar field."""
    _, metadata = grpc_channel_and_metadata
    field_name = fields_info[0].solver_name
    surface_id = surfaces_info[0].surface_ids[0].id
    resp = stub.GetRange(
        field_data_pb2.GetRangeRequest(
            field_name=field_name,
            surface_ids=[field_data_pb2.SurfaceId(id=surface_id)],
            node_value=True,
        ),
        metadata=metadata,
    )
    assert resp.minimum < resp.maximum


def test_begin_fields_streaming_opens_stream(stub, grpc_channel_and_metadata):
    """BeginFieldsStreaming must open a server-streaming call without error."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.BeginFieldsStreaming(
        field_data_pb2.BeginFieldsStreamingRequest(
            chunk_size=262144, provide_bytes_stream=False
        ),
        metadata=metadata,
    )
    assert stream is not None
    stream.cancel()


def test_begin_fields_streaming_byte_stream_opens(stub, grpc_channel_and_metadata):
    """BeginFieldsStreaming with provide_bytes_stream=True must open without error."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.BeginFieldsStreaming(
        field_data_pb2.BeginFieldsStreamingRequest(
            chunk_size=262144, provide_bytes_stream=True
        ),
        metadata=metadata,
    )
    assert stream is not None
    stream.cancel()


def test_get_fields_empty_request_opens_stream(stub, grpc_channel_and_metadata):
    """GetFields with an empty request must open a stream (possibly returning nothing)."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.GetFields(
        field_data_pb2.GetFieldsRequest(), metadata=metadata
    )
    assert stream is not None
    stream.cancel()


def test_get_fields_with_surface_request(stub, grpc_channel_and_metadata, surfaces_info):
    """GetFields with a SurfaceRequest must stream responses with valid chunk types."""
    if not surfaces_info:
        pytest.skip("No surfaces available — cannot test GetFields")
    _, metadata = grpc_channel_and_metadata
    surface_id = surfaces_info[0].surface_ids[0].id
    stream = stub.GetFields(
        field_data_pb2.GetFieldsRequest(
            provide_bytes_stream=False,
            surface_requests=[
                field_data_pb2.SurfaceRequest(
                    surface_id=surface_id,
                    provide_vertices=True,
                    provide_faces=True,
                )
            ],
        ),
        metadata=metadata,
    )
    valid_chunks = {"byte_payload", "double_payload", "float_payload",
                    "long_payload", "int_payload", "payload_info"}
    received = []
    try:
        for resp in stream:
            chunk_type = resp.WhichOneof("chunk")
            if chunk_type is not None:
                assert chunk_type in valid_chunks
            received.append(resp)
            if len(received) >= 10:
                break
    except grpc.RpcError as e:
        if e.code() not in (grpc.StatusCode.CANCELLED,):
            raise
    finally:
        stream.cancel()


def test_get_fields_with_scalar_field_request(
    stub, grpc_channel_and_metadata, surfaces_info, fields_info
):
    """GetFields with a ScalarFieldRequest must stream responses."""
    if not surfaces_info or not fields_info:
        pytest.skip("Surfaces or scalar fields unavailable — cannot test GetFields scalar")
    _, metadata = grpc_channel_and_metadata
    surface_id = surfaces_info[0].surface_ids[0].id
    field_name = fields_info[0].solver_name
    stream = stub.GetFields(
        field_data_pb2.GetFieldsRequest(
            provide_bytes_stream=False,
            scalar_field_requests=[
                field_data_pb2.ScalarFieldRequest(
                    surface_id=surface_id,
                    scalar_field_name=field_name,
                    data_location=field_data_pb2.DATA_LOCATION_NODES,
                    provide_boundary_values=False,
                )
            ],
        ),
        metadata=metadata,
    )
    assert stream is not None
    stream.cancel()


def test_get_surfaces_opens_stream(stub, grpc_channel_and_metadata, surfaces_info):
    """GetSurfaces must open a server-streaming call and return SurfaceData."""
    if not surfaces_info:
        pytest.skip("No surfaces available — cannot test GetSurfaces")
    _, metadata = grpc_channel_and_metadata
    surface_id = surfaces_info[0].surface_ids[0].id
    stream = stub.GetSurfaces(
        field_data_pb2.GetSurfacesRequest(
            surface_ids=[field_data_pb2.SurfaceId(id=surface_id)],
            overset_mesh=False,
        ),
        metadata=metadata,
    )
    chunk = _first_chunk(stream)
    if chunk is not None:
        assert hasattr(chunk, "surface_data")


def test_get_scalar_field_opens_stream(
    stub, grpc_channel_and_metadata, surfaces_info, fields_info
):
    """GetScalarField must open a server-streaming call without immediate error."""
    if not surfaces_info or not fields_info:
        pytest.skip("Surfaces or fields unavailable — cannot test GetScalarField")
    _, metadata = grpc_channel_and_metadata
    surface_id = surfaces_info[0].surface_ids[0].id
    field_name = fields_info[0].solver_name
    stream = stub.GetScalarField(
        field_data_pb2.GetScalarFieldRequest(
            surface_ids=[field_data_pb2.SurfaceId(id=surface_id)],
            scalar_field=field_name,
            node_value=True,
            boundary_values=False,
        ),
        metadata=metadata,
    )
    chunk = _first_chunk(stream)
    if chunk is not None:
        assert hasattr(chunk, "scalar_field_data")


def test_get_vector_field_opens_stream(
    stub, grpc_channel_and_metadata, surfaces_info, fields_info, vector_fields_info
):
    """GetVectorField must open a server-streaming call without immediate error."""
    _, metadata = grpc_channel_and_metadata
    surface_id = surfaces_info[0].surface_ids[0].id
    scalar_name = fields_info[0].solver_name if fields_info else ""
    vector_name = vector_fields_info[0].display_name
    stream = stub.GetVectorField(
        field_data_pb2.GetVectorFieldRequest(
            surface_ids=[field_data_pb2.SurfaceId(id=surface_id)],
            scalar_field=scalar_name,
            vector_field=vector_name,
            node_value=True,
        ),
        metadata=metadata,
    )
    chunk = _first_chunk(stream)
    if chunk is not None:
        assert hasattr(chunk, "vector_field_data")


def test_get_pathlines_field_opens_stream(
    stub, grpc_channel_and_metadata, surfaces_info, fields_info
):
    """GetPathlinesField must open a server-streaming call without immediate error."""
    _, metadata = grpc_channel_and_metadata
    surface_id = surfaces_info[0].surface_ids[0].id
    field_name = fields_info[0].solver_name if fields_info else "pressure"
    stream = stub.GetPathlinesField(
        field_data_pb2.GetPathlinesFieldRequest(
            release_froms=[field_data_pb2.SurfaceId(id=surface_id)],
            field1=field_name,
            node_value=True,
            steps=100,
            step_size=1.0,
            skip=0,
            reverse=False,
        ),
        metadata=metadata,
    )
    assert stream is not None
    stream.cancel()
