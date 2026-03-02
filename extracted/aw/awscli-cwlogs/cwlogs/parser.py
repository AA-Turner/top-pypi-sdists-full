#  Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  Licensed under the Amazon Software License (the "License").
#  You may not use this file except in compliance with the License.
#  A copy of the License is located at
#
#  http://aws.amazon.com/asl/
#
#  or in the "license" file accompanying this file. This file is distributed
#  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
#  express or implied. See the License for the specific language governing
#  permissions and limitations under the License.

import re
from datetime import datetime, date
from dateutil.tz import tzoffset, tzlocal, tzutc
import logging
import _strptime

logger = logging.getLogger(__name__)


class DateTimeParser(object):
    """
    This parser passes datetime from a string according to the given
    datetime format. The string might contain datatime and extra characters.
    """

    def __init__(self, datetime_format, time_zone=None):
        """
        Create a parser object based on datetime_format. Throw an exception
        if datetime_format is invalid.

        This parser uses python ``datetime.strptime()`` with some extensions,
        so any format codes supported by ``strptime()`` can be used here.
        Time zone offset (%z) is also supported though it's not supported
        until python 3.2.
        ``time_zone`` is only used if time zone offset is not specified in
        ``datetime_format``.
        """
        self._format = datetime_format
        self._time_zone = time_zone
        if datetime_format is not None:
            # %z is not supported by py2, so construct the pattern
            # manually, use negative lookbehind to ignore %%z
            self._has_tzoffset = re.search('(?<!%)%z', datetime_format)
            if self._has_tzoffset:
                # Remove %z from format
                self._format = self._format.replace('%z', '')
                datetime_format = datetime_format.replace('%z', '%%z')
            pattern = _strptime.TimeRE().pattern(datetime_format)
            if self._has_tzoffset:
                pattern = pattern.replace('%z',
                                          '(?P<z>[+-]\\d\\d[0-5]\\d)')
            # TimeRE expands format to lower case, so ignore case
            self.dt_re = re.compile('(?P<dt>%s)' % pattern, re.IGNORECASE)
            # The format might not include year information
            self._has_year = re.search('(?<!%)%[yY]', datetime_format)
        self.last_dt_str = None
        self.last_dt = None

    def parse(self, message):
        """
        Parse datetime from ``message`` based on ``datetime_format``.

        If %z is not provided, the returned datetime has no timezone info.
        If %y or %Y is not provided, year is inferred based on current month
        and parsed month, current year is used if parsed month is earlier than
        or same as current month, otherwise last year is used.
        """
        if self._format is None:
            return None
        m = self.dt_re.search(message)
        if m:
            dt_str = m.group('dt')
            dt = self._parse(dt_str)
            if dt:
                return dt
            offset = 0
            # Check if timezone offset is matched
            if self._has_tzoffset and m.group('z'):
                z = m.group('z')
                # Remove offset from datetime str
                dt_str = (message[m.start('dt'):m.start('z')] +
                          dt_str[m.end('z'):m.end('dt')])
                # Convert [+-]HHMM offset to seconds
                offset = int(z[1:3]) * 3600 + int(z[3:5]) * 60
                if z.startswith('-'):
                    offset = -offset
            dt = datetime.strptime(dt_str, self._format)
            # Use local timezone by default
            tz = tzlocal()
            if self._has_tzoffset:
                tz = tzoffset(name=None, offset=offset)
            elif self._time_zone:
                if self._time_zone == 'UTC':
                    tz = tzutc()
                elif self._time_zone == 'LOCAL':
                    tz = tzlocal()
            dt = dt.replace(tzinfo=tz)
            # If year is missing, infer it based on month. This is to
            # address boundary issue where a message is generated in last
            # year but processed in current year.
            if not self._has_year:
                today = date.today()
                if dt.month <= today.month:
                    dt = dt.replace(year=today.year)
                else:
                    dt = dt.replace(year=today.year - 1)
            (self.last_dt_str, self.last_dt) = (dt_str, dt)
            return dt
        else:
            return None

    def _parse(self, dt_str):
        if dt_str == self.last_dt_str:
            return self.last_dt
        else:
            return None
