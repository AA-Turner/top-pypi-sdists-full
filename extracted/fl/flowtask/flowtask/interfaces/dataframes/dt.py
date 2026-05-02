from typing import Union, Any, ParamSpec
from io import BytesIO
import orjson
import pyarrow as pa
import datatable as dt
import pandas as pd
from .abstract import BaseDataframe
from ...exceptions import ComponentError, DataNotFound


P = ParamSpec("P")


def is_empty(obj):
    """check_empty.
    Check if a basic object, a Polars DataFrame, an Apache Arrow Table,
    or a Python DataTable Frame is empty or not.
    """
    if isinstance(obj, (pa.Table, dt.Frame)):
        return obj.nrows == 0
    else:
        return bool(not obj)


class DtDataframe(BaseDataframe):
    """DtDataframe.

    Converts any result into a Datatable DataFrame.
    """

    async def create_dataframe(
        self, result: Union[dict, bytes, Any], *args: P.args, **kwargs: P.kwargs
    ) -> Any:
        """
        Converts any result into a Datatable DataFrame.

        :param result: The result data to be converted into a Datatable DataFrame.
        :return: A DataFrame containing the result data.
        """
        if is_empty(result):
            raise DataNotFound("Frame: No Data was Found.")
        try:
            if isinstance(result, str):
                try:
                    result = orjson.loads(result)
                except Exception:
                    pass
            if isinstance(result, (list, dict)):
                df = dt.Frame(result, **kwargs)
            elif isinstance(result, bytes) or isinstance(result, BytesIO):
                # Reset the pointer to the start of the stream
                result.seek(0)
                # Assuming bytes is a CSV format, adjust as needed
                df = dt.Frame(pd.read_csv(result))
            else:
                raise ValueError("Unsupported data type for DataTable Frame creation")

            columns = list(df.names)
            numrows = df.nrows
            numcols = df.ncols
            try:
                self._variables["_numRows_"] = numrows
                self.add_metric("NUM_ROWS", numrows)
                self.add_metric("NUM_COLS", numcols)
            except Exception:
                pass
            return df
        except Exception as err:
            raise ComponentError(f"Error Creating Frame: {err!s}")
