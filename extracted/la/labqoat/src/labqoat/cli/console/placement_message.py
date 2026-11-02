"""Name the machine a run landed on and what it costs, and say when a cheaper fit existed."""

from decimal import Decimal, InvalidOperation

from labqoat.json_document import JsonDocument


class PlacementMessage:
    """Sentences for worker assignment and costlier-host events."""

    @staticmethod
    def describe(label: str, kind: str, data: JsonDocument) -> str:
        """``Worker assigned · g6e.xlarge $1.86/h``, or the placed and cheapest machines with their prices."""
        if kind == "placement.costlier":
            placed = PlacementMessage.machine(data.get("placed"), "hourly_rate")
            cheapest = PlacementMessage.machine(data.get("cheapest"), "hourly_rate")
            return f"{label} · {placed}, the cheapest fit is {cheapest}; the run pays for the whole host"
        pricing = data.get("pricing")
        machine = PlacementMessage.machine(pricing, "machine_hourly_rate")
        return f"{label} · {machine}" if isinstance(pricing, dict) else label

    @staticmethod
    def machine(value: object, rate_key: str) -> str:
        """An instance type with its hourly price in dollars."""
        document = value if isinstance(value, dict) else {}
        try:
            rate = Decimal(str(document.get(rate_key))).quantize(Decimal("0.01"))
        except InvalidOperation:
            return str(document.get("instance_type", "an unknown machine"))
        return f"{document.get('instance_type', 'a machine')} ${rate}/h"
