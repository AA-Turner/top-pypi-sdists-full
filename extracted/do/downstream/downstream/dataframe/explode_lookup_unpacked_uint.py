import functools
import logging

from joinem import dataframe_cli

from .._version import __version__ as downstream_version
from ._explode_lookup_unpacked import explode_lookup_unpacked

if __name__ == "__main__":
    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
    )
    dataframe_cli(
        description="Explode downstream-curated data from one-buffer-per-row "
        "(with each buffer containing multiple data items) to "
        "one-data-item-per-row, applying downstream lookup to identify origin "
        "time `Tbar` of each item.",
        module="downstream.dataframe.explode_lookup_unpacked_uint",
        version=downstream_version,
        output_dataframe_op=functools.partial(
            explode_lookup_unpacked,
            value_type="uint64",
        ),
    )
