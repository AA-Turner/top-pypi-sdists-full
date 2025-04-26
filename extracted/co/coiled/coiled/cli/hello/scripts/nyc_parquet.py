import dask.dataframe as dd
from dask.distributed import progress

import coiled

# Spin up cluster
cluster = coiled.Cluster(n_workers=20, region="us-east-2")
client = cluster.get_client()
print("Cluster is up!\n")
print("Dask dashboard:  ", client.dashboard_link)
print("Coiled dashboard:", cluster.details_url, "\n")

# Load dataset
print("Loading Parquet data and aggregating results...")
df = dd.read_parquet(
    "s3://coiled-data/uber/",
    storage_options={"anon": True},
)

# Compute results
results = df[["driver_pay", "base_passenger_fare"]].mean().persist()
progress(results)
driver_pay, passenger_fare = results
print("Average driver pay:     $%0.2f" % driver_pay)
print("Average passenger fare: $%0.2f" % passenger_fare)

# Tip: Press enter to run this cell.
# When you're done, type "exit" + enter to exit IPython.
