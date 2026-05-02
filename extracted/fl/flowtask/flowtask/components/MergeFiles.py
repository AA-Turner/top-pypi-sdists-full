import os
import logging
import asyncio
from collections.abc import Callable
import types
from functools import reduce
import pandas as pd
import numpy as np
import cchardet as chardet
from ..exceptions import ComponentError
from ..parsers.maps import open_model
from .flow import FlowComponent
from .OpenWithBase import detect_encoding, excel_based


class MergeFiles(FlowComponent):
    """
    MergeFiles

    Overview

        The MergeFiles class is a component for merging multiple files into a single file or dataframe. It supports various
        file formats, including CSV, Excel, and HTML, and handles encoding detection and conversion as needed.

    :widths: auto

        | filename         |   No     | The name of the merged output file.                                                              |
        | file             |   No     | The file object to be merged.                                                                    |
        | filepath         |   No     | The directory path for the merged output file.                                                   |
        | ContentType      |   No     | The content type of the files being merged, defaults to "text/csv".                              |
        | as_dataframe     |   No     | Boolean flag indicating if the result should be returned as a dataframe, defaults to False.      |

    Return

        The methods in this class manage the merging of files, including initialization, execution, and result handling.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          MergeFiles:
          ContentType: application/vnd.ms-excel
          model: worked_hours
          pd_args:
          skiprows: 6
          as_dataframe: true
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
        self.filename = ""
        self.file = None
        self.filepath = ""
        self.ContentType: str = "text/csv"
        self.as_dataframe: bool = False
        super(MergeFiles, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """
        start.
            Start connection.
        """
        if self.previous:
            try:
                if isinstance(self.input, list):
                    # is a list of files
                    self.data = self.input
                elif isinstance(self.input, dict):
                    if "files" in self.input:
                        self.data = self.input["files"]
                    else:
                        self.data = {k: v for k, v in self.input.items()}
                elif isinstance(self.input, types.GeneratorType):
                    # is a generator:
                    self.data = list(self.input)
                else:
                    raise ComponentError(
                        "MergeFiles Error: incompatible kind of previous Object."
                    )
            except Exception as err:
                raise ComponentError(f"Error Filtering Data {err}") from err
        self._logger.debug(f"List of Files: {self.data!r}")
        if hasattr(self, "destination"):
            # we need to calculated the result filename of this component
            filename = self.destination["filename"]
            self.filepath = self.destination["directory"]
            if hasattr(self, "masks"):
                for mask, replace in self._mask.items():
                    filename = str(filename).replace(mask, replace)
            if self._variables:
                filename = filename.format(**self._variables)
            self.filename = os.path.join(self.filepath, filename)
            self.add_metric("MERGED_FILENAME", self.filename)
        return True

    async def close(self):
        """
        close.

            close method
        """

    def _merge_dataframe(self, dfs: list):
        """
        Merges a list of DataFrames based on their common columns.

        Args:
        dfs: A list of pandas DataFrames.

        Returns:
        A single merged DataFrame.
        """
        if not hasattr(self, 'use_merge'):
            # Concatenate the DataFrames
            return pd.concat(dfs)
        # Calculate the common columns in all dataframes
        common_columns = set(dfs[0].columns)
        for df in dfs[1:]:
            common_columns = common_columns.intersection(set(df.columns))
        if not common_columns:
            raise ComponentError("MergeFiles Error: No common columns found.")
        if self.use_merge:
            # Cast column types based on the first dataframe:
            for df in dfs[1:]:
                for col in common_columns:
                    df[col] = df[col].astype(dfs[0][col].dtype)
            merged_df = reduce(
                lambda left, right: pd.merge(left, right, how='outer', on=list(common_columns)), dfs
            )
            # Drop columns with all missing values (empty)
            merged_df = merged_df.dropna(axis=1, how='all')
            return merged_df
        return pd.concat(dfs)

    async def run(self):
        """
        run.

            Run the connection and merge all the files
        """
        np_array_list = []
        df = None
        np_array_list = []
        if isinstance(self.data, list):
            # is a list of files
            if self.ContentType in excel_based:
                args = self.pd_args if hasattr(self, "pd_args") else {}
                if self.ContentType == "application/vnd.ms-excel":
                    file_engine = "xlrd"
                elif (
                    self.ContentType
                    == "application/vnd.ms-excel.sheet.binary.macroEnabled.12"
                ):
                    file_engine = "pyxlsb"
                else:
                    file_engine = "openpyxl"
                # get the Model (if any):
                if hasattr(self, "model"):
                    columns = await open_model(self.model, self._program)
                    fields = []
                    dates = []
                    for field, dtype in columns["fields"].items():
                        fields.append(field)
                        try:
                            t = dtype["data_type"]
                        except KeyError:
                            t = "str"
                        if t in {"date", "datetime", "time"}:
                            dates.append(field)
                    args["names"] = fields
                    if dates:
                        args["parse_dates"] = dates
                files = []
                file_stats = {}
                for file in self.data:
                    if not file:
                        continue
                    try:
                        df = pd.read_excel(
                            file,
                            na_values=["TBD", "NULL", "null", "", "#NA"],
                            engine=file_engine,
                            keep_default_na=True,
                            **args,
                        )
                        file_args = {}
                        if hasattr(self, 'file_stats'):
                            first_row = df.iloc[0][self.file_stats['columns']].to_dict()
                            file_args = first_row
                        file_stats[file.name] = {
                            "numrows": len(df.index),
                            **file_args
                        }
                    except TypeError as ex:
                        self._logger.error(f"Merge Excel Error: {ex}")
                    files.append(df)
                try:
                    self._result = self._merge_dataframe(files)
                    self.add_metric("FILE_STATS", file_stats)
                    self._print_data_(self._result, 'Merged data')
                    if self._debug is True:
                        print("::: Combined File ::: ")
                        print(self._result)
                    if self.as_dataframe is True:
                        numrows = len(self._result)
                        self.add_metric("NUMROWS", numrows)
                        self.add_metric("COLUMNS", self._result.shape[1])
                        return self._result
                    else:
                        # saved as CSV.
                        self._result.to_csv(
                            self.filename, index=False, encoding="utf-8-sig"
                        )
                        self._result = self.filename
                        self.add_metric("MERGED_FILE", self.filename)
                    return self._result
                except Exception as err:
                    logging.exception(
                        f"Error Merging Excel Files: {err}", stack_info=True
                    )
                    self._result = None
                    return False
            elif self.ContentType == "text/html":
                encoding = "utf-8"
                try:
                    if len(self.data) == 1:
                        # there is no other files to merge:
                        combined_csv = pd.read_html(self.data[0], encoding=encoding)
                    else:
                        dfs = []
                        for f in self.data:
                            try:
                                dt = pd.read_html(f, encoding=encoding)
                                dfs.append(dt[0])
                            except (TypeError, ValueError):
                                continue
                        # combine all files in the list
                        combined_csv = pd.concat(
                            dfs, sort=False, axis=0, ignore_index=True
                        ).reindex(dfs[0].index)
                except UnicodeDecodeError:
                    combined_csv = pd.concat(
                        [pd.read_html(f, encoding="windows-1252") for f in self.data]
                    )
                except Exception as err:
                    raise ComponentError(f"{err!s}") from err
                try:
                    if self.as_dataframe is True:
                        self._result = combined_csv
                        self.add_metric("MERGED_DF", self._result.columns)
                    else:
                        # export to csv
                        combined_csv.to_csv(
                            self.filename, index=False, encoding="utf-8-sig"
                        )
                        self._result = self.filename
                        self.add_metric("MERGED_FILE", self.filename)
                    return self._result
                except Exception as err:
                    logging.error(err)
                    self._result = None
                    return False
            elif self.ContentType == "text/csv":
                args = {}
                if hasattr(self, "pd_args"):
                    args = self.pd_args
                if hasattr(self, "encoding"):
                    encoding = self.encoding
                else:
                    encoding = None
                    for file in self.data:
                        try:
                            buffer = None
                            with open(file, "rb") as f:
                                buffer = f.read(10000)
                            result_charset = chardet.detect(buffer)
                            enc = result_charset["encoding"]
                            if encoding is not None and enc != encoding:
                                logging.warning(
                                    "MergeFiles: files has different encoding"
                                )
                            encoding = enc
                            if encoding == "ASCII":
                                encoding = "utf-8-sig"
                        except Exception as err:
                            logging.warning(f"MergeFiles: DECODING ERROR {err}")
                            _, encoding = detect_encoding(file, encoding)
                            if not encoding:
                                encoding = "utf-8-sig"
                try:
                    if len(self.data) == 1:
                        # there is no other files to merge:
                        combined_csv = pd.read_csv(self.data[0], encoding=encoding)
                    else:
                        dfs = [pd.read_csv(f, encoding=encoding) for f in self.data]
                        # combine all files in the list
                        combined_csv = self._merge_dataframe(dfs)
                    print(f"COMBINED CSV: {combined_csv}")
                except UnicodeDecodeError:
                    combined_csv = pd.concat(
                        [pd.read_csv(f, encoding="windows-1252") for f in self.data]
                    )
                except Exception as err:
                    raise ComponentError(f"{err!s}") from err
                try:
                    if self.as_dataframe is True:
                        self._result = combined_csv
                        self.add_metric("MERGED_DF", self._result.columns)
                    else:
                        # export to csv
                        combined_csv.to_csv(
                            self.filename, index=False, encoding="utf-8-sig"
                        )
                        self._result = self.filename
                        self.add_metric("MERGED_FILE", self.filename)
                    return self._result
                except Exception as err:
                    self._logger.error(err)
                    self._result = None
                    return False
        elif isinstance(self.data, dict):
            for f in self.data:
                ip = self.data[f]["data"]
                if self.ContentType == "application/json":
                    if self.data[f]["type"] == "binary/octet-stream":
                        # wrapper = io.TextIOWrapper(input, encoding='utf-8')
                        content = ip.getvalue()
                    else:
                        # convert to string:
                        # wrapper = io.TextIOWrapper(input, encoding='utf-8')
                        content = ip
                    # content = wrapper.read()
                    df = pd.read_json(content, orient="records")
                    columns = list(df.columns)
                    np_array_list.append(df.values)
                comb_np_array = np.vstack(np_array_list)
                df = pd.DataFrame(comb_np_array)
                df.columns = columns
            self._result = df
            self._print_data_(df, 'Merged data')
            return True
        else:
            self._result = None
            return False
