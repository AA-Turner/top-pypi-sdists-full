from typing import Union, Any, ParamSpec
import pandas as pd
import orjson
import pyarrow as pa
import pyarrow.csv as pc
import pyarrow.parquet as pq
from io import BytesIO
from .abstract import BaseDataframe
from ...exceptions import ComponentError, DataNotFound


P = ParamSpec("P")


def is_empty(obj):
    """check_empty.
    Check if a basic object, a Apache Arrow Table is empty or not.
    """
    if isinstance(obj, pa.Table):
        return obj.num_rows == 0
    else:
        return bool(not obj)


class ArrowDataframe(BaseDataframe):
    """ArrowDataframe.

    Converts any result into a Arrow DataFrame.
    """

    async def create_dataframe(
        self, result: Union[dict, bytes, Any], *args: P.args, **kwargs: P.kwargs
    ) -> Any:
        """
        Converts any result into a Arrow DataFrame.

        :param result: The result data to be converted into a Arrow DataFrame.
        :return: A DataFrame containing the result data.
        """
        if is_empty(result):
            raise DataNotFound("DataFrame: No Data was Found.")
        try:
            if isinstance(result, str):
                try:
                    result = orjson.loads(result)
                except Exception:
                    pass
            if isinstance(result, list):
                names = list(result[0].keys())
                df = pa.Table.from_arrays(result, names=names, **kwargs)
            elif isinstance(result, bytes) or isinstance(result, BytesIO):
                try:
                    # Reset the pointer to the start of the stream
                    result.seek(0)
                    df = pc.read_csv(result, **kwargs)
                except pa.lib.ArrowInvalid as e:
                    # Use pyarrow.parquet.read_table to read Parquet data
                    df = pq.read_table(result)
            else:
                df = pa.Table.from_pandas(pd.DataFrame(result, **kwargs))
            numrows = df.num_rows
            numcols = df.num_columns
            try:
                self._variables["_numRows_"] = numrows
                self.add_metric("NUM_ROWS", numrows)
                self.add_metric("NUM_COLS", numcols)
            except Exception:
                pass
            return df
        except Exception as err:
            raise ComponentError(f"Error Creating Dataframe: {err!s}")
