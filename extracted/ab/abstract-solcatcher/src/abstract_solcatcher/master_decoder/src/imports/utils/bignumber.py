from .imports import *
class BN:
    """
    Thin wrapper for Decimal with BigNumber.js-like interface.
    Use Decimal for precision, expose familiar methods.
    """
    
    __slots__ = ('_v',)
    
    def __init__(self, value: Union[int, str, float, 'BN', Decimal]):
        if isinstance(value, BN):
            self._v = value._v
        elif isinstance(value, Decimal):
            self._v = value
        else:
            self._v = Decimal(str(value))
    
    def __repr__(self) -> str:
        return f"BN({self._v})"
    
    def __str__(self) -> str:
        return str(self._v)
    
    # Arithmetic
    def plus(self, other: 'BN') -> 'BN':
        return BN(self._v + BN(other)._v)
    
    def minus(self, other: 'BN') -> 'BN':
        return BN(self._v - BN(other)._v)
    
    def multiplied_by(self, other: 'BN') -> 'BN':
        return BN(self._v * BN(other)._v)
    
    def divided_by(self, other: 'BN') -> 'BN':
        return BN(self._v / BN(other)._v)
    
    def pow(self, exp: int) -> 'BN':
        return BN(self._v ** exp)
    
    def abs(self) -> 'BN':
        return BN(abs(self._v))
    
    def integer_value(self) -> 'BN':
        return BN(int(self._v))
    
    # Comparisons
    def gt(self, other: 'BN') -> bool:
        return self._v > BN(other)._v
    
    def gte(self, other: 'BN') -> bool:
        return self._v >= BN(other)._v
    
    def lt(self, other: 'BN') -> bool:
        return self._v < BN(other)._v
    
    def lte(self, other: 'BN') -> bool:
        return self._v <= BN(other)._v
    
    def is_zero(self) -> bool:
        return self._v == 0
    
    # Conversion
    def to_number(self) -> float:
        return float(self._v)
    
    def to_int(self) -> int:
        return int(self._v)
    
    def to_string(self) -> str:
        return str(self._v)
