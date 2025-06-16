import six
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from functools import total_ordering


@total_ordering
@six.python_2_unicode_compatible
class Amount(object):
    """
    An amount of a currency.
    """

    def __init__(self, currency, value):
        """
        Initialises the Amount with a Currency object and an
        integer value of its minor unit (i.e. cents for USD)
        """
        assert isinstance(value, six.integer_types)
        assert not isinstance(currency, six.string_types)
        self.currency = currency
        self.value = value

    @classmethod
    def from_code_and_minor(cls, currency_code, value):
        """
        Initialises the amount with a currency code and an integer value
        of minor units
        """
        from .currency import currencies
        try:
            return cls(currencies[currency_code.upper()], value)
        except KeyError:
            raise ValueError("Invalid currency code %s" % currency_code)

    @classmethod
    def from_code_and_major(cls, currency_code, value, force_round=False):
        """
        Initialises the amount with a currency code and a value
        in the major unit (e.g. "1.43", Decimal("1.43"), 10)
        """
        from .currency import currencies
        try:
            currency = currencies[currency_code.upper()]
            return cls(currency, currency.major_to_minor(Decimal(value), force_round=force_round))
        except KeyError:
            raise ValueError("Invalid currency code %s" % currency_code)
        except InvalidOperation:
            raise ValueError("Invalid currency value %s" % value)

    def __str__(self):
        return self.currency.format(self.value)

    def __repr__(self):
        return "<Amount %s, %s>" % (self.currency, self.value)

    def __eq__(self, other):
        if not isinstance(other, Amount):
            return False
        if other is _ZeroAmount.instance:
            return other == self
        return (self.currency == other.currency) and (self.value == other.value)

    def __ne__(self, other):
        return not (self == other)

    def __add__(self, other):
        if other is _ZeroAmount.instance:
            return Amount(self.currency, self.value)
        if self.currency != other.currency:
            raise ValueError("You cannot add amounts of different currencies (%s and %s)" % (self.currency, other.currency))
        return Amount(self.currency, self.value + other.value)

    def __sub__(self, other):
        if other is _ZeroAmount.instance:
            return Amount(self.currency, self.value)
        if self.currency != other.currency:
            raise ValueError("You cannot subtract amounts of different currencies (%s and %s)" % (self.currency, other.currency))
        return Amount(self.currency, self.value - other.value)

    def __lt__(self, other):
        if other is _ZeroAmount.instance:
            return other > self
        if self.currency != other.currency:
            raise ValueError("You cannot compare amounts of different currencies (%s and %s)" % (self.currency, other.currency))
        return self.value < other.value

    def __nonzero__(self):
        return bool(self.value)

    def __bool__(self):
        return self.__nonzero__()

    def apply_factor(self, other):
        if not isinstance(other, six.integer_types + (Decimal, )):
            raise ValueError("You can only apply an integer, long or Decimal factor to an Amount")
        return Amount(
            self.currency,
            int(Decimal(self.value * other).to_integral(ROUND_HALF_UP)),
        )

    def convert_currency(self, new_code, rate):
        """
        Converts this Amount into an Amount of another currency at the given rate

        Rate is the number of new currency for each unit of the old -
        new = old * rate. Rate can be a float or a Decimal.
        """
        if not isinstance(rate, six.integer_types + (float, Decimal)):
            raise ValueError("You can only apply an integer, long, float or Decimal factor to an Amount")
        return Amount.from_code_and_minor(
            new_code,
            int(Decimal(self.value * rate).to_integral(ROUND_HALF_UP)),
        )

    def integral_division(self, divisor):
        """
        Divides the value through by the integer provided.
        Errors if the result is not exact.
        """
        if not isinstance(divisor, six.integer_types):
            raise ValueError("You can only divide by an integer or a long.")
        new_value = self.value / float(divisor)
        if int(new_value) != new_value:
            raise ValueError("Amount not exactly divisible by provided divisor")
        return Amount(self.currency, int(new_value))

    def divide_and_round(self, divisor, mode=ROUND_HALF_UP):
        """
        Divides the value through by the divisor provided.
        Optional mode from Decimal specifies rounding behaviour.
        """
        if not isinstance(divisor, six.integer_types + (float, Decimal)):
            raise ValueError("You can only divide by an integer, long, float or Decimal")
        return Amount(
            self.currency, int((Decimal(self.value) / Decimal(divisor)).to_integral_exact(mode))
        )

    def to_major_decimal(self):
        "Returns our value as a Decimal of major units"
        return self.currency.minor_to_major(self.value)


@six.python_2_unicode_compatible
class _ZeroAmount(Amount):
    """
    Amount singleton that doesn't have any currency.

    It can be used as the start of a sum() operation when you don't know the
    currency involved (yet).
    """
    instance = None

    def __init__(self):
        super(_ZeroAmount, self).__init__(None, 0)

    def __new__(cls, *args, **kwargs):
        """
        Force a singleton instance of _ZeroAmount
        """
        if cls.instance is None:
            cls.instance = super(_ZeroAmount, cls).__new__(cls)
        return cls.instance

    def __add__(self, other):
        if other is _ZeroAmount.instance:
            return self
        return Amount(other.currency, other.value)

    def __sub__(self, other):
        if other is _ZeroAmount.instance:
            return self
        return Amount(other.currency, -other.value)

    def __eq__(self, other):
        if not isinstance(other, Amount):
            return False
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self):
        return six.text_type(self.value)

    def __nonzero__(self):
        return False

    def __bool__(self):
        return False

    @classmethod
    def from_code_and_minor(cls, currency_code, value):
        raise NotImplementedError

    @classmethod
    def from_code_and_major(cls, currency_code, value):
        raise NotImplementedError

    def to_major_decimal(self):
        return Decimal(self.value)


Amount.ZERO = _ZeroAmount()
