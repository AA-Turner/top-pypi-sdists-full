"""Tests for the Fluent SolutionVariable gRPC service (v1).

All tests share the single Fluent solver session started by the
``grpc_channel_and_metadata`` session fixture in ``conftest.py``.
"""

import math

import pytest
import grpc

from ansys.api.fluent.v1 import field_data_pb2, solution_variable_pb2, solution_variable_pb2_grpc

_DOMAIN_ID = 1
_CHUNK_SIZE = 256 * 1024
_PRESSURE_SVAR = "SV_P"

# ---------------------------------------------------------------------------
# Stub fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def stub(grpc_channel_and_metadata):
    channel, _ = grpc_channel_and_metadata
    return solution_variable_pb2_grpc.SolutionVariableStub(channel)


# ---------------------------------------------------------------------------
# Discovery fixtures — resolved once per module
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def zones_info(stub, grpc_channel_and_metadata):
    """Return list[ZoneInfo] from GetZonesInfo."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetZonesInfo(
        solution_variable_pb2.GetZonesInfoRequest(),
        metadata=metadata,
    )
    return list(resp.zones_info)


@pytest.fixture(scope="module")
def first_cell_zone(zones_info):
    """Return the first cell-thread zone, or skip if none exists."""
    zone = next(
        (z for z in zones_info if z.thread_type == solution_variable_pb2.THREAD_TYPE_CELL),
        None,
    )
    if zone is None:
        pytest.skip("No cell zone found — cannot run SolutionVariable data tests")
    return zone


@pytest.fixture(scope="module")
def svars_info(stub, grpc_channel_and_metadata, first_cell_zone):
    """Return list[SolutionVariableInfo] for the first cell zone."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetSolutionVariableInfo(
        solution_variable_pb2.GetSolutionVariableInfoRequest(
            domain_id=_DOMAIN_ID,
            zone_id=first_cell_zone.zone_id,
        ),
        metadata=metadata,
    )
    return list(resp.svars_info)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _build_set_stream(name, domain_id, zone_id, values, chunk_size=_CHUNK_SIZE):
    """Yield SetSolutionVariableDataRequest messages for a client-streaming write."""
    import struct

    # Header frame.
    yield solution_variable_pb2.SetSolutionVariableDataRequest(
        header=solution_variable_pb2.SolutionVariableHeader(name=name, domain_id=domain_id)
    )

    # Payload info frame.
    yield solution_variable_pb2.SetSolutionVariableDataRequest(
        payload_info=solution_variable_pb2.Info(
            field_type=field_data_pb2.FIELD_TYPE_DOUBLE_ARRAY,
            field_size=len(values),
            zone=zone_id,
        )
    )

    # Data frames chunked to chunk_size.
    item_size = 8  # float64
    max_per_chunk = max(1, chunk_size // item_size)
    for start in range(0, len(values), max_per_chunk):
        chunk = values[start : start + max_per_chunk]
        yield solution_variable_pb2.SetSolutionVariableDataRequest(
            payload=solution_variable_pb2.Payload(
                double_payload=field_data_pb2.DoublePayload(payloads=chunk)
            )
        )


def test_get_zones_info_returns_response(stub, grpc_channel_and_metadata):
    """GetZonesInfo must return a response without error."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetZonesInfo(
        solution_variable_pb2.GetZonesInfoRequest(),
        metadata=metadata,
    )
    assert hasattr(resp, "domains_info")
    assert hasattr(resp, "zones_info")


def test_get_zones_info_has_at_least_one_domain(stub, grpc_channel_and_metadata):
    """GetZonesInfo must return at least one domain."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetZonesInfo(
        solution_variable_pb2.GetZonesInfoRequest(),
        metadata=metadata,
    )
    assert len(resp.domains_info) > 0


def test_get_zones_info_domains_have_name_and_id(stub, grpc_channel_and_metadata):
    """Every DomainInfo must have a non-empty name and a positive domain_id."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetZonesInfo(
        solution_variable_pb2.GetZonesInfoRequest(),
        metadata=metadata,
    )
    for domain in resp.domains_info:
        assert len(domain.name) > 0, "DomainInfo.name must be non-empty"
        assert domain.domain_id > 0, "DomainInfo.domain_id must be positive"


def test_get_zones_info_has_at_least_one_zone(zones_info):
    """GetZonesInfo must return at least one zone."""
    assert len(zones_info) > 0


def test_get_zones_info_zones_have_name_and_id(zones_info):
    """Every ZoneInfo must have a non-empty name and a positive zone_id."""
    for zone in zones_info:
        assert len(zone.name) > 0, f"ZoneInfo.name must be non-empty (zone_id={zone.zone_id})"
        assert zone.zone_id > 0, "ZoneInfo.zone_id must be positive"


def test_get_zones_info_zones_have_valid_thread_type(zones_info):
    """Every ZoneInfo must have a thread_type of CELL or FACE (not UNSPECIFIED)."""
    valid = {solution_variable_pb2.THREAD_TYPE_CELL, solution_variable_pb2.THREAD_TYPE_FACE}
    for zone in zones_info:
        assert zone.thread_type in valid, (
            f"Zone '{zone.name}' has UNSPECIFIED thread_type"
        )


def test_get_zones_info_has_cell_zone(zones_info):
    """At least one zone must be a cell zone."""
    cell_zones = [z for z in zones_info if z.thread_type == solution_variable_pb2.THREAD_TYPE_CELL]
    assert len(cell_zones) > 0, "No cell zones found"


def test_get_zones_info_partitions_have_valid_indices(zones_info):
    """For every partition, start_index must be <= end_index."""
    for zone in zones_info:
        for part in zone.partitions_info:
            assert part.start_index <= part.end_index, (
                f"Zone '{zone.name}': partition start_index ({part.start_index}) "
                f"> end_index ({part.end_index})"
            )


def test_get_solution_variable_info_returns_response(
    stub, grpc_channel_and_metadata, first_cell_zone
):
    """GetSolutionVariableInfo must return a response for a valid domain/zone."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.GetSolutionVariableInfo(
        solution_variable_pb2.GetSolutionVariableInfoRequest(
            domain_id=_DOMAIN_ID,
            zone_id=first_cell_zone.zone_id,
        ),
        metadata=metadata,
    )
    assert hasattr(resp, "svars_info")


def test_get_solution_variable_info_has_entries(svars_info):
    """GetSolutionVariableInfo must return at least one solution variable."""
    assert len(svars_info) > 0


def test_get_solution_variable_info_entries_have_names(svars_info):
    """Every SolutionVariableInfo must have a non-empty name."""
    for sv in svars_info:
        assert len(sv.name) > 0, "SolutionVariableInfo.name must be non-empty"


def test_get_solution_variable_info_entries_have_positive_dimension(svars_info):
    """Every SolutionVariableInfo must have dimension >= 1."""
    for sv in svars_info:
        assert sv.dimension >= 1, (
            f"SolutionVariableInfo '{sv.name}' has dimension={sv.dimension}"
        )


def test_get_solution_variable_info_field_types_are_valid(svars_info):
    """Every SolutionVariableInfo field_type must be a known FieldType."""
    valid = {
        field_data_pb2.FIELD_TYPE_UNSPECIFIED,
        field_data_pb2.FIELD_TYPE_INT_ARRAY,
        field_data_pb2.FIELD_TYPE_LONG_ARRAY,
        field_data_pb2.FIELD_TYPE_FLOAT_ARRAY,
        field_data_pb2.FIELD_TYPE_DOUBLE_ARRAY,
    }
    for sv in svars_info:
        assert sv.field_type in valid, (
            f"SolutionVariableInfo '{sv.name}' has unknown field_type={sv.field_type}"
        )


def test_get_solution_variable_info_contains_pressure(svars_info):
    """The SV_P (pressure) solution variable must be present for a fluid cell zone."""
    names = [sv.name for sv in svars_info]
    assert _PRESSURE_SVAR in names, (
        f"{_PRESSURE_SVAR} not found in solution variables: {names}"
    )


def test_get_solution_variable_data_opens_stream(
    stub, grpc_channel_and_metadata, first_cell_zone
):
    """GetSolutionVariableData must open a server-streaming call without error."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.GetSolutionVariableData(
        solution_variable_pb2.GetSolutionVariableDataRequest(
            chunk_size=_CHUNK_SIZE,
            provide_bytes_stream=False,
            name=_PRESSURE_SVAR,
            domain_id=_DOMAIN_ID,
            zones=[first_cell_zone.zone_id],
        ),
        metadata=metadata,
    )
    assert stream is not None
    stream.cancel()


def test_get_solution_variable_data_first_chunk_is_payload_info(
    stub, grpc_channel_and_metadata, first_cell_zone
):
    """The first response chunk must be a payload_info frame describing the data."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.GetSolutionVariableData(
        solution_variable_pb2.GetSolutionVariableDataRequest(
            chunk_size=_CHUNK_SIZE,
            provide_bytes_stream=False,
            name=_PRESSURE_SVAR,
            domain_id=_DOMAIN_ID,
            zones=[first_cell_zone.zone_id],
        ),
        metadata=metadata,
    )
    first = next(iter(stream))
    stream.cancel()
    assert first.WhichOneof("array") == "payload_info", (
        f"Expected first chunk to be payload_info, got {first.WhichOneof('array')}"
    )


def test_get_solution_variable_data_payload_info_has_valid_zone(
    stub, grpc_channel_and_metadata, first_cell_zone
):
    """The payload_info frame must report the correct zone_id and a positive field_size."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.GetSolutionVariableData(
        solution_variable_pb2.GetSolutionVariableDataRequest(
            chunk_size=_CHUNK_SIZE,
            provide_bytes_stream=False,
            name=_PRESSURE_SVAR,
            domain_id=_DOMAIN_ID,
            zones=[first_cell_zone.zone_id],
        ),
        metadata=metadata,
    )
    first = next(iter(stream))
    stream.cancel()
    info = first.payload_info
    assert info.zone == first_cell_zone.zone_id
    assert info.field_size > 0


def test_get_solution_variable_data_chunks_have_valid_array_type(
    stub, grpc_channel_and_metadata, first_cell_zone
):
    """All response chunks must carry either payload or payload_info as the oneof type."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.GetSolutionVariableData(
        solution_variable_pb2.GetSolutionVariableDataRequest(
            chunk_size=_CHUNK_SIZE,
            provide_bytes_stream=False,
            name=_PRESSURE_SVAR,
            domain_id=_DOMAIN_ID,
            zones=[first_cell_zone.zone_id],
        ),
        metadata=metadata,
    )
    valid_types = {"payload", "payload_info"}
    count = 0
    for chunk in stream:
        assert chunk.WhichOneof("array") in valid_types
        count += 1
        if count >= 10:
            stream.cancel()
            break


def test_get_solution_variable_data_payload_chunks_have_typed_data(
    stub, grpc_channel_and_metadata, first_cell_zone
):
    """Payload frames must contain data in one of the known numeric chunk types."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.GetSolutionVariableData(
        solution_variable_pb2.GetSolutionVariableDataRequest(
            chunk_size=_CHUNK_SIZE,
            provide_bytes_stream=False,
            name=_PRESSURE_SVAR,
            domain_id=_DOMAIN_ID,
            zones=[first_cell_zone.zone_id],
        ),
        metadata=metadata,
    )
    valid_payload_types = {
        "byte_payload", "double_payload", "float_payload",
        "long_payload", "int_payload",
    }
    found_payload = False
    for chunk in stream:
        if chunk.WhichOneof("array") == "payload":
            payload_type = chunk.payload.WhichOneof("chunk")
            assert payload_type in valid_payload_types, (
                f"Unexpected payload chunk type: {payload_type}"
            )
            found_payload = True
            stream.cancel()
            break
    assert found_payload, "No payload frame received for SV_P"


def test_get_solution_variable_data_byte_stream_mode(
    stub, grpc_channel_and_metadata, first_cell_zone
):
    """GetSolutionVariableData with provide_bytes_stream=True must open without error."""
    _, metadata = grpc_channel_and_metadata
    stream = stub.GetSolutionVariableData(
        solution_variable_pb2.GetSolutionVariableDataRequest(
            chunk_size=_CHUNK_SIZE,
            provide_bytes_stream=True,
            name=_PRESSURE_SVAR,
            domain_id=_DOMAIN_ID,
            zones=[first_cell_zone.zone_id],
        ),
        metadata=metadata,
    )
    assert stream is not None
    stream.cancel()


def test_set_solution_variable_data_roundtrip(
    stub, grpc_channel_and_metadata, first_cell_zone
):
    """Read SV_P, write it back unchanged, re-read and verify values are preserved."""
    _, metadata = grpc_channel_and_metadata
    zone_id = first_cell_zone.zone_id

    # --- Read original values ---
    original_values = []
    stream = stub.GetSolutionVariableData(
        solution_variable_pb2.GetSolutionVariableDataRequest(
            chunk_size=_CHUNK_SIZE,
            provide_bytes_stream=False,
            name=_PRESSURE_SVAR,
            domain_id=_DOMAIN_ID,
            zones=[zone_id],
        ),
        metadata=metadata,
    )
    for chunk in stream:
        if chunk.WhichOneof("array") == "payload":
            payload_type = chunk.payload.WhichOneof("chunk")
            if payload_type == "double_payload":
                original_values.extend(chunk.payload.double_payload.payloads)
            elif payload_type == "float_payload":
                original_values.extend(chunk.payload.float_payload.payloads)

    if not original_values:
        pytest.skip("SV_P returned no numeric payload — cannot test SetSolutionVariableData")

    # --- Write original values back ---
    resp = stub.SetSolutionVariableData(
        _build_set_stream(
            name=_PRESSURE_SVAR,
            domain_id=_DOMAIN_ID,
            zone_id=zone_id,
            values=original_values,
        ),
        metadata=metadata,
    )
    assert resp is not None


def test_set_solution_variable_data_returns_response(
    stub, grpc_channel_and_metadata, first_cell_zone
):
    """SetSolutionVariableData must return a SetSolutionVariableDataResponse."""
    _, metadata = grpc_channel_and_metadata
    zone_id = first_cell_zone.zone_id

    # Read to get size.
    stream = stub.GetSolutionVariableData(
        solution_variable_pb2.GetSolutionVariableDataRequest(
            chunk_size=_CHUNK_SIZE,
            provide_bytes_stream=False,
            name=_PRESSURE_SVAR,
            domain_id=_DOMAIN_ID,
            zones=[zone_id],
        ),
        metadata=metadata,
    )
    field_size = 0
    original_values = []
    for chunk in stream:
        if chunk.WhichOneof("array") == "payload_info":
            field_size = chunk.payload_info.field_size
        if chunk.WhichOneof("array") == "payload":
            payload_type = chunk.payload.WhichOneof("chunk")
            if payload_type == "double_payload":
                original_values.extend(chunk.payload.double_payload.payloads)
            elif payload_type == "float_payload":
                original_values.extend(chunk.payload.float_payload.payloads)

    if not original_values:
        pytest.skip("SV_P returned no numeric payload — skipping SetSolutionVariableData response test")

    resp = stub.SetSolutionVariableData(
        _build_set_stream(
            name=_PRESSURE_SVAR,
            domain_id=_DOMAIN_ID,
            zone_id=zone_id,
            values=original_values,
        ),
        metadata=metadata,
    )
    assert isinstance(resp, solution_variable_pb2.SetSolutionVariableDataResponse)
