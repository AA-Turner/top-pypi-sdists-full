# btrdb.transformers
# Value transformation utilities
#
# Author:   PingThings
# Created:  Fri Dec 21 14:57:30 2018 -0500
#
# For license information, see LICENSE.txt
# ID: transformers.py [] allen@pingthings.io $

"""
Value transformation utilities
"""

##########################################################################
## Imports
##########################################################################

import contextlib
import csv
from collections import OrderedDict
from typing import TYPE_CHECKING

try:
    import pyarrow as pa
except ImportError:
    pa = None
try:
    import polars as pl
except ImportError:
    pl = None
try:
    import pandas as pd
except ImportError:
    pd = None
try:
    import numpy as np
except ImportError:
    np = None

if TYPE_CHECKING:
    import numpy as np
    import pandas as pd
    import polars as pl
    import pyarrow as pa

_IMPORT_ERR_MSG = (
    """Package(s) expected, but not found. Please pip install the following: {}"""
)

##########################################################################
## Helper Functions
##########################################################################

_STAT_PROPERTIES = ("min", "mean", "max", "count", "stddev")


def _get_time_from_row(row):
    for item in row:
        if item:
            return item.time
    raise Exception("Row contains no data")


def _stream_names(streamset, func):
    """
    private convenience function to come up with proper final stream names
    before sending a collection of streams (dataframe, etc.) back to the
    user.
    """
    return tuple(func(s) for s in streamset._streams)


##########################################################################
## Transform Functions
##########################################################################


def to_series(streamset, datetime64_index=True, agg="mean", name_callable=None):
    """
    Returns a list of Pandas Series objects indexed by time

    Parameters
    ----------
    datetime64_index: bool
        Directs function to convert Series index to np.datetime64[ns] or
        leave as np.int64.

    agg : str, default: "mean"
        Specify the StatPoint field (e.g. aggregating function) to create the Series
        from. Must be one of "min", "mean", "max", "count", or "stddev". This
        argument is ignored if RawPoint values are passed into the function.

    name_callable : lambda, default: lambda s: s.collection + "/" +  s.name
        Specify a callable that can be used to determine the series name given a
        Stream object.


    .. note::

        This method does **not** use the ``arrow`` -accelerated endpoints for faster and more efficient data retrieval.

    """
    if pd is None:
        raise ImportError(_IMPORT_ERR_MSG.format("pandas"))

    # TODO: allow this at some future point
    if agg == "all":
        raise AttributeError("cannot use 'all' as aggregate at this time")

    if not callable(name_callable):
        name_callable = lambda s: s.collection + "/" + s.name

    result = []
    stream_names = _stream_names(streamset, name_callable)

    for idx, output in enumerate(streamset.values()):
        times, values = [], []
        for point in output:
            times.append(point.time)
            if point.__class__.__name__ == "RawPoint":
                values.append(point.value)
            else:
                values.append(getattr(point, agg))

        if datetime64_index:
            times = pd.Index(times, dtype="datetime64[ns]", name="time")

        result.append(pd.Series(data=values, index=times, name=stream_names[idx]))
    return result


def arrow_to_series(streamset, agg=None, name_callable=None):
    """
    Returns a list of Pandas Series objects indexed by time

    Parameters
    ----------
    agg : List[str], default: ["mean"]
        Specify the StatPoint field or fields (e.g. aggregating function) to create the Series
        from. Must be one or more of "min", "mean", "max", "count", or "stddev". This
        argument is ignored if RawPoint values are passed into the function.

    name_callable : lambda, default: lambda s: s.collection + "/" +  s.name
        Specify a callable that can be used to determine the series name given a
        Stream object.


    Returns
    -------
    List[pandas.Series]


    .. note::

        This method is available for commercial customers with arrow-enabled servers.


    .. note::

        If you are not performing a ``window`` or ``aligned_window`` query, the ``agg`` parameter will be ignored.

    Examples
    --------
    Return a list of series of raw data per stream.

    >>> conn = btrdb.connect()
    >>> s1 = conn.stream_from_uuid('c9fd8735-5ec5-4141-9a51-d23e1b2dfa42')
    >>> s2 = conn.stream_from_uuid('9173fa70-87ab-4ac8-ac08-4fd63b910cae'
    >>> streamset = btrdb.stream.StreamSet([s1,s2])
    >>> streamset.filter(start=1500000000000000000, end=1500000000900000001).arrow_to_series(agg=None)
        [time
        2017-07-14 02:40:00+00:00            1.0
        2017-07-14 02:40:00.100000+00:00     2.0
        2017-07-14 02:40:00.200000+00:00     3.0
        2017-07-14 02:40:00.300000+00:00     4.0
        2017-07-14 02:40:00.400000+00:00     5.0
        2017-07-14 02:40:00.500000+00:00     6.0
        2017-07-14 02:40:00.600000+00:00     7.0
        2017-07-14 02:40:00.700000+00:00     8.0
        2017-07-14 02:40:00.800000+00:00     9.0
        2017-07-14 02:40:00.900000+00:00    10.0
        Name: new/stream/collection/foo, dtype: double[pyarrow],
        time
        2017-07-14 02:40:00+00:00            1.0
        2017-07-14 02:40:00.100000+00:00     2.0
        2017-07-14 02:40:00.200000+00:00     3.0
        2017-07-14 02:40:00.300000+00:00     4.0
        2017-07-14 02:40:00.400000+00:00     5.0
        2017-07-14 02:40:00.500000+00:00     6.0
        2017-07-14 02:40:00.600000+00:00     7.0
        2017-07-14 02:40:00.700000+00:00     8.0
        2017-07-14 02:40:00.800000+00:00     9.0
        2017-07-14 02:40:00.900000+00:00    10.0
        Name: new/stream/bar, dtype: double[pyarrow]]


        A window query of 0.5seconds long.

        >>> streamset.filter(start=1500000000000000000, end=1500000000900000001)
        ...          .windows(width=int(0.5 * 10**9))
        ...          .arrow_to_series(agg=["mean", "count"])
            [time
            2017-07-14 02:40:00+00:00           2.5
            2017-07-14 02:40:00.400000+00:00    6.5
            Name: new/stream/collection/foo/mean, dtype: double[pyarrow],
        ...
            time
            2017-07-14 02:40:00+00:00           4
            2017-07-14 02:40:00.400000+00:00    4
            Name: new/stream/collection/foo/count, dtype: uint64[pyarrow],
        ...
            time
            2017-07-14 02:40:00+00:00           2.5
            2017-07-14 02:40:00.400000+00:00    6.5
            Name: new/stream/bar/mean, dtype: double[pyarrow],
        ...
            time
            2017-07-14 02:40:00+00:00           4
            2017-07-14 02:40:00.400000+00:00    4
            Name: new/stream/bar/count, dtype: uint64[pyarrow]]


    """
    if not streamset._btrdb._ARROW_ENABLED:
        raise NotImplementedError(
            "arrow_to_series requires an arrow-enabled BTrDB server."
        )
    if pa is None or pd is None:
        raise ImportError(_IMPORT_ERR_MSG.format(",".join(["pyarrow", "pandas"])))
    if agg is None:
        agg = ["mean"]
    if not isinstance(agg, list):
        raise ValueError(
            f"Expected argument 'agg' to be a list of strings, was provided type - {type(agg)} with values - {agg}"
        )
    arrow_df = arrow_to_dataframe(
        streamset=streamset, agg=agg, name_callable=name_callable
    )
    return [arrow_df[col] for col in arrow_df]


def arrow_to_dataframe(streamset, agg=None, name_callable=None) -> pd.DataFrame:
    """
    Returns a Pandas DataFrame object indexed by time and using the values of a
    stream for each column.

    Parameters
    ----------
    agg : List[str], default: ["mean"]
        Specify the StatPoint fields (e.g. aggregating function) to create the dataframe
        from. Must be one or more of "min", "mean", "max", "count", "stddev", or "all". This
        argument is ignored if not using StatPoints.

    name_callable : lambda, default: lambda s: s.collection + "/" +  s.name
        Specify a callable that can be used to determine the series name given a
        Stream object.


    .. note::

        This method is available for commercial customers with arrow-enabled servers.


    Examples
    --------

    >>> conn = btrdb.connect()
    >>> s1 = conn.stream_from_uuid('c9fd8735-5ec5-4141-9a51-d23e1b2dfa42')
    >>> s2 = conn.stream_from_uuid('9173fa70-87ab-4ac8-ac08-4fd63b910cae'
    >>> streamset = btrdb.stream.StreamSet([s1,s2])
    >>> streamset.filter(start=1500000000000000000, end=1500000000900000001).arrow_to_dataframe()
                                            new/stream/collection/foo       new/stream/bar
        time
        2017-07-14 02:40:00+00:00                               1.0             1.0
        2017-07-14 02:40:00.100000+00:00                        2.0             2.0
        2017-07-14 02:40:00.200000+00:00                        3.0             3.0
        2017-07-14 02:40:00.300000+00:00                        4.0             4.0
        2017-07-14 02:40:00.400000+00:00                        5.0             5.0
        2017-07-14 02:40:00.500000+00:00                        6.0             6.0
        2017-07-14 02:40:00.600000+00:00                        7.0             7.0
        2017-07-14 02:40:00.700000+00:00                        8.0             8.0
        2017-07-14 02:40:00.800000+00:00                        9.0             9.0
        2017-07-14 02:40:00.900000+00:00                       10.0            10.0


    Use the stream uuids as their column names instead, using a lambda function.

    >>> streamset.filter(start=1500000000000000000, end=1500000000900000001)
    ...          .arrow_to_dataframe(
    ...             name_callable=lambda s: str(s.uuid)
    ...          )
                                      c9fd8735-5ec5-4141-9a51-d23e1b2dfa42  9173fa70-87ab-4ac8-ac08-4fd63b910cae
        time
        2017-07-14 02:40:00+00:00                                          1.0                                   1.0
        2017-07-14 02:40:00.100000+00:00                                   2.0                                   2.0
        2017-07-14 02:40:00.200000+00:00                                   3.0                                   3.0
        2017-07-14 02:40:00.300000+00:00                                   4.0                                   4.0
        2017-07-14 02:40:00.400000+00:00                                   5.0                                   5.0
        2017-07-14 02:40:00.500000+00:00                                   6.0                                   6.0
        2017-07-14 02:40:00.600000+00:00                                   7.0                                   7.0
        2017-07-14 02:40:00.700000+00:00                                   8.0                                   8.0
        2017-07-14 02:40:00.800000+00:00                                   9.0                                   9.0
        2017-07-14 02:40:00.900000+00:00                                  10.0                                  10.0


    A window query, with a window width of 0.4 seconds, and only showing the ``mean`` statpoint.

    >>> streamset.filter(start=1500000000000000000, end=1500000000900000001)
    ...          .windows(width=int(0.4*10**9))
    ...          .arrow_to_dataframe(agg=["mean"])
                                                new/stream/collection/foo/mean  new/stream/bar/mean
        time
        2017-07-14 02:40:00+00:00                                    2.5                  2.5
        2017-07-14 02:40:00.400000+00:00                             6.5                  6.5


    A window query, with a window width of 0.4 seconds, and only showing the ``mean`` and ``count``  statpoints.

    >>> streamset.filter(start=1500000000000000000, end=1500000000900000001)
    ...          .windows(width=int(0.4*10**9))
    ...          .arrow_to_dataframe(agg=["mean", "count"])
                                  new/stream/collection/foo/mean  new/stream/collection/foo/count  new/stream/bar/mean  new/stream/bar/count
        time
        2017-07-14 02:40:00+00:00               2.5                                4                  2.5                     4
        2017-07-14 02:40:00.400000+00:00        6.5                                4                  6.5                     4
    """

    def _rename(col_name, col_names_map):
        if col_name == "time":
            return col_name
        col_name_parts = col_name.split("/")
        if len(col_name_parts) == 1:
            uuid = col_name_parts[0]
            new_col_name = col_names_map[uuid]
        elif len(col_name_parts) == 2:
            uuid, _ = col_name_parts
            new_col_name = col_name.replace(uuid, col_names_map[uuid])
        return new_col_name

    if not streamset._btrdb._ARROW_ENABLED:
        raise NotImplementedError(
            "arrow_to_dataframe requires an arrow-enabled BTrDB server."
        )
    if pa is None or pd is None:
        raise ImportError(_IMPORT_ERR_MSG.format(",".join(["pyarrow", "pandas"])))

    if agg is None:
        agg = ["mean"]
    if not isinstance(agg, list):
        raise ValueError(
            f"Argument 'agg' not provided as a list of strings was provided type - {type(agg)} with values - {agg}"
        )
    # do not allow agg="all" with RawPoints
    if "all" in agg and streamset.allow_window:
        agg = ""
    elif any(["all" in val for val in agg]) and not streamset.allow_window:
        agg = ["min", "mean", "max", "count", "stddev"]
    else:
        agg = agg

    # default arg values
    if not callable(name_callable):
        name_callable = lambda s: s.collection + "/" + s.name
    # format is: uuid/stat_type
    tmp = streamset.arrow_values()
    # assume time col is the first column
    time_col = tmp.column_names[0]

    tmp_df = tmp.to_pandas(
        date_as_object=False,
        types_mapper=pd.ArrowDtype,
        split_blocks=True,
        self_destruct=True,
    ).set_index(time_col)
    tmp_df.index.name = time_col
    col_names = _stream_names(streamset, name_callable)
    col_names_map = {str(s.uuid): c for s, c in zip(streamset, col_names)}
    tmp_df.rename(
        columns=lambda col_name: _rename(col_name, col_names_map), inplace=True
    )
    if not streamset.allow_window:
        usable_cols = []
        for column_str in tmp_df.columns:
            for agg_name in agg:
                if agg_name in column_str:
                    usable_cols.append(column_str)
        tmp_df = tmp_df.loc[:, usable_cols]

    return tmp_df


def to_dataframe(streamset, agg="mean", name_callable=None):
    """
    Returns a Pandas DataFrame object indexed by time and using the values of a
    stream for each column.

    Parameters
    ----------
    agg : str, default: "mean"
        Specify the StatPoint field (e.g. aggregating function) to create the Series
        from. Must be one of "min", "mean", "max", "count", "stddev", or "all". This
        argument is ignored if not using StatPoints.

    name_callable : lambda, default: lambda s: s.collection + "/" +  s.name
        Specify a callable that can be used to determine the series name given a
        Stream object.  This is not compatible with agg == "all" at this time


    .. note::

        This method does **not** use the ``arrow`` -accelerated endpoints for faster and more efficient data retrieval.

    """
    if pd is None:
        raise ImportError(_IMPORT_ERR_MSG.format("pandas"))

    # TODO: allow this at some future point
    if agg == "all" and name_callable is not None:
        raise AttributeError(
            "cannot provide name_callable when using 'all' as aggregate at this time"
        )

    # do not allow agg="all" with RawPoints
    if agg == "all" and streamset.allow_window:
        agg = ""

    # default arg values
    if not callable(name_callable):
        name_callable = lambda s: s.collection + "/" + s.name

    df = pd.DataFrame(to_dict(streamset, agg=agg, name_callable=name_callable))

    if not df.empty:
        df = df.set_index("time")
        df.index.name = "time"

        if agg == "all" and not streamset.allow_window:
            stream_names = [
                [s.collection, s.name, prop]
                for s in streamset._streams
                for prop in _STAT_PROPERTIES
            ]
            df.columns = pd.MultiIndex.from_tuples(stream_names)
        else:
            df.columns = _stream_names(streamset, name_callable)

    return df


def arrow_to_polars(streamset, agg=None, name_callable=None):
    """
    Returns a Polars DataFrame object with time as a column and the values of a
    stream for each additional column from an arrow table.

    Parameters
    ----------
    agg : List[str], default: ["mean"]
        Specify the StatPoint field or fields (e.g. aggregating function) to create the dataframe
        from. Must be one or multiple of "min", "mean", "max", "count", "stddev", or "all". This
        argument is ignored if not using StatPoints.

    name_callable : lambda, default: lambda s: s.collection + "/" +  s.name
        Specify a callable that can be used to determine the series name given a
        Stream object.


    .. note::

        This method is available for commercial customers with arrow-enabled servers.

    """
    if not streamset._btrdb._ARROW_ENABLED:
        raise NotImplementedError(
            "arrow_to_polars requires an arrow-enabled BTrDB server."
        )
    if pa is None or pd is None or pl is None:
        raise ImportError(
            _IMPORT_ERR_MSG.format(",".join(["pyarrow", "pandas", "polars"]))
        )
    if agg is None:
        agg = ["mean"]
    if not isinstance(agg, list):
        raise ValueError(
            f"Expected argument 'agg' to be a list of strings, was provided type - {type(agg)} with values - {agg}"
        )
    arrow_df = arrow_to_dataframe(
        streamset=streamset, agg=agg, name_callable=name_callable
    )
    return pl.from_pandas(arrow_df, include_index=True, nan_to_null=False)


def arrow_to_arrow_table(streamset):
    """Return a pyarrow table of data.


    .. note::

        This method is available for commercial customers with arrow-enabled servers.

    """
    if not streamset._btrdb._ARROW_ENABLED:
        raise NotImplementedError(
            "arrow_to_arrow_table requires an arrow-enabled BTrDB server."
        )
    if pa is None:
        raise ImportError(_IMPORT_ERR_MSG.format("pyarrow"))
    return streamset.arrow_values()


def to_polars(streamset, agg="mean", name_callable=None):
    """
    Returns a Polars DataFrame object with time as a column and the values of a
    stream for each additional column.

    Parameters
    ----------
    agg : str, default: "mean"
        Specify the StatPoint field (e.g. aggregating function) to create the Series
        from. Must be one of "min", "mean", "max", "count", "stddev", or "all". This
        argument is ignored if not using StatPoints.

    name_callable : lambda, default: lambda s: s.collection + "/" +  s.name
        Specify a callable that can be used to determine the series name given a
        Stream object.  This is not compatible with agg == "all" at this time



    .. note::

        This method does **not** use the ``arrow`` -accelerated endpoints for faster and more efficient data retrieval.

    """
    if pl is None or pd is None:
        raise ImportError(_IMPORT_ERR_MSG.format(",".join(["polars", "pandas"])))

    # TODO: allow this at some future point
    if agg == "all" and name_callable is not None:
        raise AttributeError(
            "cannot provide name_callable when using 'all' as aggregate at this time"
        )

    # do not allow agg="all" with RawPoints
    if agg == "all" and not streamset.allow_window:
        agg = ""

    # default arg values
    if not callable(name_callable):
        name_callable = lambda s: s.collection + "/" + s.name

        df = streamset.to_dataframe(agg=agg, name_callable=name_callable)
    else:
        df = pd.DataFrame(to_dict(streamset, agg=agg, name_callable=name_callable))

    if not df.empty:
        if df.index.name == "time":
            pass
        else:
            df = df.set_index("time")

        df.index = pd.DatetimeIndex(df.index, tz="UTC", name="time")
        if agg == "all" and streamset.allow_window:
            stream_names = [
                [s.collection, s.name, prop]
                for s in streamset._streams
                for prop in _STAT_PROPERTIES
            ]
            df.columns = pd.MultiIndex.from_tuples(stream_names)
        else:
            df.columns = _stream_names(streamset, name_callable)

    return pl.from_pandas(df, nan_to_null=False, include_index=True)


def to_array(streamset, agg="mean"):
    """
    Returns a multidimensional numpy array (similar to a list of lists) containing point
    classes.

    Parameters
    ----------
    agg : str, default: "mean"
        Specify the StatPoint field (e.g. aggregating function) to return for the
        arrays. Must be one of "min", "mean", "max", "count", or "stddev". This
        argument is ignored if RawPoint values are passed into the function.


    .. note::

        This method does **not** use the ``arrow`` -accelerated endpoints for faster and more efficient data retrieval.

    """
    if np is None:
        raise ImportError(_IMPORT_ERR_MSG.format("numpy"))

    # TODO: allow this at some future point
    if agg == "all":
        raise AttributeError("cannot use 'all' as aggregate at this time")

    results = []
    for points in streamset.values():
        segment = []
        for point in points:
            if point.__class__.__name__ == "RawPoint":
                segment.append(point.value)
            else:
                segment.append(getattr(point, agg))
        results.append(np.array(segment))
    return np.array(results, dtype=object)


def arrow_to_numpy(streamset, agg=None):
    """Return a multidimensional array in the numpy format.

    Parameters
    ----------
    agg : List[str], default: ["mean"]
        Specify the StatPoint field or fields (e.g. aggregating function) to return for the
        arrays. Must be one or more of "min", "mean", "max", "count", or "stddev". This
        argument is ignored if RawPoint values are passed into the function.


    .. note::

        This method first converts to a pandas data frame then to a numpy array.


    .. note::

        This method is available for commercial customers with arrow-enabled servers.

    """
    if not streamset._btrdb._ARROW_ENABLED:
        raise NotImplementedError(
            "arrow_to_numpy requires an arrow-enabled BTrDB server."
        )
    if np is None or pa is None or pd is None:
        raise ImportError(
            _IMPORT_ERR_MSG.format(",".join(["numpy", "pyarrow", "pandas"]))
        )
    arrow_df = arrow_to_dataframe(streamset=streamset, agg=agg, name_callable=None)
    return arrow_df.values


def to_dict(streamset, agg="mean", name_callable=None):
    """
    Returns a list of OrderedDict for each time code with the appropriate
    stream data attached.

    Parameters
    ----------
    agg : str, default: "mean"
        Specify the StatPoint field (e.g. aggregating function) to constrain dict
        keys. Must be one of "min", "mean", "max", "count", or "stddev". This
        argument is ignored if RawPoint values are passed into the function.

    name_callable : lambda, default: lambda s: s.collection + "/" +  s.name
        Specify a callable that can be used to determine the series name given a
        Stream object.


    .. note::

        This method does **not** use the ``arrow`` -accelerated endpoints for faster and more efficient data retrieval.

    """
    if not callable(name_callable):
        name_callable = lambda s: s.collection + "/" + s.name

    data = []
    stream_names = _stream_names(streamset, name_callable)

    for row in streamset.rows():
        item = OrderedDict(
            {
                "time": _get_time_from_row(row),
            }
        )
        for idx, col in enumerate(stream_names):
            if row[idx].__class__.__name__ == "RawPoint":
                item[col] = row[idx].value if row[idx] else None
            else:
                if agg == "all":
                    for stat in _STAT_PROPERTIES:
                        item["{}-{}".format(col, stat)] = (
                            getattr(row[idx], stat) if row[idx] else None
                        )
                else:
                    item[col] = getattr(row[idx], agg) if row[idx] else None
        data.append(item)
    return data


def arrow_to_dict(streamset, agg=None, name_callable=None):
    """
    Returns a list of dicts for each time code with the appropriate
    stream data attached.

    Parameters
    ----------
    agg : List[str], default: ["mean"]
        Specify the StatPoint field or fields (e.g. aggregating function) to constrain dict
        keys. Must be one or more of "min", "mean", "max", "count", or "stddev". This
        argument is ignored if RawPoint values are passed into the function.

    name_callable : lambda, default: lambda s: s.collection + "/" +  s.name
        Specify a callable that can be used to determine the series name given a
        Stream object.


    .. note::

        This method is available for commercial customers with arrow-enabled servers.

    """
    if not streamset._btrdb._ARROW_ENABLED:
        raise NotImplementedError(
            "arrow_to_dict requires an arrow-enabled BTrDB server."
        )
    if pa is None or pd is None:
        raise ImportError(_IMPORT_ERR_MSG.format(",".join(["pyarrow", "pandas"])))
    if agg is None:
        agg = ["mean"]
    if not isinstance(agg, list):
        raise ValueError(
            f"Expected a list of strings for 'agg', was provided type - {type(agg)} with values {agg}."
        )
    arrow_df = arrow_to_dataframe(
        streamset=streamset, agg=agg, name_callable=name_callable
    )
    return arrow_df.to_dict(orient="index")


def to_csv(
    streamset, fobj, dialect=None, fieldnames=None, agg="mean", name_callable=None
):
    """
    Saves stream data as a CSV file.

    Parameters
    ----------
    fobj: str or file-like object
        Path to use for saving CSV file or a file-like object to use to write to.

    dialect: csv.Dialect
        CSV dialect object from Python csv module.  See Python's csv module for
        more information.

    fieldnames: sequence
        A sequence of strings to use as fieldnames in the CSV header.  See
        Python's csv module for more information.

    agg : str, default: "mean"
        Specify the StatPoint field (e.g. aggregating function) to return when
        limiting results. Must be one of "min", "mean", "max", "count", or "stddev".
        This argument is ignored if RawPoint values are passed into the function.

    name_callable : lambda, default: lambda s: s.collection + "/" +  s.name
        Specify a callable that can be used to determine the series name given a
        Stream object.


    .. note::

        This method does **not** use the ``arrow`` -accelerated endpoints for faster and more efficient data retrieval.

    """

    # TODO: allow this at some future point
    if agg == "all":
        raise AttributeError("cannot use 'all' as aggregate at this time")

    if not callable(name_callable):
        name_callable = lambda s: s.collection + "/" + s.name

    @contextlib.contextmanager
    def open_path_or_file(path_or_file):
        if isinstance(path_or_file, str):
            f = file_to_close = open(path_or_file, "w", newline="")
        else:
            f = path_or_file
            file_to_close = None
        try:
            yield f
        finally:
            if file_to_close:
                file_to_close.close()

    with open_path_or_file(fobj) as csvfile:
        stream_names = _stream_names(streamset, name_callable)
        fieldnames = fieldnames if fieldnames else ["time"] + list(stream_names)

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, dialect=dialect)
        writer.writeheader()

        for item in to_dict(streamset, agg=agg):
            writer.writerow(item)


def to_table(streamset, agg="mean", name_callable=None):
    """
    Returns string representation of the data in tabular form using the tabulate
    library.

    Parameters
    ----------
    agg : str, default: "mean"
        Specify the StatPoint field (e.g. aggregating function) to create the Series
        from. Must be one of "min", "mean", "max", "count", or "stddev". This
        argument is ignored if RawPoint values are passed into the function.

    name_callable : lambda, default: lambda s: s.collection + "/" +  s.name
        Specify a callable that can be used to determine the column name given a
        Stream object.


    .. note::

        This method does **not** use the ``arrow`` -accelerated endpoints for faster and more efficient data retrieval.

    """
    try:
        from tabulate import tabulate
    except ImportError:
        raise ImportError(
            "Please install tabulate to use this transformation function."
        )

    # TODO: allow this at some future point
    if agg == "all":
        raise AttributeError("cannot use 'all' as aggregate at this time")

    if not callable(name_callable):
        name_callable = lambda s: s.collection + "/" + s.name

    return tabulate(
        streamset.to_dict(agg=agg, name_callable=name_callable), headers="keys"
    )


##########################################################################
## Transform Classes
##########################################################################


class StreamSetTransformer(object):
    """
    Base class for StreamSet or Stream transformations
    """

    to_dict = to_dict
    arrow_to_dict = arrow_to_dict

    to_array = to_array
    arrow_to_numpy = arrow_to_numpy

    to_series = to_series
    arrow_to_series = arrow_to_series

    to_dataframe = to_dataframe
    arrow_to_dataframe = arrow_to_dataframe

    to_polars = to_polars
    arrow_to_polars = arrow_to_polars

    arrow_to_arrow_table = arrow_to_arrow_table

    to_csv = to_csv
    to_table = to_table
