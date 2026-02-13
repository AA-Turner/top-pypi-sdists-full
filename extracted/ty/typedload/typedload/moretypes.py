"""
typedload

Additional types
"""

# Copyright (C) 2026 Salvo "LtWorf" Tomaselli
#
# typedload is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# author Salvo "LtWorf" Tomaselli <tiposchi@tiscali.it>

__all__ = [
    'HexRGB'
]


class HexRGB:
    '''
    A class for RGB colours.

    Can be initialised with:
    HexRGB('#00ff00')
    HexRGB(1234)
    '''

    __slots__ = ['value']
    value: int

    def __new__(cls, value: str | int):
        if isinstance(value, str):
            if len(value) != 7:
                raise ValueError(f'Invalid length for HexRGB string: {value!r}')
            if value[0] != '#':
                raise ValueError(f'Invalid prefix for HexRGB string: {value[0]!r}')
            v = int(value[1:], 16)
        elif isinstance(value, int):
            v = value
        else:
            raise TypeError(f'Invalid type {type(value)} to create HexRGB')

        if v < 0 or v > 16777215:
            raise ValueError(f'Colour value out of range: {v}')

        # Some weird magic since this class is immutable
        instance = object.__new__(cls)
        object.__setattr__(instance, "value", v)
        return instance

    def __int__(self) -> int:
        return self.value

    def __eq__(self, o) -> bool:
        if not isinstance(o, HexRGB):
            return False
        return self.value == o.value

    def __hash__(self):
        return hash(self.value)

    def __setattr__(self, name, value) -> None:
        raise AttributeError('HexRGB is read only')

    def __repr__(self) -> str:
        return f"HexRGB({self.value})"

    def __str__(self) -> str:
        return f'#{self.value:06X}'

    def rgb(self) -> tuple[int, int, int]:
        '''
        Returns a tuple with the RGB values in integer format
        '''
        v = self.value
        b = v & 255
        v >>= 8
        g = v & 255
        v >>= 8
        r = v
        return r, g, b
