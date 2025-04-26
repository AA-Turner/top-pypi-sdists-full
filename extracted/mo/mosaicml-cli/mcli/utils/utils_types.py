"""Type Utils for converting between nested structures"""
from enum import Enum
from typing import Callable, Optional, Type, TypeVar, Union

EnumType = TypeVar('EnumType', bound=Enum)  # pylint: disable=invalid-name


class CommonEnum(Enum):
    """Base class for enums that provides a proper __str__ method and ensure_enum
    """

    def __str__(self) -> str:
        return str(self.value)

    @classmethod
    def ensure_enum(cls: Type[EnumType], val: Union[str, EnumType]) -> EnumType:
        if isinstance(val, str):
            try:
                return cls[val]
            except KeyError as e:
                valid = ', '.join(str(x) for x in cls)
                raise ValueError(f'Invalid {cls.__name__}: got {val}. Must be one of: {valid}') from e

        elif isinstance(val, cls):
            return val
        raise ValueError(f'Unable to ensure {val} is a {cls.__name__} enum')


def get_hours_type(max_value: Optional[float] = None) -> Callable[[Union[str, float]], Union[float, None]]:
    """Returns a type checker that verifies a value is a float and lies between 0 and max_value
    """

    def _validate_hours(value: Union[str, float]) -> Union[float, None]:
        float_value: Union[float, None] = None
        try:
            float_value = float(value)

        except ValueError:
            # If float_value can't convert to a float, the
            # --hours argument is misconfigured or an invalid
            # argument was passed in. Stopping execution here
            # allows the correct error to propegate.
            return

        if float_value <= 0 or (max_value and float_value > max_value):
            if not max_value:
                range_str = f'between 0 and {max_value}'
            else:
                range_str = 'greater than 0'
            raise ValueError(f'The value for `--hours` must be a float {range_str}, but {float_value} was specified. '
                             'Please specify a value within this range.')
        return float_value

    return _validate_hours
