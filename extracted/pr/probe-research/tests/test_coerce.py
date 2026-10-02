"""`probe.sdk.coerce`: what researchers pass as config, as plain JSON (plan (c)).

Before, every non-JSON config value became its repr() on the way out
(`unstorable.normalize_json`): a Namespace or a dataclass arrived as ONE string,
a Hydra DictConfig as "{'lr': 0.1}", a numpy float as "np.float32(0.1)".
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime as dt
import enum
import json
import pathlib
import subprocess
import sys
import warnings

import pytest

from probe import errors
from probe.sdk import coerce

np = pytest.importorskip("numpy")


class Mode(enum.Enum):
    FAST = "fast"


@dataclasses.dataclass
class Optim:
    lr: float = 3e-4
    betas: tuple = (0.9, 0.99)
    mode: Mode = Mode.FAST


def test_namespace_dataclass_enum_date_path_and_sets_become_plain_json():
    config = coerce.to_config(
        argparse.Namespace(
            optim=Optim(),
            started=dt.date(2026, 9, 27),
            at=dt.datetime(2026, 9, 27, 12, 0, tzinfo=dt.timezone.utc),
            out=pathlib.Path("/runs/a"),
            seeds={3, 1, 2},
        )
    )
    assert config == {
        "optim": {"lr": 3e-4, "betas": [0.9, 0.99], "mode": "fast"},
        "started": "2026-09-27",
        "at": "2026-09-27T12:00:00+00:00",
        "out": "/runs/a",
        "seeds": [1, 2, 3],
    }
    json.dumps(config, allow_nan=False)  # strictly JSON


def test_non_finite_floats_become_strings_json_can_hold():
    assert coerce.to_config({"a": float("nan"), "b": float("inf"), "c": -float("inf")}) == {
        "a": "NaN",
        "b": "Infinity",
        "c": "-Infinity",
    }


def test_numpy_scalars_small_arrays_and_big_arrays():
    config = coerce.to_config(
        {
            "f": np.float32(0.5),
            "i": np.int64(3),
            "b": np.bool_(True),
            "small": np.arange(3),
            "nan_inside": np.array([1.0, np.nan]),
            "big": np.zeros(5_000),
        }
    )
    assert config["f"] == 0.5 and config["i"] == 3 and config["b"] is True
    assert config["small"] == [0, 1, 2]
    assert config["nan_inside"] == [1.0, "NaN"]
    assert config["big"] == "<ndarray shape=(5000,) dtype=float64>"


def test_a_dictconfig_is_resolved_and_a_missing_value_never_raises():
    omegaconf = pytest.importorskip("omegaconf")
    cfg = omegaconf.OmegaConf.create(
        {"opt": {"lr": 3e-4, "warmup_lr": "${opt.lr}"}, "data": "???", "tags": ["a", "b"]}
    )
    assert coerce.to_config(cfg) == {
        "opt": {"lr": 3e-4, "warmup_lr": 3e-4},
        "data": "???",
        "tags": ["a", "b"],
    }
    broken = omegaconf.OmegaConf.create({"a": "${nowhere.x}"})
    assert coerce.to_config(broken) == {"a": "${nowhere.x}"}


def test_a_pydantic_model_becomes_its_fields():
    pydantic = pytest.importorskip("pydantic")

    class Cfg(pydantic.BaseModel):
        lr: float = 0.1
        name: str = "adam"

    assert coerce.to_config(Cfg()) == {"lr": 0.1, "name": "adam"}


def test_a_cycle_is_cut_not_followed():
    loop: dict = {"a": 1}
    loop["self"] = loop
    config = coerce.to_config(loop)
    assert config["a"] == 1 and isinstance(config["self"], str)


def test_non_string_keys_become_strings():
    assert coerce.to_config({1: "a", Mode.FAST: "b"}) == {"1": "a", "Mode.FAST": "b"}


@pytest.mark.parametrize("bad", [[1, 2], "lr=0.1", 3, None])
def test_a_top_level_that_is_not_a_mapping_is_refused_locally(bad):
    with pytest.raises(errors.ValidationError, match="config must be a mapping"):
        coerce.to_config(bad)


def test_an_unknown_leaf_is_its_repr_as_before():
    class Opaque:
        def __repr__(self) -> str:
            return "<opaque>"

    assert coerce.to_config({"x": Opaque()}) == {"x": "<opaque>"}


# -- Run.log's metric unwrapping ------------------------------------------------
def test_array_scalar_unwraps_one_element_and_refuses_many():
    with warnings.catch_warnings():
        # numpy >= 1.25 WARNS on float(np.array([x])); under -W error that
        # warning used to raise into the training loop.
        warnings.simplefilter("error")
        assert coerce.array_scalar(np.float32(0.25)) == 0.25
        assert coerce.array_scalar(np.array([1.5])) == 1.5
        assert coerce.array_scalar(np.array([[2.0]])) == 2.0
        assert coerce.array_scalar(np.bool_(True)) == 1.0
    assert coerce.array_scalar(np.zeros(3)) is None
    assert coerce.array_scalar(0.3) is coerce.NOT_AN_ARRAY
    assert coerce.array_scalar("0.3") is coerce.NOT_AN_ARRAY


class _TorchShaped:
    """The slice of `torch.Tensor` coerce touches: size() is the SHAPE there,
    numel() the count, item() the value. `__module__` is what marks it."""

    __module__ = "torch"

    def __init__(self, values):
        self.values = list(values)
        self.ndim = 0 if len(self.values) == 1 else 1

    def numel(self):
        return len(self.values)

    def size(self):
        return (len(self.values),)

    def item(self):
        if len(self.values) != 1:
            raise RuntimeError("a Tensor with 2 elements cannot be converted to Scalar")
        return self.values[0]

    def detach(self):
        return self

    def cpu(self):
        return self

    def tolist(self):
        return list(self.values)


def test_a_tensor_is_read_by_numel_not_by_its_shape():
    assert coerce.array_scalar(_TorchShaped([0.5])) == 0.5
    assert coerce.array_scalar(_TorchShaped([0.5, 0.25])) is None
    assert coerce.to_config({"t": _TorchShaped([1.0, 2.0])}) == {"t": [1.0, 2.0]}


def test_a_real_tensor_with_grad_unwraps():
    torch = pytest.importorskip("torch")
    loss = torch.tensor(0.5, requires_grad=True) * 2
    assert coerce.array_scalar(loss) == 1.0
    assert coerce.array_scalar(torch.ones(3)) is None


def test_scalar_is_only_for_zero_d_values():
    assert coerce.scalar(np.int64(3)) == 3
    assert coerce.scalar(np.zeros(2)) is coerce.NOT_AN_ARRAY
    assert coerce.scalar(3) is coerce.NOT_AN_ARRAY


def test_importing_probe_loads_none_of_the_libraries_it_recognises():
    code = (
        "import sys, probe, probe.sdk.coerce, probe.sdk.run;"
        "loaded = {'numpy', 'omegaconf', 'torch'} & set(sys.modules);"
        "print(sorted(loaded))"
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert out.stdout.strip() == "[]"


# -- #2032 review ---------------------------------------------------------------
def test_a_dictconfig_never_resolves_a_secret_but_resolves_the_rest(monkeypatch):
    omegaconf = pytest.importorskip("omegaconf")
    monkeypatch.setenv("SERVICE_KEY", "env-value-123456")
    cfg = omegaconf.OmegaConf.create(
        {
            "db": {"password": "hunter2hunter2"},
            "url": "postgres://u:${db.password}@h/db",
            "key": "${oc.env:SERVICE_KEY}",
            "opt": {"lr": 0.1, "warmup_lr": "${opt.lr}"},
            "tags": ["${opt.lr}", "${oc.env:SERVICE_KEY}"],
        }
    )
    config = coerce.to_config(cfg)
    assert config["url"] == "postgres://u:${db.password}@h/db"
    assert config["key"] == "${oc.env:SERVICE_KEY}"
    assert config["opt"] == {"lr": 0.1, "warmup_lr": 0.1}
    assert config["tags"] == [0.1, "${oc.env:SERVICE_KEY}"]


def test_a_dataclass_field_with_repr_false_is_left_out():
    @dataclasses.dataclass
    class Conn:
        host: str = "h"
        token: str = dataclasses.field(default="secret-value", repr=False)

    assert coerce.to_config(Conn()) == {"host": "h"}


def test_a_pydantic_field_with_repr_false_is_left_out_like_a_dataclass_one():
    """`Field(repr=False)` is pydantic's mark for a field not to show; it was
    sent anyway while a dataclass's `repr=False` field was dropped. Nested
    models are walked the same way."""
    pydantic = pytest.importorskip("pydantic")

    class Conn(pydantic.BaseModel):
        host: str = "h"
        token: str = pydantic.Field(default="secret-value", repr=False)

    class Cfg(pydantic.BaseModel):
        lr: float = 0.1
        conn: Conn = Conn()
        cache: dict = pydantic.Field(default_factory=lambda: {"big": 1}, repr=False)

    assert coerce.to_config(Cfg()) == {"lr": 0.1, "conn": {"host": "h"}}
    assert coerce.to_config(Conn(host="db")) == {"host": "db"}
    assert coerce.to_config(pydantic.RootModel[dict]({"a": 1})) == {"a": 1}, "as model_dump gave"


def test_torchvision_and_torchmetrics_objects_are_not_tensors():
    class Transform:
        __module__ = "torchvision.transforms"

        def item(self):  # pragma: no cover -- must never be called
            raise AssertionError("treated as a tensor")

    class Metric:
        __module__ = "torchmetrics.classification"

        def item(self):  # pragma: no cover
            raise AssertionError("treated as a tensor")

    assert coerce.array_scalar(Transform()) is coerce.NOT_AN_ARRAY
    assert coerce.array_scalar(Metric()) is coerce.NOT_AN_ARRAY


def test_keys_that_collide_as_json_strings_warn():
    with pytest.warns(UserWarning, match="both become '1'"):
        assert coerce.to_config({1: "a", "1": "b"}) == {"1": "b"}


# -- jax arrays (environment matrix E2) ----------------------------------------
class _JaxShaped:
    """The slice of ``jax.Array`` (``jaxlib._jax.ArrayImpl``) coerce touches:
    ``size`` is an int attribute, ``item()`` / ``tolist()`` as numpy's, and
    ``float()`` REFUSES anything with ``ndim > 0`` -- a size-1 vector included
    ("Only scalar arrays can be converted to Python scalars"), unlike numpy."""

    __module__ = "jaxlib._jax"

    def __init__(self, values, ndim=None):
        self.values = list(values)
        self.ndim = (0 if len(self.values) == 1 else 1) if ndim is None else ndim
        self.size = len(self.values)

    def item(self):
        if self.size != 1:
            raise TypeError("item() needs one element")
        return self.values[0]

    def tolist(self):
        return self.values[0] if self.ndim == 0 else list(self.values)

    def __float__(self):
        if self.ndim:
            raise TypeError(f"Only scalar arrays can be converted to Python scalars; got arr.ndim={self.ndim}")
        return float(self.values[0])

    def __repr__(self):
        return f"Array({self.tolist()}, dtype=float32)"


def test_a_size_one_jax_vector_is_a_metric_like_numpys():
    from probe.sdk.run import _as_metric_value

    # np.array([3.5]) is a point; jnp.array([3.5]) went to the step record as
    # its repr, with a "not JSON-serialisable" warning.
    assert _as_metric_value(np.array([3.5])) == 3.5
    assert _as_metric_value(_JaxShaped([3.5], ndim=1)) == 3.5
    assert _as_metric_value(_JaxShaped([1.5])) == 1.5
    assert _as_metric_value(_JaxShaped([1.0, 2.0])) is None


def test_jax_values_in_config_are_numbers_not_their_repr():
    from probe.sdk.unstorable import normalize_json

    # update_config({"lr": jnp.float32(0.1)}) stored "Array(0.1, dtype=float32)".
    assert coerce.to_config({"lr": _JaxShaped([0.1]), "w": _JaxShaped([1.0, 2.0])}) == {
        "lr": 0.1,
        "w": [1.0, 2.0],
    }
    assert coerce.scalar(_JaxShaped([0.25])) == 0.25
    assert normalize_json({"lr": _JaxShaped([0.25])}) == {"lr": 0.25}


def test_real_jax_arrays():
    jnp = pytest.importorskip("jax.numpy")
    from probe.sdk.run import _as_metric_value

    assert _as_metric_value(jnp.array([3.5])) == 3.5
    assert _as_metric_value(jnp.array(2.25)) == 2.25
    assert _as_metric_value(jnp.array([1.0, 2.0])) is None
    assert coerce.to_config({"lr": jnp.float32(0.5), "w": jnp.array([1.0, 2.0])}) == {
        "lr": 0.5,
        "w": [1.0, 2.0],
    }
