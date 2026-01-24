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
# Name:        time
# Purpose:
#
# Author:      Luzzi Valerio
#
# Created:     15/02/2013
# -------------------------------------------------------------------------------

import datetime
import re
import time
import xlrd
from .strings import *


def now():
    """
    now - shortcut for datetime.datetime.now
    """
    return datetime.datetime.now()

def ctod(text=""):
    """
    ctod - convert a string to a datetime
    """
    if not text:
        return datetime.datetime.now()

    elif isinstance(text, (datetime.date)):
        return text

    elif isinstance(text, (datetime.datetime, datetime.time)):
        return text

    elif isinstance(text, time.struct_time):
        return ctod(list(text)[:6])

    elif isinstance(text, (xlrd.sheet.Cell,)) and text.ctype == xlrd.XL_CELL_DATE:
        try:
            text = xlrd.xldate_as_tuple(text.value, 0)
            return ctod(text)
        except Exception as ex:
            return None

    elif isinstance(text, (xlrd.sheet.Cell,)) and text.ctype == xlrd.XL_CELL_TEXT:
        return ctod(text.value)

    elif isstring(text):

        text = re.sub(r'[/:\-\\.]', ' ', text)

        # #text= 20131113120000
        if len(text) >= 8 and text.find(" ") < 0:
            text = (text + ("0" * 14))[:14]
            frmt = "%Y%m%d%H%M%S"
            return datetime.datetime.strptime(text, frmt)

        text = text.split(" ")
        text = [int(item) for item in text if len(item) > 0]
        return ctod(text)

    elif isinstance(text, (list, tuple)):
        text = list(text)
        # Se il terzo numero e' un YYYY allora il formato e' dd-mm-YYYY
        # Se il primo e il terzo numero sono di due cifre allora il formato e' dd-mm-YY
        # Quindi effettuo uno swap di anno con giorno
        if len(text) > 2:
            if len("%s" % text[2]) == 4:
                tmp = text[0]
                text[0] = text[2]
                text[2] = tmp
            elif (len("%s" % text[0]) <= 2 and len("%s" % text[2]) <= 2):
                tmp = text[0]
                text[0] = 2000 + text[2]
                text[2] = tmp

        # Correggo le date nulle
        if len(text) > 2:
            text[0] = text[0] if text[0] > 0 else 1900
            text[1] = text[1] if (text[1] > 0 and text[1] <= 12) else 1
            text[2] = text[2] if (text[2] > 0 and text[2] <= 31) else 1
            return datetime.datetime(*text)

    return None


def strftime(frmt="%Y-%m-%d", data=None):
    """
    strftime
    """
    try:
        if not data:
            data = datetime.datetime.now()
        if isstring(data) or isinstance(data, (str, tuple, list, xlrd.sheet.Cell)):
            data = ctod(data)
            return datetime.datetime.strftime(data, frmt) if data else ""
        if isinstance(data, (datetime.date, datetime.datetime)):
            return datetime.datetime.strftime(data, frmt) if data else ""
        if isinstance(data, time.struct_time):
            return time.strftime(frmt, data)
        return ""
    except Exception as ex:
        print(ex)
        pass


def dtos(data=None, frmt="%Y-%m-%d"):
    """
    dtos
    """
    return strftime(frmt, data)


def datediff(dateB, dateA, interval):
    """
    datediff
    """
    dateA = ctod(dateA)
    dateB = ctod(dateB)
    interval = ("%s" % interval)
    if interval == "h":
        delta = (dateB - dateA).total_seconds() / 3600
    elif interval == "s":
        delta = (dateB - dateA).total_seconds()
    else:
        delta = (dateB - dateA).days
    return delta


def firstdayofmonth(date):
    """
    firstdayofmonth
    """
    date = date + "01" if isstring(date) and len(date) == 6 else date
    date = strftime("%Y-%m-01", date)
    return ctod(date)


def lastdayofmonth(date):
    """
    lastdayofmonth
    """
    date = date + "01" if isstring(date) and len(date) == 6 else date
    date = ctod(date)
    for d in (28, 29, 30, 31):
        date1 = datetime.date(date.year, date.month, d)
        if (date1 + datetime.timedelta(days=1)).month != date.month:
            return strftime("%Y-%m-%d", date1)
    return ""


def days_of_month(date):
    """
    days_of_month
    """
    return int(strftime("%d", lastdayofmonth(date)))


def period_of(date):
    """
    period_of
    """
    date = date + "01" if isstring(date) and len(date) == 6 else date
    return strftime('%Y%m', date)


def next_period(date):
    """
    next_period
    """
    period = "%s" % (date) if isstring(date) and len(date) == 6 else strftime("%Y%m", date)
    YYYY, mm = int(period[:4]), int(period[4:6])
    YYYY = YYYY if mm < 12 else YYYY + 1
    mm = mm + 1 if mm < 12 else 1
    return "%04d%02d" % (YYYY, mm)


def prev_period(date):
    """
    prev_period
    """
    period = "%s" % (date) if isstring(date) and len(date) == 6 else strftime("%Y%m", date)
    YYYY, mm = int(period[:4]), int(period[4:6])
    YYYY = YYYY if mm > 1 else YYYY - 1
    mm = mm - 1 if mm > 1 else 12
    return "%04d%02d" % (YYYY, mm)


def minus_one_month(date):
    """
    minus_one_month
    """
    n = days_of_month(prev_period(date))
    return ctod(date) - datetime.timedelta(n)


# -------------------------------------------------------------------------------
#   test
# -------------------------------------------------------------------------------
def test():
    date1 = ctod("2017-04-01")
    # print(lastdayofmonth(date1))


if __name__ == '__main__':
    test()
