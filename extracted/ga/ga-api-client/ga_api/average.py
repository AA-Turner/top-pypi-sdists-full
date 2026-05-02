import math

class Average:
    def __init__(self, arg=[0, 0]):
        self._sum = arg[0]
        self._count = arg[1]
    def __add__(self, other):
        return Average([self._sum + other._sum, self._count + other._count])

    def __radd__(self, other):
        return Average([self._sum + other._sum, self._count + other._count])

    def __iadd__(self, other):
        self._sum += other._sum
        self._count += other._count
        return self

    def __str__(self):
        return f'{self.value()}'

    def __repr__(self):
        return f'$avg(sum={self._sum}, count={self._count})'

    def value(self):
        if self._count == 0:
            return math.nan
        return self._sum / self._count
