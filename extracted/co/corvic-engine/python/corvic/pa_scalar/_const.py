"""Parameterized constants."""


def signed_limits(nbits: int) -> tuple[int, int]:
    return (-(2 ** (nbits - 1)), 2 ** (nbits - 1) - 1)


def unsigned_limits(nbits: int) -> tuple[int, int]:
    return (0, 2 ** (nbits) - 1)


def unit_to_frac_digits(unit: str) -> int:
    match unit:
        case "s":
            return 0
        case "ms":
            return 3
        case "us":
            return 6
        case "ns":
            return 9
        case _:
            raise ValueError(f"unexpected unit: {unit}")


def unit_to_seconds(unit: str) -> int:
    match unit:
        case "s":
            return 1
        case "ms":
            return 1_000
        case "us":
            return 1_000_000
        case "ns":
            return 1_000_000_000
        case _:
            raise ValueError(f"unexpected unit: {unit}")
