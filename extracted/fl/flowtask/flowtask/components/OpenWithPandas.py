from typing import Any
from pathlib import PurePath
from io import BytesIO
import aiofiles
from xml.sax import parse
import warnings
import pandas
from pandas._libs.parsers import STR_NA_VALUES
import orjson
import xlrd
import numpy as np
from ..utils import check_empty
from ..exceptions import ComponentError, DataNotFound, EmptyFile
from .OpenWithBase import OpenWithBase, detect_encoding, excel_based, ExcelHandler


# Suppress specific warning
warnings.filterwarnings("ignore", category=UserWarning)

class OpenWithPandas(OpenWithBase):
    """
    OpenWithPandas

    Overview

            This component opens various file types (CSV, Excel, HTML, JSON) into Pandas DataFrames.

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
        if self.mime == "text/xml":
            xmlparser = ExcelHandler()
            parse(filename, xmlparser)
            if hasattr(self, "skiprows"):
                row = self.skiprows
                columns = self.skiprows + 1
                start = columns + 1
            else:
                row = 0
                columns = 0
                start = columns + 1
            try:
                if (
                    hasattr(self, "add_columns") and hasattr(self, "rename")
                    and self.rename is True
                ):
                    cols = add_columns
                else:
                    cols = xmlparser.tables[0][columns]
                df = pandas.DataFrame(data=xmlparser.tables[0][start:], columns=cols)
                return df
            except pandas.errors.EmptyDataError as err:
                raise EmptyFile(f"Empty File {filename}: {err}") from err
            except pandas.errors.ParserError as err:
                raise ComponentError(f"Parsing File {filename}: {err}") from err
            except Exception as err:
                raise ComponentError(
                    f"Generic Error on file {filename}, error: {err}"
                ) from err
        else:
            if (
                self.mime == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            ):
                # xlsx or any openxml based document
                file_engine = self._params.get("file_engine", "openpyxl")
            elif self.mime == "application/vnd.ms-excel.sheet.binary.macroEnabled.12":
                file_engine = self._params.get("file_engine", "pyxlsb")
            else:
                try:
                    ext = filename.suffix
                except (AttributeError, ValueError) as e:
                    print(f"Error detecting extension: {e}")
                    ext = ".xls"
                if ext == ".xls":
                    file_engine = self._params.get("file_engine", "xlrd")
                else:
                    file_engine = self._params.get("file_engine", "calamine")
            try:
                arguments = {**self.args, **add_columns, **self.parse_dates}
                if self._limit is not None and isinstance(self._limit, int):
                    arguments["nrows"] = self._limit
                if self.sheet_name is not None:
                    arguments["sheet_name"] = self.sheet_name
                # TODO: if sheet_name is None, then open all worksheets
                # work with the dictionary of dataframes.
                df = pandas.read_excel(
                    filename,
                    na_values=self.na_values,
                    na_filter=self.filter_nan,
                    engine=file_engine,
                    keep_default_na=False,
                    **arguments,
                )
                return df
            except (IndexError, xlrd.biffh.XLRDError) as err:
                raise ComponentError(
                    f"Excel Index error on File {filename}: {err}"
                ) from err
            except pandas.errors.EmptyDataError as err:
                raise EmptyFile(f"Empty File {filename}: {err}") from err
            except pandas.errors.ParserError as err:
                raise ComponentError(f"Error Parsing File {filename}: {err}") from err
            except TypeError as err:
                err_msg = str(err)
                if "NoneType" in err_msg or "expected str" in err_msg:
                    raise ComponentError(
                        f"Error reading Excel file {filename}: the file may be "
                        f"corrupted, empty, or not a valid Excel format "
                        f"(engine={file_engine}). "
                        f"Verify the file is a genuine .xls/.xlsx file "
                        f"and not an HTML or CSV file saved with an Excel extension. "
                        f"Detail: {err}"
                    ) from err
                raise ComponentError(
                    f"Type error opening Excel file {filename}: {err}"
                ) from err
            except Exception as err:
                raise ComponentError(
                    f"Error opening Excel file {filename}: {err}"
                ) from err

    async def open_html(
        self, filename: str, add_columns: dict, encoding: str
    ) -> pandas.DataFrame:
        self._logger.debug(
            f"Opening an HTML file {filename} with Pandas, encoding={encoding}"
        )
        if "dtype" in self.args:
            del self.args["dtype"]
        if "skiprows" in self.args:
            del self.args["skiprows"]
        try:
            dfs = pandas.read_html(
                filename,
                keep_default_na=False,
                flavor="html5lib",
                na_values=self.na_values,
                encoding=encoding,
                **self.parse_dates,
                **self.args,
            )
            if dfs:
                df = dfs[0]
            else:
                df = None
            if "names" in add_columns:
                df.columns = add_columns["names"]
            return df
        except pandas.errors.EmptyDataError as err:
            raise EmptyFile(message=f"Empty File {filename}: {err}") from err
        except pandas.errors.ParserError as err:
            raise ComponentError(message=f"Parsing File {filename}: {err}") from err
        except Exception as err:
            raise ComponentError(
                message=f"Generic Error on file {filename}: {err}"
            ) from err

    async def open_parquet(
        self, filename: str, add_columns: dict, encoding
    ) -> pandas.DataFrame:
        pass

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
        # TODO: add columns functionality.
        try:
            df = pandas.read_json(
                filename, orient="records", encoding=encoding, **self.args
            )
            return df
        except pandas.errors.EmptyDataError as err:
            raise EmptyFile(message=f"Empty File {filename}: {err}") from err
        except pandas.errors.ParserError as err:
            raise ComponentError(
                message=f"Error Parsing File {filename}: {err}"
            ) from err
        except Exception as err:
            raise ComponentError(
                message=f"Generic Error on file {filename}: {err}"
            ) from err

    async def open_csv(
        self, filename: str, add_columns: dict, encoding
    ) -> pandas.DataFrame:
        self._logger.debug(
            f"Opening CSV file {filename} with Pandas, encoding={encoding}"
        )
        try:
            add_columns["low_memory"] = False
            add_columns["float_precision"] = "high"
        except KeyError:
            pass
        try:
            # can we use pyarrow.
            engine = self.args["engine"]
            del self.args["engine"]
        except KeyError:
            engine = "c"
        if self._limit is not None and isinstance(self._limit, int):
            add_columns["nrows"] = self._limit
        # try to fix the encoding problem on files:
        _, new_encoding = detect_encoding(filename, encoding)
        if new_encoding != encoding:
            self._logger.warning(
                f"Encoding on file: {new_encoding} and \
                declared by Task ({encoding}) are different"
            )
            # encoding = new_encoding
        # open file:
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
        else:
            try:
                return pandas.read_csv(
                    filename,
                    sep=self.separator,
                    quotechar='"',
                    decimal=",",
                    engine=engine,
                    keep_default_na=False,
                    na_values=self.na_values,
                    na_filter=self.filter_nan,
                    encoding=encoding,
                    skipinitialspace=True,
                    **add_columns,
                    **self.parse_dates,
                    **self.args,
                )
            except UnicodeDecodeError as exc:
                self._logger.warning(
                    f"Invalid Encoding {encoding}: {exc}"
                )
                # fallback to a default unicode:
                _, encoding = detect_encoding(filename, encoding)
                self._logger.debug(f"Detected Encoding > {encoding!s}")
                last_encoding = None
                fname = filename
                if hasattr(self, 'clean_null_bytes'):
                    async with aiofiles.open(filename, 'rb') as file:
                        # Removing all null bytes
                        content = await file.read()
                        content = content.replace(b'\x00', b'')
                    fname = BytesIO(content)
                for enc in ('utf-8', 'latin1', 'ascii'):
                    last_encoding = enc
                    try:
                        return pandas.read_csv(
                            fname,
                            sep=self.separator,
                            quotechar='"',
                            decimal=",",
                            engine=engine,
                            keep_default_na=False,
                            na_values=self.na_values,
                            na_filter=self.filter_nan,
                            encoding=enc,
                            skipinitialspace=True,
                            on_bad_lines='warn',
                            **add_columns,
                            **self.parse_dates,
                            **self.args,
                        )
                    except Exception as e:
                        print(e)
                        continue
                else:
                    # No encoding match
                    raise ComponentError(
                        f"Cannot Open the file with encoding {last_encoding}"
                    )
            except ValueError as exc:
                # Open Pandas with default settings for detect discrepancies
                df = pandas.read_csv(
                    filename,
                    sep=self.separator,
                    quotechar='"',
                    decimal=",",
                    engine=engine,
                    encoding=encoding,
                    dtype=str,
                    header=None,
                )
                # columns in Pandas:
                num_cols = int(df.shape[1])
                expected = len(add_columns.get('names', []))
                if expected > 0 and num_cols - expected > 0:
                    # some extra columns were found:
                    raise ComponentError(
                        (
                            f"There are more columns in FILE than expected. "
                            f"There are {num_cols} in File received vs "
                            f"{expected} columns in Mapping definition."
                        )
                    )
                try:
                    del self.args['dtype']
                except KeyError:
                    pass
                self._logger.error(
                    (
                        f"Some columns have wrong type in Model: {exc}, "
                        "Opening file with default settings (str)"
                    )
                )
                try:
                    return pandas.read_csv(
                        filename,
                        sep=self.separator,
                        quotechar='"',
                        decimal=",",
                        engine=engine,
                        keep_default_na=False,
                        na_values=self.na_values,
                        na_filter=self.filter_nan,
                        encoding=encoding,
                        **add_columns,
                        **self.parse_dates,
                        **self.args,
                    )
                except Exception as ex:
                    raise ComponentError(
                        f"Invalid types of columns found on file {filename}, {ex}"
                    )
            except pandas.errors.EmptyDataError as err:
                raise ComponentError(
                    f"Empty Data in file: {filename}, error: {err}"
                ) from err
            except pandas.errors.ParserError as err:
                raise ComponentError(
                    f"Error parsing File: {filename}, error: {err}"
                ) from err
            except Exception as err:
                raise ComponentError(
                    f"Generic Error on file: {filename}, error: {err}"
                ) from err

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
                    print("ERR ::", column, dtype, err, type(err))
                    self._logger.warning(
                        f"Cannot set data type for column {column}: {err}"
                    )
                    continue
        self._result = df
        numrows = len(df.index)
        self._variables["_numRows_"] = numrows
        self._variables[f"{self.StepName}_NUMROWS"] = numrows
        self.add_metric("NUMROWS", numrows)
        self.add_metric("OPENED_FILES", self._filenames)
        if self._debug is True:
            print(df)
            print("::: Printing Column Information === ")
            columns = list(df.columns)
            for column, t in df.dtypes.items():
                print(column, "->", t, "->", df[column].iloc[0])
            self._logger.debug(f"Opened File(s) with Pandas {self._filenames}")
        return self._result
