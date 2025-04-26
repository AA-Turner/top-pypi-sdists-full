from __future__ import annotations

from rich.markdown import Markdown

from ..utils import render_example


def xarray_nwm() -> bool | None:
    msg_start = Markdown(
        """
## Example: Aggregate 2 TB of geospatial data

NOAA hosts their National Water Model (NWM) on AWS in this bucket

```
s3://noaa-nwm-retrospective-2-1-zarr-pds
```

Let's use Xarray, Dask, and Coiled to churn through this data
and compute a spatial average.\n
"""
    )

    return render_example(
        name="xarray-nwm",
        dependencies=["coiled", "dask", "numpy", "bokeh", "xarray", "zarr", "s3fs", "ipython"],
        msg_start=msg_start,
    )
