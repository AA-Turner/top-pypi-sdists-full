"""OpenTelemetry trace and span id parsing shared across the SDK."""


def parse_otel_id(value: str | int, *, name: str, hex_digits: int) -> int:
    if isinstance(value, int):
        parsed = value
    else:
        normalized = value.removeprefix("0x")
        if len(normalized) != hex_digits:
            message = f"{name} must be {hex_digits} hexadecimal characters"
            raise ValueError(message)
        try:
            parsed = int(normalized, 16)
        except ValueError as exc:
            message = f"{name} must be {hex_digits} hexadecimal characters"
            raise ValueError(message) from exc

    max_value = 1 << (hex_digits * 4)
    if parsed <= 0 or parsed >= max_value:
        message = f"{name} must be a non-zero {hex_digits}-digit hexadecimal identifier"
        raise ValueError(message)
    return parsed
