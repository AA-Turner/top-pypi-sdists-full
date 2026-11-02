"""Text for one resource value according to the role of its field."""

from datetime import UTC, datetime

from labqoat.json_document import JsonValue


class FieldText:
    """Keep identifiers and instants exact for agents and abbreviate them for people."""

    @staticmethod
    def kind(name: str) -> str:
        """Infer a role from a field name when no curated column declares one."""
        if name.endswith("_at"):
            return "time"
        if name == "id" or name.endswith("_id"):
            return "id"
        return "status" if name in ("status", "state", "availability") else "text"

    @staticmethod
    def compact(value: JsonValue, kind: str) -> str:
        """Exact values with the least text: whole identifiers and second-precision instants."""
        if kind == "time" and isinstance(value, str):
            return value.split(".")[0].rstrip("Z") + "Z"
        return repr(value) if isinstance(value, float) and kind == "text" else FieldText.plain(value, kind)

    @staticmethod
    def pretty(value: JsonValue, kind: str, now: datetime) -> str:
        """Short identifiers and relative ages; everything else as plain text."""
        if kind == "id" and isinstance(value, str) and len(value) == 36 and value.count("-") == 4:
            return value[:8]
        if kind == "time" and isinstance(value, str):
            return FieldText.age(value, now)
        return FieldText.plain(value, kind)

    @staticmethod
    def plain(value: JsonValue, kind: str) -> str:
        """Familiar words for absent and boolean values, units for sizes, joined scalar lists."""
        if value is None or value == "" or value == [] or value == {}:
            return "-"
        if isinstance(value, bool):
            return "yes" if value else "no"
        if isinstance(value, (int, float)) and kind in ("cpu", "memory", "bytes"):
            return FieldText.quantity(float(value), kind)
        if isinstance(value, float):
            return f"{value:.6g}"
        if isinstance(value, list):
            return ", ".join(FieldText.plain(item, "text") for item in value)
        if isinstance(value, dict):
            return f"{len(value)} fields"
        return str(value)

    @staticmethod
    def quantity(value: float, kind: str) -> str:
        """Cores from millicores, and binary sizes from megabytes or bytes."""
        if kind == "cpu":
            return f"{value / 1000:g}"
        megabytes = value if kind == "memory" else value / 1_048_576
        return f"{megabytes / 1024:.1f} GB" if megabytes >= 1024 else f"{megabytes:.0f} MB"

    @staticmethod
    def age(value: str, now: datetime) -> str:
        """Describe an instant relative to now; unparseable text is shown unchanged."""
        try:
            seconds = int((now - datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)).total_seconds())
        except ValueError:
            return value
        if seconds < 0:
            return "in " + FieldText.span(-seconds)
        return FieldText.span(seconds) + " ago"

    @staticmethod
    def span(seconds: int) -> str:
        """The largest whole unit that fits."""
        for size, unit in ((86_400, "d"), (3_600, "h"), (60, "m")):
            if seconds >= size:
                return f"{seconds // size}{unit}"
        return f"{seconds}s"
