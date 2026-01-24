from __future__ import annotations

from dataclasses import dataclass, field

from fa_purity import Result, ResultE, Unsafe


@dataclass(frozen=True)
class Natural:
    """Defines a natural number i.e. integers >= 0."""

    @dataclass(frozen=True)
    class _Private:
        pass

    _private: Natural._Private = field(repr=False, hash=False, compare=False)
    value: int

    @staticmethod
    def from_int(value: int) -> ResultE[Natural]:
        if value >= 0:
            return Result.success(Natural(Natural._Private(), value))
        err = "`Natural` must be >= 0"
        return Result.failure(ValueError(err))

    @classmethod
    def zero(cls) -> Natural:
        return cls.from_int(0).alt(Unsafe.raise_exception).to_union()

    @classmethod
    def succ(cls, number: Natural) -> Natural:
        return cls.from_int(number.value + 1).alt(Unsafe.raise_exception).to_union()

    def __str__(self) -> str:
        """Str representation."""
        return f"Natural({self.value})"

    def __repr__(self) -> str:
        """Str representation."""
        return str(self)

    def __add__(self, number: Natural) -> Natural:
        """Add than operator."""
        return Natural.from_int(self.value + number.value).alt(Unsafe.raise_exception).to_union()

    def __lt__(self, number: Natural) -> bool:
        """Less than operator."""
        return self.value < number.value


@dataclass(frozen=True)
class NaturalOperations:
    @staticmethod
    def add(number: Natural, number_2: Natural) -> Natural:
        return (
            Natural.from_int(number.value + number_2.value).alt(Unsafe.raise_exception).to_union()
        )

    @staticmethod
    def absolute(number: int) -> Natural:
        return Natural.from_int(abs(number)).alt(Unsafe.raise_exception).to_union()
