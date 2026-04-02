__all__ = [
    'ThirtyTwoBits',
]

from dataclasses import dataclass
from typing import Final, Optional

class ThirtyTwoBits:
    """
    This class represents 32 bits that can be interpreted either as a signed or unsigned 32-bit integer, with an additional name field.
    ThirtyTwoBits values can be equality-compared to integers; the comparision will return True for both the signed and unsigned interpretation of the underlying 32 bits.

    Properties:
    - signed_value: The numeric value, interpreted as a 32-bit signed integer.
    - unsigned_value: The numeric value, interpreted as a 32-bit unsigned integer.
    - exit_code: The numeric value, interpreted in a way that it can be passed to `sys.exit()` without information loss. (Alias to `signed_value`.)
    - name: Name that can be used to refer to the value in human contexts. Typically the name of a WinAPI constant.

    Static methods:
    - `ThirtyTwoBits.check(value)`: Checks if `value` can be represented as a 32-bit signed or unsigned integer. If `value` is not an `int`, raises `TypeError`. If `value` is an `int`, but it cannot fit into 32 bits, raises `ValueError`.
    """

    @staticmethod
    def check(value: int) -> None:
        if not isinstance(value, int):
            raise TypeError(f'Not a valid int value: {repr(value)}')

        min_signed = -2**31
        max_unsigned = 2**32-1
        if value < min_signed or value > max_unsigned:
            raise ValueError(f'Value must be in [{min_signed}, {max_unsigned}] to be representable in 32 bits: {value}')

    def __init__(self, value: int = 0, name: str = '') -> None:
        """
        Constructor a ThirtyTwoBits object.

        Arguments:
        - `value: int`: Can be any (signed or unsigned) value that can be represented in 32 bits, i.e. any value in the range [-2147483648, 4294967295]. Passing a value not representable in 32 bits raises a ValueError, while passing any other type of value raises a TypeError. If no value is passed, defaults to 0.
        - `name: str`: Name to use when converting to string. If no value is passed, defaults to ''. (In which case `__str__()` will return the value as an unsigned hexadecimal number.)
        """

        ThirtyTwoBits.check(value)

        if value < 0:
            value = value + 2**32

        self._underlying_unsigned_value: Final[int] = value
        self._name: Final[str] = name

    def __str__(self) -> str:
        if self.name:
            return self.name
        else:
            return f'0x{self.unsigned_value:08X}L'


    def __repr__(self) -> str:
        return f'ThirtyTwoBits(0x{self.unsigned_value:08X}, \'{self.name}\')'

    @property
    def name(self) -> str:
        return self._name

    @property
    def unsigned_value(self) -> int:
        """
        The numeric value of the ThirtyTwoBits object, interpreted as a 32-bit unsigned integer.
        Always will be in range [0, 4294967295].
        x == x.usigned_value returns True for all ThirtyTwoBits values.
        """

        return self._underlying_unsigned_value

    @property
    def signed_value(self) -> int:
        """
        The numeric value of the ThirtyTwoBits object, interpreted as a 32-bit signed integer.
        Always will be in range [-2147483648, 2147483647].
        x == x.signed_value returns True for all ThirtyTwoBits values.
        """

        return (self._underlying_unsigned_value ^ 0x80000000) - 0x80000000

    @property
    def exit_code(self) -> int:
        """
        The numeric value of the ThirtyTwoBits object, interpreted in a way that it can be passed to sys.exit() without information loss.
        Implemented as an alias to signed_value.
        """

        return self.signed_value

    def __eq__(self, other: object) -> bool:
        """
        Equality check for NtStatus. It supports checking ThirtyTwoBits instances against other ThirtyTwoBits instances and ints.
        In the latter case, returns True for both the signed and unsigned interpretation of the underlying 32 bits.
        """

        if isinstance(other, ThirtyTwoBits):
            return self._underlying_unsigned_value == other._underlying_unsigned_value

        if isinstance(other, int):
            try:
                return self == ThirtyTwoBits(other)
            except ValueError:
                return False

        return NotImplemented
