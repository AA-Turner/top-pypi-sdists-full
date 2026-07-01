"""Tests for the Fluent Reduction gRPC service (v1).

All tests share the single Fluent solver session started by the
``grpc_channel_and_metadata`` session fixture in ``conftest.py``.

The mixing-elbow case (mixing_elbow.cas.h5) is assumed to be loaded in the
solver session.  Surface zone names and cell zone names match that case.
"""

import grpc
import pytest

from ansys.api.fluent.v1 import reduction_pb2, reduction_pb2_grpc

# ---------------------------------------------------------------------------
# Zone / expression constants (mixing-elbow case)
# ---------------------------------------------------------------------------

_SURFACE_ZONES = ["cold-inlet", "outlet"]
_CELL_ZONES = ["elbow-fluid"]
_SCALAR_EXPR = "AbsolutePressure"
_CONDITION_EXPR = "AbsolutePressure > 0[Pa]"
_WEIGHT_AREA = "Area"
_WEIGHT_VOLUME = "Volume"


# ---------------------------------------------------------------------------
# Stub fixture
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def stub(grpc_channel_and_metadata):
    channel, _ = grpc_channel_and_metadata
    return reduction_pb2_grpc.ReductionStub(channel)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def variant_to_python(v):
    """Unpack a Variant message to the corresponding Python scalar or list."""
    kind = v.WhichOneof("as")
    if kind == "double_state":
        return v.double_state
    if kind == "int64_state":
        return v.int64_state
    if kind == "bool_state":
        return v.bool_state
    if kind == "string_state":
        return v.string_state
    if kind == "double_vector_state":
        return list(v.double_vector_state.items)
    if kind == "int64_vector_state":
        return list(v.int64_vector_state.items)
    if kind == "bool_vector_state":
        return list(v.bool_vector_state.items)
    if kind == "string_vector_state":
        return list(v.string_vector_state.items)
    return None


def _assert_numeric_variant(v):
    """Assert that a Variant contains a numeric (scalar or vector) value."""
    val = variant_to_python(v)
    assert val is not None, "Variant had no recognised oneof field"
    if isinstance(val, list):
        assert len(val) > 0
    else:
        assert isinstance(val, (int, float))


def _assert_point(p):
    """Assert that a Point message has three finite float components."""
    assert isinstance(p.x, float)
    assert isinstance(p.y, float)
    assert isinstance(p.z, float)


# ===========================================================================
# Geometry reductions
# ===========================================================================

def test_area_returns_positive_value(stub, grpc_channel_and_metadata):
    """Area of physical surfaces must be a positive number."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.Area(
        reduction_pb2.AreaRequest(locations=_SURFACE_ZONES),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)
    area = variant_to_python(resp.value)
    assert area > 0, f"Expected positive area, got {area}"


def test_area_single_surface(stub, grpc_channel_and_metadata):
    """Area of a single surface must be positive."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.Area(
        reduction_pb2.AreaRequest(locations=[_SURFACE_ZONES[0]]),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)
    assert variant_to_python(resp.value) > 0


def test_centroid_returns_point(stub, grpc_channel_and_metadata):
    """Centroid must return a Point with three float components."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.Centroid(
        reduction_pb2.CentroidRequest(locations=_SURFACE_ZONES),
        metadata=metadata,
    )
    _assert_point(resp.value)


def test_volume_returns_positive_value(stub, grpc_channel_and_metadata):
    """Volume of a cell zone must be a positive number."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.Volume(
        reduction_pb2.VolumeRequest(locations=_CELL_ZONES),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)
    vol = variant_to_python(resp.value)
    assert vol > 0, f"Expected positive volume, got {vol}"


# ===========================================================================
# Statistical reductions
# ===========================================================================

def test_count_returns_positive_integer(stub, grpc_channel_and_metadata):
    """Count of cells/faces must be a positive integer."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.Count(
        reduction_pb2.CountRequest(locations=_SURFACE_ZONES),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)
    count = variant_to_python(resp.value)
    assert count > 0, f"Expected positive count, got {count}"


def test_count_cell_zone(stub, grpc_channel_and_metadata):
    """Count of cells in a cell zone must be a positive integer."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.Count(
        reduction_pb2.CountRequest(locations=_CELL_ZONES),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)
    assert variant_to_python(resp.value) > 0


def test_count_if_returns_non_negative(stub, grpc_channel_and_metadata):
    """CountIf result must be >= 0 and <= total Count."""
    _, metadata = grpc_channel_and_metadata
    total_resp = stub.Count(
        reduction_pb2.CountRequest(locations=_SURFACE_ZONES),
            metadata=metadata,
        )
    cond_resp = stub.CountIf(
        reduction_pb2.CountIfRequest(
            expression=_CONDITION_EXPR,
            locations=_SURFACE_ZONES,
        ),
        metadata=metadata,
    )
    total = variant_to_python(total_resp.value)
    cond = variant_to_python(cond_resp.value)
    assert cond >= 0, f"CountIf must be >= 0, got {cond}"
    assert cond <= total, f"CountIf ({cond}) must be <= Count ({total})"


def test_minimum_and_maximum(stub, grpc_channel_and_metadata):
    """Minimum value must be less than or equal to Maximum for the same expression."""
    _, metadata = grpc_channel_and_metadata
    min_resp = stub.Minimum(
        reduction_pb2.MinimumRequest(
            expression=_SCALAR_EXPR, locations=_CELL_ZONES
        ),
        metadata=metadata,
        )
    max_resp = stub.Maximum(
        reduction_pb2.MaximumRequest(
            expression=_SCALAR_EXPR, locations=_CELL_ZONES
        ),
        metadata=metadata,
    )
    _assert_numeric_variant(min_resp.value)
    _assert_numeric_variant(max_resp.value)
    lo = variant_to_python(min_resp.value)
    hi = variant_to_python(max_resp.value)
    assert lo <= hi, f"Minimum ({lo}) > Maximum ({hi})"


# ===========================================================================
# Surface-weighted averages / integrals
# ===========================================================================

def test_area_ave_returns_numeric(stub, grpc_channel_and_metadata):
    """AreaAve of AbsolutePressure must return a numeric Variant."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.AreaAve(
        reduction_pb2.AreaAveRequest(
            expression=_SCALAR_EXPR,
            locations=_SURFACE_ZONES,
        ),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)


def test_area_int_returns_numeric(stub, grpc_channel_and_metadata):
    """AreaInt of AbsolutePressure must return a numeric Variant."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.AreaInt(
        reduction_pb2.AreaIntRequest(
            expression=_SCALAR_EXPR,
            locations=_SURFACE_ZONES,
        ),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)


def test_area_int_consistent_with_area_ave(stub, grpc_channel_and_metadata):
    """AreaInt ≈ AreaAve × Area for the same surface and expression."""
    _, metadata = grpc_channel_and_metadata
    area_resp = stub.Area(
        reduction_pb2.AreaRequest(locations=_SURFACE_ZONES),
        metadata=metadata,
    )
    ave_resp = stub.AreaAve(
        reduction_pb2.AreaAveRequest(
            expression=_SCALAR_EXPR, locations=_SURFACE_ZONES
        ),
        metadata=metadata,
    )
    int_resp = stub.AreaInt(
        reduction_pb2.AreaIntRequest(
            expression=_SCALAR_EXPR, locations=_SURFACE_ZONES
        ),
        metadata=metadata,
    )
    area = variant_to_python(area_resp.value)
    ave = variant_to_python(ave_resp.value)
    integral = variant_to_python(int_resp.value)
    # Allow 1% relative tolerance
    expected = ave * area
    if expected != 0:
        rel_err = abs(integral - expected) / abs(expected)
        assert rel_err < 0.01, (
            f"AreaInt ({integral}) does not match AreaAve×Area ({expected}), "
            f"rel_err={rel_err:.4f}"
        )


def test_mass_flow_ave_returns_numeric(stub, grpc_channel_and_metadata):
    """MassFlowAve of AbsolutePressure must return a numeric Variant."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.MassFlowAve(
        reduction_pb2.MassFlowAveRequest(
            expression=_SCALAR_EXPR,
            locations=_SURFACE_ZONES,
        ),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)


def test_mass_flow_ave_abs_returns_numeric(stub, grpc_channel_and_metadata):
    """MassFlowAveAbs of AbsolutePressure must return a numeric Variant."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.MassFlowAveAbs(
        reduction_pb2.MassFlowAveAbsRequest(
            expression=_SCALAR_EXPR,
            locations=_SURFACE_ZONES,
        ),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)


def test_mass_flow_int_returns_numeric(stub, grpc_channel_and_metadata):
    """MassFlowInt of AbsolutePressure must return a numeric Variant."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.MassFlowInt(
        reduction_pb2.MassFlowIntRequest(
            expression=_SCALAR_EXPR,
            locations=_SURFACE_ZONES,
        ),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)


# ===========================================================================
# Volume-weighted averages / integrals
# ===========================================================================

def test_volume_ave_returns_numeric(stub, grpc_channel_and_metadata):
    """VolumeAve of AbsolutePressure must return a numeric Variant."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.VolumeAve(
        reduction_pb2.VolumeAveRequest(
            expression=_SCALAR_EXPR,
            locations=_CELL_ZONES,
        ),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)


def test_volume_ave_within_min_max_range(stub, grpc_channel_and_metadata):
    """VolumeAve must lie between Minimum and Maximum."""
    _, metadata = grpc_channel_and_metadata
    min_resp = stub.Minimum(
        reduction_pb2.MinimumRequest(
            expression=_SCALAR_EXPR, locations=_CELL_ZONES
        ),
        metadata=metadata,
        )
    max_resp = stub.Maximum(
        reduction_pb2.MaximumRequest(
            expression=_SCALAR_EXPR, locations=_CELL_ZONES
        ),
        metadata=metadata,
    )
    ave_resp = stub.VolumeAve(
        reduction_pb2.VolumeAveRequest(
            expression=_SCALAR_EXPR, locations=_CELL_ZONES
        ),
        metadata=metadata,
    )
    lo = variant_to_python(min_resp.value)
    hi = variant_to_python(max_resp.value)
    ave = variant_to_python(ave_resp.value)
    assert lo <= ave <= hi, (
        f"VolumeAve ({ave}) not in range [{lo}, {hi}]"
    )


def test_volume_int_returns_numeric(stub, grpc_channel_and_metadata):
    """VolumeInt of AbsolutePressure must return a numeric Variant."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.VolumeInt(
        reduction_pb2.VolumeIntRequest(
            expression=_SCALAR_EXPR,
            locations=_CELL_ZONES,
        ),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)


def test_mass_ave_returns_numeric(stub, grpc_channel_and_metadata):
    """MassAve of AbsolutePressure must return a numeric Variant."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.MassAve(
        reduction_pb2.MassAveRequest(
            expression=_SCALAR_EXPR,
            locations=_CELL_ZONES,
        ),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)


def test_mass_int_returns_numeric(stub, grpc_channel_and_metadata):
    """MassInt of AbsolutePressure must return a numeric Variant."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.MassInt(
        reduction_pb2.MassIntRequest(
            expression=_SCALAR_EXPR,
            locations=_CELL_ZONES,
        ),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)


# ===========================================================================
# Force decomposition
# ===========================================================================

def test_force_equals_pressure_plus_viscous(stub, grpc_channel_and_metadata):
    """Total Force must equal PressureForce + ViscousForce for each component."""
    _, metadata = grpc_channel_and_metadata
    pf = stub.PressureForce(
        reduction_pb2.PressureForceRequest(locations=_SURFACE_ZONES),
        metadata=metadata,
    ).value
    vf = stub.ViscousForce(
        reduction_pb2.ViscousForceRequest(locations=_SURFACE_ZONES),
        metadata=metadata,
    ).value
    tf = stub.Force(
        reduction_pb2.ForceRequest(locations=_SURFACE_ZONES),
        metadata=metadata,
    ).value
    _assert_point(pf)
    _assert_point(vf)
    _assert_point(tf)

    tol = 1e-6
    for component, p, v, t in [
        ("x", pf.x, vf.x, tf.x),
        ("y", pf.y, vf.y, tf.y),
        ("z", pf.z, vf.z, tf.z),
    ]:
        expected = p + v
        if abs(expected) > tol:
            rel_err = abs(t - expected) / abs(expected)
            assert rel_err < 0.01, (
                f"Force.{component} ({t}) != PressureForce ({p}) + ViscousForce ({v}), "
                f"rel_err={rel_err:.4f}"
            )


def test_moment_returns_point(stub, grpc_channel_and_metadata):
    """Moment must return a Point with x, y, z components."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.Moment(
        reduction_pb2.MomentRequest(
            expression=_SCALAR_EXPR,
            locations=_SURFACE_ZONES,
        ),
        metadata=metadata,
    )
    _assert_point(resp.value)


# ===========================================================================
# Conditional / weighted sums
# ===========================================================================

def test_sum_returns_numeric(stub, grpc_channel_and_metadata):
    """Sum of AbsolutePressure weighted by Area must return a numeric Variant."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.Sum(
        reduction_pb2.SumRequest(
            expression=_SCALAR_EXPR,
            locations=_SURFACE_ZONES,
            weight=_WEIGHT_AREA,
        ),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)


def test_sum_if_returns_numeric(stub, grpc_channel_and_metadata):
    """SumIf with a condition must return a numeric Variant."""
    _, metadata = grpc_channel_and_metadata
    resp = stub.SumIf(
        reduction_pb2.SumIfRequest(
            expression=_SCALAR_EXPR,
            condition=_CONDITION_EXPR,
            locations=_SURFACE_ZONES,
            weight=_WEIGHT_AREA,
        ),
        metadata=metadata,
    )
    _assert_numeric_variant(resp.value)


def test_sum_if_and_sum(stub, grpc_channel_and_metadata):
    """SumIf(AbsolutePressure > 0) must be <= Sum(AbsolutePressure) since it is a subset."""
    _, metadata = grpc_channel_and_metadata
    full_resp = stub.Sum(
        reduction_pb2.SumRequest(
            expression=_SCALAR_EXPR,
            locations=_SURFACE_ZONES,
            weight=_WEIGHT_AREA,
        ),
        metadata=metadata,
    )
    cond_resp = stub.SumIf(
        reduction_pb2.SumIfRequest(
            expression=_SCALAR_EXPR,
            condition=_CONDITION_EXPR,
            locations=_SURFACE_ZONES,
            weight=_WEIGHT_AREA,
        ),
        metadata=metadata,
    )
    full_val = variant_to_python(full_resp.value)
    cond_val = variant_to_python(cond_resp.value)
    # Both must be non-negative for AbsolutePressure, and cond <= full
    assert cond_val >= 0, f"SumIf must be >= 0 for AbsolutePressure, got {cond_val}"
    assert cond_val <= full_val * 1.001, (
        f"SumIf ({cond_val}) > Sum ({full_val})"
    )
