from __future__ import annotations

from rich.markdown import Markdown

from ..utils import (
    render_example,
)


def nyc_parquet() -> bool | None:
    msg_start = Markdown(
        """
## Example: Aggregate 1 TB of Parquet data

There's 1 TB of Parquet data sitting in this S3 bucket:

```
s3://coiled-data/uber/
```

Let's run this Python script to calculate how much Uber/Lyft riders paid vs
how much Uber/Lyft drivers got paid in NYC.\n
""".strip()
    )

    return render_example(
        name="nyc-parquet",
        dependencies=["coiled", "dask", "bokeh", "numpy", "pandas", "pyarrow", "s3fs", "ipython"],
        msg_start=msg_start,
    )
