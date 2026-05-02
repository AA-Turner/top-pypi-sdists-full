import math
class Std:
    def __init__(self, arg=[0, 0, 0]):
        self._mean = arg[0]
        self._count = arg[1]
        self._variance = arg[2]
    def __add__(self, other):
        new_count = self._count + other._count
        new_mean = (self._mean * self._count + other._mean * other._count) / new_count
        new_variance = self._variance + other._variance + (self._mean - other._mean)**2 * self._count * other._count / new_count
        return Std([new_mean, new_count, new_variance])

    def __radd__(self, other):
        new_count = self._count + other._count
        new_mean = (self._mean * self._count + other._mean * other._count) / new_count
        new_variance = self._variance + other._variance + (self._mean - other._mean)**2 * self._count * other._count / new_count
        return Std([new_mean, new_count, new_variance])

    def __iadd__(self, other):
        new_count = self._count + other._count
        new_mean = (self._mean * self._count + other._mean * other._count) / new_count
        new_variance = self._variance + other._variance + (self._mean - other._mean)**2 * self._count * other._count / new_count
        self._mean = new_mean
        self._count = new_count
        self._variance = new_variance
        return self

    def __str__(self):
        return f'{self.value()}'

    def __repr__(self):
        return f'$std(mean={self._mean}, count={self._count}, variance={self._variance})'

    def value(self):
        if self._count == 0:
            return math.nan
        return math.sqrt(self._variance / self._count)

if __name__ == '__main__':
    pass
    # x = Std([10, 1734592909000, 1734592910000])
    # y = Std([20, 1734592909000, 1734592910000])
    # print('x = ', x)
    # print('y = ', y)
    # print('x + y = ', x + y)
    # print('repr(x) = ', repr(x))
    # print('repr(y) = ', repr(y))