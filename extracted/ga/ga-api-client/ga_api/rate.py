import math
from datetime import datetime, timezone
class Rate:
    def __init__(self, arg=[0, math.inf, 0]):
        self._sum = arg[0]
        self._start_ms = arg[1]
        self._end_ms = arg[2]
        if (isinstance(self._start_ms, str) and self._start_ms.startswith('d:')):
            dt = datetime.strptime(self._start_ms[2:-1], "%Y-%m-%dT%H:%M:%S.%f")
            self._start_ms = dt.replace(tzinfo=timezone.utc).timestamp() * 1000
        if (isinstance(self._end_ms, str) and self._end_ms.startswith('d:')):
            dt = datetime.strptime(self._end_ms[2:-1], "%Y-%m-%dT%H:%M:%S.%f")
            self._end_ms = dt.replace(tzinfo=timezone.utc).timestamp() * 1000
    def __add__(self, other):
        first = self._start_ms if self._start_ms < other._start_ms else other._start_ms
        last = self._end_ms if self._end_ms > other._end_ms else other._end_ms
        return Rate([self._sum + other._sum, first, last])

    def __radd__(self, other):
        first = self._start_ms if self._start_ms < other._start_ms else other._start_ms
        last = self._end_ms if self._end_ms > other._end_ms else other._end_ms
        return Rate([self._sum + other._sum, first, last])

    def __iadd__(self, other):
        self._sum += other._sum
        self._start_ms = self._start_ms if self._start_ms < other._start_ms else other._start_ms
        self._end_ms = self._end_ms if self._end_ms > other._end_ms else other._end_ms        
        return self

    def __str__(self):
        return f'{self.value()}'

    def __repr__(self):
        if self._end_ms <= self._start_ms:
            return f'$rate (empty)'
        return f'$rate(sum={self._sum}, start={datetime.fromtimestamp(self._start_ms/1000, tz=timezone.utc)}, end={datetime.fromtimestamp(self._end_ms/1000, tz=timezone.utc)}'
    def value(self):
        if self._end_ms <= self._start_ms:
            return math.nan
        return self._sum / ((self._end_ms - self._start_ms)/1000)

if __name__ == '__main__':
    x = Rate([10, 1734592909000, 1734592910000])
    y = Rate([20, 1734592909000, 1734592910000])
    z = Rate([30, "d:2020-12-20T10:00:00Z", "d:2020-12-20T10:00:05Z"])
    print('x = ', x)
    print('y = ', y)
    print('x + y = ', x + y)
    print('repr(x) = ', repr(x))
    print('repr(y) = ', repr(y))
    print('z = ', z)