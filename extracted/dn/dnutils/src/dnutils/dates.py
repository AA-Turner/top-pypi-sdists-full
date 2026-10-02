import calendar
import datetime
import re
import sys
import time
from io import StringIO

from dnutils import ifnone
from dnutils.math import sign
from dnutils.tools import ifstr, mapstr


def datetimestr(d):
    '''Returns a human readable string of the datetime ``d``'''
    return d.strftime('%Y-%m-%d %H:%M:%S')


def unixtime(dt):
    '''Convert a datetime object into a unix timestamp'''
    return time.mktime(dt.timetuple())


def from_unixtime(ts):
    return datetime.datetime.utcfromtimestamp(ts)


def date2datetime(date):
    '''Convert a ``datetime.date`` object into a ``datetime.datetime`` object that represents the same date
    at 00:00 AM.'''
    if isinstance(date, datetime.datetime):
        return date
    return datetime.datetime(year=date.year, month=date.month, day=date.day,
                             hour=0, minute=0, second=0, microsecond=0)


def parsedate(datestr):
    return datetime.datetime.strptime(datestr, '%Y-%m-%d' if '-' in datestr else '%d.%m.%Y').date()


def strdate(d, separator='-'):
    return datetime.datetime.strftime(d, '%Y-%m-%d' if separator == '-' else '%d.%m.%Y')


tdeltapatternstr = r'^(?P<plusminus>\+|-)?((?P<days>\d+)d)?((?P<hours>\d+)h)?((?P<minutes>\d+)min)?((?P<seconds>\d+)s)?((?P<milliseconds>\d+)ms)?((?P<microseconds>\d+)mus)?$'
tdeltamachine = re.compile(tdeltapatternstr)


def parse_timedelta(s):
    '''
    Parse the given string into a Python ``datetime.timedelta`` object.

    Example: "-1d4h5min13s" represents the delta -1 day, 4 hours, 5 minutes and 13 seconds.
             If no sign is given, plus is assumed.

    :param s:
    :return:
    '''
    match = tdeltamachine.match(s)
    pm = ifnone(match.group('plusminus'), '+')
    tdelta = datetime.timedelta(days=ifnone(match.group('days'), 0, int),
                                hours=ifnone(match.group('hours'), 0, int),
                                minutes=ifnone(match.group('minutes'), 0, int),
                                seconds=ifnone(match.group('seconds'), 0, int),
                                milliseconds=ifnone(match.group('milliseconds'), 0, int),
                                microseconds=ifnone(match.group('microseconds'), 0, int))
    return {'+': tdelta, '-': -tdelta}[pm]


def next_weekday(d, weekday):
    '''
    Get the date of the next given weekday, specified by an integer, after date ``d``. Monday is ``0``.
    :param d:
    :param weekday:
    :return:
    '''
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)


class SimpleSchedule:
    '''
    Simple schedule parsing and checking functionality.

    A schedule consists of a set of weekdays/time interval specifications. A given point in time is considered
    in schedule, when it is in at least one of the intervals specifided, and off schedule otherwise.

    A common use of such scheduler specifications is in alarm clocks. Example:

        "Mon-Fri:19:00-8:00,Sat:10:00-12:00"
    '''

    DOW = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    class Entry:

        def __init__(self, fromday=None, today=None, fromtime=None, totime=None):
            if (fromday, today) == (None, None):
                self.fromday = 0
                self.today = 6
            elif fromday is None:
                self.today = self.fromday = ifstr(today, SimpleSchedule.DOW.index)
            elif today is None:
                self.today = self.fromday = ifstr(fromday, SimpleSchedule.DOW.index)
            else:
                self.fromday = ifstr(fromday, SimpleSchedule.DOW.index)
                self.today = ifstr(today, SimpleSchedule.DOW.index)
            if (fromtime, totime) == (None, None):
                self.fromtime = datetime.time.min
                self.totime = datetime.time.max
            else:
                self.fromtime = fromtime
                self.totime = totime

        def __contains__(self, item):
            if isinstance(item, datetime.datetime):
                dow = item.weekday()
                admissibledays = list(range(self.fromday, 7 if self.fromday > self.today else self.today + 1)) + \
                                 (list(range(0, self.today + 1)) if self.fromday > self.today else [])
                if dow in admissibledays and (self.fromtime <= self.totime and self.fromtime <= item.time() <= self.totime) or\
                    (self.fromtime > self.totime and (item.time() > self.fromtime or item.time() < self.totime)):
                    return True
                return False

        def __str__(self):
            day1 = SimpleSchedule.DOW[self.fromday]
            day2 = SimpleSchedule.DOW[self.today]
            daystr = '%s-%s' % (day1, day2) if day1 != day2 else day1
            # print(tuple(t.strftime('%H:%M') for t in (self.fromtime, self.totime)))
            timestr = '%s-%s' % tuple(t.strftime('%H:%M') for t in (self.fromtime, self.totime))
            return '%s:%s' % (daystr, timestr)

    def __init__(self, entries=None):
        self.entries = ifnone(entries, [])

    def check(self, time):
        return any([time in e for e in self.entries]) or not self.entries

    def addrule(self, s):
        try:
            dows = '|'.join(SimpleSchedule.DOW)
            hours = '|'.join(mapstr(range(24)) + '00,01,02,03,04,05,06,07,08,09'.split(','))
            minutes = '|'.join(['%.2d' % m for m in range(60)])
            time_ = '(%s):(%s)' % (hours, minutes)
            pattern = r'^((?P<fromday>%s)(-(?P<today>%s))?)?:?((?P<fromtime>%s)-(?P<totime>%s))?$' % (dows, dows, time_, time_)
            d = re.match(pattern, s, re.IGNORECASE).groupdict()
            if d.get('fromtime') is not None:
                h, m = d.get('fromtime').split(':')
                fromtime = datetime.time(hour=int(h), minute=int(m))
            else:
                fromtime = None
            if d.get('totime') is not None:
                h, m = d.get('totime').split(':')
                totime = datetime.time(hour=int(h), minute=int(m))
            else:
                totime = None
            self.entries.append(SimpleSchedule.Entry(fromday=d.get('fromday'), today=d.get('today'), fromtime=fromtime, totime=totime))
        except Exception as e:
            raise ValueError('Malformed schedule entry: "%s" -- %s' % (s, str(e)))

    def write(self, stream=None):
        stream = ifnone(stream, sys.stdout)
        for r in self.entries:
            stream.write('%s\n' % r)

    def format(self):
        with StringIO() as s:
            self.write(s)
            return s.getvalue()

    def __str__(self):
        return self.format()


def addmonths(y, m, d):
    '''Returns a pair ``(Y, M)`` which is the year and month one obtains from going ahead ``d`` months from the month
    ``m`` in the year ``y``. Also works with negative deltas, which corresponds to going back ``d`` months.
    :param y: the year
    :param m: the month in yeary ``y``
    :param d: the delta in months
    :return:
    '''

    def addmonth(y_, m_, d_):
        assert d_ in (+1, -1, 0)
        if m_ + d_ > 12:
            return y_ + 1, 1
        if m_ + d_ < 1:
            return y_ - 1, 12
        return y_, m_ + d_

    for _ in range(abs(d)):
        y, m = addmonth(y, m, sign(d))
    return y, m


class MonthIterator:
    '''
    This iterator allows to iterate over ``datetime.date`` objects on a monthly basis.

    A user can specify, which day of every month to pick, e.g. ``0`` will always select
    the first day of the month, whereas `-1`` will always select the last, ``-2`` the second-last,
    and so on.
    '''

    def __init__(self, day=0, since=None, until=None, reverse=False):
        self.current = ifnone(since, datetime.date.min if not reverse else datetime.date.max,
                              lambda d: d.date() if isinstance(d, datetime.datetime) else d)
        self.since = self.current
        self.until = ifnone(until, datetime.date.max if not reverse else datetime.date.min,
                            lambda d: d.date() if isinstance(d, datetime.datetime) else d)
        if not 0 <= day <= 27 and not -1 >= day >= -27:
            raise ValueError('Days of a monthly iterator must be in [0,27] or [-1,-27]')
        self.day = day
        self.reverse = self.since > self.until

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.until and not self.reverse or self.reverse and self.current <= self.until:
            raise StopIteration()
        newyear, newmonth = addmonths(self.current.year, self.current.month, -1 if self.reverse else 1)
        days = calendar.monthrange(newyear, newmonth)[1]
        self.current = datetime.date(newyear, newmonth, list(range(1, days + 1))[self.day])
        return self.current


def itermonths(day=0, since=None, until=None, reverse=False):
    return MonthIterator(day, since, until, reverse=reverse)
