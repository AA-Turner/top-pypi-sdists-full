import json
import re
from enum import Enum, auto
from typing import Optional

__all__ = ["DmiParser"]

_HANDLE_RE = re.compile(r"^Handle\s(.+?),\sDMI\stype\s(\d+?),\s(\d+?)\sbytes\s*$")


class DmiParserState(Enum):
    NONE = auto()
    GET_SECT = auto()
    GET_PROP = auto()
    GET_PROP_ITEM = auto()


class DmiParserSectionHandle:
    """A handle looks like this

    Handle 0x0066, DMI type 148, 48 bytes
    """

    def __init__(self) -> None:
        self.id = ""
        self.type = ""
        self.bytes = ""

    def __str__(self) -> str:
        """
        @return: JSON dump string
        """
        return json.dumps(self.__dict__)


class DmiParserSectionProp:
    """A property looks like this

    Characteristics:
            3.3 V is provided
            PME signal is supported
            SMBus signal is supported
    """

    def __init__(self, value: str) -> None:
        """
        @param value: property text
        """
        self.values = []

        if value:
            self.append(value)

    def __str__(self) -> str:
        """
        @return: JSON dump string
        """
        return json.dumps(self.__dict__)

    def append(self, item: str) -> None:
        """
        @param item: item value
        """
        self.values.append(item)


class DmiParserSection:
    """A section looks like this

    On Board Device 1 Information
            Type: Video
            Status: Enabled
            Description: ServerEngines Pilot III
    """

    def __init__(self) -> None:
        self.handle = None
        self.name = ""
        self.props = {}

    def __str__(self) -> str:
        """
        @return: JSON dump string
        """
        return json.dumps(self.__dict__)

    def append(self, key: str, prop: dict) -> None:
        """
        @param key: property name
        @param prop: property
        """
        self.props[key] = prop


class DmiParser:
    """This parse dmidecode output to JSON text"""

    def __init__(self, text: str, **kwargs) -> None:
        """
        @param text: output of command dmidecode
        @param kwargs: these will pass to json.dumps()
        """
        if not isinstance(text, str):
            raise TypeError("text must be a str, got {}".format(type(text).__name__))

        self._text = text
        self._kwargs = kwargs
        self._sections = []

        self._parse()

    @staticmethod
    def _indent_lv(line: str) -> int:
        """Return the count of leading tab characters in line."""
        return len(line) - len(line.lstrip("\t"))

    def __str__(self) -> str:
        """
        @return: JSON dump string
        """
        return json.dumps(self._sections, **self._kwargs)

    def _parse(self) -> None:
        state: DmiParserState = DmiParserState.NONE
        handle: Optional[DmiParserSectionHandle] = None
        prop: Optional[DmiParserSectionProp] = None
        section: Optional[DmiParserSection] = None
        k: Optional[str] = None
        lines = self._text.splitlines()
        # peek past blank lines so they never trigger a state
        # transition (blank lines legally separate properties in some dmidecode
        # outputs, e.g. loongarch 3.5 type 4).
        next_nonempty = [None] * len(lines)
        last_nonempty = None

        for j in range(len(lines) - 1, -1, -1):
            next_nonempty[j] = last_nonempty
            if lines[j]:
                last_nonempty = lines[j]

        def flush_section() -> None:
            nonlocal section, prop, k
            if section:
                if prop:
                    section.append(k, json.loads(str(prop)))
                    prop = None
                    k = None
                self._sections.append(json.loads(str(section)))
                section = None

        for i, line in enumerate(lines):
            if DmiParserState.GET_SECT == state:
                flush_section()

            if not line:
                continue

            match = _HANDLE_RE.match(line)

            if match:
                state = DmiParserState.GET_SECT
                handle = DmiParserSectionHandle()
                handle.id, handle.type, handle.bytes = match.groups()
                continue

            # Malformed Handle line detection
            stripped = line.rstrip()

            if stripped.startswith("Handle") and (stripped.endswith("bytes") or stripped.endswith("byte")):
                raise ValueError("Malformed Handle line: {!r}".format(line))

            if DmiParserState.GET_SECT == state:
                section = DmiParserSection()
                section.handle = json.loads(str(handle))
                section.name = line
                state = DmiParserState.GET_PROP
                continue

            lv = self._indent_lv(line)
            nxt = next_nonempty[i]

            if nxt is not None:
                lv -= self._indent_lv(nxt)

            if DmiParserState.GET_PROP == state:
                if ":" not in line:
                    raise ValueError("Malformed property line (no ':'): {!r}".format(line))

                k, v = [x.strip() for x in line.split(":", 1)]
                prop = DmiParserSectionProp(v)

                if v:
                    if -1 == lv:
                        state = DmiParserState.GET_PROP_ITEM
                        continue

                    if 0 == lv:
                        section.append(k, json.loads(str(prop)))
                        prop = None
                else:
                    if -1 == lv:
                        state = DmiParserState.GET_PROP_ITEM
                        continue

                # Next section for this handle
                if nxt is not None and 0 == self._indent_lv(nxt):
                    state = DmiParserState.GET_SECT

            if DmiParserState.GET_PROP_ITEM == state:
                prop.append(line.strip())

                if 0 != lv:
                    section.append(k, json.loads(str(prop)))
                    prop = None
                    state = DmiParserState.GET_SECT if lv > 1 else DmiParserState.GET_PROP

        flush_section()
