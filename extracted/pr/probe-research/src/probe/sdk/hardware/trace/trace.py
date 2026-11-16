"""Keep early observations and each device's latest reading within one fixed budget."""


class GpuTrace:
    def __init__(self, max_readings=512) -> None:
        self.max_readings = max_readings
        self.readings = []
        self._latest = {}
        self.dropped = 0
        self.is_incomplete = False

    def append(self, reading: dict) -> None:
        if len(self.readings) < self.max_readings:
            self._latest[reading["device"]] = len(self.readings)
            self.readings.append(reading)
            return
        # A multi-GPU tick needs one latest slot per device, not one shared final slot.
        index = self._latest.get(reading["device"])
        if index is None:
            reserved = set(self._latest.values())
            index = next((index for index in range(len(self.readings) - 1, -1, -1)
                          if index not in reserved), len(self.readings) - 1)
            previous = self.readings[index]["device"]
            if self._latest.get(previous) == index:
                self._latest.pop(previous)
        self.readings[index] = reading
        self._latest[reading["device"]] = index
        self.dropped += 1

    def extend(self, trace) -> None:
        self.dropped += int(trace.get("dropped") or 0)
        self.is_incomplete |= bool(trace.get("incomplete"))
        for reading in trace.get("readings") or []:
            self.append(reading)

    def to_dict(self) -> dict:
        return {"readings": self.readings, "dropped": self.dropped, "incomplete": self.is_incomplete}
