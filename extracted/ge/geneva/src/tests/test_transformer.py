# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

import logging
import pickle as std_pickle
import signal
import time
import warnings
from contextlib import nullcontext
from pathlib import Path
from typing import Any, NamedTuple

import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pytest

import geneva.cloudpickle as cloudpickle
from geneva import Columns, connect, udf
from geneva.transformer import (
    UDF,
    UDFArgType,
    UnpackedUDF,
    _blob_list_to_record_batch,
    _scalar_results_to_array,
)

HAS_SIGALRM_TIMEOUT = all(
    hasattr(signal, attr)
    for attr in ("SIGALRM", "ITIMER_REAL", "setitimer", "getitimer")
)


def _legacy_timeout_plus_one(x: int) -> int:
    return x + 1


def test_udf_fsl(tmp_path: Path) -> None:
    @udf(data_type=pa.list_(pa.float32(), 4))
    def gen_fsl(b: pa.RecordBatch) -> pa.Array:
        arr = pa.array([b * 1.0 for b in range(8)])
        fsl = pa.FixedSizeListArray.from_arrays(arr, 4)
        return fsl

    assert gen_fsl.data_type == pa.list_(pa.float32(), 4)

    db = connect(tmp_path)
    tbl = pa.table({"a": [1, 2]})
    tbl = db.create_table("t1", tbl)

    # RecordBatch UDFs don't use input_columns - they receive the entire batch
    tbl.add_columns(
        {"embed": gen_fsl},
    )

    tbl = db.open_table("t1")
    assert tbl.schema == pa.schema(
        [
            pa.field("a", pa.int64()),
            pa.field("embed", pa.list_(pa.float32(), 4)),
        ],
    )


def test_udf_data_type_inference() -> None:
    @udf
    def foo(x: int, y: int) -> int:
        return x + y

    assert foo.data_type == pa.int64()
    assert foo.arg_type is UDFArgType.SCALAR

    for np_dtype in [
        np.bool_,
        np.uint8,
        np.uint16,
        np.uint32,
        np.uint64,
        np.int8,
        np.int16,
        np.int32,
        np.int64,
        np.float16,
        np.float32,
        np.float64,
    ]:

        @udf
        def foo_np(x: int, np_dtype=np_dtype) -> np_dtype:
            return np_dtype(x)

        assert foo_np.data_type == pa.from_numpy_dtype(np_dtype)
        assert foo_np.arg_type is UDFArgType.SCALAR

    @udf
    def bool_val(x: int) -> bool:
        return x % 2 == 0

    assert bool_val.data_type == pa.bool_()
    assert bool_val.arg_type is UDFArgType.SCALAR

    @udf
    def foo_str(x: int) -> str:
        return str(x)

    assert foo_str.data_type == pa.string()
    assert foo_str.arg_type is UDFArgType.SCALAR

    @udf
    def np_bool(x: int) -> np.bool_:
        return np.bool_(x % 2 == 0)

    assert np_bool.data_type == pa.bool_()
    assert np_bool.arg_type is UDFArgType.SCALAR


def test_udf_columns_namedtuple_infers_struct_type() -> None:
    class Dimensions(NamedTuple):
        height: int
        width: int

    @udf
    def dimensions(image_id: int) -> Columns[Dimensions]:
        return Dimensions(image_id + 1, image_id + 2)

    assert dimensions.is_multi_output is True
    assert dimensions.data_type == pa.struct(
        [
            pa.field("height", pa.int64()),
            pa.field("width", pa.int64()),
        ]
    )


def test_unpacked_udf_validates_prefix() -> None:
    class Dimensions(NamedTuple):
        height: int
        width: int

    @udf
    def dimensions(image_id: int) -> Columns[Dimensions]:
        return Dimensions(image_id + 1, image_id + 2)

    unpacked = UnpackedUDF(dimensions, prefix="img_")
    assert [field.output_column for field in unpacked.fields] == [
        "img_height",
        "img_width",
    ]

    with pytest.raises(ValueError, match="valid identifier prefix"):
        UnpackedUDF(dimensions, prefix="img-")

    with pytest.raises(TypeError, match="prefix must be a string"):
        UnpackedUDF(dimensions, prefix=1)  # type: ignore[arg-type]


def test_scalar_udf_accepts_numpy_list_inputs() -> None:
    seen = []

    @udf(data_type=pa.list_(pa.float32()))
    def double_vec(x: np.ndarray) -> np.ndarray:
        seen.append(type(x))
        return x * 2

    rb = pa.RecordBatch.from_arrays(
        [pa.array([[1.0, 2.0], [3.0]], type=pa.list_(pa.float32()))],
        ["x"],
    )

    result = double_vec(rb)

    assert result.type == pa.list_(pa.float32())
    assert result.to_pylist() == [[2.0, 4.0], [6.0]]
    assert all(t is np.ndarray for t in seen)


def test_scalar_udf_accepts_numpy_fixed_size_list_inputs() -> None:
    @udf(data_type=pa.list_(pa.float32(), 2))
    def add_one(x: np.ndarray) -> np.ndarray:
        return x + 1

    rb = pa.RecordBatch.from_arrays(
        [pa.array([[0.0, 1.0], [2.0, 3.0]], type=pa.list_(pa.float32(), 2))],
        ["x"],
    )

    result = add_one(rb)

    assert result.type == pa.list_(pa.float32(), 2)
    assert result.to_pylist() == [[1.0, 2.0], [3.0, 4.0]]


def test_scalar_udf_accepts_numpy_list_string_inputs() -> None:
    @udf(data_type=pa.list_(pa.string()))
    def shout(x: np.ndarray) -> np.ndarray:
        return np.array([v.upper() for v in x], dtype=object)

    rb = pa.RecordBatch.from_arrays(
        [pa.array([["a", "b"], ["c", "d", "e"]], type=pa.list_(pa.string()))],
        ["x"],
    )

    result = shout(rb)

    assert result.type == pa.list_(pa.string())
    assert result.to_pylist() == [["A", "B"], ["C", "D", "E"]]


def test_scalar_udf_accepts_numpy_nested_lists() -> None:
    @udf(data_type=pa.list_(pa.list_(pa.int32())))
    def inc_nested(x: np.ndarray) -> np.ndarray:
        return np.array([[v + 1 for v in inner] for inner in x], dtype=object)

    rb = pa.RecordBatch.from_arrays(
        [pa.array([[[1, 2], [3]], [[4], [5, 6]]], type=pa.list_(pa.list_(pa.int32())))],
        ["x"],
    )

    result = inc_nested(rb)

    assert result.type == pa.list_(pa.list_(pa.int32()))
    assert result.to_pylist() == [[[2, 3], [4]], [[5], [6, 7]]]


def test_scalar_udf_list_annotation_returns_python_list() -> None:
    seen: list[type | None] = []

    @udf(data_type=pa.int32())
    def sum_list(x: list[int] | None) -> int | None:
        if x is None:
            seen.append(None)
            return None
        seen.append(type(x))
        return sum(x)

    rb = pa.RecordBatch.from_arrays(
        [pa.array([[1, 2], None, [3, 4]], type=pa.list_(pa.int32()))],
        ["x"],
    )

    result = sum_list(rb)

    assert result == pa.array([3, None, 7], type=pa.int32())
    assert seen == [list, None, list]


def test_scalar_udf_string_list_annotation_returns_python_list() -> None:
    @udf(data_type=pa.int32())
    def sum_list(x: "list[int] | None") -> int | None:
        if x is None:
            return None
        assert isinstance(x, list)
        return sum(x)

    rb = pa.RecordBatch.from_arrays(
        [pa.array([[1, 2], None], type=pa.list_(pa.int32()))],
        ["x"],
    )

    result = sum_list(rb)

    assert result == pa.array([3, None], type=pa.int32())


def test_string_annotation_eval_missing_globals() -> None:
    def sum_list_any(x: "list[dict[str, Any]] | None") -> int | None:
        if x is None:
            return None
        assert isinstance(x, list)
        return len(x)

    # Simulate Ray/cloudpickle dropping names only used in annotations.
    sum_list_any.__globals__.pop("Any", None)

    wrapped = udf(data_type=pa.int32())(sum_list_any)

    struct_type = pa.struct([("a", pa.int32())])
    rb = pa.RecordBatch.from_arrays(
        [
            pa.array(
                [[{"a": 1}, {"a": 2}], None],
                type=pa.list_(struct_type),
            )
        ],
        ["x"],
    )

    result = wrapped(rb)
    assert result == pa.array([2, None], type=pa.int32())


def test_scalar_udf_accepts_list_structs() -> None:
    struct_type = pa.struct([("a", pa.int32()), ("b", pa.string())])

    @udf(data_type=pa.list_(struct_type))
    def bump_struct(x: np.ndarray) -> list[dict[str, object]]:
        # x is a numpy object array of dicts; preserve shape and types
        return [{"a": elem["a"] + 1, "b": elem["b"].upper()} for elem in x]

    rb = pa.RecordBatch.from_arrays(
        [
            pa.array(
                [
                    [{"a": 1, "b": "c"}, {"a": 2, "b": "d"}],
                    [{"a": 10, "b": "e"}],
                ],
                type=pa.list_(struct_type),
            )
        ],
        ["x"],
    )

    result = bump_struct(rb)

    assert result.type == pa.list_(struct_type)
    assert result.to_pylist() == [
        [{"a": 2, "b": "C"}, {"a": 3, "b": "D"}],
        [{"a": 11, "b": "E"}],
    ]


def test_scalar_udf_accepts_list_structs_as_python_list() -> None:
    struct_type = pa.struct([("a", pa.int32()), ("b", pa.string())])

    @udf(data_type=pa.list_(struct_type))
    def bump_struct_pylist(
        x: list[dict[str, object]] | None,
    ) -> list[dict[str, object]] | None:
        if x is None:
            return None
        assert isinstance(x, list)
        return [{"a": elem["a"] + 1, "b": elem["b"].upper()} for elem in x]

    rb = pa.RecordBatch.from_arrays(
        [
            pa.array(
                [
                    [{"a": 1, "b": "c"}, {"a": 2, "b": "d"}],
                    [{"a": 10, "b": "e"}],
                    None,
                ],
                type=pa.list_(struct_type),
            )
        ],
        ["x"],
    )

    result = bump_struct_pylist(rb)

    assert result.type == pa.list_(struct_type)
    assert result.to_pylist() == [
        [{"a": 2, "b": "C"}, {"a": 3, "b": "D"}],
        [{"a": 11, "b": "E"}],
        None,
    ]


def test_udf_as_regular_functions() -> None:
    @udf
    def add_three_numbers(a: int, b: int, c: int) -> int:
        return a + b + c

    assert add_three_numbers(1, 2, 3) == 6
    assert add_three_numbers(10, 20, 30) == 60
    assert add_three_numbers.arg_type is UDFArgType.SCALAR
    assert add_three_numbers.data_type == pa.int64()

    @udf
    def make_string(x: int, y: str) -> str:
        return f"{y}-{x}"

    assert make_string(42, "answer") == "answer-42"
    assert make_string.arg_type is UDFArgType.SCALAR
    assert make_string.data_type == pa.string()

    @udf(data_type=pa.float32())
    def multi_by_two(batch: pa.RecordBatch) -> pa.Array:
        arr = pc.multiply(batch.column(0), 2)
        return arr

    rb = pa.RecordBatch.from_arrays([pa.array([1, 2, 3])], ["col"])
    assert multi_by_two(rb) == pa.array([2, 4, 6])
    assert multi_by_two.arg_type is UDFArgType.RECORD_BATCH

    # Confirm direct calls with multiple arguments still work as expected
    assert make_string(7, "num") == "num-7"
    assert add_three_numbers(2, 3, 4) == 9


def test_udf_with_batch_mode() -> None:
    """Test using a scalar UDF, but filled with batch model"""

    @udf
    def powers(a: int, b: int) -> int:
        return a**b

    # a RecordBatch with a and b columns
    rb = pa.RecordBatch.from_arrays(
        [pa.array([1, 2, 3]), pa.array([4, 5, 6])],
        ["a", "b"],
    )
    result = powers(rb)
    assert result == pa.array([1, 2**5, 3**6])


def test_udf_checkpoint_size_sets_batch_size() -> None:
    @udf(data_type=pa.int64(), checkpoint_size=32)
    def take_batch(x: int) -> int:
        return x

    assert isinstance(take_batch, UDF)
    assert take_batch.batch_size == 32

    @udf(
        data_type=pa.int64(),
        batch_size=16,
        checkpoint_size=32,
    )
    def mismatch(x: int) -> int:
        return x

    assert mismatch.batch_size == 32


def test_scalar_udf_timeout_metadata() -> None:
    @udf(timeout=0.25)
    def slow(x: int) -> int:
        return x

    assert slow.timeout == pytest.approx(0.25)


@pytest.mark.parametrize("timeout", [0, -1, float("inf"), float("nan")])
def test_udf_timeout_validation_rejects_invalid(timeout: float) -> None:
    with pytest.raises(
        ValueError, match="timeout must be a positive finite number of seconds"
    ):

        @udf(timeout=timeout)
        def invalid_timeout(x: int) -> int:
            return x


def test_udf_timeout_rejects_array_udf() -> None:
    with pytest.raises(ValueError, match="timeout is only supported for scalar UDFs"):

        @udf(data_type=pa.int64(), timeout=0.1)
        def array_timeout(x: pa.Array) -> pa.Array:
            return x


def test_udf_timeout_rejects_record_batch_udf() -> None:
    with pytest.raises(ValueError, match="timeout is only supported for scalar UDFs"):

        @udf(data_type=pa.int64(), timeout=0.1)
        def record_batch_timeout(batch: pa.RecordBatch) -> pa.Array:
            return pa.array([1] * len(batch), type=pa.int64())


def test_udf_timeout_warns_about_signal_constraints() -> None:
    with pytest.warns(UserWarning, match="SIGALRM/ITIMER_REAL"):

        @udf(timeout=0.1)
        def warned_timeout_udf(x: int) -> int:
            return x + 1


@pytest.mark.parametrize(
    ("dumps", "loads"),
    [
        pytest.param(std_pickle.dumps, std_pickle.loads, id="pickle"),
        pytest.param(cloudpickle.dumps, cloudpickle.loads, id="cloudpickle"),
    ],
)
def test_udf_roundtrip_fills_missing_timeout_for_legacy_instances(
    dumps: Any, loads: Any
) -> None:
    legacy_udf = udf(data_type=pa.int64())(_legacy_timeout_plus_one)

    object.__delattr__(legacy_udf, "timeout")

    restored = loads(dumps(legacy_udf))

    assert restored.timeout is None
    rb = pa.RecordBatch.from_arrays([pa.array([1], type=pa.int64())], ["x"])
    assert restored(rb) == pa.array([2], type=pa.int64())


@pytest.mark.skipif(
    not HAS_SIGALRM_TIMEOUT, reason="signal.setitimer(SIGALRM) not available"
)
def test_udf_timeout_restores_signal_state_on_success() -> None:
    previous_handler = signal.getsignal(signal.SIGALRM)
    previous_timer = signal.getitimer(signal.ITIMER_REAL)

    def outer_handler(signum, frame) -> None:  # noqa: ARG001
        return None

    try:
        signal.signal(signal.SIGALRM, outer_handler)
        signal.setitimer(signal.ITIMER_REAL, 5.0, 0.0)

        @udf(timeout=0.05)
        def fast(x: int) -> int:
            return x + 1

        rb = pa.RecordBatch.from_arrays([pa.array([1], type=pa.int64())], ["x"])
        assert fast(rb) == pa.array([2], type=pa.int64())
        assert signal.getsignal(signal.SIGALRM) is outer_handler

        restored_timer = signal.getitimer(signal.ITIMER_REAL)
        assert restored_timer[0] > 0.0
        assert restored_timer[0] < 5.0
        assert restored_timer[1] == 0.0
    finally:
        signal.signal(signal.SIGALRM, previous_handler)
        signal.setitimer(signal.ITIMER_REAL, previous_timer[0], previous_timer[1])


@pytest.mark.skipif(
    not HAS_SIGALRM_TIMEOUT, reason="signal.setitimer(SIGALRM) not available"
)
def test_udf_timeout_restores_signal_state_on_failure() -> None:
    previous_handler = signal.getsignal(signal.SIGALRM)
    previous_timer = signal.getitimer(signal.ITIMER_REAL)

    def outer_handler(signum, frame) -> None:  # noqa: ARG001
        return None

    try:
        signal.signal(signal.SIGALRM, outer_handler)
        signal.setitimer(signal.ITIMER_REAL, 5.0, 0.0)

        @udf(timeout=0.01)
        def slow(x: int) -> int:
            time.sleep(0.05)
            return x + 1

        rb = pa.RecordBatch.from_arrays([pa.array([1], type=pa.int64())], ["x"])
        with pytest.raises(TimeoutError, match=r"UDF 'slow' exceeded timeout=0.01"):
            slow(rb)

        assert signal.getsignal(signal.SIGALRM) is outer_handler
        restored_timer = signal.getitimer(signal.ITIMER_REAL)
        assert restored_timer[0] > 0.0
        assert restored_timer[0] < 5.0
        assert restored_timer[1] == 0.0
    finally:
        signal.signal(signal.SIGALRM, previous_handler)
        signal.setitimer(signal.ITIMER_REAL, previous_timer[0], previous_timer[1])


def test_udf_timeout_disarms_alarm_before_restoring_previous_handler(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[str, object, object | None]] = []
    previous_handler = object()

    monkeypatch.setattr(signal, "getsignal", lambda signum: previous_handler)
    monkeypatch.setattr(signal, "getitimer", lambda which: (5.0, 0.0))

    monotonic_values = iter([10.0, 10.5])
    monkeypatch.setattr(time, "monotonic", lambda: next(monotonic_values))

    def fake_signal(signum: object, handler: object) -> object:
        calls.append(("signal", handler, None))
        return handler

    def fake_setitimer(
        which: object, seconds: object, interval: float = 0.0
    ) -> tuple[float, float]:
        calls.append(("setitimer", seconds, interval))
        return (0.0, 0.0)

    monkeypatch.setattr(signal, "signal", fake_signal)
    monkeypatch.setattr(signal, "setitimer", fake_setitimer)

    @udf(timeout=1.0)
    def fast(x: int) -> int:
        return x + 1

    with fast._scalar_timeout_context():
        pass

    assert calls[-3:] == [
        ("setitimer", 0.0, 0.0),
        ("signal", previous_handler, None),
        ("setitimer", 4.5, 0.0),
    ]


def test_udf_task_size_passes_through(caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.WARNING):

        @udf(data_type=pa.int64(), task_size=10)
        def supported(x: int) -> int:
            return x

    assert supported.batch_size is None
    assert supported.task_size == 10


def test_stateful_callable() -> None:
    @udf
    class StatefulFn:
        def __init__(self) -> None:
            self.state = 0

        def __call__(self, x: int) -> int:
            self.state += x
            return self.state

    stateful_fn = StatefulFn()
    assert isinstance(stateful_fn, UDF)
    assert stateful_fn(1) == 1
    assert stateful_fn.arg_type is UDFArgType.SCALAR
    assert stateful_fn.data_type == pa.int64()
    assert stateful_fn.input_columns == ["x"]

    @udf(data_type=pa.int64())
    class StatefulBatchFn:
        def __init__(self) -> None:
            self.state = 0

        def __call__(self, batch: pa.RecordBatch) -> pa.Array:
            self.state += sum(batch.column(0).to_pylist())
            return pa.array([self.state] * batch.num_rows)

    stateful_batch_fn = StatefulBatchFn()
    assert isinstance(stateful_batch_fn, UDF)
    assert stateful_batch_fn.arg_type is UDFArgType.RECORD_BATCH
    assert stateful_batch_fn.data_type == pa.int64()


def test_batched_udf_with_explicity_columns() -> None:
    @udf(data_type=pa.int64())
    def add_columns(a: pa.Array, b: pa.Array) -> pa.Array:
        return pc.add(a, b)

    assert add_columns.arg_type is UDFArgType.ARRAY
    assert add_columns.data_type == pa.int64()
    assert add_columns.input_columns == ["a", "b"]

    with pytest.raises(
        ValueError, match="multiple parameters with 'pa.RecordBatch' type"
    ):

        @udf
        def bad_udf(a: pa.RecordBatch, b: pa.RecordBatch) -> pa.Array:
            return pc.add(a.column(0), b.column(0))


def test_default_no_cuda_no_num_gpus_uses_0_no_warning() -> None:
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")

        @udf
        def f(x: int) -> int:
            return x

        assert isinstance(f, UDF)
        assert f.num_gpus == 0.0
        # No deprecation warning since caller didn't provide cuda
        assert not [w for w in rec if issubclass(w.category, DeprecationWarning)]


@pytest.mark.parametrize(
    ("cuda", "num_gpus", "expected"),
    [
        (True, None, 1.0),  # deprecated behavior
        (False, None, 0.0),  # deprecated behavior
        (False, 1.0, 1.0),  # respect num_gpus over cuda
        (True, 0.0, 0.0),  # respect num_gpus over cuda
        (None, None, 0.0),  # default
        (None, 2.5, 2.5),  # new behavior
        (None, 3, 3.0),  # int to float conversion
    ],
)
def test_fallback_to_cuda_when_num_gpus_none(cuda, num_gpus, expected) -> None:
    ctx = (
        pytest.warns(DeprecationWarning, match=r".*'cuda'.*deprecated.*")
        if cuda
        else nullcontext()
    )
    with ctx:

        @udf(cuda=cuda, num_gpus=num_gpus)
        def f(x: int) -> int:
            return x

    assert f.num_gpus == expected


GE_ZERO_RE = r".*>=\s*0(\.0)?"


def test_negative_num_gpus_rejected_on_init() -> None:
    with pytest.raises(ValueError, match=GE_ZERO_RE):

        @udf(num_gpus=-1)
        def f(x: int) -> int:
            return x


def test_set_time_validation_rejects_negative() -> None:
    @udf(num_gpus=0.0)
    def f(x: int) -> int:
        return x

    with pytest.raises(ValueError, match=GE_ZERO_RE):
        f.num_gpus = -0.1  # on_setattr=attrs.setters.validate should enforce validator


def test_cloudpickle_preserves_num_gpus() -> None:
    """Test that num_gpus is preserved through cloudpickle serialization."""
    import geneva.cloudpickle as cloudpickle

    @udf(num_gpus=2.5)
    def gpu_func(x: int) -> int:
        return x * 2

    # Serialize and deserialize
    pickled = cloudpickle.dumps(gpu_func)
    restored = cloudpickle.loads(pickled)

    # Verify all GPU-related attributes are preserved
    assert restored.num_gpus == 2.5
    assert restored.num_cpus == 1.0
    assert restored.cuda is False


def test_cloudpickle_preserves_cuda_deprecated() -> None:
    """Test that cuda=True (deprecated) is preserved through cloudpickle."""
    import geneva.cloudpickle as cloudpickle

    with pytest.warns(DeprecationWarning, match=r".*'cuda'.*deprecated.*"):

        @udf(cuda=True)
        def cuda_func(x: int) -> int:
            return x * 2

    # Serialize and deserialize
    pickled = cloudpickle.dumps(cuda_func)
    restored = cloudpickle.loads(pickled)

    # cuda=True sets num_gpus=1.0
    assert restored.num_gpus == 1.0
    assert restored.cuda is True


def test_cloudpickle_preserves_cpu_only() -> None:
    """Test that CPU-only UDFs (num_gpus=0) are preserved."""
    import geneva.cloudpickle as cloudpickle

    @udf(num_gpus=0.0)
    def cpu_func(x: int) -> int:
        return x * 2

    pickled = cloudpickle.dumps(cpu_func)
    restored = cloudpickle.loads(pickled)

    assert restored.num_gpus == 0.0
    assert restored.cuda is False


def test_struct_field_input_columns_supported() -> None:
    struct_type = pa.struct(
        [
            ("left", pa.string()),
            ("right", pa.string()),
            ("nested", pa.struct([("x", pa.int32()), ("y", pa.int32())])),
        ]
    )
    schema = pa.schema([pa.field("info", struct_type)])

    @udf(data_type=pa.string(), input_columns=["info.left"])
    def left_upper(left: str | None) -> str | None:
        return left.upper() if left is not None else None

    @udf(data_type=pa.int32(), input_columns=["info.nested.x"])
    def nested_x_plus_one(x: int | None) -> int | None:
        return x + 1 if x is not None else None

    # validate dotted column path against schema
    left_upper.validate_against_schema(schema)
    nested_x_plus_one.validate_against_schema(schema)

    rb = pa.RecordBatch.from_arrays(
        [
            pa.array(
                [
                    {
                        "left": "alpha",
                        "right": "one",
                        "nested": {"x": 1, "y": 10},
                    },
                    {
                        "left": "beta",
                        "right": "two",
                        "nested": {"x": 2, "y": 20},
                    },
                    {
                        "left": None,
                        "right": "three",
                        "nested": {"x": None, "y": None},
                    },
                ],
                type=struct_type,
            )
        ],
        ["info"],
    )

    assert left_upper(rb) == pa.array(["ALPHA", "BETA", None])
    assert nested_x_plus_one(rb) == pa.array([2, 3, None], type=pa.int32())


def test_struct_field_input_columns_support_escaped_literal_dot_fields() -> None:
    struct_type = pa.struct(
        [
            ("a.b", pa.string()),
            ("plain", pa.string()),
        ]
    )
    schema = pa.schema([pa.field("literal", struct_type)])

    @udf(data_type=pa.string(), input_columns=["literal.`a.b`"])
    def literal_dot_upper(value: str | None) -> str | None:
        return value.upper() if value is not None else None

    @udf(data_type=pa.string(), input_columns=["literal.a.b"])
    def unescaped_literal_dot(value: str | None) -> str | None:
        return value

    literal_dot_upper.validate_against_schema(schema)

    with pytest.raises(ValueError, match="not found in table schema"):
        unescaped_literal_dot.validate_against_schema(schema)

    rb = pa.RecordBatch.from_arrays(
        [
            pa.array(
                [
                    {"a.b": "alpha", "plain": "one"},
                    {"a.b": "beta", "plain": "two"},
                    {"a.b": None, "plain": "three"},
                ],
                type=struct_type,
            )
        ],
        ["literal"],
    )

    assert literal_dot_upper(rb) == pa.array(["ALPHA", "BETA", None])


def test_struct_field_input_columns_resolve_case_insensitive() -> None:
    struct_type = pa.struct([("UserId", pa.int32())])
    schema = pa.schema([pa.field("MetaData", struct_type)])

    @udf(data_type=pa.int32(), input_columns=["metadata.userid"])
    def user_id_plus_one(value: int | None) -> int | None:
        return value + 1 if value is not None else None

    user_id_plus_one.validate_against_schema(schema)

    rb = pa.RecordBatch.from_arrays(
        [pa.array([{"UserId": 1}, {"UserId": 2}, {"UserId": None}], type=struct_type)],
        ["MetaData"],
    )
    assert user_id_plus_one(rb) == pa.array([2, 3, None], type=pa.int32())


def test_struct_list_field_numpy_input() -> None:
    struct_type = pa.struct([("vals", pa.list_(pa.int32()))])
    schema = pa.schema([pa.field("info", struct_type)])

    @udf(data_type=pa.int32(), input_columns=["info.vals"])
    def sum_vals(vals: np.ndarray | None) -> int | None:
        if vals is None:
            return None
        assert isinstance(vals, np.ndarray)
        return int(np.sum(vals))

    sum_vals.validate_against_schema(schema)

    rb = pa.RecordBatch.from_arrays(
        [
            pa.array(
                [
                    {"vals": [1, 2, 3]},
                    {"vals": [1]},
                    {"vals": None},
                ],
                type=struct_type,
            )
        ],
        ["info"],
    )

    assert sum_vals(rb) == pa.array([6, 1, None], type=pa.int32())


def test_ndarray_annotation_requires_list_column() -> None:
    schema = pa.schema([pa.field("x", pa.int32())])

    @udf(data_type=pa.list_(pa.int32()))
    def expects_array(x: np.ndarray) -> np.ndarray:
        return x

    with pytest.raises(
        ValueError, match=r"numpy\.ndarray.*list, large_list, or fixed-size"
    ):
        expects_array.validate_against_schema(schema)


def test_list_annotation_requires_list_column() -> None:
    schema = pa.schema([pa.field("x", pa.int32())])

    @udf
    def expects_list(x: list[int]) -> int:
        return len(x)

    with pytest.raises(
        ValueError, match=r"Python list\. List annotations require Arrow list"
    ):
        expects_list.validate_against_schema(schema)


def test_required_params_more_than_input_columns_rejected() -> None:
    schema = pa.schema([pa.field("a", pa.int64()), pa.field("b", pa.int64())])

    @udf(data_type=pa.int64(), input_columns=["a"])
    def add_two(a: int, b: int) -> int:
        return a + b

    with pytest.raises(ValueError, match=r"expects at least 2 parameters"):
        add_two.validate_against_schema(schema)


@pytest.mark.parametrize(
    ("num_gpus", "num_cpus"),
    [
        (0.0, 1.0),
        (1.0, 2.0),
        (2.5, 4.0),
        (None, None),  # None means use defaults
    ],
)
def test_packager_preserves_gpu_cpu_settings(num_gpus, num_cpus) -> None:
    """Test that UDFPackager marshal/unmarshal preserves GPU/CPU settings."""
    from geneva.packager import DockerUDFPackager

    kwargs = {}
    if num_gpus is not None:
        kwargs["num_gpus"] = num_gpus
    if num_cpus is not None:
        kwargs["num_cpus"] = num_cpus

    @udf(**kwargs)
    def compute_func(x: int) -> int:
        return x * 3

    expected_num_gpus = num_gpus if num_gpus is not None else 0.0
    expected_num_cpus = num_cpus if num_cpus is not None else 1.0

    # Create packager without workspace (no workspace zip needed for this test)
    packager = DockerUDFPackager(prebuilt_docker_img="test:latest")

    # Marshal and unmarshal
    spec = packager.marshal(compute_func)
    restored = packager.unmarshal(spec)

    # Verify GPU/CPU settings are preserved
    assert restored.num_gpus == expected_num_gpus
    assert restored.num_cpus == expected_num_cpus
    assert restored.name == compute_func.name


def test_packager_preserves_cuda_deprecated() -> None:
    """Test that packager preserves cuda=True through marshal/unmarshal."""
    from geneva.packager import DockerUDFPackager

    with pytest.warns(DeprecationWarning, match=r".*'cuda'.*deprecated.*"):

        @udf(cuda=True, num_cpus=2.0)
        def cuda_compute(x: int) -> int:
            return x * 4

    packager = DockerUDFPackager(prebuilt_docker_img="test:latest")

    spec = packager.marshal(cuda_compute)
    restored = packager.unmarshal(spec)

    # cuda=True sets num_gpus=1.0
    assert restored.num_gpus == 1.0
    assert restored.cuda is True
    assert restored.num_cpus == 2.0


def test_udf_auto_backfill_default() -> None:
    @udf(data_type=pa.int64())
    def my_func(x: int) -> int:
        return x

    assert my_func.auto_backfill is False


def test_udf_auto_backfill_true() -> None:
    @udf(data_type=pa.int64(), auto_backfill=True)
    def my_func(x: int) -> int:
        return x

    assert my_func.auto_backfill is True


def test_udf_auto_backfill_class_decorator() -> None:
    @udf(data_type=pa.int64(), auto_backfill=True)
    class MyUDF:
        def __call__(self, x: int) -> int:
            return x

    result = MyUDF()
    assert result.auto_backfill is True


class _FakeBlobFile:
    """Minimal stand-in for lance.blob.BlobFile used in unit tests."""

    def __init__(self, data: bytes) -> None:
        self._data = data

    def readall(self) -> bytes:
        return self._data


def test_blob_list_to_record_batch_materializes_blobs(monkeypatch) -> None:
    """BlobFile values are eagerly read into bytes."""
    # Patch BlobFile in transformer so isinstance checks match our fake
    import geneva.transformer as _t

    monkeypatch.setattr(_t, "BlobFile", _FakeBlobFile)

    rows: list[dict[str, Any]] = [
        {"id": 1, "blob": _FakeBlobFile(b"hello")},
        {"id": 2, "blob": _FakeBlobFile(b"the world")},
    ]
    rb = _blob_list_to_record_batch(rows)
    assert isinstance(rb, pa.RecordBatch)
    assert rb.num_rows == 2
    assert rb.column("id").to_pylist() == [1, 2]
    assert rb.column("blob").to_pylist() == [b"hello", b"the world"]


def test_blob_list_to_record_batch_empty(monkeypatch) -> None:
    """Empty row list returns an empty RecordBatch (known limitation: zero columns)."""
    rb = _blob_list_to_record_batch([])
    assert isinstance(rb, pa.RecordBatch)
    assert rb.num_rows == 0


def test_blob_list_to_record_batch_no_blobs() -> None:
    """Rows without any BlobFile pass through unchanged."""
    rows: list[dict[str, Any]] = [
        {"a": 10, "b": "x"},
        {"a": 20, "b": "y"},
    ]
    rb = _blob_list_to_record_batch(rows)
    assert rb.column("a").to_pylist() == [10, 20]
    assert rb.column("b").to_pylist() == ["x", "y"]


def test_scalar_binary_udf_accepts_buffer_outputs() -> None:
    @udf(data_type=pa.large_binary())
    def make_blob(x: int) -> pa.Buffer:
        return pa.py_buffer(f"row-{x}".encode())

    batch = pa.RecordBatch.from_pydict({"x": [1, 2]})

    assert make_blob(batch, use_applier=True).to_pylist() == [b"row-1", b"row-2"]


def test_scalar_binary_udf_accepts_memoryview_outputs() -> None:
    @udf(data_type=pa.large_binary())
    def make_blob(x: int) -> memoryview:
        return memoryview(f"row-{x}".encode())

    batch = pa.RecordBatch.from_pydict({"x": [1, 2]})

    assert make_blob(batch, use_applier=True).to_pylist() == [b"row-1", b"row-2"]


@pytest.mark.parametrize("data_type", [pa.binary(), pa.large_binary()])
def test_scalar_binary_result_builder_allocates_validity_lazily(
    data_type: pa.DataType,
) -> None:
    all_valid = _scalar_results_to_array(iter([b"a", b"bb"]), data_type)

    assert all_valid.to_pylist() == [b"a", b"bb"]
    assert all_valid.null_count == 0
    assert all_valid.buffers()[0] is None

    with_null = _scalar_results_to_array(iter([b"a", None, b"bb"]), data_type)

    assert with_null.to_pylist() == [b"a", None, b"bb"]
    assert with_null.null_count == 1
    assert with_null.buffers()[0] is not None


# ---------------------------------------------------------------------------
# UDF.__call__ dispatch with list[dict] batches  (GEN-410)
# ---------------------------------------------------------------------------


def test_udf_array_dispatch_with_list_dict(monkeypatch) -> None:
    """ARRAY UDF called with list[dict] (blob batch) converts and dispatches."""
    import geneva.transformer as _t

    monkeypatch.setattr(_t, "BlobFile", _FakeBlobFile)

    @udf(data_type=pa.int64(), input_columns=["blob"])
    def blob_len(blob: pa.Array) -> pa.Array:
        return pa.array([len(b.as_py()) for b in blob], type=pa.int64())

    rows = [
        {"id": 1, "blob": _FakeBlobFile(b"hello")},
        {"id": 2, "blob": _FakeBlobFile(b"the world")},
    ]
    # Direct call without use_applier — exercises the expanded guard
    result = blob_len(rows)
    assert result.to_pylist() == [5, 9]


def test_udf_recordbatch_dispatch_with_list_dict(monkeypatch) -> None:
    """RECORD_BATCH UDF called with list[dict] converts and dispatches."""
    import geneva.transformer as _t

    monkeypatch.setattr(_t, "BlobFile", _FakeBlobFile)

    @udf(data_type=pa.int64())
    def rb_blob_len(batch: pa.RecordBatch) -> pa.Array:
        return pa.array(
            [len(b) for b in batch.column("blob").to_pylist()], type=pa.int64()
        )

    rows = [
        {"id": 1, "blob": _FakeBlobFile(b"hello")},
        {"id": 2, "blob": _FakeBlobFile(b"the world")},
    ]
    result = rb_blob_len(rows, use_applier=True)
    assert result.to_pylist() == [5, 9]


def test_has_preprocess_ignores_instance_attribute() -> None:
    """A callable instance attribute named ``preprocess`` is not the protocol.

    Mirrors the in-tree shape of ``GenEmbeddings`` (OpenCLIP), which
    keeps an image-transform callable on ``self.preprocess``. A naive
    ``callable(getattr(instance, 'preprocess'))`` check would treat that
    transform as the optional pipelining hook and route record batches
    through it.
    """

    class StatefulNoProtocol:
        def __init__(self) -> None:
            self.preprocess = lambda x: x  # not the protocol method

        def __call__(self, a: int) -> int:
            return a

    wrapped: UDF = udf(input_columns=["a"], data_type=pa.int64())(StatefulNoProtocol)()
    assert wrapped.has_preprocess() is False


def test_has_preprocess_detects_class_method() -> None:
    """A class-level ``preprocess(self, batch)`` is the protocol."""

    class WithProtocol:
        def preprocess(self, batch: pa.RecordBatch) -> pa.RecordBatch:
            return batch

        def __call__(self, a: int) -> int:
            return a

    wrapped: UDF = udf(input_columns=["a"], data_type=pa.int64())(WithProtocol)()
    assert wrapped.has_preprocess() is True


def test_has_preprocess_false_for_plain_function() -> None:
    """Function UDFs never have preprocess, even with a function attribute."""

    @udf(input_columns=["a"], data_type=pa.int64())
    def fn(a: int) -> int:
        return a

    fn.func.preprocess = lambda x: x  # type: ignore[attr-defined]
    assert fn.has_preprocess() is False


class TestUdfManifestParameter:
    """Tests for the optional manifest= parameter on the @udf decorator."""

    def test_explicit_manifest_stored_on_udf(self) -> None:
        from geneva.manifest import GenevaManifest

        m = GenevaManifest.create_pip("test").pip(["numpy"]).build()

        @udf(data_type=pa.int64(), manifest=m)
        def my_udf(x: int) -> int:
            return x + 1

        assert my_udf.manifest is m

    def test_no_manifest_defaults_to_none(self) -> None:
        @udf(data_type=pa.int64())
        def my_udf(x: int) -> int:
            return x + 1

        assert my_udf.manifest is None

    def test_capture_local_environment_manifest_accepted(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """A manifest produced by ``db.capture_local_environment()``
        (eager upload at call time) is accepted by ``@udf(manifest=...)``."""
        from types import TracebackType

        from geneva.manifest import mgr as mgr_mod
        from geneva.packager.uploader import Uploader

        class _FakeCtx:
            def __enter__(self) -> list[list[str]]:
                return [["s3://upload/workspace.zip"]]

            def __exit__(
                self,
                exc_type: type[BaseException] | None,
                exc: BaseException | None,
                tb: TracebackType | None,
            ) -> None:
                return None

        monkeypatch.setattr(
            "geneva.packager.autodetect.upload_local_env",
            lambda **_k: _FakeCtx(),
        )
        monkeypatch.setattr(
            mgr_mod,
            "_build_capture_uploader",
            lambda _conn: Uploader.__new__(Uploader),
        )

        db = connect(tmp_path)
        capture = db.capture_local_environment(skip_site_packages=True)
        assert capture.zips == [["s3://upload/workspace.zip"]]

        @udf(data_type=pa.int64(), manifest=capture)
        def my_udf(x: int) -> int:
            return x + 1

        assert my_udf.manifest is capture

    def test_non_manifest_type_raises_typeerror(self) -> None:
        with pytest.raises(TypeError, match="GenevaManifest"):

            @udf(data_type=pa.int64(), manifest="not-a-manifest")  # type: ignore[arg-type]
            def my_udf(x: int) -> int:
                return x + 1

    def test_manifest_dict_raises_typeerror(self) -> None:
        """A bare dict is a common mistake — should fail loudly."""
        with pytest.raises(TypeError, match="GenevaManifest"):

            @udf(data_type=pa.int64(), manifest={"image": "foo"})  # type: ignore[arg-type]
            def my_udf(x: int) -> int:
                return x + 1

    def test_manifest_survives_cloudpickle_roundtrip(self) -> None:
        from geneva.manifest import GenevaManifest

        m = (
            GenevaManifest.create_pip("test-roundtrip")
            .pip(["numpy", "pandas"])
            .head_image("custom:latest")
            .build()
        )

        @udf(data_type=pa.int64(), manifest=m)
        def my_udf(x: int) -> int:
            return x + 1

        restored = cloudpickle.loads(cloudpickle.dumps(my_udf))

        assert isinstance(restored, UDF)
        assert restored.manifest is not None
        assert restored.manifest.name == "test-roundtrip"
        assert restored.manifest.pip == ["numpy", "pandas"]
        assert restored.manifest.head_image == "custom:latest"
        # Checksum stable across the round-trip.
        assert restored.manifest.checksum == m.checksum

    def test_partial_form_threads_manifest(self) -> None:
        """`@udf(manifest=m)` with no positional func returns a partial that
        still threads the manifest through when applied to the callable."""
        from geneva.manifest import GenevaManifest

        m = GenevaManifest.create_pip("partial-test").pip(["numpy"]).build()

        decorator = udf(data_type=pa.int64(), manifest=m)

        @decorator
        def my_udf(x: int) -> int:
            return x + 1

        assert isinstance(my_udf, UDF)
        assert my_udf.manifest is m

    def test_class_decorator_threads_manifest(self) -> None:
        """Decorating a class also threads manifest through to the inner UDF."""
        from geneva.manifest import GenevaManifest

        m = GenevaManifest.create_pip("class-test").pip(["numpy"]).build()

        @udf(data_type=pa.int64(), manifest=m)
        class MyUdfFactory:
            def __init__(self) -> None:
                self._offset = 1

            def __call__(self, x: int) -> int:
                return x + self._offset

        instance = MyUdfFactory()  # invoke the wrapper to get a UDF
        assert isinstance(instance, UDF)
        assert instance.manifest is m


def test_checkpoint_version_defaults_to_version() -> None:
    """checkpoint_version is the UDF version when no override is set, and it is
    the token embedded in the key's ``_ver-`` segment."""

    @udf(data_type=pa.int64())
    def my_udf(x: int) -> int:
        return x + 1

    assert my_udf.checkpoint_version == my_udf.version
    prefix = my_udf.checkpoint_prefix(column="c", dataset_uri="memory://t")
    assert f"_ver-{my_udf.checkpoint_version}_col-c_" in prefix


def test_checkpoint_version_uses_override() -> None:
    """An explicit checkpoint_key override drives both checkpoint_version and the
    key's ``_ver-`` token, so mismatch detection compares the right value."""

    @udf(data_type=pa.int64())
    def my_udf(x: int) -> int:
        return x + 1

    my_udf.checkpoint_key = "pinned"
    assert my_udf.checkpoint_version == "pinned"
    prefix = my_udf.checkpoint_prefix(column="c", dataset_uri="memory://t")
    assert "_ver-pinned_col-c_" in prefix
