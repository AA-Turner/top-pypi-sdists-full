import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
import numpy as np
import matplotlib.pyplot as plt
import math

# Input / Output paths
input_path = r"D:\Users\ritvik\projects\GEOGLAM\Input\Global_Datasets\Masks\wolayita_maize.tif"
output_path = r"D:\Users\ritvik\projects\GEOGLAM\Input\Global_Datasets\Masks\wolayita_maize_5km_percentage.tif"

import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from math import ceil
import numpy as np

input_path = r"D:\Users\ritvik\projects\GEOGLAM\Input\Global_Datasets\Masks\wolayita_maize.tif"
output_path = r"D:\Users\ritvik\projects\GEOGLAM\Input\Global_Datasets\Masks\wolayita_maize_5km_percentage.tif"

with rasterio.open(input_path) as src:
    # 1) If needed, assign correct CRS
    # Example: if you know it's actually EPSG:32637 but isn't set
    # src_crs = rasterio.crs.CRS.from_epsg(32637)
    # else if it's already correct, do:
    src_crs = src.crs

    # 2) Decide your pixel size.
    # If src_crs is lat/lon (EPSG:4326), use ~0.045 deg for ~5 km.
    # If src_crs is UTM in meters, use 5000 for 5 km.
    pixel_size = 0.045  # or 5000 if in meters

    transform, width, height = calculate_default_transform(
        src_crs,  # source crs
        src_crs,  # target crs (same if you just want coarser in place)
        src.width,
        src.height,
        *src.bounds,
        resolution=pixel_size
    )

    # Prepare output fraction array
    fraction_array = np.full((height, width), -9999, dtype=np.float32)

    # Reproject with average -> fraction
    reproject(
        source=rasterio.band(src, 1),
        destination=fraction_array,
        src_transform=src.transform,
        src_crs=src_crs,
        dst_transform=transform,
        dst_crs=src_crs,
        resampling=Resampling.average,
        dst_nodata=-9999
    )

# Now fraction_array should have values in [0..1], with -9999 for nodata.
valid_mask = (fraction_array != -9999)

if not np.any(valid_mask):
    print("No valid cells at all (everything is nodata). This indicates a bounding box or CRS mismatch.")
else:
    frac_min = fraction_array[valid_mask].min()
    frac_max = fraction_array[valid_mask].max()
    print("Fraction min:", frac_min)
    print("Fraction max:", frac_max)

    # If both min and max are 0.0, it means there's truly no coverage or it's extremely small.
    # Otherwise you might see something like 0.0, 0.01, 0.5, etc.

    # Then let's see if maybe they're all below 0.005:
    below_005 = (fraction_array[valid_mask] < 0.005).all()
    print("All fractions < 0.5%?", below_005)

breakpoint()
with rasterio.open(input_path) as src:
    # If src.crs is None but you KNOW it's EPSG:4326, assign it:
    # src_crs = rasterio.crs.CRS.from_epsg(4326)
    # Otherwise, just use what's in the file:
    src_crs = src.crs

    # Let's assume the file is already lat/lon (EPSG:4326).
    # We'll define ~0.045° as "5 km" at the equator.
    new_res = 0.045

    # Calculate a new transform and new shape
    # for coarser resolution in the SAME EPSG:4326.
    transform, width, height = calculate_default_transform(
        src_crs,  # src CRS
        src_crs,  # dst CRS (same if you want to stay in lat/lon)
        src.width,
        src.height,
        *src.bounds,
        resolution=new_res  # sets pixel size to 0.045 degrees
    )

    # Read full data for histogram plotting
    data_in = src.read(1, masked=True)
    in_profile = src.profile.copy()

# Plot input histogram (0 or 1)
arr_in = data_in.compressed()
plt.figure()
plt.hist(arr_in, bins=[-0.5, 0.5, 1.5], edgecolor='black')
plt.title("Input (0/1)")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.show()

# Prepare output array, float32 with sentinel -9999
out_array = np.full((height, width), -9999, dtype=np.float32)

with rasterio.open(input_path) as src:
    reproject(
        source=rasterio.band(src, 1),
        destination=out_array,
        src_transform=src.transform,
        src_crs=src.crs,
        dst_transform=transform,
        dst_crs=src_crs,  # same
        resampling=Resampling.average,
        dst_nodata=-9999
    )

# Now out_array has fraction in [0..1]. Convert to % (0..100).
breakpoint()
mask_valid = (out_array != -9999)
out_array[mask_valid] *= 100.0
out_array[mask_valid] = np.rint(out_array[mask_valid])  # round
out_array = out_array.astype(np.int32)

# Update profile
out_profile = in_profile.copy()
out_profile.update({
    'driver': 'GTiff',
    'width': width,
    'height': height,
    'transform': transform,
    'crs': src_crs,
    'dtype': 'int32',
    'nodata': -9999
})

# Write out
with rasterio.open(output_path, 'w', **out_profile) as dst:
    dst.write(out_array, 1)

print("Wrote:", output_path)

# Plot histogram of output (ignore -9999)
out_data = np.where(out_array == -9999, np.nan, out_array)
valid_data = out_data[~np.isnan(out_data)]
plt.figure()
plt.hist(valid_data, bins=50, edgecolor="black")
plt.title("5km Percentage (0-100)")
plt.xlabel("Percent cropped")
plt.ylabel("Frequency")
plt.show()
