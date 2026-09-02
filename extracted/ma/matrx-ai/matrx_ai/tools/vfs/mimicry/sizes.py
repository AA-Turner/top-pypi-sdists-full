from __future__ import annotations

# IEC suffixes used by GNU coreutils `ls -h`, `du -h`, etc.
_SUFFIXES = ("K", "M", "G", "T", "P", "E", "Z", "Y")


def format_size_human(n: int) -> str:
    if n < 0:
        return "-" + format_size_human(-n)
    if n < 1024:
        return str(n)

    # Find the largest unit where the value is >= 1.
    value = float(n)
    suffix = ""
    for s in _SUFFIXES:
        value = value / 1024.0
        suffix = s
        if value < 1024:
            break

    # GNU coreutils rounding: half away from zero, one decimal place when < 10,
    # no decimals when >= 10.
    if value < 10:
        # Round to one decimal half-away-from-zero by adding 0.05 then truncating.
        scaled = int(value * 10 + 0.5)
        whole = scaled // 10
        frac = scaled % 10
        if scaled >= 100:
            # Rounded up to 10.0 -> drop decimal.
            return f"{scaled // 10}{suffix}"
        return f"{whole}.{frac}{suffix}"
    # value >= 10: round half away from zero to integer.
    rounded = int(value + 0.5)
    if rounded >= 1024 and suffix != _SUFFIXES[-1]:
        # Promote to next unit if it rounded up past 1024.
        idx = _SUFFIXES.index(suffix)
        return f"1.0{_SUFFIXES[idx + 1]}"
    return f"{rounded}{suffix}"
