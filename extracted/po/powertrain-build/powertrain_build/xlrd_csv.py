# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module for providing an xlrd interface for csv files.

TODO: Handle sheet names in a better way!
"""

import csv
import os
import re


class WorkBook:
    """Emulate xlrd of csv files."""

    def __init__(self, csv_files):
        """Init."""
        self._worksheets = {}
        self._read_csv_files_to_worksheets(csv_files)

    def _read_csv_files_to_worksheets(self, csv_files):
        """Read CSV-files, and store them as worksheets."""
        csv_files = [csv_files] if isinstance(csv_files, str) else csv_files
        if len(csv_files) > 1:
            for file_ in csv_files:
                sheet_name = re.match(r'.*?\w*_([\w\$]+)\.\w+', file_).group(1)
                self._worksheets[sheet_name] = WorkSheet(sheet_name, file_)
        else:
            _, sheet_name = os.path.split(csv_files[0])
            self._worksheets[sheet_name] = WorkSheet(sheet_name, csv_files[0])

    def sheet_by_name(self, name):
        """Get a worksheet name from a workbook class."""
        return self._worksheets[name]

    def single_sheet(self):
        """Get single worksheet if only one file was read."""
        return next(iter(self._worksheets.values())) if len(self._worksheets) == 1 else None


class WorkSheet:
    """Emulate xlrd for csv files."""

    def __init__(self, sheet_name, file_name):
        """Init."""
        self._sheet_name = sheet_name
        self._read_work_sheet(file_name)

    def _read_work_sheet(self, file_name):
        """Read csv-file as a worksheet."""
        with open(file_name, 'r', encoding="ISO-8859-1") as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            self._rows = [[Data(elem) for elem in row] for row in reader]
            self._nrows = len(self._rows)

    @property
    def nrows(self):
        """Get number of rows in a worksheet."""
        return self._nrows

    def row(self, row):
        """Get row from sheet."""
        return self._rows[row]


class Data:
    """Class for wrapping data in a worksheet."""

    def __init__(self, value):
        """Init."""
        # TODO: Investigate quoting string values when exporting to CSV
        if re.fullmatch('[+-]?[0-9]+', value):
            self._value = int(value)
        elif re.fullmatch('[+-]?[0-9.]+', value):
            self._value = float(value)
        else:
            self._value = value

    def __repr__(self):
        """Get representation of object."""
        return self._value

    @property
    def value(self):
        """Provide the value of the data object."""
        return self._value
