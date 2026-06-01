from typing import TYPE_CHECKING, Literal, TypeAlias

import numpy as np
import zarr
from pydantic import BaseModel, computed_field

from arraylake.log_util import get_logger

if TYPE_CHECKING:
    from xarray import Dataset

logger = get_logger(__name__)


# sentinel key indicating some grid_mapping is present
GRID_MAPPING_SENTINEL_KEY: "CFAttributeKey" = "grid_mapping"
CFAttributeName: TypeAlias = Literal["axis", "standard_name"]
CFAttributeKey: TypeAlias = Literal["X", "Y", "Z", "latitude", "longitude", "vertical", "T", "time", "grid_mapping"]
SPATIAL_CF_KEYS: list[CFAttributeKey] = ["X", "Y", "Z", "latitude", "longitude", "vertical"]
TIME_CF_KEYS: list[CFAttributeKey] = ["T", "time"]
AXIS_CF_KEYS: list[CFAttributeKey] = ["X", "Y", "Z", "T"]
STANDARD_NAME_CF_KEYS: list[CFAttributeKey] = ["latitude", "longitude", "vertical", "time"]
ARRAYLAKE_COMPUTE_SERVICES: TypeAlias = Literal["dap2", "edr", "tiles", "wms"]
EDR_REQUIRED_CF_KEYS: list[CFAttributeKey] = ["X", "Y"]
WMS_REQUIRED_CF_KEYS: list[CFAttributeKey] = ["latitude", "longitude"]
REQUIRED_CF_KEYS: list[CFAttributeKey] = EDR_REQUIRED_CF_KEYS + WMS_REQUIRED_CF_KEYS
GRID_MAPPING_KEYS = [GRID_MAPPING_SENTINEL_KEY, "spatial_ref", "crs"]


class CFDiagnosisMissing(BaseModel):
    name: CFAttributeKey
    attr_name: CFAttributeName
    required: bool
    proposed_variable: str | None

    def __hash__(self):
        return hash((self.name, self.required))

    def __lt__(self, other: "CFDiagnosisMissing") -> bool:
        if self.required != other.required:
            return not self.required
        if self.proposed_variable is None and other.proposed_variable is not None:
            return True
        return False


class CFDiagnosisInvalid(BaseModel):
    name: CFAttributeKey
    attr_name: CFAttributeName
    issue: str

    def __hash__(self):
        return hash((self.name, self.issue))


class CFDiagnosisSummary(BaseModel):
    found: set[CFAttributeKey]  # All of the correct CF keys found
    missing: set[CFDiagnosisMissing]
    invalid: set[CFDiagnosisInvalid]

    @property
    def missing_required_keys(self) -> bool:
        return any(m.required for m in self.missing)

    @property
    def sorted_missing_keys(self) -> list[CFDiagnosisMissing]:
        return sorted(self.missing, reverse=True)

    @property
    def has_invalid_keys(self) -> bool:
        return len(self.invalid) > 0

    @computed_field  # type: ignore[prop-decorator]
    @property
    def is_healthy(self) -> bool:
        return not self.missing_required_keys and not self.has_invalid_keys

    @computed_field  # type: ignore[prop-decorator]
    @property
    def compatible_services(self) -> set[ARRAYLAKE_COMPUTE_SERVICES]:
        compatible: set[ARRAYLAKE_COMPUTE_SERVICES] = {"dap2"}
        if _is_edr_compatible(self.found):
            compatible.add("edr")
        if _is_wms_compatible(self.found):
            compatible.add("wms")
        if _is_tiles_compatible(self.found):
            compatible.add("tiles")
        return compatible

    @computed_field  # type: ignore[prop-decorator]
    @property
    def incompatible_services(self) -> set[ARRAYLAKE_COMPUTE_SERVICES]:
        incompatible: set[ARRAYLAKE_COMPUTE_SERVICES] = set()
        if not _is_edr_compatible(self.found):
            incompatible.add("edr")
        if not _is_wms_compatible(self.found):
            incompatible.add("wms")
        if not _is_tiles_compatible(self.found):
            incompatible.add("tiles")
        return incompatible


def _guess_cf_axes_and_coords(ds: "Dataset", interactive: bool = True) -> "Dataset":
    import cf_xarray  # noqa

    new_ds = ds.cf.guess_coord_axis()
    cf_rep = new_ds.cf
    coords = cf_rep.coordinates
    axes = cf_rep.axes

    # In non-interactive mode (server context), make reasonable assumptions
    if "longitude" not in coords and "X" in axes:
        if len(axes["X"]) == 1 and any(key not in new_ds[axes["X"][0]].attrs for key in ["standard_name", "units"]):
            if interactive:
                message = f"Does the X axis ({axes['X'][0]!r}) represent longitude? (y/n): "
                modify_x = input(message).lower() == "y"
            else:
                # In server mode, assume X axis represents longitude if it's missing standard_name
                modify_x = "standard_name" not in new_ds[axes["X"][0]].attrs
            if modify_x:
                new_ds[axes["X"][0]].attrs["standard_name"] = "longitude"
    if "latitude" not in coords and "Y" in axes:
        if len(axes["Y"]) == 1 and any(key not in new_ds[axes["Y"][0]].attrs for key in ["standard_name", "units"]):
            if interactive:
                message = f"Does the Y axis ({axes['Y'][0]!r}) represent latitude? (y/n): "
                modify_y = input(message).lower() == "y"
            else:
                # In server mode, assume Y axis represents latitude if it's missing standard_name
                modify_y = "standard_name" not in new_ds[axes["Y"][0]].attrs
            if modify_y:
                new_ds[axes["Y"][0]].attrs["standard_name"] = "latitude"
    if "vertical" not in coords and "Z" in axes:
        if len(axes["Z"]) == 1 and any(key not in new_ds[axes["Z"][0]].attrs for key in ["standard_name", "units"]):
            if interactive:
                message = f"Does the Z axis ({axes['Z'][0]!r}) represent vertical? (y/n): "
                modify_z = input(message).lower() == "y"
            else:
                # In server mode, assume Z axis represents vertical if it's missing standard_name
                modify_z = "standard_name" not in new_ds[axes["Z"][0]].attrs
            if modify_z:
                new_ds[axes["Z"][0]].attrs["standard_name"] = "vertical"
    if "time" not in coords and "T" in axes:
        if len(axes["T"]) == 1 and any(key not in new_ds[axes["T"][0]].attrs for key in ["standard_name", "units"]):
            if interactive:
                message = f"Does the T axis ({axes['T'][0]!r}) represent time? (y/n): "
                modify_t = input(message).lower() == "y"
            else:
                # In server mode, assume T axis represents time if it's missing standard_name
                modify_t = "standard_name" not in new_ds[axes["T"][0]].attrs
            if modify_t:
                new_ds[axes["T"][0]].attrs["standard_name"] = "time"

    return new_ds


def _is_edr_compatible(keys: set[CFAttributeKey]) -> bool:
    return all(k in keys for k in EDR_REQUIRED_CF_KEYS)


def _is_wms_compatible(keys: set[CFAttributeKey]) -> bool:
    return all(k in keys for k in WMS_REQUIRED_CF_KEYS)


def _is_tiles_compatible(keys: set[CFAttributeKey]) -> bool:
    return _is_edr_compatible(keys) or _is_wms_compatible(keys) or GRID_MAPPING_SENTINEL_KEY in keys


def check_cf_attribute_completeness(ds: "Dataset", *, interactive: bool = True, raise_on_empty: bool = True) -> CFDiagnosisSummary:
    """Returns a dictionary of the CF compliance errors in the provided dataset.

    Args:
        ds: The xarray dataset to check.
        interactive: Whether to prompt user for input when guessing CF attributes.
        raise_on_empty: Whether to raise for an empty dataset

    Returns:
        dict: A diagnostic dictionary containing the found, missing, and invalid CF compliance errors.
    """
    import cf_xarray  # noqa

    if raise_on_empty and not ds.variables:
        raise ValueError("Attempting to diagnose an empty dataset. Please pass an appropriate --group argument.")

    cf_keys = ds.cf.keys()
    if ds.cf.grid_mapping_names or "spatial_ref" in ds.variables or "crs" in ds.variables:
        cf_keys.add(GRID_MAPPING_SENTINEL_KEY)
    found, missing, invalid = (
        set[CFAttributeKey](),
        set[CFDiagnosisMissing](),
        set[CFDiagnosisInvalid](),
    )

    # Guess the axes, to use for fixing missing attributes
    proposed_fix_ds = _guess_cf_axes_and_coords(ds, interactive=interactive)

    for k in SPATIAL_CF_KEYS:
        if k in cf_keys:
            found.add(k)
        else:
            # Only X,Y,Lat,Lng are required always
            required = k in REQUIRED_CF_KEYS
            if k in proposed_fix_ds.cf.keys():
                proposed_variable = proposed_fix_ds.cf[k].name
            else:
                logger.debug(f"Error getting proposed variable for {k}")
                proposed_variable = None
            spatial_attr_name: CFAttributeName = "axis" if k in AXIS_CF_KEYS else "standard_name"
            missing.add(CFDiagnosisMissing(name=k, attr_name=spatial_attr_name, required=required, proposed_variable=proposed_variable))

    for gk in GRID_MAPPING_KEYS:
        if gk in cf_keys:
            found.add(GRID_MAPPING_SENTINEL_KEY)

    # If time vars are provided, they must have a dtype of datetime 64. This
    # could be potentially smarter, by checking the dimensions and then checking
    # if any dims have datetime types
    for t in TIME_CF_KEYS:
        time_attr_name: CFAttributeName = "axis" if t in AXIS_CF_KEYS else "standard_name"
        if t in cf_keys:
            dtype = ds.cf[t].dtype
            is_datetime = np.issubdtype(dtype, np.datetime64)
            if is_datetime:
                found.add(t)
            else:
                invalid.add(
                    CFDiagnosisInvalid(
                        name=t,
                        attr_name=time_attr_name,
                        issue=f"Expected {t} to be datetime-like, found dtype {dtype}",
                    )
                )
        else:
            try:
                if t == "time":
                    # Time isn't guessed by cf xarray
                    proposed_variable = proposed_fix_ds.cf["T"].name
                else:
                    proposed_variable = proposed_fix_ds.cf[t].name
            except Exception as e:
                logger.debug(f"Error getting proposed variable for {t}: {e}")
                proposed_variable = None

            missing.add(CFDiagnosisMissing(name=t, attr_name=time_attr_name, required=False, proposed_variable=proposed_variable))

    return CFDiagnosisSummary(found=found, missing=missing, invalid=invalid)


def fix_cf_noncompliance(diagnosis: CFDiagnosisSummary, store: str, group: str | None):
    """Returns a fixed dataset based on the provided CF compliance diagnosis.

    Also updates the attributes in the Zarr store with the values from the xarray.Dataset.

    Args:
        diagnosis: The CF compliance diagnosis.
        store: The Zarr store to update with the fixed attributes.
        group: The group within the Zarr store to update with the fixed attributes.

    Returns:
        Dataset: The fixed dataset.
    """
    zarr_store: zarr.Group = zarr.open(store, zarr_format=3, mode="r+", path=group)  # type: ignore[unused-ignore,assignment]
    for m in diagnosis.missing:
        if m.proposed_variable:
            # Write updated attributes to store
            # This must be done with the zarr API since xarray does not support metadata-only updates
            zarr_store[m.proposed_variable].attrs[m.attr_name] = m.name
