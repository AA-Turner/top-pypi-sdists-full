import os
from typing import Any
from collections.abc import Callable
from abc import abstractmethod
import logging
from io import StringIO
import pandas
import asyncio
import codecs
import mimetypes
from pathlib import Path, PurePath, PosixPath
from xml.sax import ContentHandler
import magic
import chardet
from asyncdb import AsyncDB
from asyncdb.exceptions import NoDataFound
from querysource.conf import asyncpg_url
from ..exceptions import FileNotFound, ComponentError
from ..utils.mail import MailMessage
from ..utils import check_empty
from ..parsers.maps import open_map, open_model
from ..conf import TASK_PATH, DEFAULT_ENCODING
from .flow import FlowComponent
from ..utils.constants import excel_based


supported_extensions = (
    ".xls",
    ".xlsx",
    ".xlsm",
    ".xlsb",
    ".xml",
    ".txt",
    ".csv",
    ".json",
    ".htm",
    ".html",
)


def detect_encoding(filename, encoding: str = "utf-8"):
    bt = min(256, os.path.getsize(filename))
    enc = ""
    raw = open(filename, "rb").read(bt)
    if raw.startswith(codecs.BOM_UTF8):
        enc = "utf-8-sig"
    elif raw.startswith(codecs.BOM_UTF16_LE):
        enc = "utf-16le"
    elif raw.startswith(codecs.BOM_UTF16):
        enc = "utf-16"
    elif raw.startswith(codecs.BOM_UTF16_BE):
        enc = "utf-16be"
    elif raw.startswith(codecs.BOM_UTF32_LE):
        enc = "utf-32"
    else:
        try:
            result = chardet.detect(raw)
            if result["encoding"] in ("ASCII", "ascii"):
                # let me try to repair the file:
                content = None
                with open(filename, "rb") as fp:
                    content = fp.read()
                decoded = content.decode(encoding, "ignore")
                output = StringIO()
                output.write(decoded)
                output.seek(0)
                return [output, encoding]
            else:
                enc = result["encoding"]
        except UnicodeDecodeError:
            try:
                raw = open(filename, "r+", encoding=encoding).read(bt)
                result = raw.encode("utf-8")
                output = StringIO()
                output.write(result.decode("utf-8"))
                output.seek(0)
                return [output, encoding]
            except UnicodeEncodeError:
                return [None, "iso-8859-1"]
        except Exception as exc:
            logging.warning(f"Unable to determine enconding of file: {exc}")
            return [None, DEFAULT_ENCODING]
    return [None, enc]


# Reference https://goo.gl/KaOBG3
class ExcelHandler(ContentHandler):
    def __init__(self):
        self.chars = []
        self.cells = []
        self.rows = []
        self.tables = []
        super(ExcelHandler, self).__init__()

    def characters(self, content):
        self.chars.append(content)

    def startElement(self, name, attrs):
        if name == "Cell":
            self.chars = []
        elif name == "Row":
            self.cells = []
        elif name == "Table":
            self.rows = []

    def endElement(self, name):
        if name == "Cell":
            self.cells.append("".join(self.chars))
        elif name == "Row":
            self.rows.append(self.cells)
        elif name == "Table":
            self.tables.append(self.rows)


class OpenWithBase(FlowComponent):
    """
    OpenWithBase


        Overview

            Abstract Component for Opening Files into DataFrames.
            Supports various file types such as CSV, Excel, and XML.

        :widths: auto


        | directory    |   No     | The directory where the files are located.                        |
        | filename     |   No     | The name of the file to be opened. Supports glob patterns.        |
        | file         |   No     | A dictionary containing the file patterns to be used.             |
        | mime         |   No     | The MIME type of the file. Default is "text/csv".                 |
        | separator    |   No     | The delimiter to be used in CSV files. Default is ",".            |
        | encoding     |   No     | The encoding of the file.                                         |
        | datatypes    |   No     | Specifies the datatypes to be used for columns.                   |
        | parse_dates  |   No     | Specifies columns to be parsed as dates.                          |
        | filter_nan   |   No     | If True, filters out NaN values. Default is True.                 |
        | na_values    |   No     | List of strings to recognize as NaN. Default is ["NULL", "TBD"].  |
        | clean_nat    |   No     | If True, cleans Not-A-Time (NaT) values.                          |
        | no_multi     |   No     | If True, disables multi-threading.                                |
        | flavor       |   No     | Specifies the database flavor to be used for column information.  |
        | force_map    |   No     | If True, forces the use of a mapping file.                        |
        | skipcols     |   No     | List of columns to be skipped.                                    |
        | pd_args      |   No     | Additional arguments to be passed to pandas read functions.       |

        Returns

        This component opens files and prepares them for further processing. The actual return type depends on the concrete
        implementation, but typically it returns a list of filenames or file data.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          OpenWithBase:
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
    ):
        """Init Method."""
        # self.directory: str = None
        self._filenames: list[PurePath] = []
        self.filename: PurePath = kwargs.get('filename', None)
        self.directory: PurePath = None
        self._path: str = None
        self.mime: str = "text/csv"  # Default Mime type
        self.separator: str = ","
        self._colinfo = None
        self._data = None
        self.force_map: bool = False
        self.parse_dates = {}
        self.filter_nan: bool = True
        self.na_values: list = ["NULL", "TBD"]
        self.remove_empty_strings: bool = True
        self.no_multi: bool = False
        self.sheet_name: str = None
        self.clean_nat = kwargs.pop(
            "clean_nat", False
        )
        self._limit = kwargs.pop('limit', None)
        self._flavor: str = kwargs.pop('flavor', 'postgres')
        super(OpenWithBase, self).__init__(loop=loop, job=job, stat=stat, **kwargs)
        if hasattr(self, "pd_args"):
            self.args = getattr(self, "pd_args", {})
        else:
            self.args = {}

    async def close(self) -> None:
        pass

    @abstractmethod
    def set_datatypes(self):
        pass

    async def column_info(
        self, table: str, schema: str = "public", flavor: str = "postgres"
    ) -> list:
        if not self.force_map:
            result = None
            if flavor == "postgres":
                tablename = f"{schema}.{table}"
                discover = f"""SELECT attname AS column_name,
                 atttypid::regtype AS data_type, attnotnull::boolean as notnull
                  FROM pg_attribute WHERE attrelid = '{tablename}'::regclass
                  AND attnum > 0 AND NOT attisdropped ORDER  BY attnum;
                """
                try:
                    try:
                        event_loop = asyncio.get_running_loop()
                    except RuntimeError:
                        event_loop = asyncio.get_event_loop()
                    db = AsyncDB("pg", dsn=asyncpg_url, loop=event_loop)
                    async with await db.connection() as conn:
                        result, error = await conn.query(discover)
                        if error:
                            raise ComponentError(f"Column Info Error {error}")
                except NoDataFound:
                    pass
                finally:
                    db = None
            else:
                raise ValueError(f"Column Info: Flavor not supported yet: {flavor}")
            if result:
                return {item["column_name"]: item["data_type"] for item in result}
        model = await open_model(table, schema)
        if model:
            fields = model["fields"]
            return {field: fields[field]["data_type"] for field in fields}
        else:
            if self.force_map:
                self._logger.debug(
                    f"Open Map: Forcing using of Map File {schema}.{table}"
                )
            else:
                self._logger.error(f"Open Map: Table {schema}.{table} doesn't exist")
            return None

    def previous_component(self):
        # TODO: check if input is a list of paths (purepath?)
        self._filenames = []
        if isinstance(self.input, (PosixPath, PurePath)):
            self.filename = self.input
            self._filenames.append(self.input)
        elif isinstance(self.input, list):
            self._data = []
            for filename in self.input:
                # check if is a MailMessage Object
                if isinstance(filename, MailMessage):
                    for f in filename.attachments:
                        fname = f["filename"]
                        logging.debug(f"File: Detected Attachment: {fname}")
                        self._filenames.append(fname)
                elif isinstance(filename, (PosixPath, PurePath)):
                    self.filename = filename
                    self._filenames.append(filename)
                elif isinstance(filename, str):
                    fname = self.mask_replacement(filename)
                    if "*" in fname:
                        listing = list(self.directory.glob(fname))
                        for fname in listing:
                            logging.debug(f"Filename > {fname}")
                    self._filenames.append(fname)
                    self._filenames.append(PosixPath(fname))
                elif isinstance(filename, (bytes, bytearray)):
                    self._data.append(filename)
                else:
                    raise ValueError(
                        f"OpenWithBase: Unknown Input type {type(filename)}"
                    )
        elif isinstance(self.input, dict):
            if "files" in self.input:
                for filename in self.input["files"]:
                    if filename.suffix.lower() not in supported_extensions:
                        continue
                    if filename.exists():
                        self._filenames.append(filename)
            else:
                filenames = list(self.input.keys())
                for filename in filenames:
                    if not isinstance(filename, PurePath):
                        filename = PosixPath(filename)
                    if filename.suffix.lower() not in supported_extensions:
                        continue
                    fname = self.mask_replacement(filename)
                    self._filenames.append(fname)
        elif isinstance(self.input, pandas.DataFrame):
            # if is a dataframe, we don't have filenames information
            self.data = self.input
            self._data = None
            self._filenames = []
        else:
            if hasattr(self, "FileIterator"):
                self._data = self.chunkData
            elif isinstance(self.input, (bytes, bytearray)):
                self.filename = None
                self._data = self.input
            else:
                self.filename = self.input
                self._filenames = self._filenames.append(self.input)

    async def start(self, **kwargs):
        if self.previous and not check_empty(self.input):
            self.previous_component()
        if "iterate" in self._params and self._params["iterate"] is True:
            ## re-evaluate previous data:
            self.previous_component()
        if self.directory:
            p = Path(self.directory)
            if p.exists() and p.is_dir():
                self.directory = p
            else:
                logging.error(f"Path doesn't exists: {self.directory}")
                raise FileNotFound(f"Path doesn't exists: {self.directory}")
        else:
            # TODO: using FileStorage
            self.directory = Path(TASK_PATH, self._program, "files")
        if not self._filenames:
            if self.filename:
                if isinstance(self.filename, list):
                    for file in self.filename:
                        self._filenames.append(self.directory.joinpath(file))
                elif isinstance(self.filename, str):
                    self.filename = self.mask_replacement(self.filename)
                    if "*" in self.filename:
                        # is a glob list of files
                        listing = list(self.directory.glob(self.filename))
                        for fname in listing:
                            logging.debug(f"Filename > {fname}")
                            self._filenames.append(fname)
                    else:
                        self._path = self.directory.joinpath(self.filename)
                        self._filenames.append(self._path)
            elif hasattr(self, "file"):
                filename = self.process_pattern("file")
                if hasattr(self, "masks"):
                    filename = self.mask_replacement(filename)
                # path for file
                listing = list(self.directory.glob(filename))
                for fname in listing:
                    logging.debug(f"Filename > {fname}")
                    self._filenames.append(fname)
        if not self._filenames:
            raise FileNotFound("OpenWithPandas: File is empty or doesn't exists")
        # definition of data types:
        if hasattr(self, "datatypes"):
            # need to build a definition of datatypes
            self.set_datatypes()
        # check if data is not none:
        if self._filenames is None and self._data is not None:
            self._filenames = []
            if not isinstance(self._data, list):
                # convert into a list:
                self._data = [self._data]
        else:
            m = magic.Magic(mime=True)
            for file in self._filenames:
                if isinstance(file, str):
                    file = PosixPath(file)
                if file.exists() and file.is_file():
                    if not self.mime:
                        # detecting the MIME type
                        try:
                            self.mime = m.from_file(str(file))
                            self._logger.debug(f":: Detected MIME IS: {self.mime}")
                        except Exception as err:
                            logging.error(err)
                            self.mime = mimetypes.guess_type(file)[0]
                            if not self.mime:
                                ext = file.suffix
                                if ext == ".xlsx" or ext == ".xls":
                                    self.mime = "application/vnd.ms-excel"
                                elif ext == ".csv" or ext == ".txt":
                                    self.mime = "text/csv"
                                else:
                                    self.mime = "text/plain"
                else:
                    raise FileNotFound(f"{__name__}: File doesn't Exists: {file}")
        return True

    async def colinfo(self):
        add_columns = {}
        if hasattr(self, "model"):
            raise NotImplementedError("Using Models is not implemented yet.")
        elif hasattr(self, "map"):
            try:
                replace = self.map["replace"]
            except KeyError:
                replace = False
            try:
                self.force_map = self.map["use_map"]
            except KeyError:
                self.force_map = False
            ## schema name:
            try:
                schema = self.map["schema"]
            except KeyError:
                schema = self._program
            ## first: check if Table exists:
            try:
                tablename = self.map["tablename"]
                colinfo = await self.column_info(
                    table=tablename, schema=schema, flavor=self._flavor
                )
            except KeyError:
                mapping = self.map["map"]
                model = await open_model(mapping, schema)
                fields = model["fields"]
                colinfo = {field: fields[field]["data_type"] for field in fields}
                if not colinfo:
                    # last effort:
                    colinfo = await open_map(mapping, schema)
            if colinfo is not None:
                try:
                    ignore = self.map["ignore"]
                    colinfo = {k: v for k, v in colinfo.items() if k not in ignore}
                except KeyError:
                    pass
                # skipcols
                if "skipcols" in self.map:
                    # need to remove some columns
                    if "num_cols" in self.map:
                        cols = self.map["num_cols"]
                    else:
                        cols = len(colinfo.keys())
                    colrange = range(cols + 1)
                    remcols = self.map["skipcols"]
                    self.args["usecols"] = list(set(colrange) - set(remcols))
                # change the functionality to use the columns and not first row
                self._colinfo = colinfo
                if replace:
                    if (
                        hasattr(self, "pd_args")
                        and isinstance(self.pd_args, dict)
                        and "skiprows" in self.pd_args
                    ):
                        self.pd_args["skiprows"].append(
                            self.pd_args["skiprows"][-1] + 1
                        )
                        self.args["skiprows"] = self.pd_args["skiprows"]
                    else:
                        self.args["skiprows"] = [0]
                    replace_columns = {"header": None, "names": list(colinfo.keys())}
                    add_columns = {**add_columns, **replace_columns}
                    # parse dates and dataTypes
                    dates = []
                    dtypes = {}
                    try:
                        mapped_types = self.args["dtype"]
                    except KeyError:
                        mapped_types = {}
                    coliter = colinfo.copy()
                    for column, dtype in coliter.items():
                        # print('COL ', column, dtype, mapped_types)
                        if column in mapped_types:
                            ## is already overrided by datetypes:
                            colinfo[column] = mapped_types[column]
                            dtypes[column] = mapped_types[column]
                            continue
                        if dtype in (
                            "timestamp without time zone",
                            "timestamp with time zone",
                            "date",
                        ):
                            dates.append(column)
                        elif dtype in (
                            "time",
                            "time with time zone",
                            "time without time zone",
                        ):
                            dates.append(column)
                            # dtypes[column] = 'datetime64[ns]'
                        elif dtype in ("varchar", "character varying", "str"):
                            dtypes[column] = "str"
                        elif dtype == "character" or dtype == "text":
                            dtypes[column] = "object"
                        elif (
                            dtype == "integer"
                            or dtype == "smallint"
                            or dtype == "bigint"
                        ):
                            dtypes[column] = "Int64"
                        elif dtype == "float" or dtype == "double precision":
                            dtypes[column] = float
                        else:
                            dtypes[column] = "object"
                        if self.mime in excel_based:
                            # can safely convert to integer
                            if dtype == "numeric" or dtype == "float":
                                dtypes[column] = float
                            elif dtype == "real":
                                dtypes[column] = float
                            elif dtype == "double precision":
                                dtypes[column] = float
                            elif dtype == "integer":
                                try:
                                    dtypes[column] = "Int32"
                                except Exception:
                                    dtypes[column] = "Int64"
                            elif dtype == "bigint":
                                dtypes[column] = "Int64"
                            else:
                                dtypes[column] = "object"
                    if dates:
                        self.parse_dates["parse_dates"] = dates
                    if dtypes:
                        self.args["dtype"] = dtypes
                elif not replace and hasattr(self, "no_header") and self.no_header:
                    if self._data is not None:
                        replace_columns = {"columns": list(colinfo.keys())}
                    else:
                        replace_columns = {
                            "header": None,
                            "names": list(colinfo.keys()),
                        }
                    add_columns = {**add_columns, **replace_columns}
            else:
                raise ComponentError("Failed to Load Column Information")
        elif hasattr(self, "add_columns"):
            try:
                if self._data is not None:
                    add_columns = {"columns": self.add_columns}
                else:
                    if isinstance(self.add_columns, list):
                        add_columns = {"names": list(self.add_columns)}
                        if hasattr(self, "replace_columns"):
                            add_columns["header"] = None
                            add_columns["skiprows"] = [0]
            except AttributeError:
                pass
        elif hasattr(self, "skipcols"):
            ## Skip Columns from Raw Table.
            skipcols = self.skipcols
            if isinstance(skipcols[0], str):
                ### directly the name of a Column:
                add_columns = {"usecols": skipcols}
            elif isinstance(skipcols[0], int):
                ### Discover the number of Columns:
                headers = self.get_column_headers()
                ### because all files need to be equal, using first one:
                try:
                    columns = headers[0]
                    colrange = range(len(columns))
                    usecols = list(set(colrange) - set(skipcols))
                    add_columns = {"usecols": usecols}
                except (IndexError, ValueError, KeyError):
                    pass
        return add_columns

    async def run(self) -> Any:
        print(f"Opening File(s): {self._filenames!r}")

    def check_encoding(self, filename):
        encoding = "utf-8"  # default encoding
        try:
            if hasattr(self, "encoding"):
                encoding = self.encoding
            else:
                count = 0
                # migrate to aiofile
                bt = min(32, os.path.getsize(filename))
                with open(filename, "rb") as f:
                    line = f.read(bt)
                    # with open(filename, 'rb') as f:
                    #    line = f.readline()
                    while line and count < 20:
                        curChar = chardet.detect(line)
                        if curChar != chardet.detect(line):
                            result_charset = chardet.detect(line)
                        else:
                            result_charset = curChar
                        count = count + 1
                    self._logger.debug(
                        f"Detected Charset in file {filename} > {result_charset!s}"
                    )
                    if result_charset["confidence"] < 0.8:
                        # failed confidence, need to use:
                        if result_charset["encoding"] in ("ascii", "ASCII"):
                            encoding = "ISO-8859–1"
                        else:
                            encoding = "utf-8"
                    else:
                        encoding = result_charset["encoding"]
                    if result_charset["encoding"] in ("ascii", "ASCII"):
                        encoding = "ISO-8859–1"
                    else:
                        encoding = result_charset["encoding"]
        except Exception:
            encoding = "utf-8"
        #  returns default encoding
        return encoding

    @abstractmethod
    async def open_csv(self, filename: str, add_columns: dict, encoding) -> Any:
        pass

    @abstractmethod
    async def open_excel(self, filename: str, add_columns: dict, encoding) -> Any:
        pass
