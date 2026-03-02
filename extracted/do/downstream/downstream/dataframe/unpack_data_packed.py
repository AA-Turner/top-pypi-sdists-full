from joinem import dataframe_cli

from .._version import __version__ as downstream_version
from ._unpack_data_packed import unpack_data_packed

if __name__ == "__main__":
    dataframe_cli(
        description="Unpack data with dstream buffer and counter serialized "
        "into a single hexadecimal data field.",
        module="downstream.dataframe.unpack_data_packed",
        version=downstream_version,
        output_dataframe_op=unpack_data_packed,
    )
