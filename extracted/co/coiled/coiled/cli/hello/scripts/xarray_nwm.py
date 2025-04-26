import xarray as xr
from dask.distributed import progress

import coiled

# Spin up cluster
cluster = coiled.Cluster(
    n_workers=50,
    region="us-east-1",
)
client = cluster.get_client()
print("Cluster is up!\n")
print("Dask dashboard:  ", client.dashboard_link)
print("Coiled dashboard:", cluster.details_url, "\n")

# Load NWM dataset
print("Loading Zarr data and doing spatial average...")
ds = xr.open_zarr(
    "s3://noaa-nwm-retrospective-2-1-zarr-pds/rtout.zarr",
    consolidated=True,
    storage_options={"anon": True},
).drop_encoding()
data = ds.zwattablrt.sel(time=slice("2020-01-01", "2020-03-31"))

# Aggregate over space
avg = data.mean(dim=["x", "y"]).persist()
progress(avg)
print("Result:", avg.compute())

# Tip: Press enter to run this cell.
# When you're done, type "exit" + enter to exit IPython.
