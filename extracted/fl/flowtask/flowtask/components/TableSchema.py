import asyncio
from typing import Dict, Any
from collections.abc import Callable
from pathlib import PosixPath, Path
import re
from decimal import Decimal
import datetime
import numpy as np
import pandas as pd
import dask.dataframe as dd
from asyncdb.models import Model
from dateutil.parser import parse as _dateutil_parse
from navconfig.logging import logging
from ..exceptions import FileError, ComponentError, DataNotFound
from ..interfaces.flow import FlowComponent
from ..interfaces.qs import QSSupport
from ..utils.transformations import (
    is_camelcase,
    is_snakecase,
    remove_illegal_chars,
    camelcase_split
)
from ..utils.constants import excel_based


logging.getLogger("fsspec").setLevel(logging.CRITICAL)


dtypes = {
    "varchar": str,
    "character varying": str,
    "string": str,
    "object": str,
    "int": int,
    "int4": int,
    "integer": int,
    "bigint": np.int64,
    "int64": np.int64,
    "uint64": np.int64,
    "Int8": int,
    "float64": Decimal,
    "float": Decimal,
    "bool": bool,
    "datetime64[ns]": datetime.datetime,
    "date": datetime.date,
}


# adding support for primary keys on raw tables
pk_sentence = """ALTER TABLE {schema}.{table}
ADD CONSTRAINT {schema}_{table}_pkey PRIMARY KEY({fields});

        Example:

        ```yaml
        TableSchema:
          normalize_names: true
          tablename: photos_raw
          schema: banco_chile
          pk:
          - photo_id
          replace_names:
            url: url_thumbnail
            full_size_url: photo_path
            categories: categories_names
            form_visit_id: form_id
            inserted: inserted_at
        ```

    """


def datetime_to_name(value: datetime.datetime, mask: str):
    return value.strftime(mask)


# Lista de palabras reservadas comunes en SQL
SQL_RESERVED_WORDS = [
    "all", "analyse", "analyze", "and", "any", "array", "as", "asc",
    "asymmetric", "authorization", "binary", "both", "case", "cast",
    "check", "collate", "collation", "column", "constraint", "create",
    "cross", "current_catalog", "current_date", "current_role",
    "current_time", "current_timestamp", "current_user", "default",
    "deferrable", "desc", "distinct", "do", "else", "end", "except",
    "false", "fetch", "for", "foreign", "freeze", "from", "full",
    "grant", "group", "having", "ilike", "in", "initially", "inner",
    "intersect", "into", "is", "isnull", "join", "lateral", "leading",
    "left", "like", "limit", "localtime", "localtimestamp", "natural",
    "not", "notnull", "null", "offset", "on", "only", "or", "order",
    "outer", "overlaps", "placing", "primary", "references", "returning",
    "right", "select", "session_user", "similar", "some", "symmetric",
    "table", "tablesample", "then", "to", "trailing", "true", "union",
    "unique", "user", "using", "variadic", "verbose", "when", "where",
    "window", "with"
]


class TableSchema(QSSupport, FlowComponent):
    """
    TableSchema

        Overview

            The TableSchema class is a component for reading a CSV file or DataFrame and creating a table schema based
            on data models. It supports various formatting and normalization options for column names, datatype inference,
            and automatic handling of primary keys. This component also supports normalization settings for column names,
            such as camelCase to snake_case conversion, illegal character removal, and customizable name replacements.

        :widths: auto

            | filename          |   Yes    | The CSV file or DataFrame input to read and infer schema from.               |
            | schema            |   No     | The database schema for the table.                                           |
            | tablename         |   Yes    | The name of the table to be created based on the data model.                 |
            | drop              |   No     | Boolean specifying if an existing table with the same name should be dropped.|
            | normalize_names   |   No     | Dictionary with options for column name normalization.                       |
            | pk                |   No     | List of columns to define as primary keys.                                   |
            | replace_names     |   No     | Dictionary of column name replacements for renaming specific columns.        |

        Returns

            This component returns the input data after creating a database table schema based on the data's inferred or
            specified structure. If the input is a file, it reads and processes the file; if a DataFrame, it directly
            processes the DataFrame. The component provides detailed metrics on column structure and row counts, as well as
            logging for SQL execution status and any schema creation errors.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          TableSchema:
          # attributes here
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        """Init Method."""
        self.separator: str = ","
        self.params: Dict = {}
        self.fields: Dict = {}
        self.replace_names: Dict = {}
        self.drop: bool = False
        self.data: Any = None
        self.filename: str = None
        # info about table:
        self.tablename: str = None
        self.schema: str = None
        self.credentials = kwargs.pop('credentials', None)
        self._driver: str = kwargs.pop('driver', 'pg')
        super(TableSchema, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    async def start(self, **kwargs):
        if self.previous:
            if isinstance(self.input, PosixPath):
                self.filename = self.input
            elif isinstance(self.input, list):
                self.filename = PosixPath(self.input[0])
            elif isinstance(self.input, str):
                self.filename = PosixPath(self.input)
            elif isinstance(self.input, dict):
                filenames = list(self.input.keys())
                if filenames:
                    try:
                        self.filename = PosixPath(filenames[0])
                    except IndexError as err:
                        raise FileError(f"File doesnt exists: {filenames}") from err
            elif isinstance(self.input, dd.DataFrame) or isinstance(
                self.input, pd.DataFrame
            ):
                self.filename = None
                self.data = self.input
            else:
                raise FileError(f"File doesnt exists: {self.input}")
        elif hasattr(self, "filename"):
            self.filename = Path(self.filename)
        else:
            raise ComponentError(
                "TableSchema: This Component requires a File or Dataframe from input."
            )
        if hasattr(self, "replace_names") and self.replace_names:
            for col, replace in self.replace_names.items():
                if not isinstance(replace, (str, dict)):
                    self._logger.warning(
                        f"Invalid replace_names value for '{col}': expected string or dict, got {type(replace).__name__}"
                    )
                elif isinstance(replace, dict) and "type" in replace and replace["type"] not in dtypes:
                    self._logger.warning(
                        f"Type '{replace['type']}' in replace_names for column '{col}' is not valid. Valid types: {list(dtypes.keys())}"
                    )

        await super().start(**kwargs)
        self.processing_credentials()

    async def close(self):
        pass

    def rename_repeated_col(self, col, cols):
        renamed = False
        count = 1
        for c, t in cols:
            if c == col:
                if not renamed:
                    col = f"{col}_{count}"
                    count += 1
                    renamed = True
                else:
                    col = col.split("_", 1)[0]
                    col = f"{col}_{count}"
                    count += 1
        return col

    def handle_sql_reserved_word(self, column_name):
        """
        Verify if the column name is a SQL reserved word
        and raise an error if it is.

        Args:
            column_name (str): Column name to verify

        Returns:
            str: The same column name if it is not a reserved word

        Raises:
            ComponentError: If the column name is a SQL reserved word
        """
        if column_name.lower() in SQL_RESERVED_WORDS:
            error_msg = (f"Column name '{column_name}' is a SQL reserved word. "
                        f"Please use 'replace_names' to change this column name.")
            self._logger.error(error_msg)
            raise ComponentError(error_msg)
        return column_name

    async def run(self):
        self.result = None
        if not hasattr(self, "mime"):
            self.mime = "text/csv"
        if self.filename:
            if self.mime in excel_based:
                if (
                    self.mime == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ):
                    # xlsx or any openxml based document
                    file_engine = self.params.get("file_engine", "openpyxl")
                elif (
                    self.mime == "application/vnd.ms-excel.sheet.binary.macroEnabled.12"
                ):
                    file_engine = self.params.get("file_engine", "pyxlsb")
                else:
                    try:
                        ext = self.filename.suffix
                    except (AttributeError, ValueError):
                        ext = ".xls"
                    if ext == ".xls":
                        file_engine = self.params.get("file_engine", "xlrd")
                    else:
                        file_engine = self.params.get("file_engine", "openpyxl")
                # passed arguments to Pandas directly
                arguments = {**self.params}
                if hasattr(self, "pd_args") and isinstance(self.pd_args, dict):
                    arguments = {**self.params, **self.pd_args}
                df = pd.read_excel(
                    self.filename,
                    engine=file_engine,
                    keep_default_na=True,
                    na_filter=False,
                    **arguments,
                )
            else:
                self.params = {"infer_datetime_format": True}
                arguments = {**self.params}
                if hasattr(self, "pd_args") and isinstance(self.pd_args, dict):
                    arguments = {**self.params, **self.pd_args}
                try:
                    # can we use pyarrow.
                    engine = arguments["engine"]
                    del arguments["engine"]
                except KeyError:
                    engine = "c"
                tp = pd.read_csv(
                    self.filename,
                    sep=self.separator,
                    decimal=",",
                    engine=engine,
                    keep_default_na=False,
                    na_values=["TBD", "NULL", "null"],
                    na_filter=True,
                    skipinitialspace=True,
                    iterator=True,
                    chunksize=1000,
                    **arguments,
                )
                df = pd.concat(tp, ignore_index=True)
            # read filename from self.filename
            self._result = self.filename
        elif self.data is not None:
            # is already a dataframe:
            df = self.data
            self._result = self.data
        else:
            return False
        if df is None or df.empty:
            raise DataNotFound(f"Empty File or Data: {self.filename}")
        # adding stat from dataframe:
        pd.set_option("display.float_format", lambda x: "%.3f" % x)
        self.add_metric("COLUMNS", df.columns)
        self.add_metric("ROWS", len(df.index))
        # removing empty cols
        if hasattr(self, "drop_empty"):
            df.dropna(axis="columns", how="all", inplace=True)
            df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
        if hasattr(self, "dropna"):
            df.dropna(subset=self.dropna, how="all", inplace=True)
        if hasattr(self, "trim"):
            cols = list(df.columns)
            for col in cols:
                df[col] = df[col].astype(str).str.strip()
        if self._debug:
            print(df)
            # print('COLS: >> ', df.columns)
        columns = df.columns
        cols = []
        replaced_columns = list(self.replace_names.keys())
        if hasattr(self, "pre_rename"):
            ### can rename columns PREVIOUS TO normalize
            for col in columns:
                datatype = df.dtypes[col]
                try:
                    t = dtypes[datatype]
                except KeyError:
                    t = str
                if col in self.pre_rename:
                    col = self.pre_rename[col]
                col = self.rename_repeated_col(col, cols)
                col = self.handle_sql_reserved_word(col)
                f = (col, t)
                cols.append(f)
        elif hasattr(self, "normalize_names"):
            for col in columns:
                datatypes = str(df.dtypes[col])
                t = str
                tmp_col = col
                try:
                    t = dtypes[datatypes]
                    data = df[col].iloc[0]
                    if datatypes == "object":
                        # try to infer datatype:
                        if isinstance(data, str) and data != np.nan:
                            if data.isalpha():
                                t = str
                            else:
                                try:
                                    dt = _dateutil_parse(str(data))
                                    if isinstance(dt, datetime.datetime):
                                        t = datetime.datetime
                                except (ValueError, TypeError):
                                    pass
                except KeyError:
                    t = str

                if isinstance(col, (datetime.datetime, datetime.date)):
                    mask = getattr(self, "mask_datetime", "%b_%d_%Y")
                    new_name = datetime_to_name(col, mask)
                elif is_snakecase(col):
                    new_name = col.strip().lower()
                elif is_camelcase(col):
                    new_name = "_".join(
                        [x.lower().strip() for x in camelcase_split(col)]
                    )
                else:
                    new_name = re.sub(r"[^a-zA-Z0-9_]", "", col).strip()
                    if hasattr(self, "normalize"):
                        ## making some changes on col_name:
                        if (
                            "remove_prefix" in self.normalize and self.normalize["remove_prefix"]
                        ):
                            prefix = self.normalize["remove_prefix"]
                            new_name = new_name.removeprefix(prefix)
                        if "trim" in self.normalize and self.normalize["trim"] is True:
                            new_name = new_name.strip()
                        ### remove any illegal character
                        new_name = remove_illegal_chars(new_name)
                        # re-covert again from camelCase:
                        if (
                            "camelcase" in self.normalize and self.normalize["camelcase"] is True
                        ):
                            new_name = new_name.replace(" ", "").translate(
                                str.maketrans("", "", "/:.")
                            )
                            new_name = re.sub(r"\([^)]*\)", "", new_name)
                        else:
                            new_name = "_".join(
                                [x.lower().strip() for x in camelcase_split(new_name)]
                            )

                # Log names after basic normalization but before replace_names
                if self._debug:
                    # Store initial normalizations for later display
                    if not hasattr(self, '_initial_normalizations'):
                        self._initial_normalizations = []

                    # Get type as string
                    type_str = getattr(t, "__name__", str(t))

                    # Get a sample value from the original column
                    sample_value = "N/A"
                    try:
                        if len(df) > 0 and col in df.columns:
                            sample_value = df[col].iloc[0]
                    except:
                        pass

                    # Store information for later display
                    self._initial_normalizations.append((new_name, type_str, sample_value))

                # RENAMING THE COLUMN WITH A NEW NAME:
                if new_name in replaced_columns:
                    replace = self.replace_names[new_name]
                    if isinstance(replace, str):
                        new_name = self.replace_names[new_name]
                    elif isinstance(replace, dict):
                        if "name" in replace:
                            new_name = replace["name"]
                        if "type" in replace:
                            try:
                                t = dtypes[replace["type"]]
                            except KeyError:
                                self._logger.warning(
                                    f"Type '{replace['type']}' not found in dtypes for column '{new_name}', using default type."
                                )
                    else:
                        self._logger.warning(
                            f"Invalid replace_names value for '{new_name}': expected string or dict, got {type(replace).__name__}"
                        )
                if new_name in self.fields:
                    t = dtypes[self.fields[new_name]]
                new_name = self.rename_repeated_col(new_name, cols)
                f = (new_name, t)
                cols.append(f)
                if tmp_col == new_name:
                    self._logger.warning(
                        f"The Column '{new_name}' has not normalized"
                    )
                else:
                    self._logger.debug(
                        f" - Normalized Name: {new_name}"
                    )
        else:
            for col in columns:
                datatype = df.dtypes[col]
                try:
                    t = dtypes[datatype]
                except KeyError:
                    t = str
                col = self.rename_repeated_col(col, cols)
                f = (col, t)
                cols.append(f)
        try:
            cls = Model.make_model(
                name=self.tablename,
                schema=self.schema,
                fields=cols
            )
            # Show all collected information in clean format
            if hasattr(self, '_debug') and self._debug and hasattr(self, '_initial_normalizations'):
                print("\n::: First Normalization columns === ")
                for name, type_str, value in self._initial_normalizations:
                    print(f"{name} -> {type_str} -> {value}")
                print("=== End :::\n")
        except Exception as err:
            print("ERROR:", err)
            raise ComponentError(str(err)) from err
        if cls:
            # mdl = cls()  # empty model, I only need the schema
            # TODO: open the metadata table and compare with model
            if sql := cls.model(dialect="sql"):
                print("SQL IS ", sql)

                try:
                    connection = await self.create_connection(driver=self._driver)

                    async with await connection.connection() as conn:

                        if self.drop is True:
                            self._logger.info(f"Dropping table {self.schema}.{self.tablename}")
                            result, error = await conn.execute(
                                sentence=f"DROP TABLE IF EXISTS {self.schema}.{self.tablename};"
                            )

                        self._logger.info(f"Creating table {self.schema}.{self.tablename}")
                        result, error = await conn.execute(sentence=sql)
                        if error:
                            self._logger.error(f"Error creating table: {error}")
                            raise ComponentError(f"Error on Table creation: {error}")
                        else:
                            self.add_metric("Table", result)
                            self._logger.info(f"Table {self.schema}.{self.tablename} created successfully")
                            if self._debug is True:
                                logging.debug(f"TableSchema: {result!s}")

                        # add Primary Key to table:
                        if hasattr(self, "pk"):
                            pk = pk_sentence.format(
                                schema=self.schema,
                                table=self.tablename,
                                fields=",".join(self.pk),
                            )
                            self._logger.info(f"Adding primary key on columns: {self.pk}")
                            _primary, error = await conn.execute(sentence=pk)
                            if error:
                                self._logger.warning(f"Error adding primary key: {error}")
                            else:
                                self._logger.info("Primary key added successfully")
                            logging.debug(f"TableSchema: PK creation: {_primary}, {error}")
                except Exception as err:
                    self._logger.error(f"Error connecting to database: {err}")
                    raise ComponentError(f"Error on database connection: {err}") from err
        # passthrough the previous component value:
        self._result = self.input
        return self.input
