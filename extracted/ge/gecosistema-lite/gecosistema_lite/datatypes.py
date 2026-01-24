# -------------------------------------------------------------------------------
# Licence:
# Copyright (c) 2012-2017 Luzzi Valerio 
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
#
# Name:        datatypes.py
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     27/07/2017
# -------------------------------------------------------------------------------
import datetime
import numpy as np
import xlrd, xlwt
import json

from .stime import strftime, ctod
from .strings import *


def parseInt(text):
    """
    parseInt
    """
    if isstring(text):
        PATTERN1 = """^[-+]?\d+$"""
        PATTERN = """(?P<target>(%s))""" % (PATTERN1)
        text = text.strip()
        g = re.match(PATTERN, text, re.IGNORECASE | re.MULTILINE)
        if g:
            res = g.groupdict()["target"]
            return int(res)
    return None


def parseFloat(text):
    """
    parseFloat
    """
    if isstring(text):
        PATTERN1 = """^[-+]?(?:(\d+|\d+\.\d*|\d*\.\d+)(e[-+]?\d+)?)$"""
        PATTERN = """(?P<target>(%s))""" % (PATTERN1)
        text = text.strip()
        g = re.match(PATTERN, text, re.IGNORECASE | re.MULTILINE)
        if g:
            res = g.groupdict()["target"]
            return float(res)
    return None


def parseDate(text):
    """
    parseDate
    """
    if isstring(text):
        PATTERN1 = """^\d{1,2}-\d{1,2}-(\d{4,4}|\d{2,2})$"""  # 1-1-2017
        PATTERN2 = """^\d{1,2}(\/)\d{1,2}(\/)(\d{4,4}|\d{2,2})$"""  # 1/1/2017
        PATTERN3 = """^\d{4,4}-\d{1,2}-\d{1,2}$"""  # 2017-01-01
        PATTERN = """(?P<target>(%s)|(%s)|(%s))""" % (PATTERN1, PATTERN2, PATTERN3)
        text = text.strip()
        g = re.match(PATTERN, text, re.IGNORECASE | re.MULTILINE)
        if g:
            res = g.groupdict()["target"]
            return strftime("%Y-%m-%d", res)
    return None


def parseDatetime(text):
    """
    parseDatetime
    """
    if isstring(text):
        PATTERN1 = """^\d{1,2}-\d{1,2}-(\d{4,4}|\d{2,2})(\s\d{1,2}(:|\.)\d{2,2}((:|\.)\d\d)?)?$"""
        PATTERN2 = """^\d{1,2}(\/)\d{1,2}(\/)(\d{4,4}|\d{2,2})(\s\d{1,2}(:|\.)\d{2,2}((:|\.)\d\d)?)?$"""
        PATTERN3 = """^\d{4,4}-\d{1,2}-\d{1,2}(\s\d{1,2}(:|\.)\d{2,2}((:|\.)\d\d)?)?$"""
        PATTERN = """(?P<target>(%s)|(%s)|(%s))""" % (PATTERN1, PATTERN2, PATTERN3)
        text = text.strip()
        g = re.match(PATTERN, text, re.IGNORECASE | re.MULTILINE)
        if g:
            res = g.groupdict()["target"]
            return strftime("%Y-%m-%d %H:%M:%S", res)
    return None


def parseBool(text):
    """
    parseBool
    """
    if isstring(text):
        text = text.lower()
        if text in ("true", "1", "on"):
            return True
        return False

    return True if text else False


def parseColor(text, out="hex"):
    """
    parseColor - TODO
    """
    if isstring(text):

        if text in xlwt.Style.colour_map:
            return "%06x" % xlwt.Style.colour_map[text]

        elif len(listify(text.replace(r'[\s;]', ","), ",")) == 3:
            rgb = listify(text.replace(r'[\s;]', ","), ",")
            return "#%02x%02x%02x" % tuple(val(rgb))

        elif len(listify(text.replace(r'[\s;]', ","), ",")) == 4:
            rgba = listify(text.replace(r'[\s;]', ","), ",")
            (r, g, b, a) = val(rgba)
            a = int(a * 255) if a <= 1.0 else a
            return "#%02x%02x%02x%02x" % (r, g, b, a)


    return "000000"


def parseJSON(text):
    """
    parseJSON - load json txt into obj
    """
    if isinstance(text, (tuple, list, dict)):
        return text
    if isstring(text):
        return json.loads(text)
    return None

def isquery(text):
    pattern = r'^\s*((SELECT|PRAGMA|INSERT|DELETE|REPLACE|UPDATE|CREATE).*)'
    res = re.match(pattern, text, re.IGNORECASE)
    return True if res else False


def isarray(value):
    return isinstance(value, (tuple, list, np.ndarray))


def isfloat(text):
    return not parseDate(text) is None


def isdate(text):
    if isinstance(text, (datetime.date,)):
        return True
    return not parseDate(text) is None


def isdatetime(text):
    if isinstance(text, (datetime.datetime,)):
        return True
    return not parseDatetime(text) is None


def parseValue(value, nodata=("", "Na", "NaN", "-", "--", "N/A")):
    """
    parseValue - parse values from string
    """
    if value is None:
        return None
    if isstring(value) and value in nodata:
        return None
    elif isstring(value) and re.match(r'^(GEOMFROM|POINT).*', value, re.I | re.M):
        return value
    elif isdate(value):
        return strftime("%Y-%m-%d", value)
    elif isdatetime(value):
        return strftime("%Y-%m-%d %H:%M:%S", value)
    elif isfloat(value):
        return value
    elif isstring(value):
        return value
    elif isarray(value):
        return [parseValue(item) for item in value]
    return None


SQLTYPES = {
    9999: "",
    9998: "EMPTY",
    1: "TEXT",
    2: "DATETIME",
    3: "DATE",
    4: "TIME",
    5: "FLOAT",
    6: "INTEGER",
    7: "GEOMETRY",
    "": 9999,
    "EMPTY": 9998,
    "TEXT": 1,
    "DATETIME": 2,
    "DATE": 3,
    "TIME": 4,
    "FLOAT": 5,
    "INTEGER": 6,
    "GEOMETRY": 7
}

XLRDTYPES = {
    xlrd.XL_CELL_EMPTY: 9999,
    xlrd.XL_CELL_BLANK: 9999,
    xlrd.XL_CELL_TEXT: 1,
    xlrd.XL_CELL_DATE: 2,
    xlrd.XL_CELL_NUMBER: 5,
    xlrd.XL_CELL_BOOLEAN: 6
}


def sqltype(cvalue, ctype=xlrd.XL_CELL_TEXT, nodata=("", "Na", "NaN", "-", "--", "N/A")):
    """
    Type symbol	Type number	Python value
    XL_CELL_EMPTY	0	empty string u''
    XL_CELL_TEXT	1	a Unicode string
    XL_CELL_NUMBER	2	float
    XL_CELL_DATE	3	float
    XL_CELL_BOOLEAN	4	int; 1 means TRUE, 0 means FALSE
    XL_CELL_ERROR	5	int representing internal Excel codes; for a text representation, refer to the supplied dictionary error_text_from_code
    XL_CELL_BLANK	6	empty string u''. Note: this type will appear only when open_workbook(..., formatting_info=True) is used.
    """
    if isarray(cvalue):
        if not isarray(ctype):
            ctype = [ctype] * len(cvalue)
        return [sqltype(cv, ct, nodata) for cv, ct in zip(cvalue, ctype)]
    if isinstance(cvalue, xlrd.sheet.Cell):
        return sqltype(cvalue.value, cvalue.ctype, nodata)
    if ctype == xlrd.XL_CELL_EMPTY:
        return 'EMPTY'
    elif ctype == xlrd.XL_CELL_TEXT and cvalue in nodata:
        return ''
    elif ctype == xlrd.XL_CELL_TEXT and isdate(cvalue):
        return 'DATE'
    elif ctype == xlrd.XL_CELL_TEXT and isdatetime(cvalue):
        return 'DATETIME'
    elif ctype == xlrd.XL_CELL_TEXT and parseInt(cvalue):
        return 'INTEGER'
    elif ctype == xlrd.XL_CELL_TEXT and parseFloat(cvalue) != None:
        return 'FLOAT'
    elif ctype == xlrd.XL_CELL_TEXT:
        return 'TEXT'
    elif ctype == xlrd.XL_CELL_NUMBER and int(cvalue) == cvalue:
        return 'INTEGER'
    elif ctype == xlrd.XL_CELL_NUMBER:
        return 'FLOAT'
    elif ctype == xlrd.XL_CELL_DATE:
        return 'DATETIME'
    elif ctype == xlrd.XL_CELL_BOOLEAN:
        return 'INTEGER'
    elif ctype == xlrd.XL_CELL_ERROR:
        return ''
    elif ctype == xlrd.XL_CELL_BLANK:
        return ''
    else:
        return 'TEXT'


def xlsvalue(cell, nodata=("", "Na", "NaN", "-", "--", "N/A")):
    """
    Type symbol	Type number	Python value
    XL_CELL_EMPTY	0	empty string u''
    XL_CELL_TEXT	1	a Unicode string
    XL_CELL_NUMBER	2	float
    XL_CELL_DATE	3	float
    XL_CELL_BOOLEAN	4	int; 1 means TRUE, 0 means FALSE
    XL_CELL_ERROR	5	int representing internal Excel codes; for a text representation, refer to the supplied dictionary error_text_from_code
    XL_CELL_BLANK	6	empty string u''. Note: this type will appear only when open_workbook(..., formatting_info=True) is used.
    """
    if isarray(cell):
        return [xlsvalue(item, nodata) for item in cell]

    cvalue, ctype = cell.value, cell.ctype
    if ctype == xlrd.XL_CELL_EMPTY:
        return None
    elif ctype == xlrd.XL_CELL_TEXT and cvalue in nodata:
        return None
    elif ctype == xlrd.XL_CELL_TEXT and isdate(cvalue.strip()):
        return parseDate(cvalue)
    elif ctype == xlrd.XL_CELL_TEXT and isdatetime(cvalue.strip()):
        return parseDatetime(cvalue)
    elif ctype == xlrd.XL_CELL_TEXT and parseInt(cvalue):
        return parseInt(cvalue)
    elif ctype == xlrd.XL_CELL_TEXT and parseFloat(cvalue.strip()) != None:
        return parseFloat(cvalue)
    elif ctype == xlrd.XL_CELL_TEXT:
        return cvalue
    elif ctype == xlrd.XL_CELL_NUMBER:
        return cvalue
    elif ctype == xlrd.XL_CELL_DATE:
        return ctod(cell)
    elif ctype == xlrd.XL_CELL_BOOLEAN:
        return cvalue
    elif ctype == xlrd.XL_CELL_ERROR:
        return None
    elif ctype == xlrd.XL_CELL_BLANK:
        return None
    else:
        return None


def main():
    pass

if __name__ == "__main__":
    main()
