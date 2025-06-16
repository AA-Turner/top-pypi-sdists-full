# -*- coding: utf-8 -*-
###########################################################
#  Copyright (C) Joel B. Mohler <joel@kiwistrawberry.us>
#
#  Distributed under the terms of The MIT License
###########################################################
"""
Date and string matching functions.
"""

import datetime
import re
from .strings import fuzzy_match, default_match

def str_to_month(s):
    """
    >>> str_to_month("ja")
    1
    >>> str_to_month("mar")
    3
    """
    months = ["january","february","march","april","may","june","july","august","september","october","november","december"]
    indexed = [(months[i], i) for i in range(len(months))]
    return fuzzy_match(indexed, s, match_fucn=lambda x, y: default_match(x[0], y))[1]+1

def locale_format():
    has_locale = False
    try:
        from locale import nl_langinfo, D_FMT
        has_locale = True
    except ImportError as e:
        pass

    if has_locale:
        # dfmt is a string like "%a %b %e %Y"
        # %a   locale's abbreviated weekday name (e.g., Sun)
        # %b   locale's abbreviated month name (e.g., Jan)
        # %d   day of month (e.g., 01)
        # %D   date; same as %m/%d/%y
        # %e   day of month, space padded; same as %_d
        # %F   full date; same as %Y-%m-%d
        # %m   month (01..12)
        # %y   last two digits of year (00..99)
        # %Y   year
        dfmt = nl_langinfo(D_FMT)
    else:
        # nl_langinfo & friends is not available everywhere
        dfmt = "%m/%d/%Y" # US default

        # this is a hack!
        d = datetime.datetime(2022, 7, 9)
        x = d.strftime("%x")
        dfmt = x \
                .replace("2022", "%Y") \
                .replace("22", "%y") \
                .replace("09", "%d") \
                .replace("07", "%m") \
                .replace("9", "%d") \
                .replace("7", "%m")
    return dfmt

class DateParser:
    def __init__(self,today=None, dfmt=None):
        if today is None:
            today = datetime.date.today()
        self.today=today

        if dfmt is None:
            dfmt = locale_format()
        self.dfmt = dfmt

    def str_to_date_int(self,s):
        """
        :param s:  an input string to parse
        :return: a 3-tuple of numeric 4 digit year, month index 1-12 and day
            1-31

        This function is locale aware in that it reads the nl_langinfo(D_FMT)
        output to determine whether the locale has month first or day first
        semantics.  If that effort fails, we assume day first (because the
        author believes it is more logical to list the date segments in
        monotonic order).
        
        >>> DateParser().str_to_date_int("feb 2 2011")
        (2011, 2, 2)
        >>> DateParser().str_to_date_int("4 may 2011")
        (2011, 5, 4)
        >>> DateParser().str_to_date_int("2010.3.11")
        (2010, 3, 11)
        >>> DateParser().str_to_date_int("12 1 2020")
        (2020, 12, 1)

        >>> # Can parse some things for either locale
        >>> DateParser().str_to_date_int('feb 29')
        (None, 2, 29)
        >>> DateParser().str_to_date_int('29 feb')
        (None, 2, 29)
        >>> DateParser().str_to_date_int('feb 27 2015')
        (2015, 2, 27)
        >>> DateParser().str_to_date_int('feb 27 15')
        (2015, 2, 27)
        >>> DateParser().str_to_date_int('27 feb 2015')
        (2015, 2, 27)

        >>> # German date format
        >>> parser = DateParser(datetime.date(2012, 4, 28), dfmt='%d.%m.%Y')
        >>> parser.str_to_date_int('2 8')
        (None, 8, 2)
        >>> parser.str_to_date_int('4.3.2015')
        (2015, 3, 4)
        >>> parser.str_to_date_int('4.3.12')
        (2012, 3, 4)

        >>> # American date format
        >>> DateParser(datetime.date(2012, 4, 28), dfmt='%m/%d/%Y').str_to_date_int('2 8')
        (None, 2, 8)

        >>> DateParser().str_to_date_int("total junk")
        Traceback (most recent call last):
        ...
        NotImplementedError: The input date 'total junk' is unrecognized.
        """
        try:
            month_first = self.dfmt.index('m') < self.dfmt.index('d')
        except ValueError as e:
            month_first = False

        # month day year (alpha month is locale unambiguous)
        m = re.match("([a-zA-Z]+) ([0-9]{1,2})(,|) ([0-9]+)",s)
        if m:
            y = int(m.group(4))
            if y < 100:
                y += 2000
            return y,str_to_month(m.group(1)),int(m.group(2))

        # day month year (alpha month is locale unambiguous)
        m = re.match("([0-9]+) ([a-zA-Z]+)(,|) ([0-9]+)",s)
        if m:
            y = int(m.group(4))
            if y < 100:
                y += 2000
            return y,str_to_month(m.group(2)),int(m.group(1))

        # month year
        m = re.match("([a-zA-Z]+) ([0-9]{4})",s)
        if m:
            # this is a little curious, but I think it makes sense to a human
            # If I enter "March 2011", I think I mean the 1st of march ... maybe
            return int(m.group(2)),str_to_month(m.group(1)),1

        # month day (alpha month is locale unambiguous)
        m = re.match("([a-zA-Z]+) ([0-9]{1,2})",s)
        if m:
            return None,str_to_month(m.group(1)),int(m.group(2))

        # day month (alpha month is locale unambiguous)
        m = re.match("([0-9]{1,2}) ([a-zA-Z]+)",s)
        if m:
            return None,str_to_month(m.group(2)),int(m.group(1))

        # yyyy-mm-dd
        m = re.match("([0-9]{4})[-./ ]([0-9]{1,2})[-./ ]([0-9]{1,2})",s)
        if m:
            return int(m.group(1)),int(m.group(2)),int(m.group(3))

        if month_first:
            # mm-dd-yyyy
            m = re.match("([0-9]{1,2})[-./ ]([0-9]{1,2})[-./ ]([0-9]{4})",s)
            if m:
                return int(m.group(3)),int(m.group(1)),int(m.group(2))
            # mm-dd-yy
            m = re.match("([0-9]{1,2})[-./ ]([0-9]{1,2})[-./ ]([0-9]{2})",s)
            if m:
                return int(m.group(3))+2000,int(m.group(1)),int(m.group(2))
            # mm-dd
            m = re.match("([0-9]{1,2})[-./ ]+([0-9]{1,2})",s)
            if m:
                return None,int(m.group(1)),int(m.group(2))
        else: # European formats
            # dd-mm-yyyy
            m = re.match("([0-9]{1,2})[-./ ]([0-9]{1,2})[-./ ]([0-9]{4})",s)
            if m: 
                return int(m.group(3)),int(m.group(2)),int(m.group(1))
            # dd-mm-yy
            m = re.match("([0-9]{1,2})[-./ ]([0-9]{1,2})[-./ ]([0-9]{2})",s)
            if m:
                return int(m.group(3))+2000,int(m.group(2)),int(m.group(1))
            # dd-mm
            m = re.match("([0-9]{1,2})[-./ ]([0-9]{1,2})",s)
            if m:
                return None,int(m.group(2)),int(m.group(1))
         
        m = re.match(r"(-|\+)([0-9]+)",s)
        if m:
            if m.group(1)=='+':
                d = self.today + datetime.timedelta(int(m.group(2)))
            elif m.group(1)=='-':
                d = self.today - datetime.timedelta(int(m.group(2)))
            return d.year,d.month,d.day
        raise NotImplementedError("The input date '%s' is unrecognized." % (s,))

    def str_to_date(self,s):
        """
        Parses input `s` into a date.  The accepted date formats are quite flexible.
        
        jan 12, 2003
        jan 5
        2004-3-5
        +34 -- 34 days in the future (relative to todays date)
        -4 -- 4 days in the past (relative to todays date)

        >>> DateParser(datetime.date(2011,4,15)).str_to_date("may 1")
        datetime.date(2011, 5, 1)
        >>> DateParser(datetime.date(2012,4,15), dfmt='%d.%m.%Y').str_to_date("9 1")
        datetime.date(2012, 1, 9)
        """
        year,month,day = self.str_to_date_int(s)
        if year is None:
            year = self.today.year
        if month is None:
            month = self.today.month
        if day is None:
            day = self.today.day
        return datetime.date(year,month,day)

    def parse_date(self,d):
        """
        >>> DateParser(datetime.date(2011,1,1)).parse_date("+10")
        datetime.date(2011, 1, 11)
        """
        if d is None or isinstance(d,datetime.date):
            return d
        else:
            return self.str_to_date(d)

def parse_date(d):
    """
    :param d: d can be a datetime.date, None or anything with string semantics.
    
    This function only pre-checks the type for a date type or None before
    passing the lone parameter on to str_to_date.
    
    Certain import formats assume a current date to fill in missing pieces of
    the date or as a baseline for relative dates.  To provide your own baseline
    date, use the DateParser class directly.
    
    Examples:
    >>> parse_date('jan 9 1979') # my birthday
    datetime.date(1979, 1, 9)
    >>> parse_date('9 jan 1979') # my birthday
    datetime.date(1979, 1, 9)
    >>> parse_date('2010-06-17') # my youngest son's birthday
    datetime.date(2010, 6, 17)
    >>> parse_date('f 29, 2012')  # february is the unique month starting with 'f'
    datetime.date(2012, 2, 29)
    >>> parse_date('mar 2015')  # with no date, but a full month & year, assume the first of the month
    datetime.date(2015, 3, 1)
    >>> parse_date('+35')-datetime.date.today()
    datetime.timedelta(35)
    >>> parse_date('-35')-datetime.date.today()
    datetime.timedelta(-35)
    >>> parse_date(None)  # None is simply returned unchanged

    >>> # We'd expect to be able to parse any locale date
    >>> x = parse_date( 'jan 13 2012' )
    >>> x
    datetime.date(2012, 1, 13)
    >>> parse_date(x.strftime("%x"))==x
    True
    """
    return DateParser().parse_date(d)
