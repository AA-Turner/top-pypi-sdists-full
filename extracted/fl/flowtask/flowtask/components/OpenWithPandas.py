from typing import Any
from pathlib import PurePath
from io import BytesIO
import aiofiles
import warnings
import pandas
from pandas._libs.parsers import STR_NA_VALUES
import orjson
import numpy as np
from ..utils import check_empty
from ..exceptions import ComponentError, DataNotFound, EmptyFile
from .OpenWithBase import OpenWithBase, excel_based


# Suppress specific warning
warnings.filterwarnings("ignore", category=UserWarning)

class OpenWithPandas(OpenWithBase):
    """
    OpenWithPandas

    Overview

            This component opens various file types (CSV, Excel, HTML, JSON) into Pandas DataFrames.

    :consumes: file
    :produces: dataframe

       :widths: auto


    |  model      |   Yes    | A model (json) representative of the data that I am going to      |
    |             |          | open * name of a DataModel (in-development)                       |
    |  map        |   Yes    | Map the columns against the model                                 |
    | tablename   |   Yes    | Join the data from the table in the postgres database             |
    | use_map     |   Yes    | If true, then a MAP file is used instead of a table in postgresql |
    | file_engine |   Yes    | Pandas different types of engines for different types of Excel    |
    |             |          | * xlrd (legacy, xls type)                                         |
    |             |          | * openpyxl (new xlsx files)                                       |
    |             |          | * pyxlsb (to open with macros and functions)                      |
    |  dtypes     |   No     | force the data type of a column ex: { order_date: datetime }      |


    Return the list of arbitrary days


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          OpenWithPandas:
          mime: text/csv
          process: true
          separator: '|'
          drop_empty: true
          trim: true
          pk:
          columns:
          - associate_oid
          - associate_id
          append: false
          verify_integrity: true
          map:
          tablename: employees
          schema: bacardi
          map: employees
          replace: false
        ```
    """
    _version = "1.0.0"
    """
    OpenWithPandas

    Overview

        This component opens various file types (CSV, Excel, HTML, JSON) into Pandas DataFrames.

    :consumes: file
    :produces: dataframe

    .. table:: Properties
    :widths: auto


    +------------------------+----------+-----------+---------------------------------------------------------------+
    | Name                   | Required | Summary                                                                   |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | directory              |   No     | The directory where the files are located.                                |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | filename               |   No     | The name of the file to open.                                             |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | file                   |   No     | Pattern or file to open.                                                  |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | mime                   |   No     | The MIME type of the file. Default is "text/csv".                         |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | separator              |   No     | Separator for CSV files. Default is ",".                                  |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | force_map              |   No     | Force the use of a map file. Default is False.                            |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | parse_dates            |   No     | Columns to parse as dates. Default is an empty dictionary.                |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | filter_nan             |   No     | Filter out NaN values. Default is True.                                   |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | na_values              |   No     | List of values to recognize as NaN. Default is ["NULL", "TBD"].           |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | remove_empty_strings   |   No     | Remove empty strings. Default is True.                                    |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | no_multi               |   No     | Disable multi-file processing. Default is False.                          |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | clean_nat              |   No     | Clean NaT values. Default is False.                                       |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | flavor                 |   No     | The flavor of the database for column information. Default is "postgres". |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | pd_args                |   No     | Additional arguments for pandas. Default is an empty dictionary.          |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    |  model                 |   Yes    | A model (json) representative of the data that I am going to              |
    |                        |          | open * name of a DataModel (in-development)                               |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    |  map                   |   Yes    | Map the columns against the model                                         |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | tablename              |   Yes    | Join the data from the table in the postgres database                     |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | use_map                |   Yes    | If true, then a MAP file is used instead of a table in postgresql         |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    | file_engine            |   Yes    | Pandas different types of engines for different types of Excel            |
    |                        |          | * xlrd (legacy, xls type)                                                 |
    |                        |          | * openpyxl (new xlsx files)                                               |
    |                        |          | * pyxlsb (to open with macros and functions)                              |
    +------------------------+----------+-----------+---------------------------------------------------------------+
    |  dtypes                |   No     | force the data type of a column ex: { order_date: datetime }              |
    +------------------------+----------+-----------+---------------------------------------------------------------+



    Returns
        This component returns a Pandas DataFrame containing the data from the opened file(s).


        Example:

        ```yaml
        OpenWithPandas:
          mime: text/csv
          process: true
          separator: '|'
          drop_empty: true
          trim: true
          pk:
            columns:
            - associate_oid
            - associate_id
            append: false
            verify_integrity: true
          map:
            tablename: employees
            schema: bacardi
            map: employees
            replace: false
        ```

    """
    def get_column_headers(self):
        headers = []
        for filename in self._filenames:
            try:
                encoding = self.check_encoding(filename)
            except Exception:
                encoding = "UTF-8"
            df = pandas.read_csv(
                filename,
                sep=self.separator,
                skipinitialspace=True,
                encoding=encoding,
                engine="python",
                nrows=1,
            )
            headers.append(df.columns.values.tolist())
        return headers

    def set_datatypes(self):
        dtypes = {}
        for field, dtype in self.datatypes.items():
            if dtype == "uint8":
                dtypes[field] = np.uint8
            elif dtype == "uint16":
                dtypes[field] = np.uint16
            elif dtype == "uint32":
                dtypes[field] = np.uint32
            elif dtype == "int8":
                dtypes[field] = np.int8
            elif dtype == "int16":
                dtypes[field] = np.int16
            elif dtype == "int32":
                dtypes[field] = np.int32
            elif dtype == "float":
                dtypes[field] = float
            elif dtype == "float32":
                dtypes[field] = float
            elif dtype in ("string", "varchar", "str"):
                dtypes[field] = "str"
            elif dtype == "object":
                dtypes[field] = object
            else:
                # invalid datatype
                raise ComponentError(
                    f"Invalid DataType value: {field} for field {dtype}"
                )
        if dtypes:
            self.args["dtype"] = dtypes

    async def open_excel(
        self, filename: str, add_columns: dict, encoding
    ) -> pandas.DataFrame:
        if filename is None:
            raise ComponentError(
                "Cannot open Excel file: file path is None. "
                "Verify the file was downloaded or the path is correctly configured."
            )
        self._logger.debug(
            f"Opening Excel file {filename} with Pandas, encoding: {encoding}"
        )
        from .pandas_io import read_to_dataframe
        # Determine file_engine exactly as before (mime-based, then extension fallback)
        if self.mime == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            file_engine = self._params.get("file_engine", "openpyxl")
        elif self.mime == "application/vnd.ms-excel.sheet.binary.macroEnabled.12":
            file_engine = self._params.get("file_engine", "pyxlsb")
        elif self.mime == "text/xml":
            file_engine = None  # xml branch handled inside read_to_dataframe
        else:
            try:
                ext = filename.suffix
            except (AttributeError, ValueError) as e:
                self._logger.warning(
                    "Error detecting extension for file %s: %s", filename, e
                )
                ext = ".xls"
            if ext == ".xls":
                file_engine = self._params.get("file_engine", "xlrd")
            else:
                file_engine = self._params.get("file_engine", "calamine")
        rename = getattr(self, "rename", False)
        # Forward pd_args to pandas.  Several of these (sheet_name, skiprows,
        # parse_dates, na_values, ...) are *explicit* kwargs of
        # read_to_dataframe, so spreading self.args naively raises
        # "multiple values for keyword argument".  Build the call kwargs from
        # component-level defaults and let pd_args entries that name an explicit
        # parameter OVERRIDE them; everything else (header, usecols, names, ...)
        # flows through to pandas.read_excel unchanged.  Each key thus has a
        # single source in the final call — collisions are impossible.
        extra = {k: v for k, v in self.args.items() if k != "dtype"}
        # pandas uses ``engine``; our helper exposes it as ``file_engine``.
        if "engine" in extra:
            file_engine = extra.pop("engine")
        call_kwargs = {
            "file_engine": file_engine,
            "sheet_name": self.sheet_name,
            "dtypes": self.args.get("dtype"),
            "parse_dates": self.parse_dates,
            "na_values": self.na_values,
            "filter_nan": self.filter_nan,
            "add_columns": add_columns,
            "limit": self._limit,
            "skiprows": getattr(self, "skiprows", 0),
            "rename": (hasattr(self, "add_columns") and rename is True),
            # OpenWithPandas already governs empty-string handling through its
            # na_values set (built from remove_empty_strings in run()), matching
            # the pre-refactor behaviour where empty cells are PRESERVED as "".
            # Disable pandas_io's extra ``df.replace("", NA)`` so it does not
            # contradict that and turn all-empty columns into all-NA (which
            # drop_empty would then drop).
            "remove_empty_strings": False,
        }
        pandas_extra = {}
        for key, value in extra.items():
            if key in call_kwargs:
                call_kwargs[key] = value
            else:
                pandas_extra[key] = value
        # Surface which sheet/engine were actually used — helps diagnose
        # "empty result" cases caused by reading the wrong sheet.
        effective_sheet = call_kwargs["sheet_name"]
        sheet_label = effective_sheet if effective_sheet is not None else "<default: first sheet>"
        self._logger.notice(
            f"OpenWithPandas: reading Excel sheet_name={sheet_label!r} "
            f"engine={call_kwargs['file_engine']!r} from {filename}"
        )
        self.add_metric("SHEET_NAME", effective_sheet)
        self.add_metric("EXCEL_ENGINE", call_kwargs["file_engine"])
        return read_to_dataframe(
            filename,
            mime=self.mime,
            **call_kwargs,
            **pandas_extra,
        )

    async def open_html(
        self, filename: str, add_columns: dict, encoding: str
    ) -> pandas.DataFrame:
        self._logger.debug(
            f"Opening an HTML file {filename} with Pandas, encoding={encoding}"
        )
        from .pandas_io import read_to_dataframe
        # Strip kwargs that read_html does not accept (mirrors original behaviour)
        args = {k: v for k, v in self.args.items() if k not in ("dtype", "skiprows")}
        return read_to_dataframe(
            filename,
            mime="text/html",
            encoding=encoding,
            na_values=self.na_values,
            parse_dates=self.parse_dates,
            add_columns=add_columns,
            dtypes=self.args.get("dtype"),
            remove_empty_strings=False,  # na_values governs empty-string handling
            **args,
        )

    async def open_parquet(
        self, filename: str, add_columns: dict, encoding
    ) -> pandas.DataFrame:
        """Read a Parquet file into a DataFrame via pandas_io.

        Args:
            filename: Path to the Parquet file.
            add_columns: Unused; accepted for API parity with other open_* methods.
            encoding: Unused; Parquet is binary.

        Returns:
            A ``pandas.DataFrame``.
        """
        from .pandas_io import _read_parquet
        return _read_parquet(filename, **self.args)

    async def open_sql(
        self, filename: str, add_columns: dict, encoding
    ) -> pandas.DataFrame:
        pass

    async def open_json(
        self, filename: str, add_columns: dict, encoding: str
    ) -> pandas.DataFrame:
        self._logger.debug(
            f"Opening a JSON file {filename} with Pandas, encoding={encoding}"
        )
        from .pandas_io import read_to_dataframe
        # TODO: add columns functionality.
        # Filter encoding to avoid collision with the explicit param above.
        extra = {k: v for k, v in self.args.items() if k != "encoding"}
        return read_to_dataframe(
            filename,
            mime="application/json",
            encoding=encoding,
            remove_empty_strings=False,  # na_values governs empty-string handling
            **extra,
        )

    async def open_csv(
        self, filename: str, add_columns: dict, encoding
    ) -> pandas.DataFrame:
        self._logger.debug(
            f"Opening CSV file {filename} with Pandas, encoding={encoding}"
        )
        from .pandas_io import read_to_dataframe
        try:
            add_columns["low_memory"] = False
            add_columns["float_precision"] = "high"
        except KeyError:
            pass
        try:
            engine = self.args["engine"]
            del self.args["engine"]
        except KeyError:
            engine = "c"
        # bigfile path: chunked reading (not delegated to pandas_io since it
        # uses async aiofiles and a chunked iterator — kept inline).
        if hasattr(self, "bigfile"):
            try:
                tp = pandas.read_csv(
                    filename,
                    sep=self.separator,
                    decimal=",",
                    engine=engine,
                    keep_default_na=False,
                    na_values=self.na_values,
                    na_filter=self.filter_nan,
                    encoding=encoding,
                    skipinitialspace=True,
                    iterator=True,
                    chunksize=int(self.chunksize),
                    **add_columns,
                    **self.parse_dates,
                    **self.args,
                )
                return pandas.concat(tp, ignore_index=True)
            except pandas.errors.EmptyDataError as err:
                raise ComponentError(
                    f"Empty Data File on: {filename}, error: {err}"
                ) from err
            except Exception as err:
                raise ComponentError(
                    f"Generic Error on file: {filename}, error: {err}"
                ) from err

        # Standard (non-chunked) path — delegate to pandas_io helper.
        # clean_null_bytes handling stays here because it requires async aiofiles.
        buf = filename
        if hasattr(self, "clean_null_bytes"):
            async with aiofiles.open(filename, "rb") as file:
                content = await file.read()
                content = content.replace(b"\x00", b"")
            buf = BytesIO(content)

        return read_to_dataframe(
            buf,
            mime="text/csv",
            separator=self.separator,
            encoding=encoding,
            dtypes=self.args.get("dtype"),
            parse_dates=self.parse_dates,
            na_values=self.na_values,
            filter_nan=self.filter_nan,
            add_columns=add_columns,
            limit=self._limit,
            engine=engine,
            remove_empty_strings=False,  # na_values governs empty-string handling
            **{k: v for k, v in self.args.items() if k != "dtype"},
        )

    async def run(self) -> Any:
        await super(OpenWithPandas, self).run()
        add_columns = await self.colinfo()
        result = []
        df = None
        ## Define NA Values:
        default_missing = STR_NA_VALUES.copy()
        if self.remove_empty_strings is True:
            try:
                default_missing.remove("")
            except KeyError:
                pass
        for val in self.na_values:  # pylint: disable=E0203
            default_missing.add(val)
            default_missing.add(val)
        self.na_values = default_missing
        if self._filenames is None and not check_empty(self._data):
            if isinstance(self._data, list):
                for file in self._data:
                    try:
                        df = pandas.DataFrame(
                            data=file, **add_columns, **self.parse_dates, **self.args
                        )
                        result.append(df)
                    except pandas.errors.EmptyDataError as err:
                        raise ComponentError(
                            f"Error on Empty Data: error: {err}"
                        ) from err
                    except ValueError as err:
                        raise ComponentError(
                            f"Error parsing Data: error: {err}"
                        ) from err
                    except Exception as err:
                        raise ComponentError(
                            f"Generic Error on Data: error: {err}"
                        ) from err
            if df is None or df.empty:
                raise DataNotFound("Dataframe is Empty: Data not found")
        else:
            # itereate over all files or data
            self._variables["FILENAMES"] = self._filenames
            for filename in self._filenames:
                try:
                    encoding = self.check_encoding(filename)
                except Exception:
                    encoding = "UTF-8"
                if self.mime == "text/csv" or self.mime == "text/plain":
                    try:
                        df = await self.open_csv(filename, add_columns, encoding)
                        if isinstance(filename, PurePath):
                            self.add_metric(f"{filename.name}", len(df.index))
                        else:
                            self.add_metric(f"{filename}", len(df.index))
                    except Exception as err:
                        raise ComponentError(f"Encoding Error: {err}") from err
                    if hasattr(self, "add_columns") and hasattr(self, "rename"):
                        if self.rename is True:
                            df = df.drop(df.index[0])
                elif self.mime in excel_based:
                    try:
                        df = await self.open_excel(filename, add_columns, encoding)
                    except Exception as err:
                        raise ComponentError(
                            f"Error parsing Excel: {err}"
                        ) from err
                elif self.mime == "text/html" or self.mime == "application/html":
                    try:
                        df = await self.open_html(filename, add_columns, encoding)
                    except Exception as err:
                        raise ComponentError(f"Error parsing XML: {err}") from err
                elif self.mime == "application/json":
                    try:
                        df = await self.open_json(filename, add_columns, encoding)
                    except Exception as err:
                        raise ComponentError(f"Error parsing JSON: {err}") from err
                elif self.mime in ("application/parquet", "application/x-parquet"):
                    try:
                        df = await self.open_parquet(filename, add_columns, encoding)
                    except Exception as err:
                        raise ComponentError(f"Error parsing Parquet: {err}") from err
                else:
                    raise ComponentError(f"Try to Open invalid MIME Type: {self.mime}")
                if df is None or df.empty:
                    raise EmptyFile(f"Empty File {filename}")
                result.append(df)
        # at the end, concat the sources:
        if len(result) == 1:
            df = result[0]
        else:
            ## fix Pandas Concat
            if self.no_multi is True:  # get only one element
                df = result.pop()
            else:
                try:
                    df = pandas.concat(
                        result  # , ignore_index=True  # , sort=False, axis=0,
                    )  # .reindex(result[0].index)
                except Exception as err:
                    raise ComponentError(
                        f"Error Combining Resultset Dataframes: {err}"
                    ) from err
        # When --debug is on, print the RAW DataFrame exactly as read, BEFORE
        # any post-processing (drop_empty/trim/dropna). This is the place to
        # validate which columns came in and which are all-empty (and would be
        # dropped below by drop_empty).
        if self._debug is True:
            try:
                nonnull = df.notna().sum()
                empty_cols = [c for c in df.columns if nonnull[c] == 0]
                self._logger.debug(
                    "OpenWithPandas RAW READ (pre drop_empty): shape=%s, columns=%s",
                    df.shape, list(df.columns)
                )
                self._logger.debug(
                    "OpenWithPandas RAW non-null counts per column:\n%s",
                    nonnull.to_string()
                )
                if empty_cols:
                    self._logger.warning(
                        "OpenWithPandas: %d all-empty column(s) present in the "
                        "raw read%s: %s",
                        len(empty_cols),
                        " — these WILL BE DROPPED by drop_empty" if hasattr(self, "drop_empty") else "",
                        empty_cols,
                    )
            except Exception as err:  # pylint: disable=W0718
                self._logger.warning(
                    "OpenWithPandas raw debug print failed: %s", err
                )
        # post-processing:
        if hasattr(self, "remove_scientific_notation"):
            pandas.set_option("display.float_format", lambda x: "%.3f" % x)
        if hasattr(self, "drop_empty"):
            df.dropna(axis=1, how="all", inplace=True)
            df.dropna(axis=0, how="all", inplace=True)
            df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
        if hasattr(self, "dropna"):
            df.dropna(subset=self.dropna, how="all", inplace=True)
        if hasattr(self, "trim"):
            # cols = list(df.columns)
            cols = df.select_dtypes(include=["object", "string"])
            # def utrim(x): return x.strip() if isinstance(x, str) else x
            # u.applymap(utrim)
            for col in cols:
                df[col] = df[col].astype(str).str.strip()
        # define the primary keys for DataFrame
        if hasattr(self, "pk"):
            try:
                columns = self.pk["columns"]
                del self.pk["columns"]
                df.reset_index().set_index(columns, inplace=True, drop=False, **self.pk)
            except Exception as err:
                self._logger.error(f"OpenWith: Error setting index: {err}")
        if self.clean_nat is True:
            df.replace({pandas.NaT: None}, inplace=True)
        if self._colinfo:
            # fix the datatype for every column in dataframe (if needed)
            for column, dtype in self._colinfo.items():
                # print(column, '->', dtype, '->', df[column].iloc[0])
                try:
                    if (
                        dtype == "timestamp without time zone"
                        or dtype == "timestamp with time zone"
                        or dtype == "date"
                    ):
                        if df[column].dtype != "datetime64[ns]":
                            df[column] = pandas.to_datetime(df[column], errors="coerce")
                            df[column] = df[column].astype("datetime64[ns]")
                    elif (
                        dtype == "character varying"
                        or dtype == "character"
                        or dtype == "text"
                        or dtype == "varchar"
                    ):
                        # print(column, '->', dtype, '->', df[column].iloc[0])
                        df[column] = df[column].replace([np.nan], "", regex=True)
                        # df[column] = df[column].astype(str)
                        # df[column].fillna("", inplace=True)
                        df[column] = df[column].fillna("")
                        # df[column].astype(str, inplace=True, errors='coerce')
                        df[column] = df[column].astype("string", errors="raise")
                        # df[column].fillna(None, inplace=True)
                    elif dtype == "smallint":
                        df[column] = pandas.to_numeric(df[column], errors="coerce")
                        df[column] = df[column].fillna("").astype("Int8")
                    elif dtype == "integer" or dtype == "bigint":
                        try:
                            ctype = df[column].dtypes[0].name
                        except (TypeError, KeyError):
                            ctype = df[column].dtype
                        if ctype not in ("Int8", "Int32", "Int64"):
                            df[column] = pandas.to_numeric(df[column], errors="raise")
                            df[column] = df[column].astype("Int64", errors="raise")
                        else:
                            df[column] = df[column].astype("Int64", errors="raise")
                    elif dtype == "numeric" or dtype == "float":
                        df[column] = pandas.to_numeric(df[column], errors="coerce")
                        df[column] = df[column].astype("float64")
                    elif dtype == "double precision" or dtype == "real":
                        df[column] = pandas.to_numeric(df[column], errors="coerce")
                        df[column] = df[column].astype("float64")
                    elif dtype == "jsonb":
                        df[column] = df[column].apply(orjson.loads)
                    elif dtype == "object":
                        df[column] = df[column].replace([np.nan], "", regex=True)
                except Exception as err:
                    self._logger.warning(
                        "Cannot coerce column %s to dtype %s: %s (%s)",
                        column, dtype, err, type(err).__name__,
                    )
                    continue
        self._result = df
        numrows = len(df.index)
        self._variables["_numRows_"] = numrows
        self._variables[f"{self.StepName}_NUMROWS"] = numrows
        self.add_metric("NUMROWS", numrows)
        self.add_metric("OPENED_FILES", self._filenames)
        if getattr(self, 'is_debug', False) is True:
            self._logger.debug("DataFrame result:\n%s", df.to_string())
            self._logger.debug("::: Column Information ===")
            for column, t in df.dtypes.items():
                self._logger.debug(
                    "%s -> %s -> %s", column, t, df[column].iloc[0]
                )
            self._logger.debug("Opened File(s) with Pandas %s", self._filenames)
        return self._result
