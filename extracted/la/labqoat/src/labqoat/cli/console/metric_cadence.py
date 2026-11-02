"""Step or producer-time spacing for ordinary training summaries."""

import re


class MetricCadence:
    """Validation and evaluation bypass this policy; only training is sampled."""

    def __init__(self, value: str) -> None:
        """Accept positive step counts or explicit s, m, and h durations."""
        self.auto = value == "auto"
        match = re.fullmatch(r"([1-9][0-9]*)([smh]?)", "60s" if self.auto else value)
        if match is None:
            raise ValueError("--every requires a positive step count or duration such as 30s or 2m")
        self.count = int(match[1])
        self.unit = match[2]

    def due(self, previous: tuple[int, float] | None, step: int, timestamp: float, total: int | None = None) -> bool:
        """First samples are immediate; backdated records cannot reset cadence."""
        if previous is None:
            return True
        if self.auto and total:
            interval = max(1, (total + 9) // 10)
            return step // interval > previous[0] // interval
        if not self.unit:
            return step // self.count > previous[0] // self.count
        seconds = self.count * {"s": 1, "m": 60, "h": 3600}[self.unit]
        return timestamp - previous[1] >= seconds
