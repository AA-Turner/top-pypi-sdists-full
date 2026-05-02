import asyncio
from typing import Dict
from collections.abc import Callable
from pathlib import Path
import csv
import numpy as np
import pandas as pd
from ..exceptions import ComponentError, DataNotFound
from .flow import FlowComponent
from ..utils.constants import excel_based


class PandasToFile(FlowComponent):
    """
    PandasToFile

        Overview

            This component exports a pandas DataFrame to a file in CSV, Excel, or JSON format.

        :widths: auto


        | filename               |   Yes    | The name of the file to save the DataFrame to.                              |
        | directory              |   No     | The directory where the file will be saved. If not specified,               |
        |                        |          | it will be derived from the filename.                                       |
        | mime                   |   No     | The MIME type of the file. Supported types are "text/csv",                  |
        |                        |          | "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",        |
        |                        |          | "application/vnd.ms-excel", "application/json". Default is "text/csv".      |
        | zerofill               |   No     | If True, fills NaN values with "0" in string columns. Default is False.     |
        | quoting                |   No     | Specifies the quoting behavior for CSV files. Options are "all" (QUOTE_ALL),|
        |                        |          | "string" (QUOTE_NONNUMERIC), and None (QUOTE_NONE). Default is None.        |
        | pd_args                |   No     | Additional arguments for pandas' to_csv, to_excel, or to_json methods.      |
        |                        |          | Default is an empty dictionary.                                             |
        |  sep                   |   Yes    | Make a separation of the file name with this sign                           |
        | as_sheets              |   No     | Only for excel, If True, each dataframe will be displayed on a different    |
        |                        |          | sheet.                                                                      |
        | sheet_name             |   No     | An array that define de name of each sheet                                  |
        | column_format          |   No     | Set excel properties for columns                                            |

        Returns

        This component returns the filename of the saved file.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          PandasToFile:
          filename: /home/ubuntu/symbits/bose/files/report/troc_open_tickets_{today}.csv
          masks:
          '{today}':
          - today
          - mask: '%Y-%m-%d'
          mime: text/csv
          quoting: string
          pd_args:
          sep: ','
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
        self.zerofill: bool = False
        self.quoting = None
        self.params: Dict = {}
        self.args: Dict = {}
        self.filename: str = None
        self.directory: str = None
        self.mime: str = "text/csv"
        self.as_sheets: bool = False
        self.sheet_name: list = []
        self.column_format: list = []
        super(PandasToFile, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        if hasattr(self, "pd_args"):
            self.args = getattr(self, "pd_args", {})

    async def start(self, **kwargs):
        # Si lo que llega no es un DataFrame de Pandas se cancela la tarea
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found")
        if isinstance(self.data, list) and self.mime in excel_based:
            for obj in self.data:
                if not isinstance(obj, pd.DataFrame):
                    raise ComponentError(
                        'Incompatible Pandas Dataframe in list: hint> add "export_dataframe": true to tMap component'
                    )
        elif not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                'Incompatible Pandas Dataframe: hint> add "export_dataframe"\
                :true to tMap component'
            )
        if hasattr(self, "masks"):
            self.filename = self.mask_replacement(self.filename)
        # Create directory if not exists
        try:
            if not self.directory:
                self.directory = Path(self.filename).parents[0]
            self.directory.mkdir(parents=True, exist_ok=True)
        except Exception as err:
            self._logger.error(
                f"Error creating directory {self.directory}: {err}"
            )
            raise ComponentError(
                f"Error creating directory {self.directory}: {err}"
            ) from err

    async def close(self):
        pass

    async def run(self):
        self._result = {}
        if self.zerofill:
            cols = self.data.select_dtypes(include=["object", "string"])
            self.data[cols.columns] = cols.fillna("0")
            # self.data.fillna('0', inplace=True)
            self.data.replace(np.nan, 0)
            intcols = self.data.select_dtypes(include=["Int64"])
            self.data[intcols.columns] = intcols.fillna(0)
        try:
            # filename, file_extension = os.path.splitext(self.filename)
            if self.mime == "text/csv" or self.mime == "text/plain":
                if self.quoting == "all":
                    quoting = csv.QUOTE_ALL
                elif self.quoting == "string":
                    quoting = csv.QUOTE_NONNUMERIC
                else:
                    quoting = csv.QUOTE_NONE
                #  if file_extension == '.csv':
                # Los parametros se deben colocar en un diccionario en el JSON
                # donde las llaves van a ser el nombre de los parametros que se
                # muestran en la siguiente dirección
                # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
                if self.data.empty:
                    raise DataNotFound("PandasToFile: Cannot save an Empty Dataframe.")
                self._logger.debug(
                    f"PandasToFile: Export to CSV: {self.filename}"
                )
                self.data.to_csv(
                    self.filename,
                    index=False,
                    quoting=quoting,
                    quotechar='"',
                    escapechar="\\",
                    **self.args,
                )
            elif self.mime in excel_based:
                # elif file_extension == '.xlsx':
                # Los parametros se deben colocar en un diccionario en el JSON
                # donde las llaves van a ser el nombre de los parametros que se
                # muestran en la siguiente dirección
                # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_excel.html
                self._logger.debug(
                    f"PandasToFile: Export to EXCEL: {self.filename}"
                )
                if isinstance(self.data, pd.DataFrame):
                    self.data.to_excel(self.filename, index=False, **self.args)
                elif isinstance(self.data, list):
                    with pd.ExcelWriter(self.filename, engine="xlsxwriter") as writer:
                        workbook = writer.book
                        bold_format = workbook.add_format({"bold": True})
                        if self.as_sheets:
                            # One DataFrame for sheet
                            for idx, df in enumerate(self.data):
                                # Set sheet name
                                if idx < len(self.sheet_name) and self.sheet_name[idx]:
                                    sheet_name = str(self.sheet_name[idx])[:31]  # Excel límit
                                else:
                                    sheet_name = f"Sheet{idx + 1}"

                                df.to_excel(writer, sheet_name=sheet_name, index=False)
                                worksheet = writer.sheets[sheet_name]

                                # Bold header
                                worksheet.set_row(0, None, bold_format)
                                for format in self.column_format:
                                    self._logger.debug(
                                        f"PandasToFile: Set format: {fmt_dict} in column {fmt_column}"
                                    )
                                    fmt_column = format.get('column')
                                    fmt_dict = workbook.add_format(format.get('format'))
                                    worksheet.set_column(fmt_column, fmt_column, None, fmt_dict)

                        else:
                            # All DataFrames in a single sheet
                            if isinstance(self.sheet_name, list) and self.sheet_name and self.sheet_name[0]:
                                sheet_name = self.sheet_name[0]
                            else:
                                sheet_name = 'Sheet1'
                            worksheet = workbook.add_worksheet(sheet_name)
                            writer.sheets[sheet_name] = worksheet

                            current_row = 0

                            for df in self.data:
                                if df is None or df.empty:
                                    continue

                                df.to_excel(
                                    writer,
                                    sheet_name=sheet_name,
                                    startrow=current_row,
                                    index=False,
                                    header=True
                                )
                                worksheet.set_row(current_row, None, bold_format)
                                current_row += len(df) + 2
                            for format in self.column_format:
                                fmt_column = format.get('column')
                                fmt_dict = workbook.add_format(format.get('format'))
                                self._logger.debug(
                                    f"PandasToFile: Set format: {fmt_dict} in column {fmt_column}"
                                )
                                worksheet.set_column(fmt_column, fmt_column, None, fmt_dict)
            elif self.mime == "application/json":
                # elif file_extension == '.json':
                # Los parametros se deben colocar en un diccionario en el JSON
                # donde las llaves van a ser el nombre de los parametros que se
                # muestran en la siguiente dirección
                # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html
                self._logger.debug(
                    f"PandasToFile: Export to JSON: {self.filename}"
                )
                self.data.to_json(self.filename, index=False, **self.args)
            else:
                raise ComponentError(
                    "Error: Only extension supported: csv, xlsx and json are supported"
                )
            # getting filename:
            self._result[self.filename] = True
            self.setTaskVar("FILENAME", self.filename)
            self.add_metric("FILENAME", self.filename)
            return self._result
        except Exception as err:
            raise ComponentError(f"Error in PandasToFile: {err}") from err
