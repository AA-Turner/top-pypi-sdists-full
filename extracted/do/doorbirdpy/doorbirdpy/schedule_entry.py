from __future__ import annotations
import json
from typing import Any


class DoorBirdScheduleEntry:
    """
    Parse a schedule entry from the device into an object.

    :param data: The entry as a dict
    :return: A DoorBirdScheduleEntry object
    """

    @staticmethod
    def parse(data):
        entry = DoorBirdScheduleEntry(data["input"], data["param"])

        for output in data["output"]:
            entry.output.append(DoorBirdScheduleEntryOutput.parse(output))

        return entry

    """
    Parse a list of schedule entries from the device into a list of objects.
    
    :param data: The list of entries
    :return: A list of DoorBirdScheduleEntry objects
    """

    @staticmethod
    def parse_all(data) -> list[DoorBirdScheduleEntry]:
        entries: list[DoorBirdScheduleEntry] = []

        for entry_data in data:
            entries.append(DoorBirdScheduleEntry.parse(entry_data))

        return entries

    def __init__(self, input: str, param: str = "") -> None:
        self.input = input
        self.param = param
        self.output: list[DoorBirdScheduleEntryOutput] = []

    @property
    def export(self) -> dict:
        return {
            "input": self.input,
            "param": self.param,
            "output": [output.export for output in self.output],
        }

    def __str__(self) -> str:
        return json.dumps(self.export)

    def __repr__(self) -> str:
        return f"<DoorBirdScheduleEntry {self.export}>"


class DoorBirdScheduleEntryOutput:
    """
    Parse a schedule action from the device into an object.

    :param data: The output action as a dict
    :return: A DoorBirdScheduleEntryOutput object
    """

    @staticmethod
    def parse(data) -> DoorBirdScheduleEntryOutput:
        return DoorBirdScheduleEntryOutput(
            # If the "enabled" key is missing, the doorbird will assume it is enabled
            enabled=bool(data["enabled"]) if "enabled" in data else True,
            event=data["event"],
            param=data["param"],
            schedule=DoorBirdScheduleEntrySchedule.parse(data["schedule"]),
        )

    def __init__(
        self,
        enabled: bool = True,
        event: str | None = None,
        param: str = "",
        schedule: DoorBirdScheduleEntrySchedule | None = None,
    ) -> None:
        self.enabled = enabled
        self.event = event
        self.param = param
        self.schedule = (
            DoorBirdScheduleEntrySchedule() if schedule is None else schedule
        )

    @property
    def export(self) -> dict:
        return {
            "enabled": "1" if self.enabled else "0",
            "event": self.event,
            "param": self.param,
            "schedule": self.schedule.export,
        }

    def __str__(self) -> str:
        return json.dumps(self.export)

    def __repr__(self) -> str:
        return f"<DoorBirdScheduleEntryOutput {self.export}>"


class DoorBirdScheduleEntrySchedule:
    """
    Parse schedule times from the device into an object.

    :param data: The schedule as a dict
    :return: A DoorBirdScheduleEntrySchedule object
    """

    @staticmethod
    def parse(data):
        schedule = DoorBirdScheduleEntrySchedule()

        if "once" in data:
            schedule.set_once(bool(data["once"]))

        if "from-to" in data:
            for from_to in data["from-to"]:
                schedule.add_range(from_to["from"], from_to["to"])

        if "weekdays" in data:
            for weekday in data["weekdays"]:
                schedule.add_weekday(int(weekday["from"]), int(weekday["to"]))

        return schedule

    def __init__(self) -> None:
        self.once: dict[str, int] | None = None
        self.from_to: list[dict] | None = None
        self.weekdays: list[dict] | None = None

    """
    Toggle the schedule on or off. The next time it runs, it will be toggled off.
    
    :param enabled: True to enable it for one run, False to disable it until enabled again
    """

    def set_once(self, enabled: bool) -> None:
        self.once = {"valid": 1 if enabled else 0}

    """
    Run the schedule only between the two specified times.
    
    :param sec_from: A unix timestamp representing the absolute start time of the schedule (such as April 25 2018)
    :param sec_to: A unix timestamp representing the absolute end time of the schedule (such as May 25 2018)
    """

    def add_range(self, sec_from: str | int, sec_to: str | int) -> None:
        if not self.from_to:
            self.from_to = []

        self.from_to.append({"from": str(int(sec_from)), "to": str(int(sec_to))})

    """
    Run the schedule between certain times on weekdays.
    
    :param sec_from: Seconds between Sunday at 00:00 and the desired start time
    :param sec_to: Seconds between Sunday at 00:00 and the desired end time
    """

    def add_weekday(self, sec_from: str | int, sec_to: str | int) -> None:
        if not self.weekdays:
            self.weekdays = []

        self.weekdays.append({"from": str(int(sec_from)), "to": str(int(sec_to))})

    @property
    def export(self) -> dict[str, Any]:
        schedule: dict[str, Any] = {}

        if self.once:
            schedule["once"] = self.once

        if self.from_to:
            schedule["from-to"] = []
            for from_to in self.from_to:
                schedule["from-to"].append(from_to)

        if self.weekdays:
            schedule["weekdays"] = []
            for weekday in self.weekdays:
                schedule["weekdays"].append(weekday)

        return schedule

    def __str__(self) -> str:
        return json.dumps(self.export)

    def __repr__(self) -> str:
        return f"<DoorBirdScheduleEntrySchedule {self.export}>"
