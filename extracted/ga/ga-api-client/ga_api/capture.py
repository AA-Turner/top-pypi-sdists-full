from datetime import datetime, timezone
class CaptureBase:
    def __init__(self, value=None, time=None):
        # 如果 value 是列表，則分配 _v 和 _t
        if isinstance(value, list):
            time = value[0]
            self._v = value[1]
        else:
            self._v = value

        # convert _v to datetime object
        self._v = self._parse_datetime(self._v)

        # convert _t to datetime object
        self._t = self._parse_datetime(time)
        
        if self._t is None:
            self._t = datetime.fromtimestamp(0, tz=timezone.utc)


    def _parse_datetime(self, date_str):
        if isinstance(date_str, str) and date_str.startswith('d:'):
            try:
                dt = datetime.strptime(date_str[2:-1], "%Y-%m-%dT%H:%M:%S.%f")
                return dt.replace(tzinfo=timezone.utc)
            except ValueError as e:
                raise ValueError(f"Invalid datetime format: {date_str}") from e
        return date_str

    def compare(self, other):
        raise NotImplementedError("Subclasses must implement `compare` method.")

    def __add__(self, other):
        if self._t is None:
            return self.__class__([other._v, other._t])
        if other._t is None:
            return self.__class__([self._v, self._t])
        return self.compare(other)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        if self._t is None:
            self._v = other._v
            self._t = other._t
        elif other._t is not None:
            result = self.compare(other)
            self._v = result._v
            self._t = result._t
        return self

    def __str__(self):
        return f'{self._v}'

    def __repr__(self):
        return f'{self.__class__.__name__}(v={repr(self._v)}, t={repr(self._t)})'


class CaptureAnyMin(CaptureBase):
    def compare(self, other):
        print(repr(self), repr(other))
        if self._t is None:
            return self.__class__([other._t, other._v])
        elif other._t is None:
            return self.__class__([self._t, self._v])
        elif self._t < other._t:
            return self.__class__([self._t, self._v])
        return self.__class__([other._t, other._v])


class CaptureAnyMax(CaptureBase):
    def compare(self, other):
        print(repr(self), repr(other))
        if self._t is None:
            return self.__class__([other._t, other._v])
        elif other._t is None:
            return self.__class__([self._t, self._v])
        elif self._t > other._t:
            return self.__class__([self._t, self._v])
        return self.__class__([other._t, other._v])


class CaptureMin(CaptureBase):
    def compare(self, other):
        if self._v is None:
            return self.__class__([other._t, other._v ])
        elif other._v is None:
            return self.__class__([self._t, self._v])
        return self.__class__([self._t, min(self._v, other._v)])


class CaptureMax(CaptureBase):
    def compare(self, other):
        if self._v is None:
            return self.__class__([other._t, other._v ])
        elif other._v is None:
            return self.__class__([self._t, self._v])
        return self.__class__([self._t, max(self._v, other._v)])