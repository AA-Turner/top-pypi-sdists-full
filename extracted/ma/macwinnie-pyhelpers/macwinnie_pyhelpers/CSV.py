#!/usr/bin/env python3
import io
import math
import os
from datetime import datetime

import pandas as pd


ord0 = ord("A")


def xlsCol2Int(colName):
    """XLS col to int

    According to `A` is `0`, `Z` is `26`, `AA` is `27` and so on, this
    method is meant to translate the alphabetic “number” to an integer.

    Args:
        colName (str): XLS column representation, e.g. `A` or `AA`, ...

    Returns:
        int: index representation as integer
    """
    val = 0
    for ch in colName:  # base-26 decoding "+1"
        val = val * 26 + ord(ch) - ord0 + 1
    return val - 1


def int2xlsCol(colInt):
    """int index to XLS index

    According to `A` is `0`, `Z` is `26`, `AA` is `27` and so on, this
    function is meant to translate an integer to its alphabetic “number”
    representation.

    Args:
        colInt (int): index to be transferred to XLS column representation

    Returns:
        str: XLS column representation
    """
    chars = []
    while True:
        if len(chars) > 0:
            colInt = colInt - 1
        ch = colInt % 26
        chars.append(chr(ch + ord0))
        colInt = colInt // 26
        if not colInt:
            break
    return "".join(reversed(chars))


class CSV:
    """Helper class for CSV files, where named columns will be retrievable

    The class needs the data being given as list of lists. Each row (outer list)
    contains multiple cells (inner list).
    If the data is given JSON like – as a list of dictionaries where each row
    (dictionary) contains the column names as keys and the cell content as value
    – the second constructor-parameter has to be set `True`.

    Attributes:
        specs: specifications for CSV, `delimiter` defaulting to `;`, `emptyValue`
               defaulting to `None` and `linebreak` defaulting to `\\n`.
    """

    def __init__(self, data={}, kvDict=True):
        self.specs = {
            "delimiter": ";",
            "emptyValue": None,
            "linebreak": "\n",
        }
        self.data = {}
        self.rows = []
        self.rowCheck = False
        self.loadData(data, kvDict)

    def __getitem__(self, index):
        self.getRows()
        self.rowCheck = True
        return self.rows[index]

    def __len__(self):
        """count rows in CSV

        Returns:
            int: numbers of rows in CSV
        """
        return len(self.rows)

    def __str__(self):
        """convert CSV object into CSV string

        Returns:
            str: CSV string
        """
        self.refreshFromRows()

        combined = [[k] + v for k, v in self.data.items()]

        cols = pd.DataFrame(combined).T.values.tolist()
        rows = []

        for r in cols:
            i = 0

            for c in r:
                if c == self.specs["emptyValue"]:
                    r[i] = ""
                i += 1
            rows.append(
                '"{values}"'.format(
                    values='"{delim}"'.format(delim=self.specs["delimiter"]).join(
                        [
                            (
                                str(c).replace('"', '""')
                                if isinstance(c, str) or not math.isnan(c)
                                else ""
                            )
                            for c in r
                        ]
                    )
                )
            )

        return self.specs["linebreak"].join(rows) + self.specs["linebreak"]

    def readFile(self, filepath, delimiter=None):
        """read CSV file

        Method to load especially a CSV file stored in the filesystem.

        Args:
            filepath (str): path to CSV file
            delimiter (str): delimiter to resolve the CSV data (default: `None`)
        """
        self.readCSV(filepath, delimiter=delimiter, file=True)

    def readCSV(self, path_or_csvstring, delimiter=None, file=False):
        """read CSV from string or file

        [description]

        Args:
            path_or_csvstring (string): either the path to the file to resolve or CSV data itself
            delimiter (str): delimiter to resolve the CSV data (default: `None`)
            file (bool): is it a file to read? (default: `False`)
        """
        if delimiter == None:
            delimiter = self.specs["delimiter"]
        if file:
            data = pd.read_csv(path_or_csvstring, delimiter=delimiter, low_memory=False)
        else:
            data = pd.read_csv(
                io.StringIO(path_or_csvstring),
                delimiter=delimiter,
                low_memory=False,
            )
        colrows = {}
        for h in data.columns:
            colrows[h] = data.get(h).to_list()

        self.data = colrows
        self.getRows(force=True)

    def loadData(self, data, kvDict=False, emptyValue=None, skipRows=False):
        """load data

        Method to load the data of the CSV.
        If data is a list of dicts, the dicts should have the keys in
        common and `kvDict` shall be `True`.
        If the data is a dict of column-keys with a list of column-values
        where the index is the number of the row, `kvDict` shall be `False`.

        Args:
            data (mixed):       CSV data
            kvDict (bool):      is the data key-value structured? (default: `False`)
            emptyValue (mixed): value to override `self.specs['emptyValue']` to be
                                used for empty columns
            skipRows (bool):    should the data be transferred into rows? DON'T USE
                                UNLESS YOU KNOW WHAT YOU'RE DOING! (default: `False`)
        """
        self.rowCheck = False

        if emptyValue == None:
            emptyValue = self.specs["emptyValue"]

        if kvDict:
            self.data = {}
            for row in data:
                try:
                    existingRowCount = len(next(iter(self.data.values())))
                except:
                    existingRowCount = 0
                keys = row.keys()
                for k in keys:
                    if k not in self.data:
                        if existingRowCount > 0:
                            self.data[k] = [emptyValue] * existingRowCount
                        else:
                            self.data[k] = []
                for k in self.data.keys():
                    if k in row:
                        self.data[k].append(row[k])
                    else:
                        self.data[k].append(emptyValue)
        else:
            self.data = data

        if not skipRows:
            self.getRows(force=True)

    def remove(self, row):
        """remove row from CSV

        Args:
            row (dict): row object to remove from CSV
        """
        self.rowCheck = True
        self.rows.remove(row)

    def pop(self, index):
        """pop row from CSV – like from lists

        Args:
            index (int): index of row to pop

        Returns:
            dict: row removed / poped from CSV
        """
        self.rowCheck = True
        return self.rows.pop(index)

    def getCSV(self):
        """get CSV data

        Return CSV data

        Returns:
            dict: keys are column titles, assigned lists are column values per row
        """
        self.refreshFromRows()
        return self.data

    def setSpec(self, spec, val):
        """set specifications

        Method to set specifications for this CSV instance
        like the `delimiter` (default `;`) and the
        `linebreak` (default `\\n`)

        Args:
            spec(str): name of specification
            val(str): value for spec
        """
        self.specs[spec] = val

    def getRows(self, force=False, keepEmpty=True, emptyValue=None):
        """prepare rows variable

        Method to get row representation of CSV and prepare an additional variable
        `rows` that allows us to use `CSV` object as iterable.

        Args:
            force (bool): Shall the row representation be renewed by force? (default: `False`)

        Returns:
            list: list of rows in CSV
        """
        if self.rows == []:
            force = True

        if force:
            self.rows = self.keyValueRows(keepEmpty=keepEmpty, emptyValue=emptyValue)

        return self.rows

    def combine(self, csv):
        """merge another CSV object

        Args:
            csv (CSV): CSV object to merge

        Raises:
            TypeError: raises when non-CSV object is given
        """
        if not isinstance(csv, type(self)):
            raise TypeError("Only CSV objects are permitted!")
        else:
            self.rows = self.rows + csv.rows
            self.rowCheck = True
            self.refreshFromRows()

    def refreshFromRows(self):
        """reload the CSV from rows

        When one iterates over the rows of a CSV class and changes values, e.g.
        adding new columns or manipulate values, the CSV object needs to be
        rebuilt from the rows ... that's what this method is doing.
        """
        if self.rowCheck:
            self.loadData(data=self.rows, kvDict=True, skipRows=True)
            self.rowCheck = False

    def dropEmptyColumns(self, ensureKeyEquality=True, emptyValue=None):
        """drop empty columns

        sometimes it's usefull to clean up a CSV file and drop empty columns,
        e.g. if the CSV was created by an export
        """
        self.getRows(force=True, keepEmpty=False)

        if emptyValue == None:
            emptyValue = self.specs["emptyValue"]

        if ensureKeyEquality:
            keys = []
            for r in self.rows:
                keys = list(set(keys) | set(r.keys()))
            for i in range(0, len(self.rows)):
                for k in keys:
                    r = self.rows[i]
                    if k not in r:
                        r[k] = emptyValue

        self.rowCheck = True
        self.refreshFromRows()

    def keyValueRows(self, keepEmpty=False, emptyValue=None):
        """data to list of rows

        Method to get row representation of CSV.

        Args:
            keepEmpty (bool): if set to True, empty values are kept in row representation (default: `False`)
            emptyValue (mixed): value that should be used for kept empty values (default: `None`)

        Returns:
            list: list of rows in CSV
        """
        if emptyValue == None:
            emptyValue = self.specs["emptyValue"]

        self.refreshFromRows()

        kvrows = []
        keys = list(self.data.keys())
        if len(keys) > 0:
            count = len(self.data[keys[0]])
            i = 0
            while i < count:
                row = {}
                for key in keys:
                    value = self.data[key][i]
                    if (
                        value == ""
                        or (type(value) == float and math.isnan(value))
                        or value == emptyValue
                    ):
                        if keepEmpty:
                            row[key] = emptyValue
                    else:
                        row[key] = value
                kvrows.append(row)
                i += 1
        return kvrows

    def writeFile(self, filepath, delimiter=None, linebreak=None, backupExisting=False):
        """write CSV file

        Method to write out data of current object to a CSV file.

        Args:
            filepath (str): path to destination file
            delimiter (str): delimiter to be used for column separation – changes specs! (default: `None`)
            linebreak (str): linebreak to be used in CSV representation – changes specs! (default: `None`)
            backupExisting (bool): if `True` and file at filepath already exists, it will be renamed
                                   (timestamp appended) and the new file will be written out in place (default: `False`)
        """
        if delimiter != None:
            self.setSpec("delimiter", delimiter)

        if linebreak != None:
            self.setSpec("linebreak", linebreak)

        csv = str(self)

        if backupExisting and os.path.isfile(filepath):
            mtime = os.path.getmtime(filepath)
            ts = datetime.fromtimestamp(mtime).strftime("_%Y%m%d-%H%M%S")
            path, file = os.path.split(filepath)
            file = list(file.rpartition("."))
            if file[0] == "":
                file.append(ts)
            else:
                file.insert(1, ts)

            buFilepath = os.path.join(path, "".join(file))
            os.rename(filepath, buFilepath)

        with open(filepath, "w") as csv_file:
            csv_file.write(csv)

    def renameColumn(self, srcCol, dstCol):
        """change column name

        Args:
            srcCol (str): current name of column to rename
            dstCol (str): wanted name of column
        """
        self.refreshFromRows()
        if srcCol == dstCol:
            pass
        elif srcCol not in self.data.keys():
            raise Exception(
                "Key {src} not in column names ... not renaming anything. Those are available: {keyList}".format(
                    src=srcCol, keyList=", ".join(self.data.keys())
                )
            )
        elif dstCol in self.data.keys():
            raise Exception(
                "Key {dst} already exists, not renaming column {src}.".format(
                    dst=dstCol, src=srcCol
                )
            )
        else:
            key_key = {k: k if k != srcCol else dstCol for k in self.data.keys()}
            newData = {key_key[k]: v for k, v in self.data.items()}
            self.data = newData
            self.getRows(force=True)

    def dropColumn(self, colname):
        """change column name

        Args:
            srcCol (str): current name of column to rename
            dstCol (str): wanted name of column
        """
        self.refreshFromRows()
        if colname not in self.data.keys():
            raise Exception(
                "Key {src} not in column names ... not removing anything. Those are available: {keyList}".format(
                    src=colname, keyList=", ".join(self.data.keys())
                )
            )
        else:
            self.data.pop(colname)
            self.getRows(force=True)
