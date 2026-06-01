from datetime import datetime
from unittest.mock import patch

import numpy as np
import pytest
import zarr

xr = pytest.importorskip("xarray")

from arraylake.compute.doctor import (
    TIME_CF_KEYS,
    CFDiagnosisMissing,
    check_cf_attribute_completeness,
    fix_cf_noncompliance,
)


@pytest.fixture
def dataset():
    data = np.random.rand(4, 3, 2)
    coords = {"x": [10, 20, 30, 40], "y": [1, 2, 3], "z": [100, 200]}
    ds = xr.Dataset({"data_var": (["x", "y", "z"], data)}, coords=coords)

    return ds


@pytest.fixture
def zarr_store(tmp_path, dataset):
    path = tmp_path / "dataset.zarr"
    dataset.to_zarr(path, mode="w", consolidated=False)
    yield path


def test_no_cf_attrs(dataset):
    mock_inputs = ["y", "y", "y"]
    with patch("builtins.input", side_effect=mock_inputs):
        res = check_cf_attribute_completeness(dataset)

    assert not res.is_healthy
    assert {n.name for n in res.missing} == {"X", "Y", "Z", "T", "longitude", "latitude", "vertical", "time"}
    for m in res.missing:
        if m.name == "X" or m.name == "longitude":
            assert m.proposed_variable == "x"
        elif m.name == "Y" or m.name == "latitude":
            assert m.proposed_variable == "y"
        elif m.name == "Z" or m.name == "vertical":
            assert m.proposed_variable == "z"
        elif m.name == "T" or m.name == "time":
            assert m.proposed_variable is None

    assert res.compatible_services == {"dap2"}
    assert res.incompatible_services == {"wms", "edr", "tiles"}


def test_existing_cf_attrs(dataset):
    # Add CF attributes
    dataset = dataset.copy(deep=True)
    dataset["x"].attrs = {"axis": "X", "standard_name": "longitude"}
    dataset["y"].attrs = {"axis": "Y", "standard_name": "latitude"}
    dataset["z"].attrs = {"axis": "Z", "standard_name": "vertical"}

    res = check_cf_attribute_completeness(dataset)
    assert res.is_healthy
    assert res.compatible_services == {"dap2", "wms", "edr", "tiles"}
    assert res.incompatible_services == set()


def test_some_cf_attrs(dataset):
    # Add CF attributes
    dataset["x"].attrs = {"axis": "X", "standard_name": "longitude"}
    dataset["y"].attrs = {"axis": "Y", "standard_name": "latitude"}
    mock_inputs = ["y"]
    with patch("builtins.input", side_effect=mock_inputs):
        res = check_cf_attribute_completeness(dataset)
    assert res.is_healthy
    assert res.compatible_services == {"dap2", "wms", "edr", "tiles"}
    assert res.incompatible_services == set()
    assert {n.name for n in res.missing} == {"Z", "vertical", "T", "time"}
    dataset["z"].attrs = {"axis": "Z", "standard_name": "vertical"}
    dataset["x"].attrs = {"axis": "X"}
    mock_inputs = ["y"]
    with patch("builtins.input", side_effect=mock_inputs):
        res = check_cf_attribute_completeness(dataset)
    assert not res.is_healthy
    assert {n.name for n in res.missing} == {"longitude", "time", "T"}
    assert res.compatible_services == {"dap2", "edr", "tiles"}
    assert res.incompatible_services == {"wms"}
    assert res.sorted_missing_keys[0] == CFDiagnosisMissing(
        name="longitude", attr_name="standard_name", required=True, proposed_variable="x"
    )

    dataset["x"].attrs = {"standard_name": "longitude"}
    dataset["y"].attrs = {"standard_name": "latitude"}
    dataset["z"].attrs = {"standard_name": "vertical"}
    mock_inputs = ["y"]
    with patch("builtins.input", side_effect=mock_inputs):
        res = check_cf_attribute_completeness(dataset)
    assert not res.is_healthy
    assert {n.name for n in res.missing} == {"X", "Y", "Z", "T", "time"}
    assert res.compatible_services == {"dap2", "tiles", "wms"}
    assert res.incompatible_services == {"edr"}
    for m in res.missing:
        if m.name in TIME_CF_KEYS:
            assert m.proposed_variable is None
        else:
            assert m.proposed_variable is not None


def test_invalid_attrs(dataset):
    dataset["time"] = xr.DataArray(np.array([0, 1, 2, 3]), dims=["time"], attrs={"axis": "T", "standard_name": "time"})

    # Add CF attributes otherwise
    dataset["x"].attrs = {"axis": "X", "standard_name": "longitude"}
    dataset["y"].attrs = {"axis": "Y", "standard_name": "latitude"}
    dataset["z"].attrs = {"axis": "Z", "standard_name": "vertical"}

    res = check_cf_attribute_completeness(dataset)
    assert not res.is_healthy
    assert {n.name for n in res.invalid} == {"T", "time"}

    dataset["time"] = xr.DataArray(np.array([datetime.now()]), dims=["time"], attrs={"axis": "T", "standard_name": "time"})
    res = check_cf_attribute_completeness(dataset)
    assert res.is_healthy


def test_empty_dataset_errors():
    with pytest.raises(ValueError):
        check_cf_attribute_completeness(xr.Dataset(), interactive=False)
    # needed for the service
    check_cf_attribute_completeness(xr.Dataset(), interactive=False, raise_on_empty=False)


def test_grid_mapping_only_dataset(dataset):
    ds = dataset.copy(deep=True)

    ds.coords["crs"] = ((), 0)
    res = check_cf_attribute_completeness(ds, interactive=False)
    assert "grid_mapping" in res.found
    del ds.coords["crs"]

    ds.coords["spatial_ref"] = ((), 0)
    res = check_cf_attribute_completeness(ds, interactive=False)
    assert "grid_mapping" in res.found

    ds.coords["spatial_ref"] = ((), 0, {"grid_mapping_name": "latitude_longitude"})
    assert "grid_mapping" in res.found

    assert res.compatible_services == {"dap2", "tiles"}


@pytest.mark.skipif(zarr.__version__ < "3.0.0", reason="Requires zarr version 3.0.0 or higher")
def test_fix_dataset(dataset, zarr_store):
    mock_inputs = ["y", "y", "y"]
    with patch("builtins.input", side_effect=mock_inputs):
        res = check_cf_attribute_completeness(dataset)
    fix_cf_noncompliance(res, zarr_store, group=None)
    fixed = xr.open_zarr(zarr_store, zarr_version=3, group=None, consolidated=False)

    coordinates = fixed.cf.coordinates
    axes = fixed.cf.axes

    assert coordinates["longitude"][0] == "x"
    assert coordinates["latitude"][0] == "y"
    assert coordinates["vertical"][0] == "z"
    assert "time" not in coordinates
    assert axes["X"][0] == "x"
    assert axes["Y"][0] == "y"
    assert axes["Z"][0] == "z"
    assert "T" not in axes

    res_fixed = check_cf_attribute_completeness(fixed)
    assert res_fixed.is_healthy
    assert res_fixed.compatible_services == {"dap2", "wms", "tiles", "edr"}
