"""Progress percentages and ETA use only declared totals and observed producer time."""

from collections import OrderedDict


class MetricProgress:
    """Maintain a bounded first-sample reference independently for each run and attempt."""

    def __init__(self) -> None:
        """Allocate at most 256 producer-time origins."""
        self.origins: OrderedDict[str, tuple[int, float]] = OrderedDict()

    def describe(self, key: str, step: int, timestamp: float, total: int | None) -> str:
        """Never guess progress units or estimate remaining work from observer receipt time."""
        first, started = self.origins.setdefault(key, (step, timestamp))
        self.origins.move_to_end(key)
        if len(self.origins) > 256:
            self.origins.popitem(last=False)
        if total is None:
            return f"step {step:,}"
        text = f"step {step:,}/{total:,}  {100 * step / total:.0f}%"
        if step <= first or timestamp <= started or step >= total:
            return text
        remaining = round((total - step) * (timestamp - started) / (step - first))
        minutes, seconds = divmod(remaining, 60)
        return f"{text}  ETA {minutes}m{seconds:02d}s"
